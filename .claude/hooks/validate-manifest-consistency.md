---
name: validate-manifest-consistency
description: Ensures task and root manifests stay synchronized
type: PostToolUse
enabled: true
---

# Manifest Consistency Validation Hook

## Purpose

Verify that task-level and root-level manifests remain synchronized after modifications.

## Trigger

**Type**: PostToolUse (runs after tool execution)

**Triggers on**:

- Write tool calls to manifest files (`.tasks/manifest.json` or `.tasks/*/manifest.json`)
- Bash commands that modify manifests
- Task status changes that affect manifests

## Validation Checks

### 1. Task Count Consistency

```
Root manifest feature.taskCount === Task manifest tasks.length
```

### 2. Completed Count Consistency

```
Root manifest feature.completedCount ===
  Count of tasks with status="COMPLETED" in task manifest
```

### 3. Feature Status Accuracy

```
Feature status in root manifest matches task reality:

NOT_STARTED:
  - All tasks in task manifest have status NOT_STARTED

IN_PROGRESS:
  - At least one task is IN_PROGRESS or COMPLETED
  - Not all tasks are COMPLETED

COMPLETED:
  - All tasks have status COMPLETED

BLOCKED:
  - At least one task has status BLOCKED
  - No tasks IN_PROGRESS (only if all active tasks blocked)
```

### 4. Next Task Validity

```
Task manifest nextTask field:
  - Points to existing task ID
  - That task has status NOT_STARTED
  - All dependencies of that task are COMPLETED
  - OR is null if all tasks completed
```

### 5. Blocker Synchronization

```
Root manifest feature.blockers matches blocked tasks:
  - Each BLOCKED task in task manifest has entry in feature blockers
  - No phantom blockers (blocker exists but no blocked tasks)
```

## Implementation

```javascript
function validateManifestConsistency(toolCall, result) {
  // Check if manifest was modified
  const filePath = toolCall.parameters.file_path;

  let isRootManifest = filePath === ".tasks/manifest.json";
  let isTaskManifest = filePath.match(
    /\.tasks\/[0-9]{2}-[a-z0-9-]+\/manifest\.json$/,
  );

  if (!isRootManifest && !isTaskManifest) {
    return { valid: true }; // Not a manifest file
  }

  // Read both manifests
  const rootManifest = readJSON(".tasks/manifest.json");

  // Get all features to validate
  const featuresToValidate = isRootManifest
    ? rootManifest.features
    : [extractFeatureFromPath(filePath)];

  const errors = [];
  const warnings = [];

  for (const feature of featuresToValidate) {
    const featureDir = `.tasks/${feature.id}-${feature.slug}`;
    const taskManifestPath = `${featureDir}/manifest.json`;

    if (!fileExists(taskManifestPath)) {
      warnings.push(`Task manifest missing for feature ${feature.id}`);
      continue;
    }

    const taskManifest = readJSON(taskManifestPath);

    // Check 1: Task count
    if (feature.taskCount !== taskManifest.tasks.length) {
      errors.push({
        feature: feature.id,
        check: "taskCount",
        expected: taskManifest.tasks.length,
        actual: feature.taskCount,
        fix: `Update root manifest: feature ${feature.id} taskCount to ${taskManifest.tasks.length}`,
      });
    }

    // Check 2: Completed count
    const actualCompleted = taskManifest.tasks.filter(
      (t) => t.status === "COMPLETED",
    ).length;
    if (feature.completedCount !== actualCompleted) {
      errors.push({
        feature: feature.id,
        check: "completedCount",
        expected: actualCompleted,
        actual: feature.completedCount,
        fix: `Update root manifest: feature ${feature.id} completedCount to ${actualCompleted}`,
      });
    }

    // Check 3: Feature status
    const statusIssue = validateFeatureStatus(feature, taskManifest.tasks);
    if (statusIssue) {
      errors.push(statusIssue);
    }

    // Check 4: Next task validity
    const nextTaskIssue = validateNextTask(taskManifest, featureDir);
    if (nextTaskIssue) {
      errors.push(nextTaskIssue);
    }

    // Check 5: Blockers
    const blockerIssues = validateBlockers(feature, taskManifest.tasks);
    errors.push(...blockerIssues);
  }

  if (errors.length > 0) {
    return {
      valid: false,
      errors: errors,
      warnings: warnings,
      autoFixAvailable: true,
    };
  }

  if (warnings.length > 0) {
    return {
      valid: true,
      warnings: warnings,
    };
  }

  return { valid: true };
}

function validateFeatureStatus(feature, tasks) {
  const allCompleted = tasks.every((t) => t.status === "COMPLETED");
  const anyInProgress = tasks.some(
    (t) => t.status === "IN_PROGRESS" || t.status === "COMPLETED",
  );
  const anyBlocked = tasks.some((t) => t.status === "BLOCKED");
  const allNotStarted = tasks.every((t) => t.status === "NOT_STARTED");

  let expectedStatus;
  if (allCompleted) {
    expectedStatus = "COMPLETED";
  } else if (allNotStarted) {
    expectedStatus = "NOT_STARTED";
  } else if (anyBlocked && !anyInProgress) {
    expectedStatus = "BLOCKED";
  } else {
    expectedStatus = "IN_PROGRESS";
  }

  if (feature.status !== expectedStatus) {
    return {
      feature: feature.id,
      check: "featureStatus",
      expected: expectedStatus,
      actual: feature.status,
      fix: `Update root manifest: feature ${feature.id} status to ${expectedStatus}`,
    };
  }

  return null;
}

function validateNextTask(taskManifest, featureDir) {
  const nextTaskId = taskManifest.nextTask;

  // If null, all tasks should be complete
  if (nextTaskId === null) {
    const incomplete = taskManifest.tasks.find((t) => t.status !== "COMPLETED");
    if (incomplete) {
      return {
        feature: taskManifest.featureId,
        check: "nextTask",
        issue: `nextTask is null but ${incomplete.id} is ${incomplete.status}`,
        fix: `Update task manifest: set nextTask to ${incomplete.id}`,
      };
    }
    return null; // Valid
  }

  // Next task must exist
  const nextTask = taskManifest.tasks.find((t) => t.id === nextTaskId);
  if (!nextTask) {
    return {
      feature: taskManifest.featureId,
      check: "nextTask",
      issue: `nextTask ${nextTaskId} does not exist`,
      fix: `Update task manifest: find valid next task or set to null`,
    };
  }

  // Next task must be NOT_STARTED
  if (nextTask.status !== "NOT_STARTED") {
    return {
      feature: taskManifest.featureId,
      check: "nextTask",
      issue: `nextTask ${nextTaskId} has status ${nextTask.status}, not NOT_STARTED`,
      fix: `Update task manifest: find next NOT_STARTED task with met dependencies`,
    };
  }

  // Dependencies must be met
  for (const depId of nextTask.dependencies || []) {
    const depTask = taskManifest.tasks.find((t) => t.id === depId);
    if (!depTask || depTask.status !== "COMPLETED") {
      return {
        feature: taskManifest.featureId,
        check: "nextTask",
        issue: `nextTask ${nextTaskId} depends on ${depId} which is not COMPLETED`,
        fix: `Update task manifest: choose task with satisfied dependencies`,
      };
    }
  }

  return null; // Valid
}

function validateBlockers(feature, tasks) {
  const errors = [];
  const blockedTasks = tasks.filter((t) => t.status === "BLOCKED");

  // Check root manifest has blocker entry for each blocked task
  if (
    blockedTasks.length > 0 &&
    (!feature.blockers || feature.blockers.length === 0)
  ) {
    errors.push({
      feature: feature.id,
      check: "blockers",
      issue: `${blockedTasks.length} blocked tasks but no blockers in root manifest`,
      fix: `Add blocker entries to root manifest for: ${blockedTasks.map((t) => t.id).join(", ")}`,
    });
  }

  // Check no phantom blockers
  if (
    blockedTasks.length === 0 &&
    feature.blockers &&
    feature.blockers.length > 0
  ) {
    errors.push({
      feature: feature.id,
      check: "blockers",
      issue: `Root manifest has blockers but no tasks are BLOCKED`,
      fix: `Remove blocker entries from root manifest`,
    });
  }

  return errors;
}
```

