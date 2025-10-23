---
description: Unblock a task and resume work
---

You are helping the user unblock a task.

**Task**: Remove blocker and resume task via @task-manager.

## Input

User provides: `/task-unblock {TASK_ID} {feature-id}-{slug}`

Optional: `/task-unblock {TASK_ID} {feature-id}-{slug} "resolution notes"`

Example: `/task-unblock T02 01-user-authentication "API credentials obtained from DevOps"`

## Actions

1. Invoke @task-manager agent with operation: UNBLOCK_TASK
2. Task manager will:
   - Verify task status = BLOCKED
   - Update task XML: status="IN_PROGRESS", clear blocker, add resolution notes
   - Update task manifest: task status = IN_PROGRESS, remove from blockedBy
   - Update root manifest: remove blocker from feature blockers if no other tasks blocked
3. Display unblock confirmation and next steps

## Output Format

```
Task Unblocked: {TASK_ID} - {TASK_TITLE} ✓

Feature: {FEATURE_ID}-{FEATURE_SLUG}
Unblocked: {DATE_TIME}
Resolution: {User-provided resolution notes or "Blocker resolved"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Previous Blocker:
  {Original blocker reason}

Resolution:
  {Resolution notes if provided}

Task Status: IN_PROGRESS (resumed)
  Started: {Original start date}
  Blocked: {Block duration}
  Resumed: {Current date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Resume work on this task:
  - Review task description and acceptance criteria
  - Address the resolved blocker in your implementation
  - Update task output with resolution details

Task file: .tasks/{NN}-{slug}/{TASK_ID}-{slug}.xml

When complete:
  `/task-complete {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}`

Feature Progress: {N}/{TOTAL} tasks
⏳ 1 task resumed
━━━━━━━━ {XX}%
```

## Verification Questions

Before unblocking, optionally verify resolution:

```
Unblock Task: {TASK_ID} - {TASK_TITLE}

Original blocker: {blocker reason}

Has the blocker been fully resolved? (y/n)
{If no: "Please resolve the blocker before unblocking."}

{If yes, optionally:}
Provide brief resolution notes (or press Enter to skip):
```

## Integration with Task Manager

This command delegates to @task-manager agent:

```
@task-manager unblock {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG} "{resolution}"
```

The task manager handles:
- Status validation (must be BLOCKED)
- XML file update
- Manifest updates (task and root)
- Blocker removal
- Status restoration to IN_PROGRESS
- Timestamp recording

## Error Handling

- **Task not blocked**: "Cannot unblock {TASK_ID} - task is {status}, not BLOCKED."
- **Invalid task**: "Task {ID} not found in feature {FEATURE}"
- **Invalid feature**: "Feature {FEATURE} not found"
- **Premature unblock**: "Blocker may not be fully resolved. Confirm: {blocker details}"

## Example Usage

```
User: /task-unblock T02 01-user-authentication "Got API keys from admin"
```

Response: Task marked as IN_PROGRESS, blocker removed, user can resume work.

## Related Commands

- `/task-block {task} {feature} "reason"` - Block a task
- `/task-complete {task} {feature}` - Mark task complete after unblocking
- `/task-status {feature}` - Check for blocked tasks
- `/task-next {feature}` - See next available task
