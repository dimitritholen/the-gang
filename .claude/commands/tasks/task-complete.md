---
allowed-tools: Bash(code-tools:*)
description: Mark a task as completed with verification
---

You are helping the user mark a task as completed.

**Task**: Validate completion and update task status to COMPLETED with automatic manifest synchronization.

## Chain-of-Thought Reasoning

Before executing completion, reason through:

**Step 1: Input Validation**

- Is TASK_ID format valid?
- Does feature directory exist?
- Can task file be located?

**Step 2: Current State Analysis**

- What is the current task status?
- Are there blocking dependencies?
- Is this task in a valid state for completion?

**Step 3: Acceptance Criteria Evaluation**

- Extract all criteria from task XML
- Present each criterion for user verification
- Determine if ALL criteria can be met

**Step 4: Completion Impact Assessment**

- What is the current feature progress?
- How does completing this task affect the feature state?
- Are there dependent tasks that become unblocked?
- Is this the final task in the feature?

## Input

User provides: `/task-complete {TASK_ID} {feature-id}-{slug}`

Example: `/task-complete T01 01-user-authentication`

## Verification Protocol

### Phase 1: Pre-Execution Verification

```bash
# Parse and validate arguments
TASK_ID="$1"
FEATURE_SLUG="$2"
FEATURE_DIR=".tasks/${FEATURE_SLUG}"

# Verify feature directory exists
if [ ! -d "$FEATURE_DIR" ]; then
    echo "ERROR: Feature directory not found: $FEATURE_DIR"
    exit 1
fi

# Verify task file exists
TASK_FILE="${FEATURE_DIR}/${TASK_ID}-${FEATURE_SLUG##*-}.xml"
if [ ! -f "$TASK_FILE" ]; then
    echo "ERROR: Task file not found: $TASK_FILE"
    exit 1
fi

# Read task XML and extract metadata
TASK_METADATA=$(code-tools read_task_metadata --task-file "$TASK_FILE")
TASK_TITLE=$(echo "$TASK_METADATA" | code-tools parse_json --field "title")
CURRENT_STATUS=$(echo "$TASK_METADATA" | code-tools parse_json --field "status")

# Verify task is in valid state for completion
if [ "$CURRENT_STATUS" != "IN_PROGRESS" ]; then
    case "$CURRENT_STATUS" in
        "NOT_STARTED")
            echo "Cannot complete task that hasn't been started."
            echo "Run: /task-start $TASK_ID $FEATURE_SLUG"
            exit 1
            ;;
        "COMPLETED")
            echo "Task already completed."
            exit 0
            ;;
        "BLOCKED")
            echo "Task is blocked and cannot be completed."
            echo "Unblock first: /task-unblock $TASK_ID $FEATURE_SLUG"
            exit 1
            ;;
    esac
fi
```

### Phase 2: Acceptance Criteria Verification

```bash
# Extract acceptance criteria for user confirmation
CRITERIA=$(echo "$TASK_METADATA" | code-tools parse_json --field "acceptance_criteria" --format "array")

# Present criteria as interactive checklist
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Complete Task: $TASK_ID - $TASK_TITLE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Acceptance Criteria:"
echo "$CRITERIA" | while IFS= read -r line; do echo "  [ ] $line"; done
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Have all acceptance criteria been met? (y/n)"
read -r CONFIRM

# Verification checkpoint: User must explicitly confirm
if [ "$CONFIRM" != "y" ]; then
    echo ""
    echo "Task completion cancelled."
    echo ""
    echo "Options:"
    echo "  1. Complete remaining work and try again"
    echo "  2. Block task if issue prevents completion:"
    echo "     /task-block $TASK_ID $FEATURE_SLUG \"reason\""
    exit 0
fi
```

### Phase 3: Execute Completion with Validation

```bash
# Update task status (delegates to task manager for atomic update)
UPDATE_RESULT=$(code-tools update_task_status \
    --task-id "$TASK_ID" \
    --status COMPLETED \
    --feature-dir "$FEATURE_DIR")

# Verify update succeeded
SUCCESS=$(echo "$UPDATE_RESULT" | code-tools parse_json --field "ok")

if [ "$SUCCESS" = "false" ]; then
    ERROR=$(echo "$UPDATE_RESULT" | code-tools parse_json --field "error")
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Task Completion Failed"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Error: $ERROR"
    echo ""
    exit 1
fi
```

### Phase 4: Post-Completion Verification

```bash
# Read updated manifest to verify state
MANIFEST_DATA=$(code-tools read_task_manifest --path "${FEATURE_DIR}/manifest.json")
COMPLETED_COUNT=$(echo "$MANIFEST_DATA" | code-tools parse_json --field "data.completed_count")
TASK_COUNT=$(echo "$MANIFEST_DATA" | code-tools parse_json --field "data.task_count")
PERCENT=$((COMPLETED_COUNT * 100 / TASK_COUNT))

# Verify task was actually marked complete
VERIFIED_STATUS=$(code-tools get_task_status --task-id "$TASK_ID" --feature-dir "$FEATURE_DIR")
if [ "$(echo "$VERIFIED_STATUS" | code-tools parse_json --field "data.status")" != "COMPLETED" ]; then
    echo "WARNING: Task status verification failed"
    exit 1
fi

# Find next available task
NEXT_TASK=$(code-tools find_next_task --manifest "${FEATURE_DIR}/manifest.json")
HAS_NEXT=$(echo "$NEXT_TASK" | code-tools parse_json --field "data.has_next")

# Check for task output documentation
OUTPUT_FILE="${FEATURE_DIR}/${TASK_ID}-output.md"
HAS_OUTPUT=false
if [ -f "$OUTPUT_FILE" ]; then
    HAS_OUTPUT=true
fi
```

