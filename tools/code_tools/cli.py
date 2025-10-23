import argparse
import json
import os
import re
import sys
import glob as _glob
from pathlib import Path
from typing import List, Dict, Any, Optional


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


def cmd_slugify_feature(args: argparse.Namespace) -> None:
    """Convert feature name to slug format with metadata"""
    name = args.name.strip()
    # Convert to lowercase, replace spaces/special chars with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

    # Extract feature ID if provided (e.g., "01-user-auth" -> "01")
    feature_id = None
    if args.feature_id:
        feature_id = args.feature_id.strip()
    else:
        # Try to extract from slug pattern NN-rest
        match = re.match(r'^(\d+)-', slug)
        if match:
            feature_id = match.group(1)

    # Determine directory path
    if feature_id:
        dir_path = f".tasks/{feature_id}-{slug}"
    else:
        dir_path = None

    _ok("slugify_feature", {
        "slug": slug,
        "feature_id": feature_id,
        "dir": dir_path,
        "original": name
    })


def cmd_read_task_manifest(args: argparse.Namespace) -> None:
    """Read and validate task manifest.json"""
    manifest_path = Path(args.path)
    if not manifest_path.exists():
        _err("read_task_manifest", f"Manifest not found: {manifest_path}")

    try:
        with manifest_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        _err("read_task_manifest", f"Invalid JSON: {e}")

    # Validate required fields
    required = ["feature", "tasks"]
    missing = [f for f in required if f not in data]
    if missing:
        _err("read_task_manifest", f"Missing required fields: {missing}")

    # Add metadata
    result = {
        "path": str(manifest_path),
        "manifest": data,
        "task_count": len(data.get("tasks", [])),
        "completed_count": sum(1 for t in data.get("tasks", []) if t.get("status") == "COMPLETED"),
        "in_progress_count": sum(1 for t in data.get("tasks", []) if t.get("status") == "IN_PROGRESS"),
        "blocked_count": sum(1 for t in data.get("tasks", []) if t.get("status") == "BLOCKED")
    }

    _ok("read_task_manifest", result)


def cmd_update_task_status(args: argparse.Namespace) -> None:
    """Update task status in manifest and XML"""
    task_id = args.task_id
    new_status = args.status
    feature_dir = Path(args.feature_dir)

    if new_status not in ["NOT_STARTED", "IN_PROGRESS", "COMPLETED", "BLOCKED"]:
        _err("update_task_status", f"Invalid status: {new_status}")

    # Read task manifest
    task_manifest_path = feature_dir / "manifest.json"
    if not task_manifest_path.exists():
        _err("update_task_status", f"Task manifest not found: {task_manifest_path}")

    with task_manifest_path.open('r', encoding='utf-8') as f:
        task_manifest = json.load(f)

    # Find and update task
    task_found = False
    for task in task_manifest.get("tasks", []):
        if task.get("id") == task_id:
            old_status = task.get("status")
            task["status"] = new_status
            if new_status == "IN_PROGRESS" and "started" not in task:
                task["started"] = json.dumps(None)  # Placeholder for timestamp
            if new_status == "COMPLETED" and "completed" not in task:
                task["completed"] = json.dumps(None)  # Placeholder for timestamp
            task_found = True
            break

    if not task_found:
        _err("update_task_status", f"Task {task_id} not found in manifest")

    # Write updated task manifest
    with task_manifest_path.open('w', encoding='utf-8') as f:
        json.dump(task_manifest, f, indent=2)

    # Update root manifest if needed
    root_manifest_path = Path(".tasks/manifest.json")
    if root_manifest_path.exists():
        with root_manifest_path.open('r', encoding='utf-8') as f:
            root_manifest = json.load(f)

        # Update completed count
        feature_id = task_manifest.get("feature", {}).get("id")
        for feature in root_manifest.get("features", []):
            if feature.get("id") == feature_id:
                completed_count = sum(1 for t in task_manifest.get("tasks", []) if t.get("status") == "COMPLETED")
                feature["completedCount"] = completed_count
                # Update feature status
                total_tasks = len(task_manifest.get("tasks", []))
                if completed_count == 0:
                    feature["status"] = "NOT_STARTED"
                elif completed_count == total_tasks:
                    feature["status"] = "COMPLETED"
                else:
                    feature["status"] = "IN_PROGRESS"
                break

        with root_manifest_path.open('w', encoding='utf-8') as f:
            json.dump(root_manifest, f, indent=2)

    _ok("update_task_status", {
        "task_id": task_id,
        "old_status": old_status,
        "new_status": new_status,
        "updated": True
    })


