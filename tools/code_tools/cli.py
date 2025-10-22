import argparse
import json
import os
import re
import sys
import glob as _glob
from pathlib import Path
from typing import List, Dict, Any


VERSION = "1.0"


def _ok(tool: str, data: Any) -> None:
    print(json.dumps({"ok": True, "tool": tool, "version": VERSION, "data": data}, ensure_ascii=False))


def _err(tool: str, msg: str) -> None:
    print(json.dumps({"ok": False, "tool": tool, "version": VERSION, "error": msg}, ensure_ascii=False))
    sys.exit(1)


def cmd_list_dir(args: argparse.Namespace) -> None:
    base = Path(args.path)
    if not base.exists():
        _err("list_dir", f"Path not found: {base}")
    depth = args.depth
    include_hidden = args.hidden
    results = []
    for root, dirs, files in os.walk(base):
        rel_depth = Path(root).relative_to(base).parts
        if len(rel_depth) > depth:
            # prune deeper walks
            dirs[:] = []
            continue
        for name in list(dirs) + list(files):
            if not include_hidden and name.startswith('.'):
                continue
            p = Path(root) / name
            st = p.stat()
            results.append({
                "path": str(p),
                "type": "dir" if p.is_dir() else "file",
                "size": st.st_size,
                "mtime": int(st.st_mtime),
            })
    _ok("list_dir", results)


def cmd_search_file(args: argparse.Namespace) -> None:
    base = Path(args.path)
    glb = args.glob
    limit = args.limit
    matches: List[Dict[str, Any]] = []
    for path in _glob.iglob(str(base / glb), recursive=True):
        p = Path(path)
        try:
            st = p.stat()
        except FileNotFoundError:
            continue
        matches.append({
            "path": str(p),
            "size": st.st_size,
            "mtime": int(st.st_mtime),
        })
        if len(matches) >= limit:
            break
    _ok("search_file", matches)


