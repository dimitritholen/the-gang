import json
import os
import subprocess
from pathlib import Path


def run(cmd):
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)


def test_list_dir(tmp_path):
    d = tmp_path / "a"
    d.mkdir()
    (d / "x.txt").write_text("hi")
    res = run(["code-tools", "list_dir", "--path", str(tmp_path), "--depth", "1"])
    assert res["ok"]
    assert any(entry["path"].endswith("x.txt") for entry in res["data"])  # type: ignore[index]


def test_search_file(tmp_path):
    (tmp_path / "f1.py").write_text("print('a')")
    res = run(["code-tools", "search_file", "--path", str(tmp_path), "--glob", "**/*.py"]) 
    assert res["ok"]
    assert any(x["path"].endswith("f1.py") for x in res["data"])  # type: ignore[index]


def test_grep_code(tmp_path):
    p = tmp_path / "m.txt"
    p.write_text("hello\nTODO: fix\n")
    res = run(["code-tools", "grep_code", "--pattern", "TODO", "--paths", str(tmp_path)])
    assert res["ok"]
    assert any(x["path"].endswith("m.txt") for x in res["data"])  # type: ignore[index]


def test_read_file(tmp_path):
    p = tmp_path / "r.txt"
    p.write_text("a\nb\nc\n")
    res = run(["code-tools", "read_file", "--path", str(p), "--start", "2", "--end", "3"])
    assert res["ok"]
    assert res["data"]["line_count"] == 2  # type: ignore[index]


def test_create_and_search_replace_and_edit(tmp_path):
    f = tmp_path / "file.txt"
    res = run(["code-tools", "create_file", "--file", str(f), "--content", "hello world"])
    assert res["ok"] and Path(res["data"]["file"]).exists()  # type: ignore[index]
    reps = [{"original_text": "world", "new_text": "there", "replace_all": False}]
    spec = tmp_path / "reps.json"
    spec.write_text(json.dumps(reps))
    res = run(["code-tools", "search_replace", "--file", str(f), "--replacements", f"@{spec}"])
    assert res["ok"]
    # edit_file replaces content with patch text
    res = run(["code-tools", "edit_file", "--file", str(f), "--patch", "NEW\n"])
    assert res["ok"]
    assert (tmp_path / "file.txt").read_text() == "NEW\n"


def test_search_memory(tmp_path, monkeypatch):
    mem = tmp_path / ".dimitri" / "memory"
    mem.mkdir(parents=True)
    (mem / "a.md").write_text("auth flow involves login")
    (mem / "b.txt").write_text("database config and tokens")
    res = run(["code-tools", "search_memory", "--dir", str(mem), "--query", "auth flow", "--topk", "5"])
    assert res["ok"]
    assert len(res["data"]) >= 1  # type: ignore[index]


def test_fetch_content_smoke():
    proc = subprocess.run(["code-tools", "fetch_content", "--url", "https://example.com"], capture_output=True, text=True)
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data.get("ok") is True


def test_parallel_helper(tmp_path):
    a = tmp_path / "a.txt"
    a.write_text("A\nB\nC\n")
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps([
        ["code-tools", "read_file", "--path", str(a), "--start", "1", "--end", "2"],
        ["code-tools", "grep_code", "--pattern", "A", "--paths", str(tmp_path)],
    ]))
    out = subprocess.check_output(["code-tools-parallel", "--spec", str(spec)], text=True)
    merged = json.loads(out)
    assert merged["ok"] and len(merged["results"]) == 2


def test_slugify_feature():
    res = run(["code-tools", "slugify_feature", "--name", "User Authentication"])
    assert res["ok"]
    assert res["data"]["slug"] == "user-authentication"
    assert res["data"]["original"] == "User Authentication"


def test_slugify_feature_with_id():
    res = run(["code-tools", "slugify_feature", "--name", "User Auth", "--feature-id", "01"])
    assert res["ok"]
    assert res["data"]["slug"] == "user-auth"
    assert res["data"]["feature_id"] == "01"
    assert res["data"]["dir"] == ".tasks/01-user-auth"


