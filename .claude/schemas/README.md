# Task Management Schemas & Templates

This directory contains XML/JSON schemas and Markdown templates for Claude Code's task management system.

## 📁 Files

### Schemas

- **`task-schema.xsd`** - XML Schema Definition for task files
  - Validates task structure, dependencies, acceptance criteria
  - Enforces naming conventions (TaskID format: `T[0-9]{2}`)
  - Status values: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`

- **`root-manifest-schema.json`** - JSON Schema for feature-level manifest
  - Location: `.tasks/manifest.json`
  - Tracks all features in project with status and progress metrics
  - Feature status: `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, `BLOCKED`, `CANCELLED`

- **`task-manifest-schema.json`** - JSON Schema for task-level manifest
  - Location: `.tasks/{NN}-{slug}/manifest.json`
  - Tracks all tasks within a feature
  - Provides next-task navigation

### Templates

- **`TEMPLATE-feature-brief.md`** - Feature context and goals template
  - Purpose, problem statement, user scenarios
  - MVP definition, constraints, success metrics
  - Created by `requirements-analyst` agent

- **`TEMPLATE-task-output.md`** - Task execution output template
  - Work performed, test results, challenges encountered
  - Used by execution agents to document completed work

### Examples

- **`EXAMPLE-task-file.xml`** - Complete example of a task definition
  - Shows all required and optional elements
  - Demonstrates proper formatting and best practices

## 🔧 Usage

### Validating XML Task Files

```bash
# Using xmllint (requires libxml2)
xmllint --schema .claude/schemas/task-schema.xsd .tasks/01-feature/T01-task.xml
```

### Validating JSON Manifests

```bash
# Using ajv-cli (requires Node.js)
npm install -g ajv-cli
ajv validate -s .claude/schemas/root-manifest-schema.json -d .tasks/manifest.json
ajv validate -s .claude/schemas/task-manifest-schema.json -d .tasks/01-feature/manifest.json
```

## 📐 Naming Conventions

### Feature IDs

- Format: Two-digit zero-padded number (`01`, `02`, ..., `99`)
- Example: `01-user-authentication`

### Feature Slugs

- Format: lowercase letters, numbers, hyphens only
- Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Examples: `user-authentication`, `api-rate-limiting`, `email-notifications`

### Task IDs

- Format: `T` + two-digit zero-padded number
- Pattern: `^T[0-9]{2}$`
- Examples: `T01`, `T02`, `T15`

### Task Slugs

- Same as feature slugs (lowercase, hyphen-separated)
- Examples: `database-schema`, `api-endpoints`, `unit-tests`

## 🗂️ Directory Structure

```
.tasks/
├── schemas/                          # This directory
│   ├── task-schema.xsd
│   ├── root-manifest-schema.json
│   ├── task-manifest-schema.json
│   ├── TEMPLATE-feature-brief.md
│   ├── TEMPLATE-task-output.md
│   ├── EXAMPLE-task-file.xml
│   └── README.md (this file)
├── manifest.json                     # Root feature tracking
└── 01-user-authentication/           # Example feature directory
    ├── feature-brief.md              # Context and goals
    ├── requirements-user-authentication.md
    ├── tech-analysis-user-authentication.md
    ├── manifest.json                 # Task tracking for this feature
    ├── T01-database-schema.xml       # Task definition
    ├── T01-output.md                 # Task execution results
    ├── T02-api-endpoints.xml
    └── T02-output.md
```

## 🤖 Agent Responsibilities

### Requirements Analyst (`requirements-analyst`)

Creates:

- `feature-brief.md`
- `requirements-{slug}.md`
- Initial entry in root `manifest.json`

### Tech Researcher (`tech-researcher`)

Creates:

- `tech-analysis-{slug}.md`

### Implementation Planner (`implementation-planner`)

Creates:

- Task-level `manifest.json`
- `TNN-{slug}.xml` files for each task
- Updates root manifest status: NOT_STARTED → IN_PROGRESS

### Task Manager (`task-manager`)

Creates:

- Task progression and status updates
- Updates both manifests as tasks complete

### Execution Agents

Creates:

- `TNN-output.md` files documenting work completed

## 🔒 Validation Rules

### Task Dependencies

- Must reference valid task IDs within same feature
- No circular dependencies allowed
- All dependencies must exist before task can start

### Status Transitions

Valid transitions:

- `NOT_STARTED` → `IN_PROGRESS`
- `IN_PROGRESS` → `COMPLETED`
- `IN_PROGRESS` → `BLOCKED`
- `BLOCKED` → `IN_PROGRESS`

Invalid transitions:

- `COMPLETED` → any other status (completed tasks are immutable)
- `NOT_STARTED` → `COMPLETED` (must go through IN_PROGRESS)

### Manifest Consistency

- Root manifest `taskCount` must match task manifest length
- Root manifest `completedCount` must match COMPLETED tasks in task manifest
- `nextTask` must be `null` only when all tasks completed

## 📚 References

- Main workflow documentation: `../Prompt-Engineering-for-Complete-SDLC-Workflow.md`
- Agent definitions: `../.claude/agents/`
- Command definitions: `../.claude/commands/`
