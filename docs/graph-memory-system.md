# JSONL Knowledge Graph Memory System

**Status**: Implemented (v1.2)
**Date**: 2025-10-23

## Overview

Token-efficient knowledge graph system for project memory. Markdown files remain the human-readable source of truth, while JSONL graphs enable fast, targeted queries that reduce token usage by 80-95%.

## Architecture

```
.claude/memory/
├── requirements-user-auth.md          # Source markdown (human-editable)
├── user-auth.jsonl                    # Generated graph (auto-synced)
├── tech-analysis-payments.md
├── payments.jsonl
└── ...

code_tools/
├── graph.py                           # Entity/relationship models, GraphStore
├── parsers/
│   ├── requirements_parser.py         # Extract FR/NFR from markdown
│   ├── conventions_parser.py          # (TODO) Extract patterns/conventions
│   └── tech_analysis_parser.py        # (TODO) Extract decisions/rationale
└── builders/
    └── feature_graph_builder.py       # Orchestrate parse → entities → JSONL
```

## Entity Types

| Entity | Fields | Example |
|--------|--------|---------|
| Feature | id, name, status, priority, dependencies[], tags[] | `feature:user-authentication` |
| Requirement | req_type, priority, acceptance_criteria[], parent_feature | `req:FR-001` (functional), `req:NFR-SEC-001` (security) |
| TechDecision | decision, rationale, alternatives[], stakeholders[] | Why JWT vs sessions |
| Component | component_type, file_path, dependencies[], line_range | `auth_service.ts:10-50` |
| Task | status, dependencies[], blockers[], assigned_to | `T01: NOT_STARTED` |
| Pattern | pattern_type, examples[], conformance_pct, violations[] | PascalCase for components (95% conformance) |
| Convention | category, rule, conformance_pct, deviations[] | API design: REST conventions |

## Relationship Types

| Relationship | Direction | Example |
|--------------|-----------|---------|
| `requires` | Feature → Requirement | Auth feature requires FR-001 |
| `depends_on` | Feature → Feature, Task → Task | Payment depends on Auth |
| `implements` | Component → Requirement | `auth.ts` implements FR-001 |
| `follows` | Component → Pattern/Convention | `UserProfile.tsx` follows PascalCase |
| `justifies` | TechDecision → Component | JWT decision justifies token handling |
| `blocks` | Task → Task | T02 blocks T05 |
| `derived_from` | Requirement → Requirement | Child requirement from parent |

## Token Efficiency

**Before (Full Markdown)**:
```
Read requirements-user-auth.md (5.7KB)
→ 1,200-3,000 tokens per file
→ Multiple files = 5,000-15,000 tokens
```

**After (Graph Query)**:
```
Query: "security requirements for auth"
→ Returns 5 entities + 6 relationships
→ 50-300 tokens (80-95% reduction)
```

## Usage

### 1. Sync Markdown to Graph

```bash
# Sync all features
code-tools sync_memory_graph --dir .claude/memory

# Sync single feature
code-tools sync_memory_graph --dir .claude/memory --feature user-authentication
```

**Output**: `user-authentication.jsonl` (one JSON object per line)

### 2. Query Graph

```bash
# Find security requirements
code-tools query_memory \
  --feature user-authentication \
  --query "security requirements" \
  --limit 5

# Find high priority items
code-tools query_memory \
  --feature user-authentication \
  --query "high priority requirements"

# Find all requirements (type filter only)
code-tools query_memory \
  --feature user-authentication \
  --query "requirements"
```

**Query Modes**:
- `direct` (default): Fast keyword-based search across all entity fields
- `nlp` (TODO): LLM-powered natural language → graph query translation
- `auto`: Try direct first, fallback to NLP if no results

### 3. Programmatic Usage

```python
from code_tools.graph import GraphStore, EntityType
from pathlib import Path

store = GraphStore(Path('.claude/memory'))

# Query security requirements
reqs = store.query_entities(
    'user-authentication',
    entity_type=EntityType.REQUIREMENT,
    filters={'req_type': 'security'}
)

# Traverse dependencies
deps = store.traverse(
    'user-authentication',
    'feature:auth',
    RelationshipType.DEPENDS_ON,
    direction='outbound'
)
```

## Cache Management

**Auto-Invalidation**: Graphs rebuild when markdown files change (mtime tracking).

```python
# Manual invalidation (if needed)
store.invalidate_cache('user-authentication')  # Single feature
store.invalidate_cache()  # All features
```