def cmd_find_next_task(args: argparse.Namespace) -> None:
    """Find next available task with dependencies met"""
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        _err("find_next_task", f"Manifest not found: {manifest_path}")

    with manifest_path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    tasks = data.get("tasks", [])

    # Build dependency map
    completed_tasks = {t["id"] for t in tasks if t.get("status") == "COMPLETED"}

    # Find first NOT_STARTED task with all dependencies met
    for task in tasks:
        if task.get("status") != "NOT_STARTED":
            continue

        dependencies = task.get("dependencies", [])
        if all(dep in completed_tasks for dep in dependencies):
            _ok("find_next_task", {
                "task_id": task["id"],
                "task": task,
                "has_next": True
            })
            return

    # No available task
    _ok("find_next_task", {
        "task_id": None,
        "task": None,
        "has_next": False,
        "reason": "All tasks started, completed, or blocked by dependencies"
    })


def cmd_validate_manifest(args: argparse.Namespace) -> None:
    """Validate manifest consistency"""
    feature_dir = Path(args.feature_dir)
    task_manifest_path = feature_dir / "manifest.json"
    root_manifest_path = Path(".tasks/manifest.json")

    if not task_manifest_path.exists():
        _err("validate_manifest", f"Task manifest not found: {task_manifest_path}")

    with task_manifest_path.open('r', encoding='utf-8') as f:
        task_manifest = json.load(f)

    issues = []

    # Check task count
    actual_task_count = len(task_manifest.get("tasks", []))

    # Check completed count
    actual_completed = sum(1 for t in task_manifest.get("tasks", []) if t.get("status") == "COMPLETED")

    # Check feature status accuracy
    in_progress = sum(1 for t in task_manifest.get("tasks", []) if t.get("status") == "IN_PROGRESS")
    blocked = sum(1 for t in task_manifest.get("tasks", []) if t.get("status") == "BLOCKED")

    expected_status = "NOT_STARTED"
    if actual_completed == actual_task_count and actual_task_count > 0:
        expected_status = "COMPLETED"
    elif actual_completed > 0 or in_progress > 0:
        expected_status = "IN_PROGRESS"
    if blocked > 0:
        expected_status = "BLOCKED"

    # Compare with root manifest if exists
    if root_manifest_path.exists():
        with root_manifest_path.open('r', encoding='utf-8') as f:
            root_manifest = json.load(f)

        feature_id = task_manifest.get("feature", {}).get("id")
        for feature in root_manifest.get("features", []):
            if feature.get("id") == feature_id:
                if feature.get("taskCount") != actual_task_count:
                    issues.append({
                        "type": "task_count_mismatch",
                        "expected": actual_task_count,
                        "found": feature.get("taskCount")
                    })
                if feature.get("completedCount") != actual_completed:
                    issues.append({
                        "type": "completed_count_mismatch",
                        "expected": actual_completed,
                        "found": feature.get("completedCount")
                    })
                if feature.get("status") != expected_status:
                    issues.append({
                        "type": "status_mismatch",
                        "expected": expected_status,
                        "found": feature.get("status")
                    })
                break

    _ok("validate_manifest", {
        "valid": len(issues) == 0,
        "issues": issues,
        "stats": {
            "total_tasks": actual_task_count,
            "completed": actual_completed,
            "in_progress": in_progress,
            "blocked": blocked
        }
    })


