# Claude Code Workflow System

Modular task management and SDLC workflow orchestration for Claude Code using specialized agents, slash commands, and code-tools CLI.

## Getting Started

### Prerequisites

- Python 3.12+
- `uv` for virtual environment management
- Claude Code CLI installed

### Quick Setup

1. **Install code-tools CLI**:

   ```bash
   cd tools
   uv venv
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate   # Windows
   pip install -e .[web]
   ```

2. **Verify installation**:

   ```bash
   code-tools --help
   ```

3. **Run sample workflow**:

   ```bash
   # Analyze a new feature (orchestrates full SDLC)
   /analyze-feature "User authentication with JWT"

   # Or use individual phases
   /gather-requirements "User authentication"
   /research-tech user-authentication
   /plan-implementation user-authentication
   ```

### Project Structure

```
.
├── .claude/                    # Claude Code configuration
│   ├── agents/                 # Specialized agent definitions
│   ├── commands/               # Slash command workflows
│   ├── hooks/                  # Validation hooks
│   ├── memory/                 # Knowledge artifacts (JSONL graphs)
│   └── schemas/                # XML/JSON schemas + templates
├── tools/                      # code-tools CLI source
│   └── code_tools/             # Python package
└── .tasks/                     # Feature/task execution (gitignored)
```

---

## Claude Code Workflow (`.claude/`)

### Agents (`/.claude/agents/`)

Specialized agents for SDLC phases:

| Agent                    | Purpose                                          | Tools Required                       |
| ------------------------ | ------------------------------------------------ | ------------------------------------ |
| `requirements-analyst`   | Elicit requirements through structured questions | Read, Write, Bash (code-tools)       |
| `tech-researcher`        | Research technology stack + document decisions   | Read, WebFetch, Grep, Glob, Bash     |
| `implementation-planner` | Create task manifests (XML) + breakdown          | Read, Write, Bash (code-tools)       |
| `scope-guardian`         | Validate scope creep + feature drift             | Read, Bash (code-tools)              |
| `senior-developer`       | Execute tasks with code-tools enforcement        | Read, Write, Edit, Bash (code-tools) |
| `qa-engineer`            | Test execution + validation                      | Read, Write, Bash, Grep, Glob        |
| `code-review-specialist` | Pre-merge code review                            | Read, Grep, Glob, Bash               |
| `task-manager`           | Task status updates + manifest sync              | Read, Write, Bash (code-tools)       |
| `memory-manager`         | Context management + artifact synthesis          | Read, Write, Grep, Bash              |

**Key Principle**: All agents **must** use `code-tools` CLI for file operations (no direct `cat`, `grep`, `ls`).

### Commands (`/.claude/commands/`)

Slash commands organized by category:

#### Workflow (`/workflow/`)

- `/analyze-feature` - Full SDLC orchestration (requirements → research → planning → validation)
- `/implement-feature` - Execute tasks from manifest

#### Requirements (`/requirements/`)

- `/gather-requirements` - Structured requirements elicitation

#### Research (`/research/`)

- `/research-tech` - Technology stack analysis
- `/mine-patterns` - Extract codebase patterns

#### Planning (`/planning/`)

- `/plan-implementation` - Generate task manifests (XML + JSON)

#### Quality (`/quality/`)

- `/validate-scope` - Scope creep detection
- `/validate-consistency` - Codebase conformance check
- `/validate-manifests` - Manifest integrity check
- `/review-code` - Pre-merge review

#### Tasks (`/tasks/`)

- `/task-start` - Begin task (validates dependencies)
- `/task-complete` - Mark complete + sync manifests
- `/task-status` - Check progress
- `/task-next` - Get next available task
- `/task-block` - Mark blocked
- `/task-unblock` - Resume blocked task

#### Memory (`/memory/`)

- `/generate-memory` - Build knowledge graph from codebase
- `/update-memory` - Incremental graph updates
- `/cleanup-memory` - Remove stale artifacts

### Hooks (`/.claude/hooks/`)

Validation hooks executed on events:

- `validate-task-transition.md` - Enforces valid status transitions (NOT_STARTED → IN_PROGRESS → COMPLETED)
- `validate-manifest-consistency.md` - Ensures task/root manifest alignment

### Memory System (`/.claude/memory/`)

JSONL-based knowledge graph for efficient context retrieval:

**Artifacts**:

- `requirements-{slug}.md` - Feature requirements
- `tech-analysis-{slug}.md` - Technology decisions
- `{slug}.jsonl` - Knowledge graph (entities + relationships)

**Supported Entity Types**:

- Feature, Requirement, TechDecision, Component, Task, Pattern, Convention

**Supported Relationships**:

- `requires`, `depends_on`, `implements`, `follows`, `justifies`, `blocks`, `derived_from`

**Token Efficiency**: Graph queries return 50-300 tokens vs 1200-3000 tokens for full markdown (80-95% reduction).

### Schemas (`/.claude/schemas/`)

Validation schemas + templates:

- `task-schema.xsd` - XML schema for task files
- `root-manifest-schema.json` - Feature-level manifest
- `task-manifest-schema.json` - Task-level manifest
- `TEMPLATE-feature-brief.md` - Feature context template
- `TEMPLATE-task-output.md` - Task execution output
- `EXAMPLE-task-file.xml` - Reference task definition

---

## code-tools CLI (`./tools/`)

Portable CLI providing 20+ subcommands for consistent file operations across agents.