## Example Query Results

```bash
$ code-tools query_memory --feature user-authentication --query "security requirements" --limit 3
```

```json
{
  "ok": true,
  "tool": "query_memory",
  "data": {
    "mode": "direct",
    "feature": "user-authentication",
    "total_matches": 6,
    "entities": [
      {
        "id": "req:NFR-SEC-001",
        "name": "Passwords hashed with bcrypt (cost factor 12)",
        "type": "requirement",
        "req_type": "security",
        "priority": "high",
        "parent_feature": "feature:user-authentication"
      },
      {
        "id": "req:NFR-SEC-002",
        "name": "JWT tokens signed with RS256",
        "type": "requirement",
        "req_type": "security",
        "priority": "high"
      },
      {
        "id": "req:NFR-SEC-003",
        "name": "HTTPS required for all authentication endpoints",
        "type": "requirement",
        "req_type": "security",
        "priority": "high"
      }
    ],
    "relationships": [
      {
        "source_id": "feature:user-authentication",
        "target_id": "req:NFR-SEC-001",
        "type": "requires"
      }
    ]
  }
}
```

## Testing

```bash
cd tools
python -m pytest tests/test_graph.py -v
```

**Test Coverage**:
- ✅ Entity serialization/deserialization
- ✅ Relationship ID generation (deterministic)
- ✅ JSONL save/load with atomic writes
- ✅ Entity queries with type/field filters
- ✅ Graph traversal (multi-hop relationships)
- ✅ Requirements parser (FR/NFR extraction)
- ✅ Feature graph builder (end-to-end)
- ✅ Cache invalidation (mtime tracking)

## Roadmap

### Phase 1 (Completed)
- [x] Core graph models (Entity, Relationship)
- [x] JSONL persistence with caching
- [x] Requirements parser (FR/NFR)
- [x] Graph builder pipeline
- [x] CLI commands (sync, query)
- [x] Integration tests

### Phase 2 (Next)
- [ ] Conventions parser (patterns, deviations)
- [ ] Tech analysis parser (decisions, alternatives)
- [ ] Task manifest parser (dependencies, blockers)
- [ ] LLM-powered query translation (NLP mode)
- [ ] Multi-hop query DSL (find all components implementing security requirements)

### Phase 3 (Future)
- [ ] Graph visualization (Mermaid/GraphViz export)
- [ ] Incremental sync (parse only changed files)
- [ ] Cross-feature queries (find all features depending on auth)
- [ ] Query templates library (common patterns)
- [ ] Relationship inference (auto-detect component→requirement links via code analysis)

## Design Decisions

### Why JSONL instead of SQLite/Neo4j?
- **Simplicity**: No DB setup, just files
- **Streaming**: Process large graphs incrementally
- **Git-friendly**: Line-based format for diffs
- **Portability**: Pure Python, no dependencies

### Why Markdown as Source of Truth?
- **Human-readable**: Easy to write/review
- **Git workflow**: PRs, diffs, history
- **Editor support**: VS Code, vim, etc.
- **Graph is derived**: Auto-generated, disposable

### Why Per-Feature Files?
- **Modularity**: Independent graphs
- **Performance**: Query only relevant features
- **Isolation**: Changes don't affect other features
- **Scalability**: Add features without bloating single file

## Known Limitations

1. **NLP Mode**: Not yet implemented (uses placeholder)
2. **Cross-Feature Queries**: Single feature queries only (workaround: query multiple features separately)
3. **Schema Evolution**: Manual migration needed if entity structure changes
4. **Large Files**: Entire JSONL loaded into memory (mitigated by per-feature files)

## Performance

**Tested with EXAMPLE-requirements-user-authentication.md**:
- Parse + build: ~50ms
- Query (5 entities): ~5ms
- JSONL size: 12KB (17 entities, 16 relationships)
- Memory: ~50KB loaded graph

**Estimated for 50 features**:
- Total JSONL: ~600KB
- Query time: <10ms per feature
- Memory: ~2.5MB (all features loaded)

## Contributing

To add new parsers:

1. Create `code_tools/parsers/{type}_parser.py`
2. Implement `parse() -> (entities, relationships)`
3. Add builder method in `FeatureGraphBuilder`
4. Write tests in `tests/test_graph.py`
5. Update CLI commands if needed

---

**Questions?** See `tools/README.md` or run `code-tools query_memory --help`