def cmd_list_memory_artifacts(args: argparse.Namespace) -> None:
    """List memory artifacts for feature or all"""
    memory_dir = Path(args.dir or ".claude/memory")
    if not memory_dir.exists():
        _err("list_memory_artifacts", f"Memory dir not found: {memory_dir}")

    feature_filter = args.feature if args.feature else None

    artifacts = {
        "requirements": [],
        "tech_analysis": [],
        "implementation_plans": [],
        "scope_validations": [],
        "consistency_validations": [],
        "feature_briefs": [],
        "other": []
    }

    for p in memory_dir.iterdir():
        if not p.is_file() or p.suffix.lower() not in {".md", ".txt"}:
            continue

        name = p.name

        # Filter by feature if specified
        if feature_filter and feature_filter not in name:
            continue

        # Categorize
        if name.startswith("requirements-"):
            artifacts["requirements"].append(str(p))
        elif name.startswith("tech-analysis-"):
            artifacts["tech_analysis"].append(str(p))
        elif name.startswith("implementation-plan-"):
            artifacts["implementation_plans"].append(str(p))
        elif name.startswith("scope-validation-"):
            artifacts["scope_validations"].append(str(p))
        elif name.startswith("consistency-validation-"):
            artifacts["consistency_validations"].append(str(p))
        elif name.startswith("feature-brief-"):
            artifacts["feature_briefs"].append(str(p))
        else:
            artifacts["other"].append(str(p))

    _ok("list_memory_artifacts", {
        "artifacts": artifacts,
        "total": sum(len(v) for v in artifacts.values()),
        "feature_filter": feature_filter
    })


def cmd_query_memory(args: argparse.Namespace) -> None:
    """Query knowledge graph with natural language"""
    from code_tools.graph import GraphStore, EntityType, RelationshipType
    from code_tools.builders.feature_graph_builder import FeatureGraphBuilder

    memory_dir = Path(args.dir or ".claude/memory")
    query = args.query.strip()
    feature = args.feature
    mode = args.mode or "auto"

    if not memory_dir.exists():
        _err("query_memory", f"Memory dir not found: {memory_dir}")

    store = GraphStore(memory_dir)

    # Mode: direct (graph query) or nlp (LLM-powered)
    if mode == "direct":
        # Direct graph query (simple keyword matching for now)
        results = _query_direct(store, feature, query, args)
    elif mode == "nlp":
        # LLM-powered query translation (placeholder)
        results = _query_nlp(store, feature, query, args)
    else:  # auto
        # Try direct first, fall back to NLP if no results
        results = _query_direct(store, feature, query, args)
        if not results.get('entities') and not results.get('relationships'):
            results = _query_nlp(store, feature, query, args)

    _ok("query_memory", results)


def _query_direct(store: Any, feature: Optional[str], query: str, args: argparse.Namespace) -> Dict[str, Any]:
    """Direct graph query using keywords"""
    from code_tools.graph import EntityType, RelationshipType

    if not feature:
        return {'error': 'Feature slug required for direct queries', 'entities': [], 'relationships': []}

    # Parse query for entity type filters
    entity_type = None
    query_lower = query.lower()
    if 'requirement' in query_lower:
        entity_type = EntityType.REQUIREMENT
    elif 'task' in query_lower:
        entity_type = EntityType.TASK
    elif 'decision' in query_lower or 'tech' in query_lower:
        entity_type = EntityType.TECH_DECISION
    elif 'component' in query_lower:
        entity_type = EntityType.COMPONENT
    elif 'pattern' in query_lower:
        entity_type = EntityType.PATTERN
    elif 'convention' in query_lower:
        entity_type = EntityType.CONVENTION

    # Query entities
    entities = store.query_entities(feature, entity_type=entity_type)

    # Filter by keyword match in name/metadata (skip if query just contained type filter)
    keywords = set(query.lower().split())
    type_keywords = {'requirement', 'requirements', 'task', 'tasks', 'decision', 'decisions', 'tech', 'component', 'components', 'pattern', 'patterns', 'convention', 'conventions', 'feature', 'features'}
    content_keywords = keywords - type_keywords

    filtered = []
    if not content_keywords:
        # Query was just type filter, return all of that type
        filtered = entities
    else:
        # Filter by content keywords (search across all entity fields)
        for entity in entities:
            entity_text = json.dumps(entity).lower()
            if any(kw in entity_text for kw in content_keywords):
                filtered.append(entity)

    # Get related relationships
    entity_ids = {e['id'] for e in filtered}
    relationships = []
    if entity_ids:
        for eid in entity_ids:
            relationships.extend(store.query_relationships(feature, source_id=eid))
            relationships.extend(store.query_relationships(feature, target_id=eid))

    return {
        'mode': 'direct',
        'feature': feature,
        'query': query,
        'entities': filtered[:args.limit] if hasattr(args, 'limit') else filtered,
        'relationships': relationships[:args.limit * 2] if hasattr(args, 'limit') else relationships,
        'total_matches': len(filtered)
    }


