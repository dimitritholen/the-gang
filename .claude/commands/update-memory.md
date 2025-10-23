---
allowed-tools: Task, Read, Bash, Glob, Grep
argument-hint: [aspect]
description: Incrementally update memory artifacts after codebase changes
---

## Purpose

Re-analyze specific aspects of the codebase after changes (new dependencies, refactoring, etc.) without full regeneration.

## Usage

```bash
/update-memory "tech-stack"     # After adding/removing dependencies
/update-memory "conventions"    # After style changes
/update-memory "architecture"   # After refactoring
/update-memory "features"       # After adding new features
/update-memory "all"            # Full refresh
```

## Process

1. **Load existing artifacts** from `.claude/memory/`
2. **Re-analyze specified aspect** using codebase-archeologist
3. **Diff old vs new** and highlight changes
4. **Update artifact** with new analysis
5. **Preserve unchanged sections** (no unnecessary rewrites)

## Output

- Updated artifact with diff summary
- Changelog of what changed
- Confidence levels for new inferences

---

Invoke codebase-archeologist with scope: **$ASPECT**
