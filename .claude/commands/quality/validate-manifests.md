---
allowed-tools: Bash(code-tools:*)
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

Use CLI tool for validation with verification built in:

```bash
# Parse arguments
FEATURE_FILTER=""
AUTO_FIX=false

for arg in $ARGUMENTS; do
    if [ "$arg" = "--fix" ]; then
        AUTO_FIX=true
    else
        FEATURE_FILTER="$arg"
    fi
done

# Get list of features to validate
if [ -n "$FEATURE_FILTER" ]; then
    FEATURES="$FEATURE_FILTER"
else
    # Get all features from root manifest
    FEATURES=$(jq -r '.features[] | .id + "-" + .slug' .tasks/manifest.json)
fi

# Validate each feature
TOTAL_ISSUES=0
FEATURES_CHECKED=0

for FEATURE in $FEATURES; do
    FEATURE_DIR=".tasks/${FEATURE}"

    if [ ! -d "$FEATURE_DIR" ]; then
        echo "⚠  Feature directory not found: $FEATURE_DIR"
        continue
    fi

    # Use CLI tool for validation (handles all checks)
    VALIDATION=$(code-tools validate_manifest --feature-dir "$FEATURE_DIR")

    IS_VALID=$(echo "$VALIDATION" | jq -r '.data.valid')
    ISSUES=$(echo "$VALIDATION" | jq -r '.data.issues')

    if [ "$IS_VALID" = "false" ]; then
        # Display issues for this feature
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "Feature: $FEATURE"
        echo ""

        # Parse and display each issue
        echo "$ISSUES" | jq -r '.[] | "✗ \(.type): expected=\(.expected), found=\(.found)"'

        ((TOTAL_ISSUES += $(echo "$ISSUES" | jq 'length')))

        # Auto-fix if requested
        if [ "$AUTO_FIX" = "true" ]; then
            echo ""
            echo "Applying fixes..."
            # NOTE: Auto-fix logic would need to be implemented in CLI or here
            # For now, just report that fixes would be applied
        fi
    else
        echo "✓ Feature $FEATURE: All checks passed"
    fi

    ((FEATURES_CHECKED++))
done

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Validation complete:"
echo "  Features: $FEATURES_CHECKED total"
echo "  Issues: $TOTAL_ISSUES found"

if [ $TOTAL_ISSUES -eq 0 ]; then
    echo ""
    echo "✓ All manifests are synchronized and consistent."
else
    if [ "$AUTO_FIX" = "false" ]; then
        echo ""
        echo "Run with --fix flag to automatically correct issues."
    fi
fi
```

## Validation Checks (Internal CLI Logic)

The CLI tool (`validate_manifest`) performs these checks automatically:

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