def _query_nlp(store: Any, feature: Optional[str], query: str, args: argparse.Namespace) -> Dict[str, Any]:
    """NLP-powered query using LLM (placeholder)"""
    # TODO: Integrate with LLM to translate natural language to graph query
    # For now, return helpful message
    return {
        'mode': 'nlp',
        'feature': feature,
        'query': query,
        'message': 'NLP query mode not yet implemented. Use --mode direct with --feature <slug>',
        'suggestion': 'Try: code-tools query_memory --mode direct --feature user-authentication --query "security requirements"',
        'entities': [],
        'relationships': []
    }


def cmd_sync_memory_graph(args: argparse.Namespace) -> None:
    """Sync markdown files to JSONL graph"""
    from code_tools.builders.feature_graph_builder import FeatureGraphBuilder

    memory_dir = Path(args.dir or ".claude/memory")
    feature = args.feature

    if not memory_dir.exists():
        _err("sync_memory_graph", f"Memory dir not found: {memory_dir}")

    builder = FeatureGraphBuilder(memory_dir)

    if feature:
        # Sync single feature
        result = builder.rebuild_feature(feature, memory_dir)
        _ok("sync_memory_graph", result)
    else:
        # Sync all features
        results = builder.sync_all(memory_dir)
        _ok("sync_memory_graph", {
            'synced_features': len(results),
            'features': results
        })


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

    sp = sub.add_parser("slugify_feature", help="Convert feature name to slug")
    sp.add_argument("--name", required=True, help="Feature name")
    sp.add_argument("--feature-id", default=None, help="Optional feature ID (e.g., '01')")
    sp.set_defaults(func=cmd_slugify_feature)

    sp = sub.add_parser("read_task_manifest", help="Read and validate task manifest")
    sp.add_argument("--path", required=True, help="Path to manifest.json")
    sp.set_defaults(func=cmd_read_task_manifest)

    sp = sub.add_parser("update_task_status", help="Update task status in manifests")
    sp.add_argument("--task-id", required=True, help="Task ID (e.g., 'T01')")
    sp.add_argument("--status", required=True, help="New status")
    sp.add_argument("--feature-dir", required=True, help="Feature directory path")
    sp.set_defaults(func=cmd_update_task_status)

    sp = sub.add_parser("find_next_task", help="Find next available task")
    sp.add_argument("--manifest", required=True, help="Path to task manifest.json")
    sp.set_defaults(func=cmd_find_next_task)

    sp = sub.add_parser("validate_manifest", help="Validate manifest consistency")
    sp.add_argument("--feature-dir", required=True, help="Feature directory path")
    sp.set_defaults(func=cmd_validate_manifest)

    sp = sub.add_parser("list_memory_artifacts", help="List memory artifacts for feature")
    sp.add_argument("--dir", default=".claude/memory", help="Memory directory")
    sp.add_argument("--feature", default=None, help="Optional feature filter")
    sp.set_defaults(func=cmd_list_memory_artifacts)

    sp = sub.add_parser("query_memory", help="Query knowledge graph with natural language")
    sp.add_argument("--dir", default=".claude/memory", help="Memory directory")
    sp.add_argument("--query", required=True, help="Natural language query")
    sp.add_argument("--feature", default=None, help="Feature slug to query")
    sp.add_argument("--mode", choices=["auto", "direct", "nlp"], default="auto", help="Query mode")
    sp.add_argument("--limit", type=int, default=10, help="Max results to return")
    sp.set_defaults(func=cmd_query_memory)

    sp = sub.add_parser("sync_memory_graph", help="Sync markdown files to JSONL knowledge graph")
    sp.add_argument("--dir", default=".claude/memory", help="Memory directory")
    sp.add_argument("--feature", default=None, help="Feature slug (sync single feature)")
    sp.set_defaults(func=cmd_sync_memory_graph)

    return p


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
