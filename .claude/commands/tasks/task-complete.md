---
allowed-tools: Bash(code-tools:*)
description: Mark a task as completed
---

You are helping the user mark a task as completed.

**Task**: Validate completion and update task status to COMPLETED with automatic manifest synchronization.

## Input

User provides: `/task-complete {TASK_ID} {feature-id}-{slug}`

Example: `/task-complete T01 01-user-authentication`

## Actions

Use CLI tools for efficient task completion:

```bash
# Parse arguments
TASK_ID="$1"
FEATURE_SLUG="$2"
FEATURE_DIR=".tasks/${FEATURE_SLUG}"

# Read task XML to get acceptance criteria
TASK_FILE="${FEATURE_DIR}/${TASK_ID}-${FEATURE_SLUG##*-}.xml"
TASK_XML=$(cat "$TASK_FILE")

# Extract acceptance criteria for confirmation
CRITERIA=$(echo "$TASK_XML" | grep -oP '<criteria>.*?</criteria>' | sed 's/<[^>]*>//g')

# Display criteria and ask for confirmation
echo "Complete Task: $TASK_ID"
echo ""
echo "Acceptance Criteria:"
echo "$CRITERIA" | sed 's/^/- [ ] /'
echo ""
echo "Have all acceptance criteria been met? (y/n)"

# Wait for user confirmation
read -r CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "Task completion cancelled."
    exit 0
fi

# Update task status (handles validation, manifest sync, next task determination automatically)
UPDATE_RESULT=$(code-tools update_task_status --task-id "$TASK_ID" --status COMPLETED --feature-dir "$FEATURE_DIR")

# Check if update was successful
SUCCESS=$(echo "$UPDATE_RESULT" | jq -r '.ok')

if [ "$SUCCESS" = "false" ]; then
    # Display error (not in progress, already completed, etc.)
    ERROR=$(echo "$UPDATE_RESULT" | jq -r '.error')
    echo "$ERROR"
    exit 1
fi

# Get updated manifest data
MANIFEST_DATA=$(code-tools read_task_manifest --path "${FEATURE_DIR}/manifest.json")
COMPLETED_COUNT=$(echo "$MANIFEST_DATA" | jq -r '.data.completed_count')
TASK_COUNT=$(echo "$MANIFEST_DATA" | jq -r '.data.task_count')
PERCENT=$((COMPLETED_COUNT * 100 / TASK_COUNT))

# Find next available task
NEXT_TASK=$(code-tools find_next_task --manifest "${FEATURE_DIR}/manifest.json")
HAS_NEXT=$(echo "$NEXT_TASK" | jq -r '.data.has_next')

# Display success format below
```

## Acceptance Criteria Verification

Before completing, confirm with user:

```
Complete Task: {TASK_ID} - {TASK_TITLE}

Acceptance Criteria:
- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

Have all acceptance criteria been met? (y/n)
```

If user confirms, proceed with completion.

## Output Format (Success)

```
Task Completed: {TASK_ID} - {TASK_TITLE} ✓

Feature: {FEATURE_ID}-{FEATURE_SLUG}
Completed: {DATE_TIME}
Duration: {started → completed time}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria Met:
✓ {Criterion 1}
✓ {Criterion 2}
✓ {Criterion 3}

Feature Progress: {N+1}/{TOTAL} tasks ({XX}%)
━━━━━━━━━━━━ {XX}%

{If more tasks remain:}
Next Task: {NEXT_TASK_ID} - {NEXT_TASK_TITLE}
  Priority: {HIGH|MEDIUM|LOW}
  Dependencies: {All met ✓}
  Estimated: {N} hours

Ready to continue?
  `/task-start {NEXT_TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}`
  or
  `/task-next {FEATURE_ID}-{FEATURE_SLUG}` for details

{If all tasks complete:}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 Feature Completed!

All tasks in {FEATURE_ID}-{FEATURE_SLUG} are complete!
  Total tasks: {N}
  Total time: {estimated vs actual if available}
  Completed: {DATE}

Next steps:
  - Review feature deliverables
  - Run quality assurance
  - Deploy or move to next feature
  - Use `/task-status` to see other features

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task output saved to:
  .tasks/{NN}-{slug}/{TASK_ID}-output.md

{If output file doesn't exist:}
⚠️  No output file found. Consider documenting:
  - Changes made
  - Files created/modified
  - Test results
  - Known issues or follow-ups

Create output:
  Edit .tasks/{NN}-{slug}/{TASK_ID}-output.md
```

## Output Format (Validation Failure)

### Task Not In Progress

```
Cannot Complete Task

Task: {TASK_ID} - {TASK_TITLE}
Current status: {NOT_STARTED|COMPLETED|BLOCKED}

{If NOT_STARTED:}
This task hasn't been started yet.
Run: `/task-start {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}`

{If COMPLETED:}
This task was already completed on {DATE}.

{If BLOCKED:}
This task is currently blocked: {blocker reason}
Unblock first: `/task-unblock {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}`
```

### Acceptance Criteria Not Met

```
Task Completion Blocked

Task: {TASK_ID} - {TASK_TITLE}

Unmet Acceptance Criteria:
✗ {Criterion that failed}
✗ {Another unmet criterion}

This task cannot be marked complete until all acceptance
criteria are satisfied.

Options:
  1. Complete remaining work and try again
  2. Update acceptance criteria if they were incorrect
  3. Block task if issue prevents completion:
     `/task-block {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG} "reason"`
```

## Integration with Task Manager

This command delegates to @task-manager agent:

```
@task-manager complete {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}
```

The task manager handles:

- Status validation
- Manifest updates (task and root)
- XML file modifications
- Next task determination
- Feature completion detection
- Timestamp tracking

## Optional: Create Task Output

After completion, optionally create structured output document:

```
Would you like to document this task completion? (y/n)

{If yes:}
Creating .tasks/{NN}-{slug}/{TASK_ID}-output.md

Use the template to document:
- Work performed
- Files created/modified
- Test results
- Challenges encountered
- Next steps
```

## Error Handling

- **Invalid task ID**: "Task {ID} not found in feature {FEATURE}"
- **Invalid feature**: "Feature {FEATURE} not found"
- **No manifest**: "Task manifest missing"
- **File corruption**: "Task XML file corrupted"

## Example Usage

```
User: /task-complete T01 01-user-authentication
```

System asks for acceptance criteria confirmation, then marks complete and shows next task.

## Related Commands

- `/task-start {task} {feature}` - Start a task
- `/task-next {feature}` - See next available task
- `/task-block {task} {feature} "reason"` - Block a task
- `/task-status {feature}` - Check progress
