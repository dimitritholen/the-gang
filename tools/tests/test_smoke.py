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
