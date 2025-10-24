---
name: validate-task-transition
description: Validates task status transitions before tool execution
type: PreToolUse
enabled: true
---

# Task Status Transition Validation Hook

## Purpose

Prevent invalid task status transitions and ensure workflow integrity.

## Trigger

**Type**: PreToolUse (runs before tool execution)

**Triggers on**:

- Write tool calls to task XML files (`.tasks/*/T*.xml`)
- Write tool calls to task manifest files (`.tasks/*/manifest.json`)
- Bash commands that modify task files

## Validation Rules

### Valid Status Transitions

```
NOT_STARTED → IN_PROGRESS ✓
IN_PROGRESS → COMPLETED ✓
IN_PROGRESS → BLOCKED ✓
BLOCKED → IN_PROGRESS ✓

INVALID:
NOT_STARTED → COMPLETED ✗ (must go through IN_PROGRESS)
COMPLETED → any ✗ (completed is final)
NOT_STARTED → BLOCKED ✗ (must be started first)
BLOCKED → COMPLETED ✗ (must unblock first)
```

### Dependency Validation

Before transitioning NOT_STARTED → IN_PROGRESS:

- All dependencies must have status = COMPLETED
- If dependencies not met: BLOCK the tool call

### Manifest Consistency

When updating task status:

- Task manifest must reflect same status as XML
- Root manifest counts must be accurate
- nextTask must be valid (exists and dependencies met)

## Implementation

```javascript
function validateTaskTransition(toolCall) {
  // Extract task file path
  const taskFilePath = toolCall.parameters.file_path;

  // Check if this is a task file modification
  if (
    !taskFilePath.match(
      /\.tasks\/[0-9]{2}-[a-z0-9-]+\/T[0-9]{2}-[a-z0-9-]+\.xml$/,
    )
  ) {
    return { allowed: true }; // Not a task file, allow
  }

  // Read current task status from XML
  const currentXml = readFile(taskFilePath);
  const currentStatus = extractStatus(currentXml);

  // Parse new content to check new status
  const newContent =
    toolCall.parameters.content || toolCall.parameters.new_string;
  const newStatus = extractStatus(newContent);

  // Validate transition
  if (currentStatus === newStatus) {
    return { allowed: true }; // No status change
  }

  // Check valid transitions
  const validTransitions = {
    NOT_STARTED: ["IN_PROGRESS"],
    IN_PROGRESS: ["COMPLETED", "BLOCKED"],
    BLOCKED: ["IN_PROGRESS"],
    COMPLETED: [], // Cannot transition from COMPLETED
  };

  if (!validTransitions[currentStatus].includes(newStatus)) {
    return {
      allowed: false,
      reason: `Invalid status transition: ${currentStatus} → ${newStatus}`,
      suggestion: `Valid transitions from ${currentStatus}: ${validTransitions[currentStatus].join(", ")}`,
    };
  }

  // Special validation for NOT_STARTED → IN_PROGRESS
  if (currentStatus === "NOT_STARTED" && newStatus === "IN_PROGRESS") {
    const dependencies = extractDependencies(currentXml);
    const unmetDeps = checkDependencies(dependencies, taskFilePath);

    if (unmetDeps.length > 0) {
      return {
        allowed: false,
        reason: `Cannot start task - dependencies not met`,
        blockers: unmetDeps.map(
          (dep) => `${dep.id} - ${dep.title} (status: ${dep.status})`,
        ),
        suggestion: `Complete dependencies first: ${unmetDeps.map((d) => d.id).join(", ")}`,
      };
    }
  }

  return { allowed: true };
}

function extractStatus(xmlContent) {
  const match = xmlContent.match(/status="([A-Z_]+)"/);
  return match ? match[1] : null;
}

function extractDependencies(xmlContent) {
  const depMatches = xmlContent.matchAll(/<dependency task_id="(T[0-9]{2})"/g);
  return Array.from(depMatches).map((m) => m[1]);
}

function checkDependencies(depIds, currentTaskPath) {
  const featureDir = path.dirname(currentTaskPath);
  const unmet = [];

  for (const depId of depIds) {
    const depFiles = glob.sync(`${featureDir}/${depId}-*.xml`);
    if (depFiles.length > 0) {
      const depXml = readFile(depFiles[0]);
      const depStatus = extractStatus(depXml);

      if (depStatus !== "COMPLETED") {
        const depTitle = extractTitle(depXml);
        unmet.push({ id: depId, title: depTitle, status: depStatus });
      }
    }
  }

  return unmet;
}

function extractTitle(xmlContent) {
  const match = xmlContent.match(/<title>([^<]+)<\/title>/);
  return match ? match[1] : "Unknown";
}
```

## Hook Output

### Success (Transition Allowed)

```
✓ Task transition validated: NOT_STARTED → IN_PROGRESS
  Task: T01 - Database Schema Design
  All dependencies met
```

### Failure (Invalid Transition)

```
✗ Task transition blocked

Attempted: COMPLETED → IN_PROGRESS
Reason: Cannot transition from COMPLETED state

Completed tasks are immutable. If re-work needed:
  1. Create new task for changes
  2. Reference original task in description
```

### Failure (Dependencies Not Met)

```
✗ Cannot start task - dependencies not met

Task: T03 - API Endpoints
Dependencies:
  ⏳ T01 - Database Schema (IN_PROGRESS)
  ⏸️  T02 - Data Models (NOT_STARTED)

Action Required:
  1. Complete T01 first
  2. Complete T02
  3. Then start T03

Alternative: Work on independent task
  Use `/task-next feature-slug` to find available tasks
```

## Configuration

Enable/disable hook:

```yaml
hooks:
  validate-task-transition:
    enabled: true
    strict_mode: true # Block invalid transitions (vs warn only)
    check_dependencies: true
```

## Bypass (Emergency)

In rare cases where manual override needed:

```bash
# Temporarily disable hook
export SKIP_TASK_VALIDATION=true

# Make necessary changes
# ...

# Re-enable
unset SKIP_TASK_VALIDATION
```

**⚠️ Warning**: Bypassing validation can cause manifest inconsistencies. Use with caution and manually verify consistency afterward.

## Related Hooks

- `validate-manifest-consistency` - Ensures manifest synchronization
- `audit-task-changes` - Logs all task status changes for audit trail
