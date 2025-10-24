code-tools (Python)

Portable CLI providing consistent subcommands for prompts across projects.

Install

- Local dev (editable):
  - cd tools && pip install -e .[web]
- User install:
  - cd tools && pip install .[web]

Usage examples

- List: code-tools list_dir --path . --depth 1
- Search files: code-tools search_file --glob "src/\*_/_.py"
- Grep: code-tools grep_code --pattern "def main" --paths "src,lib"
- Read: code-tools read_file --path docs/code-assistant.md --start 1 --end 200
- Fetch: code-tools fetch_content --url <https://example.com>
- Replace: code-tools search_replace --file ./.dimitri/design-system.md --replacements @reps.json
- Create: code-tools create_file --file out.txt --content @content.txt --add-last-line-newline
- Edit: code-tools edit_file --file out.txt --patch @new.txt
- Memory: code-tools search_memory --dir ./.dimitri/memory --query "auth flow" --topk 5

JSON responses

- Always prints a single JSON object with ok/tool/version and data or error.

Task Management Tools (v1.1)

Six new commands for task lifecycle management:

1. **slugify_feature** - Convert feature names to slugs
   code-tools slugify_feature --name "User Authentication" [--feature-id NN]

2. **read_task_manifest** - Read manifest with metrics
   code-tools read_task_manifest --path .tasks/01-auth/manifest.json
   Returns: task_count, completed_count, in_progress_count, blocked_count

3. **update_task_status** - Update task status + sync manifests
   code-tools update_task_status --task-id T01 --status IN_PROGRESS --feature-dir .tasks/01-auth
   Statuses: NOT_STARTED | IN_PROGRESS | COMPLETED | BLOCKED

4. **find_next_task** - Get next available task (dependencies validated)
   code-tools find_next_task --manifest .tasks/01-auth/manifest.json

5. **validate_manifest** - Check manifest consistency
   code-tools validate_manifest --feature-dir .tasks/01-auth
   Checks: task counts, status accuracy, dependency validity, blocker sync

6. **list_memory_artifacts** - List/filter memory artifacts
   code-tools list_memory_artifacts --dir .claude/memory [--feature slug]
   Categories: requirements, tech_analysis, implementation_plans, scope_validations, etc.

Token Savings: These tools reduce command complexity by ~30-40% (consolidates 30-50 lines of bash into 1-2 CLI calls).

Knowledge Graph Tools (v1.2)

Three new commands for JSONL-based knowledge graph memory:

1. **sync_memory_graph** - Build JSONL graphs from markdown
   code-tools sync_memory_graph --dir .claude/memory [--feature slug]
   Parses requirements markdown → entities/relationships → JSONL
   Auto-invalidates cache on file modification (mtime tracking)

2. **query_memory** - Query knowledge graph with natural language
   code-tools query_memory --dir .claude/memory --feature slug --query "security requirements" [--mode direct|nlp|auto] [--limit 10]
   Modes:
   - direct: Fast keyword-based graph query (default for now)
   - nlp: LLM-powered query translation (placeholder)
   - auto: Try direct, fallback to NLP if no results

3. **Entity Types Supported**:
   - Feature (status, priority, dependencies, tags)
   - Requirement (functional, non-functional, security, performance, etc.)
   - TechDecision (rationale, alternatives, stakeholders)
   - Component (code components, dependencies, file paths)
   - Task (status, blockers, dependencies)
   - Pattern (naming, structure, conformance metrics)
   - Convention (rules, deviations, conformance %)

4. **Relationship Types**:
   - requires (Feature → Requirement)
   - depends_on (Feature → Feature, Task → Task, Component → Component)
   - implements (Component → Requirement)
   - follows (Component → Convention/Pattern)
   - justifies (TechDecision → Component/Feature)
   - blocks (Task → Task)
   - derived_from (Requirement → Requirement)

Token Efficiency: Graph queries return 50-300 tokens vs 1200-3000 tokens for full markdown (80-95% reduction).

Example Workflow:

# Sync markdown to graph

code-tools sync_memory_graph --dir .claude/memory

# Query graph

code-tools query_memory --feature user-authentication --query "high priority requirements" --limit 5

# Result: Returns only matching entities + relationships (not full markdown)

Architecture:

- Storage: {feature-slug}.jsonl per feature (one JSON object per line)
- Cache: mtime-based invalidation (auto-rebuilds when markdown changes)
- Parsers: requirements_parser.py (more coming: conventions, tech-analysis)
- Graph Store: code_tools/graph.py (entities, relationships, traversal, queries)

Notes

- `fetch_content` requires optional extra `web` (pip install .[web]).
- `search_web` is a placeholder that returns an error unless you wire a provider.
- Tests
- Run smoke tests with pytest:
- cd tools && python -m pip install -e .[web] && python -m pip install pytest jsonschema && pytest -q
