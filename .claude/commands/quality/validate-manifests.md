---
allowed-tools: Bash(code-tools:*)
description: Validate task and root manifest consistency
---

You are helping the user validate manifest consistency across the task management system.

**Task**: Check all manifests for consistency issues and optionally auto-fix.

## Input

User provides: `/validate-manifests [feature-id-slug] [--fix]`

Examples:
- `/validate-manifests` - Validate all features
- `/validate-manifests 01-user-authentication` - Validate specific feature
- `/validate-manifests --fix` - Validate and auto-fix issues

## Actions

Use CLI tool for validation (handles all checks internally):

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
        echo "⚠️  Feature directory not found: $FEATURE_DIR"
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

## Validation Checks

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
