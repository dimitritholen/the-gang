---
allowed-tools: Read, Glob, Edit
description: Validate task and root manifest consistency
---

You are helping the user validate manifest consistency across the task management system with systematic verification.

**Task**: Check all manifests for consistency issues and optionally auto-fix.

## Input

User provides: `/validate-manifests [feature-id-slug] [--fix]`

Examples:

- `/validate-manifests` - Validate all features
- `/validate-manifests 01-user-authentication` - Validate specific feature
- `/validate-manifests --fix` - Validate and auto-fix issues

## Systematic Validation Process

Apply step-by-step reasoning with verification at each stage:

### Phase 1: Scope Analysis

**Step 1.1: Parse and validate arguments**

- Extract feature filter if provided
- Identify auto-fix flag
- Confirm arguments are well-formed

**Step 1.2: Determine validation scope**

- If feature specified: verify feature directory exists
- If no feature: enumerate all features from root manifest
- Build list of feature directories to validate

**Verification checkpoint:**

- Does each target directory exist?
- Are we validating what the user intended?
- Document scope: "Validating N features: [list]"

### Phase 2: Individual Feature Validation

For each feature, apply systematic checks with intermediate reasoning:

**Step 2.1: Task count consistency check**

- Count actual task files in feature directory
- Read taskCount from root manifest
- Compare: `actual_files === manifest.taskCount`
- If mismatch: record discrepancy with both values

**Step 2.2: Completed count verification**

- Parse all task files
- Count tasks with status === "COMPLETED"
- Read completedCount from root manifest
- Compare: `actual_completed === manifest.completedCount`
- If mismatch: record discrepancy

**Step 2.3: Feature status derivation**

- Analyze task status distribution
- Apply status logic:
  - NOT_STARTED: ALL tasks are NOT_STARTED
  - IN_PROGRESS: At least one task started, not all complete
  - COMPLETED: ALL tasks are COMPLETED
  - BLOCKED: At least one task is BLOCKED
- Compare derived status with manifest.status
- If mismatch: record expected vs found

**Step 2.4: Next task validation**

- Identify manifest.nextTask value
- If nextTask is not null:
  - Verify task exists
  - Verify task status is NOT_STARTED
  - Verify all dependencies are COMPLETED
- If nextTask is null:
  - Verify all tasks are COMPLETED
- Record any violations

**Step 2.5: Blocker synchronization check**

- Extract all BLOCKED tasks from task files
- Read blockers array from feature manifest
- Verify each BLOCKED task has blocker entry
- Verify no phantom blockers (blocker without BLOCKED task)
- Record any mismatches

**Verification questions for this feature:**

1. Are all counts mathematically consistent with task files?
2. Does the derived status match the transition rules?
3. Is nextTask pointing to a valid, unblocked task?
4. Are blockers synchronized bidirectionally?

### Phase 3: Cross-Feature Verification

After individual checks, verify consistency across features:

**Step 3.1: Global consistency check**

- Sum all taskCount values - does it match total task files?
- Are there any orphaned task files not referenced by any feature?
- Are feature IDs unique and properly formatted?

**Step 3.2: Dependency validation**

- Check for cross-feature dependencies
- Verify referenced features exist
- Confirm no circular dependencies

### Phase 4: Issue Reporting

**Step 4.1: Categorize issues by severity**

- Critical: Data loss risk (missing tasks, incorrect counts)
- High: Incorrect workflow state (wrong status, invalid nextTask)
- Medium: Synchronization issues (blocker mismatches)
- Low: Formatting or minor inconsistencies

**Step 4.2: Verification of issues found**

Before reporting, verify each issue:

- Is this a genuine inconsistency or expected behavior?
- Could this be caused by in-progress operations?
- Is the fix deterministic and safe?

### Phase 5: Auto-Fix (if --fix flag)

**Step 5.1: Generate fix plan**

For each issue, determine fix action:

- Task count: Update manifest.taskCount to match actual files
- Completed count: Recalculate from task statuses
- Feature status: Derive correct status from task distribution
- Next task: Calculate first eligible task or null
- Blockers: Sync with BLOCKED tasks

**Step 5.2: Verify fix safety**

Before applying, check:

- Will this fix preserve data integrity?
- Are we potentially overwriting valid manual edits?
- Is there risk of concurrent modification?

**Step 5.3: Apply fixes atomically**

- Backup current manifest state
- Apply all fixes for a feature
- Verify JSON is valid after modification
- Commit changes

**Step 5.4: Post-fix verification**

- Re-run validation on fixed features
- Confirm all issues resolved
- Report any issues that persist