### Installation

```bash
cd tools
pip install -e .[web]  # Local dev (editable)
# pip install .[web]   # User install
```

### Core Commands

#### File Operations

```bash
# List directory
code-tools list_dir --path . --depth 1

# Search files by glob
code-tools search_file --glob "src/**/*.py"

# Grep code
code-tools grep_code --pattern "def main" --paths "src,lib"

# Read file
code-tools read_file --path docs/README.md --start 1 --end 200

# Create file
code-tools create_file --file out.txt --content @content.txt

# Edit file
code-tools edit_file --file out.txt --patch @new.txt

# Search/replace
code-tools search_replace --file config.md --replacements @reps.json
```

#### Web Operations

```bash
# Fetch content
code-tools fetch_content --url https://example.com
```

#### Task Management (v1.1)

```bash
# Convert feature name to slug
code-tools slugify_feature --name "User Authentication" --feature-id 01

# Read task manifest with metrics
code-tools read_task_manifest --path .tasks/01-auth/manifest.json

# Update task status + sync manifests
code-tools update_task_status --task-id T01 --status IN_PROGRESS --feature-dir .tasks/01-auth

# Find next available task (validates dependencies)
code-tools find_next_task --manifest .tasks/01-auth/manifest.json

# Validate manifest consistency
code-tools validate_manifest --feature-dir .tasks/01-auth

# List memory artifacts
code-tools list_memory_artifacts --dir .claude/memory --feature user-auth
```

#### Knowledge Graph (v1.2)

```bash
# Sync markdown → JSONL graph (auto-invalidates on mtime change)
code-tools sync_memory_graph --dir .claude/memory --feature user-authentication

# Query graph with natural language
code-tools query_memory --dir .claude/memory --feature user-authentication \
  --query "security requirements" --mode direct --limit 10

# Modes:
#   - direct: Fast keyword-based graph query (default)
#   - nlp: LLM-powered query translation (placeholder)
#   - auto: Try direct, fallback to NLP if no results
```

### Output Format

All commands return JSON:

```json
{
  "ok": true,
  "tool": "read_file",
  "version": "1.2.0",
  "data": { ... }
}
```

or

```json
{
  "ok": false,
  "tool": "read_file",
  "version": "1.2.0",
  "error": "File not found"
}
```

### Token Savings

- Task commands: 30-40% reduction (consolidates 30-50 lines of bash)
- Graph queries: 80-95% reduction (50-300 tokens vs 1200-3000 for full markdown)

---

## Workflow Example: Feature Development

### 1. Analyze Feature

```bash
/analyze-feature "User authentication with JWT"
```

**Phases executed**:

1. Requirements gathering (`requirements-analyst` agent)
2. Tech research (`tech-researcher` agent)
3. Implementation planning (`implementation-planner` agent)
4. Scope validation (`scope-guardian` agent)

**Artifacts created**:

- `.claude/memory/requirements-user-authentication.md`
- `.claude/memory/tech-analysis-user-authentication.md`
- `.claude/memory/user-authentication.jsonl` (knowledge graph)
- `.tasks/01-user-authentication/manifest.json`
- `.tasks/01-user-authentication/T01-database-schema.xml`
- `.tasks/01-user-authentication/T02-api-endpoints.xml`
- etc.

### 2. Execute Tasks

```bash
# Get next task
/task-next user-authentication

# Start task T01
/task-start T01 user-authentication

# (Work completed by senior-developer agent)

# Complete task
/task-complete T01 user-authentication
```

### 3. Code Review

```bash
/review-code user-authentication
```

### 4. QA Validation

```bash
/run-qa-validation user-authentication
```

---

## Key Design Principles

1. **Agent Specialization**: Single-responsibility agents for each SDLC phase
2. **Code-Tools Enforcement**: All file operations via `code-tools` CLI (consistency + auditability)
3. **Schema Validation**: XML/JSON schemas for task definitions + manifests
4. **Knowledge Graph**: JSONL-based memory for 80-95% token reduction
5. **Hooks**: Automated validation on task transitions + manifest updates
6. **No Hallucinations**: Agents must use code-tools to inspect codebase (no guessing)

---

## Validation

### Validate XML Tasks

```bash
xmllint --schema .claude/schemas/task-schema.xsd .tasks/01-feature/T01-task.xml
```

### Validate JSON Manifests

```bash
npm install -g ajv-cli
ajv validate -s .claude/schemas/root-manifest-schema.json -d .tasks/manifest.json
ajv validate -s .claude/schemas/task-manifest-schema.json -d .tasks/01-feature/manifest.json
```

### Validate Manifest Consistency

```bash
code-tools validate_manifest --feature-dir .tasks/01-user-authentication
```

---

## Testing

```bash
cd tools
pip install pytest jsonschema
pytest -q
```

---

## Naming Conventions

| Item         | Format                | Example               |
| ------------ | --------------------- | --------------------- |
| Feature ID   | Two-digit zero-padded | `01`, `02`, `99`      |
| Feature Slug | lowercase-hyphen      | `user-authentication` |
| Task ID      | `T` + two-digit       | `T01`, `T15`          |
| Task Slug    | lowercase-hyphen      | `database-schema`     |

---

## References

- **Agent Definitions**: `.claude/agents/*.md`
- **Command Definitions**: `.claude/commands/**/*.md`
- **Schema Documentation**: `.claude/schemas/README.md`
- **code-tools README**: `tools/README.md`
