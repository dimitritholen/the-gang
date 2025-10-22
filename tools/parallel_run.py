import argparse
import json
import subprocess
from typing import List, Dict, Any


def run_parallel(commands: List[List[str]]) -> Dict[str, Any]:
    # Prefer absolute path for code-tools if available
    import shutil
    code_tools_bin = shutil.which("code-tools") or shutil.which("code-tools", path="/home/dimitri/.pyenv/versions/3.12.11/bin")
    normalized = []
    for cmd in commands:
        if cmd and cmd[0] == "code-tools" and code_tools_bin:
            cmd = [code_tools_bin] + cmd[1:]
        normalized.append(cmd)
    procs = {i: subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for i, cmd in enumerate(normalized)}
    results: Dict[str, Any] = {}
    for i, p in procs.items():
        out, err = p.communicate()
        if p.returncode != 0:
            results[i] = {"ok": False, "error": err.strip() or out.strip(), "cmd": commands[i]}
        else:
            try:
                results[i] = json.loads(out.strip())
            except Exception:
                results[i] = {"ok": False, "error": "Non-JSON output", "stdout": out, "cmd": commands[i]}
    return {"ok": True, "results": results}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run multiple code-tools commands in parallel")
    parser.add_argument("--spec", required=True, help="Path to JSON file: array of command arrays")
    args = parser.parse_args()
    spec = json.loads(open(args.spec, "r", encoding="utf-8").read())
    if not isinstance(spec, list) or not all(isinstance(x, list) and x for x in spec):
        print(json.dumps({"ok": False, "error": "spec must be list of non-empty command arrays"}))
        raise SystemExit(1)
    merged = run_parallel(spec)
    print(json.dumps(merged, ensure_ascii=False))


if __name__ == "__main__":
    main()