## Hook Output

### Success

```
✓ Manifest consistency validated
  Feature: 01-user-authentication
  - Task count: 8 ✓
  - Completed count: 5 ✓
  - Feature status: IN_PROGRESS ✓
  - Next task: T06 ✓
  - Blockers: 0 ✓
```

### Failure with Auto-Fix

```
✗ Manifest inconsistency detected

Feature: 01-user-authentication
  ✗ Task count mismatch: expected 8, found 7 in root manifest
  ✗ Feature status: should be IN_PROGRESS, currently NOT_STARTED

Auto-fix available. Apply fixes? (y/n)

{If yes:}
  Applying fixes...
  ✓ Updated root manifest taskCount: 7 → 8
  ✓ Updated root manifest status: NOT_STARTED → IN_PROGRESS
  ✓ Manifests synchronized

{If no:}
  Manual fix required:
  1. Edit .tasks/manifest.json
  2. Update feature 01:
     - taskCount: 8
     - status: "IN_PROGRESS"
  3. Run validation again
```

### Warning (Non-Critical)

```
⚠️  Manifest warnings

Feature: 02-product-catalog
  ⚠️  Task manifest missing (no tasks created yet)
  ℹ️  Run /plan-implementation to create tasks

Consistency checks passed for other features.
```

## Auto-Fix Capability

Hook can automatically correct common inconsistencies:

```javascript
function autoFixManifest(errors) {
  const fixes = [];

  for (const error of errors) {
    switch (error.check) {
      case "taskCount":
      case "completedCount":
      case "featureStatus":
        applyRootManifestFix(error);
        fixes.push(`Fixed ${error.check} for feature ${error.feature}`);
        break;

      case "nextTask":
        applyTaskManifestFix(error);
        fixes.push(`Fixed nextTask for feature ${error.feature}`);
        break;

      case "blockers":
        applyBlockerSync(error);
        fixes.push(`Synchronized blockers for feature ${error.feature}`);
        break;
    }
  }

  return fixes;
}
```

## Configuration

```yaml
hooks:
  validate-manifest-consistency:
    enabled: true
    auto_fix: true # Automatically fix inconsistencies
    strict_mode: false # Warn vs block on inconsistency
    check_interval: "after_every_change" # or "on_demand"
```

## Manual Validation

Run validation on demand:

```bash
# Validate all manifests
/validate-manifests

# Validate specific feature
/validate-manifests 01-user-authentication

# Validate and auto-fix
/validate-manifests --fix
```

## Related Hooks

- `validate-task-transition` - Pre-validates status changes
- `audit-manifest-changes` - Logs all manifest modifications for audit trail