def test_read_task_manifest(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "feature": {"id": "01", "name": "Test"},
        "tasks": [
            {"id": "T01", "status": "COMPLETED"},
            {"id": "T02", "status": "IN_PROGRESS"},
            {"id": "T03", "status": "NOT_STARTED"}
        ]
    }))
    res = run(["code-tools", "read_task_manifest", "--path", str(manifest)])
    assert res["ok"]
    assert res["data"]["task_count"] == 3
    assert res["data"]["completed_count"] == 1
    assert res["data"]["in_progress_count"] == 1


def test_find_next_task(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "feature": {"id": "01"},
        "tasks": [
            {"id": "T01", "status": "COMPLETED", "dependencies": []},
            {"id": "T02", "status": "NOT_STARTED", "dependencies": ["T01"]},
            {"id": "T03", "status": "NOT_STARTED", "dependencies": ["T02"]}
        ]
    }))
    res = run(["code-tools", "find_next_task", "--manifest", str(manifest)])
    assert res["ok"]
    assert res["data"]["task_id"] == "T02"
    assert res["data"]["has_next"] is True


def test_find_next_task_none_available(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "feature": {"id": "01"},
        "tasks": [
            {"id": "T01", "status": "COMPLETED", "dependencies": []},
            {"id": "T02", "status": "IN_PROGRESS", "dependencies": ["T01"]}
        ]
    }))
    res = run(["code-tools", "find_next_task", "--manifest", str(manifest)])
    assert res["ok"]
    assert res["data"]["has_next"] is False


def test_list_memory_artifacts(tmp_path):
    memory = tmp_path / ".claude" / "memory"
    memory.mkdir(parents=True)
    (memory / "requirements-user-auth.md").write_text("# Requirements")
    (memory / "tech-analysis-user-auth.md").write_text("# Tech")
    (memory / "implementation-plan-user-auth.md").write_text("# Plan")
    (memory / "other-doc.md").write_text("# Other")

    res = run(["code-tools", "list_memory_artifacts", "--dir", str(memory)])
    assert res["ok"]
    assert len(res["data"]["artifacts"]["requirements"]) == 1
    assert len(res["data"]["artifacts"]["tech_analysis"]) == 1
    assert len(res["data"]["artifacts"]["implementation_plans"]) == 1
    assert len(res["data"]["artifacts"]["other"]) == 1
    assert res["data"]["total"] == 4


def test_list_memory_artifacts_with_filter(tmp_path):
    memory = tmp_path / ".claude" / "memory"
    memory.mkdir(parents=True)
    (memory / "requirements-user-auth.md").write_text("# Req1")
    (memory / "requirements-product-catalog.md").write_text("# Req2")

    res = run(["code-tools", "list_memory_artifacts", "--dir", str(memory), "--feature", "user-auth"])
    assert res["ok"]
    assert res["data"]["total"] == 1
    assert "user-auth" in res["data"]["artifacts"]["requirements"][0]


def test_validate_manifest(tmp_path):
    feature_dir = tmp_path / "01-test"
    feature_dir.mkdir()

    task_manifest = feature_dir / "manifest.json"
    task_manifest.write_text(json.dumps({
        "feature": {"id": "01"},
        "tasks": [
            {"id": "T01", "status": "COMPLETED"},
            {"id": "T02", "status": "IN_PROGRESS"}
        ]
    }))

    root_manifest = tmp_path / ".tasks" / "manifest.json"
    root_manifest.parent.mkdir(parents=True, exist_ok=True)
    root_manifest.write_text(json.dumps({
        "features": [
            {
                "id": "01",
                "taskCount": 2,
                "completedCount": 1,
                "status": "IN_PROGRESS"
            }
        ]
    }))

    # Change to tmp_path so relative paths work
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        res = run(["code-tools", "validate_manifest", "--feature-dir", "01-test"])
        assert res["ok"]
        assert res["data"]["valid"] is True
        assert len(res["data"]["issues"]) == 0
    finally:
        os.chdir(old_cwd)
