"""
Vector store for semantic code search using SQLite + VSS.

Architecture:
- SQLite database with VSS extension for vector similarity search
- Code chunks stored with embeddings
- Embedding cache to minimize API calls
- Support for incremental updates
"""

import json
import sqlite3
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import sqlite_vss
    import numpy as np
    VSS_AVAILABLE = True
except ImportError:
    VSS_AVAILABLE = False


@dataclass
class CodeChunk:
    """Represents a semantic chunk of code"""
    id: str  # SHA256 hash of file + start_line
    file_path: str
    start_line: int
    end_line: int
    chunk_type: str  # 'function', 'class', 'method', 'module'
    name: str  # Function/class name
    content: str
    language: str
    embedding: Optional[List[float]] = None
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.id is None:
            self.id = self._compute_id()

    def _compute_id(self) -> str:
        """Generate stable ID from file path + start line"""
        raw = f"{self.file_path}:{self.start_line}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


class VectorStore:
    """SQLite + VSS vector store for code chunks"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = None  # Reusable connection
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Get or create a connection with VSS loaded (reusable)"""
        if self._conn is None:
            if not VSS_AVAILABLE:
                raise RuntimeError(
                    "sqlite-vss not installed. Run: pip install sqlite-vss"
                )
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.enable_load_extension(True)
            sqlite_vss.load(self._conn)
            self._conn.enable_load_extension(False)
        return self._conn

    def _init_db(self):
        """Initialize database schema with VSS extension"""
        conn = self._get_connection()

        # Create code chunks table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS code_chunks (
                id TEXT PRIMARY KEY,
                file_path TEXT NOT NULL,
                start_line INTEGER NOT NULL,
                end_line INTEGER NOT NULL,
                chunk_type TEXT NOT NULL,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                language TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Create VSS virtual table for embeddings
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS code_embeddings USING vss0(
                embedding(1536)
            )
        """)

        # Create file hash tracking table for incremental updates
        conn.execute("""
            CREATE TABLE IF NOT EXISTS file_hashes (
                file_path TEXT PRIMARY KEY,
                content_hash TEXT NOT NULL,
                last_indexed TEXT NOT NULL,
                chunk_count INTEGER NOT NULL
            )
        """)

        # Create indexes
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_file_path
            ON code_chunks(file_path)
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_chunk_type
            ON code_chunks(chunk_type)
        """)

        conn.commit()

    def upsert_chunk(self, chunk: CodeChunk) -> None:
        """Insert or update a code chunk with its embedding"""
        if not chunk.embedding:
            raise ValueError("Chunk must have embedding")

        conn = self._get_connection()

        # Upsert chunk metadata
        conn.execute("""
            INSERT OR REPLACE INTO code_chunks
            (id, file_path, start_line, end_line, chunk_type, name,
             content, language, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            chunk.id,
            chunk.file_path,
            chunk.start_line,
            chunk.end_line,
            chunk.chunk_type,
            chunk.name,
            chunk.content,
            chunk.language,
            chunk.created_at,
            datetime.now().isoformat()
        ))

        # Upsert embedding
        embedding_blob = np.array(chunk.embedding, dtype=np.float32).tobytes()
        conn.execute("""
            INSERT OR REPLACE INTO code_embeddings(rowid, embedding)
            VALUES (?, ?)
        """, (chunk.id, embedding_blob))

        conn.commit()

    def batch_upsert(self, chunks: List[CodeChunk]) -> None:
        """Batch insert/update chunks for efficiency"""
        if not chunks:
            return

        conn = self._get_connection()

        # Batch insert metadata
        metadata = [
            (c.id, c.file_path, c.start_line, c.end_line, c.chunk_type,
             c.name, c.content, c.language, c.created_at,
             datetime.now().isoformat())
            for c in chunks
        ]

        conn.executemany("""
            INSERT OR REPLACE INTO code_chunks
            (id, file_path, start_line, end_line, chunk_type, name,
             content, language, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, metadata)

        # Batch insert embeddings
        embeddings = [
            (c.id, np.array(c.embedding, dtype=np.float32).tobytes())
            for c in chunks if c.embedding
        ]

        conn.executemany("""
            INSERT OR REPLACE INTO code_embeddings(rowid, embedding)
            VALUES (?, ?)
        """, embeddings)

        conn.commit()

    def search(
        self,
        query_embedding: List[float],
        limit: int = 10,
        file_filter: Optional[str] = None,
        chunk_type_filter: Optional[str] = None
    ) -> List[Tuple[CodeChunk, float]]:
        """
        Search for similar code chunks using vector similarity.

        Returns list of (chunk, similarity) tuples, sorted by similarity.
        Similarity is in range [0, 1] where 1 = identical, 0 = unrelated.
        Computed as: similarity = 1 / (1 + L2_distance)
        """
        conn = self._get_connection()

        query_blob = np.array(query_embedding, dtype=np.float32).tobytes()

        # Build query with optional filters
        where_clauses = []
        params = [query_blob, limit]

        if file_filter:
            where_clauses.append("c.file_path LIKE ?")
            params.insert(-1, f"%{file_filter}%")

        if chunk_type_filter:
            where_clauses.append("c.chunk_type = ?")
            params.insert(-1, chunk_type_filter)

        where_sql = f"AND {' AND '.join(where_clauses)}" if where_clauses else ""

        query = f"""
            SELECT
                c.id, c.file_path, c.start_line, c.end_line, c.chunk_type,
                c.name, c.content, c.language, c.created_at,
                e.distance
            FROM code_embeddings e
            JOIN code_chunks c ON e.rowid = c.id
            WHERE vss_search(e.embedding, ?)
            {where_sql}
            ORDER BY e.distance ASC
            LIMIT ?
        """

        cursor = conn.execute(query, params)
        results = []

        for row in cursor.fetchall():
            chunk = CodeChunk(
                id=row[0],
                file_path=row[1],
                start_line=row[2],
                end_line=row[3],
                chunk_type=row[4],
                name=row[5],
                content=row[6],
                language=row[7],
                created_at=row[8]
            )
            distance = row[9]
            # Convert L2 distance to similarity score [0, 1]
            similarity = 1.0 / (1.0 + distance)
            results.append((chunk, similarity))

        return results

    def delete_by_file(self, file_path: str) -> int:
        """Delete all chunks for a file (for incremental updates)"""
        conn = self._get_connection()

        # Get chunk IDs first
        cursor = conn.execute(
            "SELECT id FROM code_chunks WHERE file_path = ?",
            (file_path,)
        )
        chunk_ids = [row[0] for row in cursor.fetchall()]

        # Delete from both tables
        conn.execute(
            "DELETE FROM code_chunks WHERE file_path = ?",
            (file_path,)
        )

        if chunk_ids:
            placeholders = ','.join('?' * len(chunk_ids))
            conn.execute(
                f"DELETE FROM code_embeddings WHERE rowid IN ({placeholders})",
                chunk_ids
            )

        conn.commit()
        deleted = len(chunk_ids)
        return deleted

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = self._get_connection()

        cursor = conn.execute("SELECT COUNT(*) FROM code_chunks")
        total_chunks = cursor.fetchone()[0]

        cursor = conn.execute("""
            SELECT chunk_type, COUNT(*)
            FROM code_chunks
            GROUP BY chunk_type
        """)
        by_type = dict(cursor.fetchall())

        cursor = conn.execute("""
            SELECT language, COUNT(*)
            FROM code_chunks
            GROUP BY language
        """)
        by_language = dict(cursor.fetchall())

        cursor = conn.execute("""
            SELECT COUNT(DISTINCT file_path) FROM code_chunks
        """)
        total_files = cursor.fetchone()[0]

        return {
            'total_chunks': total_chunks,
            'total_files': total_files,
            'by_type': by_type,
            'by_language': by_language,
            'db_path': str(self.db_path),
            'db_size_mb': round(self.db_path.stat().st_size / 1024 / 1024, 2)
        }

    def list_files(self) -> List[str]:
        """List all indexed files"""
        conn = self._get_connection()
        cursor = conn.execute("""
            SELECT DISTINCT file_path
            FROM code_chunks
            ORDER BY file_path
        """)
        files = [row[0] for row in cursor.fetchall()]
        return files

    def get_file_hash(self, file_path: str) -> Optional[str]:
        """Get stored hash for a file"""
        conn = self._get_connection()
        cursor = conn.execute(
            "SELECT content_hash FROM file_hashes WHERE file_path = ?",
            (file_path,)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def update_file_hash(self, file_path: str, content_hash: str, chunk_count: int):
        """Update file hash after successful indexing"""
        conn = self._get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO file_hashes
            (file_path, content_hash, last_indexed, chunk_count)
            VALUES (?, ?, ?, ?)
        """, (file_path, content_hash, datetime.now().isoformat(), chunk_count))
        conn.commit()

    def clear_file_index(self, file_path: str):
        """Clear file from index and hash tracking"""
        deleted = self.delete_by_file(file_path)
        conn = self._get_connection()
        conn.execute("DELETE FROM file_hashes WHERE file_path = ?", (file_path,))
        conn.commit()
        return deleted

    def close(self):
        """Close the database connection"""
        if self._conn:
            self._conn.close()
            self._conn = None