## Output Format

### Success: Task Completed (More Tasks Remain)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task Completed: {TASK_ID} - {TASK_TITLE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: {FEATURE_ID}-{FEATURE_SLUG}
Completed: {DATE_TIME}
Duration: {started → completed time}

Acceptance Criteria Met:
  ✓ {Criterion 1}
  ✓ {Criterion 2}
  ✓ {Criterion 3}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature Progress: {N}/{TOTAL} tasks ({XX}%)
{Progress bar: ━━━━━━━━━━━━ XX%}

Next Task: {NEXT_TASK_ID} - {NEXT_TASK_TITLE}
  Priority: {HIGH|MEDIUM|LOW}
  Dependencies: {All met ✓}
  Estimated: {N} hours

Ready to continue?
  /task-start {NEXT_TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}
  or
  /task-next {FEATURE_ID}-{FEATURE_SLUG} for details

{If no output file exists:}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Note: No output file found

Consider documenting:
  - Changes made
  - Files created/modified
  - Test results
  - Known issues or follow-ups

Create output:
  Edit {FEATURE_DIR}/{TASK_ID}-output.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Success: Feature Completed (No More Tasks)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task Completed: {TASK_ID} - {TASK_TITLE}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: {FEATURE_ID}-{FEATURE_SLUG}
Completed: {DATE_TIME}

Acceptance Criteria Met:
  ✓ {Criterion 1}
  ✓ {Criterion 2}
  ✓ {Criterion 3}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature Completed!

All tasks in {FEATURE_ID}-{FEATURE_SLUG} are complete!
  Total tasks: {N}
  Total time: {estimated vs actual if available}
  Completed: {DATE}

Next steps:
  - Review feature deliverables
  - Run quality assurance
  - Deploy or move to next feature
  - Use /task-status to see other features

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Failure: Task Not In Progress

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cannot Complete Task
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: {TASK_ID} - {TASK_TITLE}
Current status: {NOT_STARTED|COMPLETED|BLOCKED}

{If NOT_STARTED:}
This task hasn't been started yet.
Run: /task-start {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}

{If COMPLETED:}
This task was already completed on {DATE}.

{If BLOCKED:}
This task is currently blocked: {blocker reason}
Unblock first: /task-unblock {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Failure: User Declined Criteria Verification

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task Completion Cancelled
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: {TASK_ID} - {TASK_TITLE}

Acceptance criteria not fully met.
This task cannot be marked complete until all acceptance
criteria are satisfied.

Options:
  1. Complete remaining work and try again
  2. Update acceptance criteria if they were incorrect
  3. Block task if issue prevents completion:
     /task-block {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG} "reason"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Integration with Task Manager

This command delegates completion logic to task manager:

```bash
code-tools update_task_status \
    --task-id {TASK_ID} \
    --status COMPLETED \
    --feature-dir {FEATURE_DIR}
```

The task manager handles:

- Atomic status transitions
- Manifest synchronization (task + root)
- XML file modifications
- Timestamp tracking
- Validation of state transitions
- Next task determination
- Feature completion detection

## Error Handling

| Error                    | Message                                    | Exit Code |
| ------------------------ | ------------------------------------------ | --------- |
| Invalid task ID          | "Task {ID} not found in feature {FEATURE}" | 1         |
| Invalid feature          | "Feature {FEATURE} not found"              | 1         |
| No manifest              | "Task manifest missing"                    | 1         |
| File corruption          | "Task XML file corrupted"                  | 1         |
| Invalid state transition | "Cannot complete task from {STATE}"        | 1         |
| Tool execution failure   | "Task manager error: {details}"            | 1         |

## Verification Checklist

Before reporting success, verify:

1. Task status is COMPLETED in XML
2. Manifest reflects correct completion count
3. Manifest progress percentage updated
4. Root manifest synchronized
5. Timestamps recorded accurately
6. Next task correctly identified (if applicable)
7. Feature completion detected (if final task)

## Related Commands

- `/task-start {task} {feature}` - Start a task
- `/task-next {feature}` - See next available task
- `/task-block {task} {feature} "reason"` - Block a task
- `/task-status {feature}` - Check progress
- `/task-unblock {task} {feature}` - Unblock a task

## Example Usage

```
User: /task-complete T01 01-user-authentication

System:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Complete Task: T01 - Implement login endpoint
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria:
  [ ] POST /api/auth/login endpoint created
  [ ] JWT token generation implemented
  [ ] Email/password validation added
  [ ] Integration tests passing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Have all acceptance criteria been met? (y/n)
User: y

System: [marks complete and shows next task]
```
