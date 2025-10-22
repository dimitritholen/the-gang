import json
import subprocess
from pathlib import Path
from jsonschema import validate


RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["ok", "tool", "version"],
    "properties": {
        "ok": {"type": "boolean"},
        "tool": {"type": "string"},
        "version": {"type": "string"},
        "data": {},
        "error": {"type": "string"},
    },
}


def run_ok(cmd):
    out = subprocess.check_output(cmd, text=True)
    data = json.loads(out)
    assert data.get("ok") is True
    assert isinstance(data.get("version"), str)
    assert isinstance(data.get("tool"), str)
    validate(instance=data, schema=RESPONSE_SCHEMA)
    return data


def run_fail(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    assert p.returncode != 0
    payload = p.stdout or p.stderr
    data = json.loads(payload)
    assert data.get("ok") is False
    validate(instance=data, schema=RESPONSE_SCHEMA)
    return data


def test_list_dir_bad_path():
    data = run_fail(["code-tools", "list_dir", "--path", "./__does_not_exist__", "--depth", "1"])
    assert "not found" in data.get("error", "").lower()


def test_search_file_no_match(tmp_path):
    data = run_ok(["code-tools", "search_file", "--path", str(tmp_path), "--glob", "**/*.xyz"])  # unlikely ext
    assert data["data"] == []


def test_grep_code_invalid_regex(tmp_path):
    p = tmp_path / "x.txt"
    p.write_text("abc\n")
    data = run_fail(["code-tools", "grep_code", "--pattern", "[", "--paths", str(tmp_path)])
    assert "error" in data


def test_read_file_bad_ranges(tmp_path):
    p = tmp_path / "r.txt"
    p.write_text("a\n")
    data = run_fail(["code-tools", "read_file", "--path", str(p), "--start", "0", "--end", "1"])  # start < 1
    assert "start must be" in data.get("error", "")


def test_search_replace_uniqueness(tmp_path):
    f = tmp_path / "t.txt"
    f.write_text("apple apple\n")
    reps = [{"original_text": "apple", "new_text": "pear", "replace_all": False}]
    spec = tmp_path / "reps.json"
    spec.write_text(json.dumps(reps))
    data = run_fail(["code-tools", "search_replace", "--file", str(f), "--replacements", f"@{spec}"])
    assert "not unique" in data.get("error", "").lower()


def test_search_replace_replace_all(tmp_path):
    f = tmp_path / "t2.txt"
    f.write_text("apple apple\n")
    reps = [{"original_text": "apple", "new_text": "pear", "replace_all": True}]
    spec = tmp_path / "r2.json"
    spec.write_text(json.dumps(reps))
    data = run_ok(["code-tools", "search_replace", "--file", str(f), "--replacements", f"@{spec}"])
    assert Path(f).read_text() == "pear pear\n"


def test_create_file_add_newline(tmp_path):
    f = tmp_path / "n.txt"
    run_ok(["code-tools", "create_file", "--file", str(f), "--content", "X", "--add-last-line-newline"])
    assert Path(f).read_text().endswith("\n")


def test_search_memory_empty_dir(tmp_path):
    mem = tmp_path / "mem"
    mem.mkdir()
    data = run_ok(["code-tools", "search_memory", "--dir", str(mem), "--query", "anything", "--topk", "5"])
    assert data["data"] == []


def test_parallel_one_failure(tmp_path):
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps([
        ["code-tools", "read_file", "--path", str(tmp_path / "no.txt"), "--start", "1", "--end", "2"],
        ["code-tools", "search_file", "--path", str(tmp_path), "--glob", "**/*"],
    ]))
    out = subprocess.check_output(["code-tools-parallel", "--spec", str(spec)], text=True)
    merged = json.loads(out)
    assert merged["ok"] is True
    # index 0 should be an error object from child
    assert merged["results"]["0"].get("ok") is False


def test_large_file_read_and_encoding(tmp_path):
    # Create a large UTF-8 file (>10k lines) with some non-ASCII content
    p = tmp_path / "large.txt"
    with p.open("w", encoding="utf-8") as f:
        for i in range(12000):
            f.write(f"línea-{i} αβγ 漢字\n")
    # Read a mid-range slice
    data = run_ok(["code-tools", "read_file", "--path", str(p), "--start", "5000", "--end", "5100"])
    assert data["data"]["line_count"] == 101
    assert "línea-5000" in data["data"]["content"]

    # Validate search_replace with UTF-8 content
    reps = [{"original_text": "αβγ", "new_text": "XYZ", "replace_all": True}]
    spec = tmp_path / "utf.json"
    spec.write_text(json.dumps(reps))
    data2 = run_ok(["code-tools", "search_replace", "--file", str(p), "--replacements", f"@{spec}"])
    # Ensure replacement applied in summary
    assert any(r["count"] > 0 for r in data2["data"]["applied"])  # type: ignore[index]
