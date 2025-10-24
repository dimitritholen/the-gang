---
description: Mark a task as blocked by an issue
---

You are helping the user mark a task as blocked.

**Task**: Record blocker and update task status to BLOCKED via @task-manager.

## Input

User provides: `/task-block {TASK_ID} {feature-id}-{slug} "blocker reason"`

Example: `/task-block T02 01-user-authentication "Missing API credentials"`

## Actions

1. Invoke @task-manager agent with operation: BLOCK_TASK
2. Task manager will:
   - Verify task status = IN_PROGRESS
   - Update task XML: status="BLOCKED", add blocker description
   - Update task manifest: task status = BLOCKED, add to blockedBy array
   - Update root manifest: add blocker to feature blockers array
3. Display blocker summary and resolution guidance

## Output Format

```
Task Blocked: {TASK_ID} - {TASK_TITLE} 🚫

Feature: {FEATURE_ID}-{FEATURE_SLUG}
Blocked: {DATE_TIME}
Reason: {Blocker reason provided by user}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This task is now blocked and cannot proceed until the issue is resolved.

Blocker Details:
  Issue: {User-provided reason}
  Severity: {Assessed based on impact}
  Impact: {Explanation of what this blocks}

Recommended Actions:
  1. {Suggested resolution step 1}
  2. {Suggested resolution step 2}
  3. {Suggested resolution step 3}

Once blocker is resolved:
  `/task-unblock {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}`

Alternative Work:
  {If other tasks available:}
  Work on alternative task while resolving blocker:
    `/task-next {FEATURE_ID}-{FEATURE_SLUG}` to find available tasks

  {If no alternatives:}
  No other tasks can proceed. Focus on resolving this blocker.

Feature Progress: {N}/{TOTAL} tasks
⚠️  1 task blocked
━━━━━━━━ {XX}%
```

## Common Blocker Categories & Resolutions

### Missing Dependencies / Resources

```
Blocker: "Missing API credentials"

Resolution Steps:
  1. Contact DevOps/admin for credentials
  2. Update .env or configuration
  3. Test connection
  4. Run `/task-unblock T02 01-user-authentication`

Estimated Resolution: {minutes/hours/days}
```

### Technical Issues

```
Blocker: "Database migration failing"

Resolution Steps:
  1. Review error logs
  2. Check database connectivity
  3. Verify schema compatibility
  4. Fix migration script
  5. Test migration
  6. Run `/task-unblock T05 01-user-authentication`

Consider:
  - Consulting database expert
  - Reviewing similar migrations
  - Rollback if needed
```

### Blocked by External Factor

```
Blocker: "Waiting for design mockups"

Resolution Steps:
  1. Contact design team
  2. Clarify timeline
  3. Consider placeholder/wireframe approach
  4. Once received, run `/task-unblock T03 02-product-catalog`

Alternative:
  Work on backend tasks that don't need designs
```

## Integration with Task Manager

This command delegates to @task-manager agent:

```
@task-manager block {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG} "{reason}"
```

The task manager handles:

- Status validation (must be IN_PROGRESS)
- XML file update with blocker
- Manifest updates (task and root)
- Blocker tracking
- Timestamp recording

## Error Handling

- **Task not in progress**: "Cannot block {TASK_ID} - task is {status}. Only IN_PROGRESS tasks can be blocked."
- **Empty reason**: "Please provide blocker reason: /task-block T01 01-feature 'reason'"
- **Invalid task**: "Task {ID} not found in feature {FEATURE}"
- **Invalid feature**: "Feature {FEATURE} not found"

## Example Usage

```
User: /task-block T02 01-user-authentication "Database connection refused - need DB admin help"
```

Response: Task marked as BLOCKED, blocker recorded, resolution guidance provided, alternative tasks suggested.

## Related Commands

- `/task-unblock {task} {feature}` - Remove blocker and resume task
- `/task-status {feature}` - See all blocked tasks
- `/task-next {feature}` - Find alternative unblocked tasks
