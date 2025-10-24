---
allowed-tools: Bash(code-tools:*)
description: Start working on a specific task
---

You are helping the user start a task.

**Task**: Mark task as IN_PROGRESS with automatic dependency validation and manifest synchronization.

## Input

User provides: `/task-start {TASK_ID} {feature-id}-{slug}`

Example: `/task-start T01 01-user-authentication`

## Actions

Use CLI tools for efficient task status update:

```bash
# Parse arguments
TASK_ID="$1"
FEATURE_SLUG="$2"
FEATURE_DIR=".tasks/${FEATURE_SLUG}"

# Validate task exists and get current status
MANIFEST_DATA=$(code-tools read_task_manifest --path "${FEATURE_DIR}/manifest.json")
TASK_EXISTS=$(echo "$MANIFEST_DATA" | jq -r ".data.manifest.tasks[] | select(.id==\"$TASK_ID\") | .id")

if [ -z "$TASK_EXISTS" ]; then
    echo "Task $TASK_ID not found in feature $FEATURE_SLUG"
    exit 1
fi

# Update task status (handles validation, dependencies, manifest sync automatically)
UPDATE_RESULT=$(code-tools update_task_status --task-id "$TASK_ID" --status IN_PROGRESS --feature-dir "$FEATURE_DIR")

# Check if update was successful
SUCCESS=$(echo "$UPDATE_RESULT" | jq -r '.ok')

if [ "$SUCCESS" = "false" ]; then
    # Display error (dependency not met, already started, etc.)
    ERROR=$(echo "$UPDATE_RESULT" | jq -r '.error')
    echo "$ERROR"
    exit 1
fi

# Read task XML for display
TASK_FILE="${FEATURE_DIR}/${TASK_ID}-${FEATURE_SLUG##*-}.xml"
TASK_XML=$(cat "$TASK_FILE")

# Extract task details
TITLE=$(echo "$TASK_XML" | grep -oP '<title>\K[^<]+')
STARTED=$(echo "$UPDATE_RESULT" | jq -r '.data.timestamp')

# Display success format below
```

## Output Format (Success)

```
Task Started: {TASK_ID} - {TASK_TITLE}

Feature: {FEATURE_ID}-{FEATURE_SLUG}
Status: IN_PROGRESS
Started: {DATE_TIME}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Task Description

{Full description}

## Acceptance Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Completion Checklist

- [ ] {Checklist item 1}
- [ ] {Checklist item 2}
- [ ] {Checklist item 3}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task file: .tasks/{NN}-{slug}/{TASK_ID}-{slug}.xml
Output will be saved to: .tasks/{NN}-{slug}/{TASK_ID}-output.md

When complete, run:
  `/task-complete {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}`

To block this task:
  `/task-block {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG} "reason"`
```

## Output Format (Validation Failure)

### Task Already Started

```
Cannot Start Task

Task: {TASK_ID} - {TASK_TITLE}
Current status: {IN_PROGRESS|COMPLETED}

{If IN_PROGRESS:}
This task is already in progress (started {DATE}).

To complete it:
  `/task-complete {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}`

To abandon and restart:
  Contact maintainer for manual status reset.

{If COMPLETED:}
This task was completed on {DATE}.
Cannot restart completed tasks.
```

### Dependencies Not Met

```
Cannot Start Task - Dependencies Not Met

Task: {TASK_ID} - {TASK_TITLE}
Status: NOT_STARTED

Blocked By:
  ⏳ {DEP1_ID} - {DEP1_TITLE} (status: IN_PROGRESS)
  ⏸️  {DEP2_ID} - {DEP2_TITLE} (status: NOT_STARTED)

This task depends on the above tasks completing first.

Recommended Action:
  1. Complete {DEP1_ID} first
  2. Then complete {DEP2_ID}
  3. Return to start {TASK_ID}

Or work on alternative task:
  {If alternatives exist:}
  `/task-next {FEATURE_ID}-{FEATURE_SLUG}` to find ready tasks
```

## Integration with Task Manager

This command delegates to @task-manager agent:

```
@task-manager start {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}
```

The task manager handles:

- Dependency validation
- Status transitions
- Manifest updates
- XML file modifications
- Timestamp tracking

## Error Handling

- **Invalid task ID**: "Task {ID} not found in feature {FEATURE}"
- **Invalid feature**: "Feature {FEATURE} not found"
- **No manifest**: "Task manifest missing. Run /plan-implementation first"
- **File corruption**: "Task XML file corrupted or missing"

## Example Usage

```
User: /task-start T01 01-user-authentication
```

Response: Task marked as IN_PROGRESS, full details displayed, ready to execute.

## Related Commands

- `/task-next {feature}` - See next available task
- `/task-complete {task} {feature}` - Mark task as completed
- `/task-block {task} {feature} "reason"` - Mark task as blocked
- `/task-status {feature}` - Check overall progress
