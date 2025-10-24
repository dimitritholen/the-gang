---
allowed-tools: Bash(code-tools:*), Glob, Grep, Read
description: Get the next task to work on
---

You are helping the user identify the next available task to work on.

**Task**: Display detailed information about the next available task for a feature.

## Input

User provides: `/task-next {feature-id}-{slug}`

## Actions

Use code tools and file system tools for efficient task discovery:

```bash
# Feature slug from arguments
FEATURE_SLUG="$ARGUMENTS"
FEATURE_DIR=".tasks/${FEATURE_SLUG}"

# Find next available task (validates dependencies automatically)
NEXT_TASK=$(code-tools find_next_task --manifest "${FEATURE_DIR}/manifest.json")

# Check if task available
HAS_NEXT=$(echo "$NEXT_TASK" | code-tools extract_json_field --field 'data.has_next')

if [ "$HAS_NEXT" = "false" ]; then
    # All tasks completed - show completion message
    MANIFEST_DATA=$(code-tools read_task_manifest --path "${FEATURE_DIR}/manifest.json")
    # Display completion format below
    exit 0
fi

# Get next task details
TASK_ID=$(echo "$NEXT_TASK" | code-tools extract_json_field --field 'data.task_id')
TASK_FILE=$(echo "$NEXT_TASK" | code-tools extract_json_field --field 'data.task_file')
```

**Alternative using file system tools**: Use Read tool to access task XML content and Grep tool to extract specific XML elements.

```bash
# Read task XML for full details
# Use Read tool with TASK_FILE path

# Extract task details using Grep tool with XML patterns
# TITLE: pattern '<title>([^<]+)</title>'
# PRIORITY: pattern '<priority>([^<]+)</priority>'
# COMPLEXITY: pattern '<complexity>([^<]+)</complexity>'
# ESTIMATE: pattern '<estimate hours="([^"]+)"'

# Get feature metadata
# Use code-tools or Read tool to access manifest.json
# FEATURE_DATA: extract from manifest using code-tools extract_json_field
# FEATURE_NAME: extract 'data.manifest.feature.name'
```

## Output Format

```
Next Task: {TASK_ID} - {TASK_TITLE}

Feature: {FEATURE_ID}-{FEATURE_SLUG} ({Feature Title})
Status: NOT_STARTED
Priority: {HIGH|MEDIUM|LOW}
Complexity: {LOW|MEDIUM|HIGH}
Estimated: {N} hours (confidence: {HIGH|MEDIUM|LOW})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Description

{Full task description from XML}

## Dependencies

{If no dependencies:}
Ready - no dependencies

{If dependencies exist:}
[x] {DEP1_ID} - {DEP1_TITLE} (completed {DATE})
[x] {DEP2_ID} - {DEP2_TITLE} (completed {DATE})

## Acceptance Criteria

{List all testable criteria}
- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Completion Checklist

- [ ] {Checklist item 1}
- [ ] {Checklist item 2}
- [ ] {Checklist item 3}

## Technical Notes

{Implementation guidance, patterns, gotchas from XML}

## Risks & Mitigations

WARNING - {SEVERITY}: {Risk description}
   Mitigation: {How to mitigate}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to start?
  Run: `/task-start {TASK_ID} {FEATURE_ID}-{FEATURE_SLUG}`

Task file: .tasks/{NN}-{slug}/{TASK_ID}-{slug}.xml
Output will be saved to: .tasks/{NN}-{slug}/{TASK_ID}-output.md
```

## Alternative: All Tasks Completed

If nextTask is null:

```
All Tasks Completed

Feature: {FEATURE_ID}-{FEATURE_SLUG}
Status: COMPLETED
Total tasks: {N}
Completed: {DATE}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Completed Tasks:
[x] {TASK_ID} - {TASK_TITLE} (completed {DATE})
[x] {TASK_ID} - {TASK_TITLE} (completed {DATE})
[x] {TASK_ID} - {TASK_TITLE} (completed {DATE})
...

Feature deliverables:
  - .tasks/{NN}-{slug}/requirements-{slug}.md
  - .tasks/{NN}-{slug}/tech-analysis-{slug}.md
  - {N} task outputs (TNN-output.md)

Next steps:
  - Review feature deliverables
  - Run quality assurance checks
  - Consider deployment or next feature
```

## Alternative: Dependencies Not Met

If nextTask has unmet dependencies:

```
Next Task Blocked

Task: {TASK_ID} - {TASK_TITLE}
Status: NOT_STARTED
Dependencies: NOT MET

Blocked By:
  PENDING {DEP1_ID} - {DEP1_TITLE} (status: IN_PROGRESS)
  PENDING {DEP2_ID} - {DEP2_TITLE} (status: NOT_STARTED)

This task cannot start until the dependencies above are completed.

Alternative tasks available:
  {If alternative tasks with met dependencies exist:}
  -> {ALT_TASK_ID} - {ALT_TASK_TITLE}
    Run: `/task-next {ALT_TASK_ID}`

  {If no alternatives:}
  No alternative tasks available. Focus on completing blockers.
```

## Error Handling

- **No .tasks/ directory**: "No tasks found. Run /gather-requirements to start."
- **Invalid feature**: "Feature not found. Use /task-status to see available features."
- **No tasks created**: "No tasks yet. Run /plan-implementation {feature-id}-{slug}"
- **Empty manifest**: "Task manifest empty or corrupted. Check .tasks/{NN}-{slug}/manifest.json"

## Example Usage

```
User: /task-next 01-user-authentication
```

Response: Full details of T01 (or current nextTask) with description, acceptance criteria, checklist, ready to execute.
