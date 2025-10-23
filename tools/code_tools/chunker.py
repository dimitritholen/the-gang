"""
Code chunking logic for semantic search.

Chunks code at function/class/method level for meaningful semantic units.
Supports Python, JavaScript, TypeScript, and other languages via AST parsing.
"""

import ast
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from code_tools.vector_store import CodeChunk


@dataclass
class ChunkMetadata:
    """Metadata for a code chunk"""
    decorators: List[str] = None
    docstring: Optional[str] = None
    complexity: int = 0  # Cyclomatic complexity estimate


class PythonChunker:
    """Chunk Python code using AST"""

    def chunk_file(self, file_path: Path) -> List[CodeChunk]:
        """Extract semantic chunks from Python file"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return []

        try:
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError:
            # Fallback to module-level chunk if parse fails
            return [self._create_module_chunk(file_path, content)]

        chunks = []
        lines = content.splitlines()

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                chunk = self._extract_function(node, file_path, lines)
                if chunk:
                    chunks.append(chunk)

            elif isinstance(node, ast.ClassDef):
                chunk = self._extract_class(node, file_path, lines)
                if chunk:
                    chunks.append(chunk)

        # If no chunks extracted, add module-level chunk
        if not chunks:
            chunks.append(self._create_module_chunk(file_path, content))

        return chunks

    def _extract_function(
        self,
        node: ast.FunctionDef,
        file_path: Path,
        lines: List[str]
    ) -> Optional[CodeChunk]:
        """Extract function as code chunk"""
        start_line = node.lineno
        end_line = node.end_lineno or start_line

        # Get function source
        content_lines = lines[start_line - 1:end_line]
        content = '\n'.join(content_lines)

        # Extract docstring
        docstring = ast.get_docstring(node)

        # Build descriptive name
        name = node.name
        if docstring:
            # Include first line of docstring for context
            first_line = docstring.split('\n')[0].strip()
            name = f"{node.name}: {first_line[:80]}"

        return CodeChunk(
            id=None,  # Will be computed
            file_path=str(file_path.relative_to(Path.cwd())),
            start_line=start_line,
            end_line=end_line,
            chunk_type='function',
            name=name,
            content=content,
            language='python'
        )

    def _extract_class(
        self,
        node: ast.ClassDef,
        file_path: Path,
        lines: List[str]
    ) -> Optional[CodeChunk]:
        """Extract class as code chunk"""
        start_line = node.lineno
        end_line = node.end_lineno or start_line

        # Get class source
        content_lines = lines[start_line - 1:end_line]
        content = '\n'.join(content_lines)

        # Extract docstring
        docstring = ast.get_docstring(node)

        # Build descriptive name
        name = node.name
        if docstring:
            first_line = docstring.split('\n')[0].strip()
            name = f"{node.name}: {first_line[:80]}"

        return CodeChunk(
            id=None,
            file_path=str(file_path.relative_to(Path.cwd())),
            start_line=start_line,
            end_line=end_line,
            chunk_type='class',
            name=name,
            content=content,
            language='python'
        )

    def _create_module_chunk(
        self,
        file_path: Path,
        content: str
    ) -> CodeChunk:
        """Create module-level chunk as fallback"""
        lines = content.splitlines()

        # Extract module docstring if present
        try:
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)
        except:
            docstring = None

        name = file_path.stem
        if docstring:
            first_line = docstring.split('\n')[0].strip()
            name = f"{file_path.stem}: {first_line[:80]}"

        return CodeChunk(
            id=None,
            file_path=str(file_path.relative_to(Path.cwd())),
            start_line=1,
            end_line=len(lines),
            chunk_type='module',
            name=name,
            content=content,
            language='python'
        )


class JavaScriptChunker:
    """Chunk JavaScript/TypeScript using regex patterns"""

    def chunk_file(self, file_path: Path) -> List[CodeChunk]:
        """Extract semantic chunks from JS/TS file"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return []

        chunks = []
        lines = content.splitlines()

        # Pattern for function declarations
        func_pattern = re.compile(
            r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(',
            re.MULTILINE
        )

        # Pattern for arrow functions assigned to const/let/var
        arrow_pattern = re.compile(
            r'^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(',
            re.MULTILINE
        )

        # Pattern for class declarations
        class_pattern = re.compile(
            r'^(?:export\s+)?class\s+(\w+)',
            re.MULTILINE
        )

        # Extract functions
        for match in func_pattern.finditer(content):
            chunk = self._extract_block(
                content, lines, match, 'function', file_path
            )
            if chunk:
                chunks.append(chunk)

        # Extract arrow functions
        for match in arrow_pattern.finditer(content):
            chunk = self._extract_block(
                content, lines, match, 'function', file_path
            )
            if chunk:
                chunks.append(chunk)

        # Extract classes
        for match in class_pattern.finditer(content):
            chunk = self._extract_block(
                content, lines, match, 'class', file_path
            )
            if chunk:
                chunks.append(chunk)

        # Fallback to module chunk
        if not chunks:
            chunks.append(self._create_module_chunk(file_path, content, lines))

        return chunks

    def _extract_block(
        self,
        content: str,
        lines: List[str],
        match: re.Match,
        chunk_type: str,
        file_path: Path
    ) -> Optional[CodeChunk]:
        """Extract code block using brace matching"""
        start_pos = match.start()
        start_line = content[:start_pos].count('\n') + 1

        # Find matching closing brace
        brace_count = 0
        in_block = False
        end_pos = start_pos

        for i, char in enumerate(content[start_pos:], start=start_pos):
            if char == '{':
                brace_count += 1
                in_block = True
            elif char == '}':
                brace_count -= 1
                if in_block and brace_count == 0:
                    end_pos = i + 1
                    break

        if end_pos <= start_pos:
            return None

        end_line = content[:end_pos].count('\n') + 1

        # Extract content
        chunk_content = '\n'.join(lines[start_line - 1:end_line])

        # Extract name
        name = match.group(1)

        # Detect language
        language = 'typescript' if file_path.suffix == '.ts' else 'javascript'

        return CodeChunk(
            id=None,
            file_path=str(file_path.relative_to(Path.cwd())),
            start_line=start_line,
            end_line=end_line,
            chunk_type=chunk_type,
            name=name,
            content=chunk_content,
            language=language
        )

    def _create_module_chunk(
        self,
        file_path: Path,
        content: str,
        lines: List[str]
    ) -> CodeChunk:
        """Create module-level chunk"""
        language = 'typescript' if file_path.suffix == '.ts' else 'javascript'

        return CodeChunk(
            id=None,
            file_path=str(file_path.relative_to(Path.cwd())),
            start_line=1,
            end_line=len(lines),
            chunk_type='module',
            name=file_path.stem,
            content=content,
            language=language
        )


class GenericChunker:
    """Fallback chunker for unsupported languages"""

    def __init__(self, max_lines: int = 100):
        self.max_lines = max_lines

    def chunk_file(self, file_path: Path) -> List[CodeChunk]:
        """Chunk file by fixed line count"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return []

        lines = content.splitlines()
        chunks = []

        # Detect language from extension
        language = self._detect_language(file_path)

        # Chunk by max_lines
        for i in range(0, len(lines), self.max_lines):
            start_line = i + 1
            end_line = min(i + self.max_lines, len(lines))

            chunk_lines = lines[i:end_line]
            chunk_content = '\n'.join(chunk_lines)

            chunks.append(CodeChunk(
                id=None,
                file_path=str(file_path.relative_to(Path.cwd())),
                start_line=start_line,
                end_line=end_line,
                chunk_type='block',
                name=f"{file_path.stem} (lines {start_line}-{end_line})",
                content=chunk_content,
                language=language
            ))

        return chunks

    def _detect_language(self, file_path: Path) -> str:
        """Detect language from file extension"""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
        }
        return ext_map.get(file_path.suffix, 'unknown')


def chunk_file(file_path: Path) -> List[CodeChunk]:
    """
    Chunk a code file into semantic units.

    Automatically selects appropriate chunker based on file type.
    """
    suffix = file_path.suffix.lower()

    if suffix == '.py':
        chunker = PythonChunker()
    elif suffix in {'.js', '.jsx', '.ts', '.tsx'}:
        chunker = JavaScriptChunker()
    else:
        chunker = GenericChunker()

    return chunker.chunk_file(file_path)


def chunk_directory(
    directory: Path,
    extensions: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None
) -> List[CodeChunk]:
    """
    Chunk all code files in a directory.

    Args:
        directory: Root directory to scan
        extensions: File extensions to include (e.g., ['.py', '.js'])
        exclude_patterns: Patterns to exclude (e.g., ['test_', '__pycache__'])

    Returns:
        List of code chunks
    """
    if extensions is None:
        extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.go', '.rs']

    if exclude_patterns is None:
        exclude_patterns = [
            '__pycache__', 'node_modules', '.git', 'venv', 'env',
            '.pytest_cache', 'dist', 'build', '.next', '.vscode'
        ]

    chunks = []

    for ext in extensions:
        for file_path in directory.rglob(f'*{ext}'):
            # Check exclusions
            if any(pattern in str(file_path) for pattern in exclude_patterns):
                continue

            # Chunk file
            file_chunks = chunk_file(file_path)
            chunks.extend(file_chunks)

    return chunks