## Implementation

Use code tools for validation with verification built in:

**Step 1: Parse arguments**

- Extract feature filter if provided
- Identify auto-fix flag
- Store in variables for later use

**Step 2: Read root manifest**

- Use Read tool to load `.tasks/manifest.json`
- Parse JSON to extract features array
- If feature filter provided, select matching feature
- If no filter, use all features

**Step 3: Enumerate feature directories**

- Use Glob tool with pattern `.tasks/*/manifest.json`
- Cross-reference with root manifest features
- Build list of feature directories to validate

**Step 4: Validate each feature**

- For each feature directory:
  - Use Glob tool with pattern `.tasks/{feature}/T*.json` to count task files
  - Use Read tool to load each task file
  - Parse task statuses, count completed tasks
  - Use Read tool to load feature manifest
  - Compare actual vs manifest values for:
    - taskCount
    - completedCount
    - status (derive from task distribution)
    - nextTask validity
    - blocker synchronization

**Step 5: Report issues**

- Categorize by severity
- Format with clear expected vs found values
- If --fix flag set, proceed to fix phase

**Step 6: Auto-fix (if requested)**

- For each issue:
  - Calculate correct value
  - Use Edit tool to update manifest JSON
  - Verify JSON validity after edit
- Re-validate after all fixes applied

**Example validation flow:**

```
1. Glob: ".tasks/*/manifest.json" → [".tasks/01-auth/manifest.json", ...]
2. Read: ".tasks/manifest.json" → parse features array
3. Read: ".tasks/01-auth/manifest.json" → extract taskCount, status, etc.
4. Glob: ".tasks/01-auth/T*.json" → count actual task files
5. Read: each task file → parse status field
6. Compare: actual_count vs manifest.taskCount
7. If mismatch: record issue
8. If --fix: Edit ".tasks/manifest.json" with corrected values
```

## Validation Checks

These checks are performed for each feature:

### 1. Task Count Consistency

```
Root manifest feature.taskCount === Task manifest tasks.length
```

### 2. Completed Count Consistency

```
Root manifest feature.completedCount === Count of COMPLETED tasks
```

### 3. Feature Status Accuracy

```
NOT_STARTED: All tasks NOT_STARTED
IN_PROGRESS: At least one task started, not all complete
COMPLETED: All tasks COMPLETED
BLOCKED: At least one task BLOCKED
```

### 4. Next Task Validity

```
- Points to existing task
- Task status is NOT_STARTED
- All dependencies COMPLETED
- OR null if all tasks complete
```

### 5. Blocker Synchronization

```
- Each BLOCKED task has entry in feature blockers
- No phantom blockers
```

## Output Format

### All Valid

```
✓ Manifest Validation Complete

Features Validated: {N}
Tasks Validated: {TOTAL_TASKS}
Issues Found: 0

All manifests are synchronized and consistent.
```

### Issues Found (No Auto-Fix)

```
✗ Manifest Validation Issues Found

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: 01-user-authentication

✗ Task count mismatch
  Expected: 8 (actual task files)
  Found: 7 (root manifest)
  Location: .tasks/manifest.json

✗ Feature status incorrect
  Expected: IN_PROGRESS
  Found: NOT_STARTED
  Reason: 3 tasks are COMPLETED, 2 are IN_PROGRESS

✓ Completed count: 3 ✓
✓ Next task valid: T06 ✓
✓ Blockers synchronized ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: 02-product-catalog

✓ All checks passed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary:
  Features: 2 total, 1 with issues
  Tasks: 15 total
  Issues: 2 found

Manual Fixes Required:
  1. Edit .tasks/manifest.json
  2. Update feature 01:
     - taskCount: 7 → 8
     - status: "NOT_STARTED" → "IN_PROGRESS"

Or run: /validate-manifests --fix
```

### Auto-Fix Applied

```
✓ Manifest Validation & Auto-Fix Complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: 01-user-authentication

Fixes Applied:
  ✓ Updated taskCount: 7 → 8
  ✓ Updated status: NOT_STARTED → IN_PROGRESS
  ✓ Updated completedCount: 2 → 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All manifests now synchronized.
Run validation again to confirm: /validate-manifests
```

## Related Commands

- `/task-status {feature}` - View feature progress
- `/task-next {feature}` - Get next task
- `@task-manager validate_manifest_consistency` - Direct agent call

## Notes

This command provides manual validation on demand. The `validate-manifest-consistency` hook runs automatically after manifest modifications.

Use this command:

- After manual manifest edits
- Before committing changes
- When debugging workflow issues
- As part of CI/CD validation
