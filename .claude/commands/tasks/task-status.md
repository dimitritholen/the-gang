---
allowed-tools: Bash(code-tools:*), Read, Glob
description: Check task progress and feature status
---

You are helping the user check task progress for a feature.

**Task**: Display comprehensive status of tasks for the specified feature.

## Input

User provides: `/task-status {feature-id}-{slug}` or `/task-status` (for all features)

## Actions

### If Specific Feature Provided

Use CLI tools to gather data efficiently:

```bash
# Feature slug from arguments
FEATURE_SLUG="$ARGUMENTS"
FEATURE_DIR=".tasks/${FEATURE_SLUG}"

# Read and validate task manifest with automatic metrics calculation
MANIFEST_DATA=$(code-tools read_task_manifest --path "${FEATURE_DIR}/manifest.json")

# Extract metrics (all computed by CLI)
TASK_COUNT=$(echo "$MANIFEST_DATA" | jq -r '.data.task_count')
COMPLETED=$(echo "$MANIFEST_DATA" | jq -r '.data.completed_count')
IN_PROGRESS=$(echo "$MANIFEST_DATA" | jq -r '.data.in_progress_count')
BLOCKED=$(echo "$MANIFEST_DATA" | jq -r '.data.blocked_count')
NOT_STARTED=$((TASK_COUNT - COMPLETED - IN_PROGRESS - BLOCKED))
PERCENT=$((COMPLETED * 100 / TASK_COUNT))

# Get feature metadata
FEATURE_DATA=$(echo "$MANIFEST_DATA" | jq -r '.data.manifest.feature')

# Find next available task (validates dependencies)
NEXT_TASK=$(code-tools find_next_task --manifest "${FEATURE_DIR}/manifest.json")
NEXT_ID=$(echo "$NEXT_TASK" | jq -r '.data.task_id // "null"')

# Display results using Output Format below
```

### If No Feature Specified (Show All)

Use Read tool to access manifest, then iterate:

```bash
# Read root manifest using Read tool
# For each feature discovered, read its manifest and display summary
```

Alternative using Glob for discovery:

```bash
# Use Glob tool to find all feature manifest files
# Pattern: .tasks/*/manifest.json
# Then Read each manifest individually
```

## Output Format

### Single Feature Status

```
Feature Status: {FEATURE_ID}-{FEATURE_SLUG}
Title: {Feature Title}
Status: {NOT_STARTED|IN_PROGRESS|COMPLETED|BLOCKED}
Priority: {CRITICAL|HIGH|MEDIUM|LOW}

Progress: {N}/{TOTAL} tasks completed ({XX}%)
-------------------- {XX}%

Task Breakdown:
  - Completed: {N} tasks
  - In Progress: {N} tasks
  - Not Started: {N} tasks
  - Blocked: {N} tasks

Next Task: {TASK_ID} - {TASK_TITLE}
  Status: NOT_STARTED
  Dependencies: {DEP1, DEP2} (all completed)
  Estimated: {N} hours
  Priority: {HIGH|MEDIUM|LOW}

Blocked Tasks:
  - {TASK_ID} - {TASK_TITLE}
    Blocked by: {Blocker description}

Completed Tasks:
  - {TASK_ID} - {TASK_TITLE} (completed {DATE})
  - {TASK_ID} - {TASK_TITLE} (completed {DATE})

Remaining Work:
  Estimated: {N} hours
  Critical path: {TASK_ID} -> {TASK_ID} -> {TASK_ID}

Files:
  - .tasks/{NN}-{slug}/feature-brief.md
  - .tasks/{NN}-{slug}/requirements-{slug}.md
  - .tasks/{NN}-{slug}/tech-analysis-{slug}.md
  - .tasks/{NN}-{slug}/manifest.json
  - {N} task files (TNN-*.xml)
```

### All Features Status

```
Project Task Status

Total Features: {N}
  - Completed: {N}
  - In Progress: {N}
  - Not Started: {N}

----------------------------------------

Feature 01: user-authentication
  Status: IN_PROGRESS
  Progress: 5/8 tasks (62%)
  Next: T06 - Integration Tests
  ------------ 62%

Feature 02: product-catalog
  Status: NOT_STARTED
  Progress: 0/12 tasks (0%)
  Next: T01 - Database Schema
  - 0%

Feature 03: admin-dashboard
  Status: COMPLETED
  Progress: 6/6 tasks (100%)
  Completed: {DATE}
  -------------------- 100%

Use `/task-status {NN}-{slug}` for detailed feature status
```

## Example Usage

```
User: /task-status 01-user-authentication
```

Response: Full detailed status for that feature with next task, progress, blockers.

```
User: /task-status
```

Response: Summary of all features with progress bars.

## Error Handling

- **No .tasks/ directory**: "No tasks found. Run /gather-requirements to start a feature."
- **Invalid feature ID**: "Feature {ID} not found. Available: {list}"
- **Empty manifest**: "No tasks created yet. Run /plan-implementation {feature-id}-{slug}"