def cmd_grep_code(args: argparse.Namespace) -> None:
    try:
        pattern = re.compile(args.pattern)
    except re.error as e:
        _err("grep_code", f"invalid regex: {e}")
    limit = args.limit
    roots = [Path(p) for p in (args.paths.split(',') if args.paths else ['.'])]
    results = []
    for root in roots:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            try:
                with path.open('r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, start=1):
                        if pattern.search(line):
                            results.append({
                                "path": str(path),
                                "line": i,
                                "preview": line.rstrip('\n'),
                            })
                            if len(results) >= limit:
                                _ok("grep_code", results)
                                return
            except Exception:
                continue
    _ok("grep_code", results)


def cmd_read_file(args: argparse.Namespace) -> None:
    p = Path(args.path)
    if not p.exists():
        _err("read_file", f"Path not found: {p}")
    start = args.start
    end = args.end
    if start is not None and start < 1:
        _err("read_file", "start must be >= 1")
    content_lines: List[str] = []
    with p.open('r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, start=1):
            if start is not None and i < start:
                continue
            if end is not None and i > end:
                break
            content_lines.append(line)
    data = {
        "path": str(p),
        "start": start,
        "end": end,
        "content": ''.join(content_lines),
        "line_count": len(content_lines),
    }
    _ok("read_file", data)


def cmd_fetch_content(args: argparse.Namespace) -> None:
    try:
        import requests  # type: ignore
    except Exception:
        _err("fetch_content", "requests not installed. pip install requests")
    url = args.url
    try:
        resp = requests.get(url, timeout=15)
        text = resp.text
        # very light extraction: strip scripts/styles
        cleaned = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.I)
        cleaned = re.sub(r"<style[\s\S]*?</style>", "", cleaned, flags=re.I)
        # naive text fallback
        only_text = re.sub(r"<[^>]+>", " ", cleaned)
        only_text = re.sub(r"\s+", " ", only_text).strip()
        _ok("fetch_content", {"status": resp.status_code, "content": only_text[:20000]})
    except Exception as e:
        _err("fetch_content", str(e))


def cmd_search_web(args: argparse.Namespace) -> None:
    _err("search_web", "Not configured. Provide SEARCH_API or implement provider.")


def cmd_search_replace(args: argparse.Namespace) -> None:
    file_path = Path(args.file)
    if not file_path.exists():
        _err("search_replace", f"File not found: {file_path}")
    # replacements file or inline JSON
    if args.replacements.startswith('@'):
        rep_path = Path(args.replacements[1:])
        reps = json.loads(rep_path.read_text(encoding='utf-8'))
    else:
        reps = json.loads(args.replacements)
    if not isinstance(reps, list):
        reps = reps.get("replacements", reps)
    content = file_path.read_text(encoding='utf-8')
    summary = []
    for r in reps:
        orig = r.get("original_text")
        new = r.get("new_text")
        replace_all = bool(r.get("replace_all", False))
        if orig is None or new is None:
            _err("search_replace", "replacement missing original_text/new_text")
        if orig == new:
            _err("search_replace", "original_text and new_text identical")
        count = content.count(orig)
        if count == 0:
            _err("search_replace", f"original_text not found: {orig[:80]}")
        if not replace_all and count != 1:
            _err("search_replace", f"original_text not unique (count={count})")
        if replace_all:
            content = content.replace(orig, new)
            summary.append({"original_text": orig[:80], "new_text": new[:80], "count": count})
        else:
            content = content.replace(orig, new, 1)
            summary.append({"original_text": orig[:80], "new_text": new[:80], "count": 1})
    file_path.write_text(content, encoding='utf-8')
    _ok("search_replace", {"file": str(file_path), "applied": summary})


def cmd_create_file(args: argparse.Namespace) -> None:
    file_path = Path(args.file)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    content: str
    if args.content.startswith('@'):
        content = Path(args.content[1:]).read_text(encoding='utf-8')
    else:
        content = args.content
    if args.add_last_line_newline and (not content.endswith('\n')):
        content += '\n'
    tmp = file_path.with_suffix(file_path.suffix + ".tmp")
    tmp.write_text(content, encoding='utf-8')
    tmp.replace(file_path)
    _ok("create_file", {"file": str(file_path), "bytes": len(content.encode('utf-8'))})


def cmd_edit_file(args: argparse.Namespace) -> None:
    file_path = Path(args.file)
    if not file_path.exists():
        _err("edit_file", f"File not found: {file_path}")
    patch: str
    if args.patch.startswith('@'):
        patch = Path(args.patch[1:]).read_text(encoding='utf-8')
    else:
        patch = args.patch
    # Minimal patch: keep only provided text as the new content between existing markers
    # Here we interpret the patch as the new full content for simplicity
    file_path.write_text(patch, encoding='utf-8')
    _ok("edit_file", {"file": str(file_path), "bytes": len(patch.encode('utf-8'))})


def cmd_search_memory(args: argparse.Namespace) -> None:
    base = Path(args.dir or ".dimitri/memory")
    query = args.query.strip()
    topk = args.topk
    if not base.exists():
        _err("search_memory", f"Memory dir not found: {base}")
    tokens = set(re.findall(r"\w+", query.lower()))
    scored: List[Dict[str, Any]] = []
    for p in base.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".md", ".txt"}:
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        words = re.findall(r"\w+", text.lower())
        score = sum(1 for w in words if w in tokens)
        if score > 0:
            # simple snippet
            snippet = text[:500]
            scored.append({"path": str(p), "score": score, "snippet": snippet})
    scored.sort(key=lambda x: x["score"], reverse=True)
    _ok("search_memory", scored[:topk])


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="code-tools", description="Portable code tools CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("list_dir", help="List directory contents")
    sp.add_argument("--path", default=".")
    sp.add_argument("--depth", type=int, default=1)
    sp.add_argument("--hidden", action="store_true")
    sp.set_defaults(func=cmd_list_dir)

    sp = sub.add_parser("search_file", help="Glob search files")
    sp.add_argument("--path", default=".")
    sp.add_argument("--glob", required=True)
    sp.add_argument("--limit", type=int, default=25)
    sp.set_defaults(func=cmd_search_file)

    sp = sub.add_parser("grep_code", help="Regex search in files")
    sp.add_argument("--pattern", required=True)
    sp.add_argument("--paths", default=".")
    sp.add_argument("--limit", type=int, default=25)
    sp.set_defaults(func=cmd_grep_code)

    sp = sub.add_parser("read_file", help="Read file content or range")
    sp.add_argument("--path", required=True)
    sp.add_argument("--start", type=int)
    sp.add_argument("--end", type=int)
    sp.set_defaults(func=cmd_read_file)

    sp = sub.add_parser("fetch_content", help="Fetch URL content")
    sp.add_argument("--url", required=True)
    sp.set_defaults(func=cmd_fetch_content)

    sp = sub.add_parser("search_web", help="Web search (placeholder)")
    sp.add_argument("--query", required=True)
    sp.add_argument("--limit", type=int, default=5)
    sp.set_defaults(func=cmd_search_web)

    sp = sub.add_parser("search_replace", help="Apply validated replacements")
    sp.add_argument("--file", required=True)
    sp.add_argument("--replacements", required=True, help="JSON or @file.json")
    sp.set_defaults(func=cmd_search_replace)

    sp = sub.add_parser("create_file", help="Create a new file atomically")
    sp.add_argument("--file", required=True)
    sp.add_argument("--content", required=True, help="Text or @file")
    sp.add_argument("--add-last-line-newline", action="store_true")
    sp.set_defaults(func=cmd_create_file)

    sp = sub.add_parser("edit_file", help="Replace file content with provided patch text")
    sp.add_argument("--file", required=True)
    sp.add_argument("--patch", required=True, help="Text or @file")
    sp.set_defaults(func=cmd_edit_file)

    sp = sub.add_parser("search_memory", help="Search .dimitri/memory for query")
    sp.add_argument("--dir", default=None)
    sp.add_argument("--query", required=True)
    sp.add_argument("--topk", type=int, default=10)
    sp.set_defaults(func=cmd_search_memory)

    return p


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
