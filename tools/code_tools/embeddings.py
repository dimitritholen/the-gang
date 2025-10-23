"""
Embedding provider abstraction with caching.

Supports multiple embedding providers with local caching to minimize API costs.
Cache is stored in SQLite for portability with .claude/ folder.
"""

import json
import sqlite3
import hashlib
from pathlib import Path
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Abstract base for embedding providers"""

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate embedding for text"""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch of texts"""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Embedding dimension"""
        pass


class AnthropicEmbeddingProvider(EmbeddingProvider):
    """Anthropic Claude embedding provider"""

    def __init__(self, api_key: Optional[str] = None):
        try:
            import anthropic
        except ImportError:
            raise RuntimeError(
                "anthropic package not installed. "
                "Run: pip install 'code-tools[embeddings]'"
            )

        import os
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. "
                "Set environment variable or pass api_key parameter."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def embed(self, text: str) -> List[float]:
        """Generate embedding using Claude"""
        # Note: Anthropic doesn't have a native embedding API yet.
        # This is a placeholder for when they do, or use Claude to generate
        # a semantic representation that can be embedded.
        # For now, we'll use a workaround or recommend OpenAI embeddings.
        raise NotImplementedError(
            "Anthropic embeddings not yet available. "
            "Use OpenAI provider instead."
        )

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed(text) for text in texts]

    @property
    def dimension(self) -> int:
        return 1536  # Placeholder, matches OpenAI's ada-002


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider using text-embedding-3-small"""

    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"):
        try:
            import openai
        except ImportError:
            raise RuntimeError(
                "openai package not installed. "
                "Run: pip install openai"
            )

        import os
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. "
                "Set environment variable or pass api_key parameter."
            )

        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model

    def embed(self, text: str) -> List[float]:
        """Generate embedding using OpenAI"""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch (more efficient)"""
        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]

    @property
    def dimension(self) -> int:
        return 1536  # text-embedding-3-small dimension


class CachedEmbeddingProvider:
    """
    Wrapper that caches embeddings in SQLite to minimize API costs.

    Cache key is SHA256 hash of text content.
    Cache is portable with .claude/ folder.
    """

    def __init__(
        self,
        provider: EmbeddingProvider,
        cache_db: Path,
        cache_enabled: bool = True
    ):
        self.provider = provider
        self.cache_db = cache_db
        self.cache_enabled = cache_enabled

        if cache_enabled:
            self._init_cache()

    def _init_cache(self):
        """Initialize cache database"""
        self.cache_db.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(str(self.cache_db))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS embedding_cache (
                text_hash TEXT PRIMARY KEY,
                text_preview TEXT NOT NULL,
                embedding BLOB NOT NULL,
                provider TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_created_at
            ON embedding_cache(created_at)
        """)
        conn.commit()
        conn.close()

    def _hash_text(self, text: str) -> str:
        """Generate cache key from text"""
        return hashlib.sha256(text.encode()).hexdigest()

    def _get_cached(self, text_hash: str) -> Optional[List[float]]:
        """Retrieve embedding from cache"""
        if not self.cache_enabled:
            return None

        conn = sqlite3.connect(str(self.cache_db))
        cursor = conn.execute(
            "SELECT embedding FROM embedding_cache WHERE text_hash = ?",
            (text_hash,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            # Deserialize from JSON stored as BLOB
            return json.loads(row[0].decode('utf-8'))
        return None

    def _cache_embedding(
        self,
        text: str,
        text_hash: str,
        embedding: List[float]
    ):
        """Store embedding in cache"""
        if not self.cache_enabled:
            return

        from datetime import datetime

        conn = sqlite3.connect(str(self.cache_db))

        # Store as JSON for portability
        embedding_blob = json.dumps(embedding).encode('utf-8')
        preview = text[:200]  # Store preview for debugging

        conn.execute("""
            INSERT OR REPLACE INTO embedding_cache
            (text_hash, text_preview, embedding, provider, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            text_hash,
            preview,
            embedding_blob,
            self.provider.__class__.__name__,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

    def embed(self, text: str) -> List[float]:
        """Get embedding with caching"""
        text_hash = self._hash_text(text)

        # Check cache
        cached = self._get_cached(text_hash)
        if cached is not None:
            return cached

        # Generate embedding
        embedding = self.provider.embed(text)

        # Cache result
        self._cache_embedding(text, text_hash, embedding)

        return embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for batch with caching"""
        if not texts:
            return []

        results: List[Optional[List[float]]] = [None] * len(texts)
        uncached_indices: List[int] = []
        uncached_texts: List[str] = []

        # Check cache for each text
        for i, text in enumerate(texts):
            text_hash = self._hash_text(text)
            cached = self._get_cached(text_hash)
            if cached is not None:
                results[i] = cached
            else:
                uncached_indices.append(i)
                uncached_texts.append(text)

        # Generate embeddings for uncached texts
        if uncached_texts:
            new_embeddings = self.provider.embed_batch(uncached_texts)

            # Cache and store results
            for idx, text, embedding in zip(
                uncached_indices, uncached_texts, new_embeddings
            ):
                text_hash = self._hash_text(text)
                self._cache_embedding(text, text_hash, embedding)
                results[idx] = embedding

        return [e for e in results if e is not None]

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.cache_enabled:
            return {'enabled': False}

        conn = sqlite3.connect(str(self.cache_db))

        cursor = conn.execute("SELECT COUNT(*) FROM embedding_cache")
        total = cursor.fetchone()[0]

        cursor = conn.execute("""
            SELECT provider, COUNT(*)
            FROM embedding_cache
            GROUP BY provider
        """)
        by_provider = dict(cursor.fetchall())

        conn.close()

        return {
            'enabled': True,
            'total_cached': total,
            'by_provider': by_provider,
            'cache_db': str(self.cache_db),
            'cache_size_mb': round(
                self.cache_db.stat().st_size / 1024 / 1024, 2
            ) if self.cache_db.exists() else 0
        }

    def clear_cache(self):
        """Clear all cached embeddings"""
        if not self.cache_enabled:
            return

        conn = sqlite3.connect(str(self.cache_db))
        conn.execute("DELETE FROM embedding_cache")
        conn.commit()
        conn.close()


def create_embedding_provider(
    provider_type: str = "openai",
    cache_dir: Optional[Path] = None,
    cache_enabled: bool = True,
    **kwargs
) -> CachedEmbeddingProvider:
    """
    Factory function to create embedding provider with caching.

    Args:
        provider_type: 'openai' or 'anthropic'
        cache_dir: Directory for cache database
        cache_enabled: Whether to enable caching
        **kwargs: Additional arguments for provider (e.g., api_key, model)

    Returns:
        CachedEmbeddingProvider instance
    """
    if provider_type == "openai":
        provider = OpenAIEmbeddingProvider(**kwargs)
    elif provider_type == "anthropic":
        provider = AnthropicEmbeddingProvider(**kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider_type}")

    if cache_dir is None:
        cache_dir = Path(".claude/memory")

    cache_db = cache_dir / "embedding_cache.db"

    return CachedEmbeddingProvider(
        provider=provider,
        cache_db=cache_db,
        cache_enabled=cache_enabled
    )
