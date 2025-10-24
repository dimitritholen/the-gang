---
allowed-tools: Task, Read, Bash, Glob, Grep
argument-hint: [--scope path] [--focus aspect] [--depth level]
description: Generate memory artifacts from existing codebase
---

<instructions>
You are orchestrating **codebase memory generation** using Task Decomposition and Chain of Command patterns to reverse-engineer an existing codebase and create comprehensive memory artifacts.

Date assertion: Before starting ANY task/action, get the current system date to ground time-sensitive reasoning.

## Purpose

Generate 5 memory artifacts documenting:

1. Project context (high-level overview)
2. Technology stack (with rationale)
3. Coding conventions (patterns to follow)
4. Architecture decisions (ADRs)
5. Feature inventory (existing features)

## Prerequisites

**Required**:

- Existing codebase with code to analyze
- Read/write access to `.claude/memory/` directory

**Optional**:

- Git repository (for commit history analysis)
- Package manifests (package.json, requirements.txt, Cargo.toml, go.mod, pom.xml, etc.)
- Configuration files (language/framework-specific linters, formatters, build configs)

</instructions>

<orchestration_strategy>

## Orchestration Pattern: Task Decomposition + Chain of Command

This command uses two complementary techniques:

**Task Decomposition**: Complex memory generation broken into hierarchical sub-tasks:

- Level 1: Parse arguments and detect scope
- Level 2: Multi-phase analysis with validation
- Level 3: Artifact generation
- Level 4: Validation and summary

**Chain of Command**: Specialized agent delegation with structured handoffs:

- Orchestrator (this command) → codebase-archeologist agent
- Agent completes phase → returns to orchestrator
- Orchestrator validates → passes to next phase
- Clear input/output contracts between phases

</orchestration_strategy>

<task_decomposition>

## Task Hierarchy

### Level 1: Scope Detection (Orchestrator Responsibility)

**Sub-task 1.1: Parse Command Arguments**

```bash
# Default values
SCOPE="."
FOCUS="all"
DEPTH="deep"

# Parse --scope flag
if [ "$1" = "--scope" ]; then
  SCOPE="$2"
fi

# Parse --focus flag (architecture, tech-stack, conventions, features, all)
if [ "$3" = "--focus" ]; then
  FOCUS="$4"
fi

# Parse --depth flag (quick, medium, deep)
if [ "$5" = "--depth" ]; then
  DEPTH="$6"
fi
```

**Sub-task 1.2: Detect Codebase Type**

Use Glob and Grep tools to:

- Check if monorepo (pnpm-workspace.yaml, lerna.json, nx.json, Cargo.toml workspace, etc.)
- Check if microservices (multiple service directories)
- Detect primary language (count file extensions)
- Estimate size (LOC, file count)

Use Glob tool for file pattern discovery:

- Search for configuration files indicating project type
- Count files by extension to determine language distribution
- Identify build/package manifests across ecosystems

**Sub-task 1.3: Present Scope Summary**

Output:

```markdown
## Codebase Scope Detected

**Type**: [Monorepo|Microservices|Monolith]
**Languages**: [Detected primary language] ([X]%), [Secondary] ([Y]%)
**Size**: ~[X] LOC across [Y] files
**Packages**: [N] ([list package names])

**Scope for Analysis**: {SCOPE}
**Focus**: {FOCUS}
**Depth**: {DEPTH}

Proceeding with analysis...
```

---

### Level 2: Multi-Phase Analysis (Agent Delegation via Chain of Command)

This level delegates to specialized agent in 4 sequential passes with 3 validation checkpoints.

#### Phase 2.1: Initial Analysis (Agent Pass 1)

**Delegate to**: codebase-archeologist agent
**Mode**: analyze_phase1
**Agent Tasks**:

- Scan directory structure
- Parse configuration files
- Identify tech stack and architecture
- Analyze technology rationale
- Document usage patterns

**Agent Input Contract**:

```json
{
  "mode": "analyze_phase1",
  "scope": "$SCOPE",
  "focus": "$FOCUS",
  "depth": "$DEPTH",
  "scope_detection_results": {
    "type": "...",
    "languages": "...",
    "size": "..."
  }
}
```

**Agent Output Contract**:

```json
{
  "status": "complete",
  "output_file": ".claude/memory/.tmp-findings-initial.md",
  "summary": {
    "technologies_identified": 15,
    "architecture_pattern": "microservices",
    "confidence_high": 8,
    "confidence_medium": 5,
    "confidence_low": 2
  }
}
```

**Quality Requirements**:

- All claims cite source files (file:line format)
- All inferences have confidence levels (High/Medium/Low)
- No invented features or patterns
- Flag contradictions explicitly
- Use "Unknown" instead of guessing

**Invoke Agent**:

```bash
Task(
  subagent_type="codebase-archeologist",
  description="Perform initial codebase analysis",
  prompt="Execute Phase 1 analysis following MODE 1 workflow"
)
```

#### Checkpoint 1: Validate Initial Findings (Orchestrator Responsibility)

**Sub-task 2.1.1: Read Agent Output**

```bash
FINDINGS_FILE=".claude/memory/.tmp-findings-initial.md"
if [ ! -f "$FINDINGS_FILE" ]; then
  echo "ERROR: Initial findings file not found"
  exit 1
fi
cat "$FINDINGS_FILE"
```

**Sub-task 2.1.2: User Validation**

Present structured questions:

1. "Tech Stack Detection: Does the identified technology stack match your project?"
2. "Architecture Assessment: Is the detected architecture accurate?"
3. "Deployment Model: Does the identified deployment model match reality?"
4. "Technology Rationale: Are there any technologies where the inferred rationale is incorrect?"
5. "Corrections Needed: Any other inaccuracies or missing information?"

**Sub-task 2.1.3: Write Corrections**

```bash
cat > .claude/memory/.tmp-corrections-initial.md <<EOF
# Corrections for Initial Analysis
# AUTO-DELETE after artifacts generated
# Created: $(date +%Y-%m-%d)

## User Corrections

### Tech Stack
[User corrections]

### Architecture
[User corrections]

### Deployment Model
[User corrections]

### Additional Notes
[User corrections]

## Validation Status
- Initial analysis validated: [YES/NO]
- Corrections provided: [YES/NO]
- Ready for next phase: YES
EOF
```

**Sub-task 2.1.4: Cleanup Temporary Files**

```bash
rm .claude/memory/.tmp-findings-initial.md
echo "Cleaned up temporary findings file"
```

---

#### Phase 2.2: Convention Analysis (Agent Pass 2)

**Delegate to**: codebase-archeologist agent
**Mode**: analyze_phase2
**Agent Tasks**:

- Read corrections from Checkpoint 1
- Mine naming conventions
- Extract code organization patterns
- Identify error handling conventions
- Analyze API design patterns
- Determine testing strategy

**Agent Input Contract**:

```json
{
  "mode": "analyze_phase2",
  "corrections_file": ".claude/memory/.tmp-corrections-initial.md",
  "validated_tech_stack": "...",
  "validated_architecture": "..."
}
```

**Agent Output Contract**:

```json
{
  "status": "complete",
  "output_file": ".claude/memory/.tmp-findings-conventions.md",
  "summary": {
    "patterns_identified": 12,
    "conformance_percentage": 85,
    "deviations_found": 8
  }
}
```

**Invoke Agent**:

```bash
Task(
  subagent_type="codebase-archeologist",
  description="Analyze coding conventions and patterns",
  prompt="Execute Phase 2 analysis following MODE 2 workflow. Apply corrections from Checkpoint 1."
)
```

#### Checkpoint 2: Validate Convention Findings (Orchestrator Responsibility)

**Sub-task 2.2.1: Read Agent Output**

```bash
FINDINGS_FILE=".claude/memory/.tmp-findings-conventions.md"
cat "$FINDINGS_FILE"
```

**Sub-task 2.2.2: User Validation**

Present questions:

1. "Naming Conventions: Do the identified patterns match your standards?"
2. "Code Organization: Is the detected organization pattern accurate?"
3. "Error Handling: Does the identified approach match your practices?"
4. "API Design: Are the identified API patterns correct?"
5. "Testing Strategy: Does the detected strategy match reality?"
6. "Pattern Conformance: Do conformance percentages seem accurate?"

**Sub-task 2.2.3: Write Corrections**

```bash
cat > .claude/memory/.tmp-corrections-conventions.md <<EOF
# Corrections for Convention Analysis
[User corrections structure]
EOF
```

**Sub-task 2.2.4: Cleanup**

```bash
rm .claude/memory/.tmp-findings-conventions.md
```

---

#### Phase 2.3: Final Analysis (Agent Pass 3)

**Delegate to**: codebase-archeologist agent
**Mode**: analyze_phase3
**Agent Tasks**:

- Read all previous corrections
- Map backend endpoints to features
- Map frontend routes to features
- Cross-reference with database schema
- Assess feature completeness
- Generate Architecture Decision Records
- Assign confidence levels to ADRs

**Agent Input Contract**:

```json
{
  "mode": "analyze_phase3",
  "corrections_initial": ".claude/memory/.tmp-corrections-initial.md",
  "corrections_conventions": ".claude/memory/.tmp-corrections-conventions.md"
}
```

**Agent Output Contract**:

```json
{
  "status": "complete",
  "output_file": ".claude/memory/.tmp-findings-final.md",
  "summary": {
    "features_identified": 23,
    "adrs_generated": 18,
    "confidence_distribution": {
      "high": 12,
      "medium": 5,
      "low": 1
    }
  }
}
```

**Invoke Agent**:

```bash
Task(
  subagent_type="codebase-archeologist",
  description="Complete feature inventory and ADR generation",
  prompt="Execute Phase 3 analysis following MODE 3 workflow. Apply all previous corrections."
)
```

#### Checkpoint 3: Validate Final Findings (Orchestrator Responsibility)

**Sub-task 2.3.1: Read Agent Output**

```bash
FINDINGS_FILE=".claude/memory/.tmp-findings-final.md"
cat "$FINDINGS_FILE"
```

**Sub-task 2.3.2: User Validation**

Questions:

1. "Feature Inventory: Are all identified features accurate and complete?"
2. "Feature Completeness: Do completeness percentages match reality?"
3. "Architecture Decisions: Do inferred ADRs reflect actual decisions?"
4. "ADR Confidence Levels: Are confidence levels appropriate?"
5. "Missing Features: Any features not identified?"

**Sub-task 2.3.3: Write Corrections**

```bash
cat > .claude/memory/.tmp-corrections-final.md <<EOF
# Corrections for Final Analysis
[User corrections structure]
EOF
```

**Sub-task 2.3.4: Cleanup**

```bash
rm .claude/memory/.tmp-findings-final.md
```

---

### Level 3: Artifact Generation (Agent Pass 4)

**Delegate to**: codebase-archeologist agent
**Mode**: generate_artifacts
**Agent Tasks**:

- Read ALL correction files from 3 checkpoints
- Generate 5 memory artifacts in `.claude/memory/`:
  1. project-context.md
  2. tech-stack-baseline.md
  3. coding-conventions.md
  4. architecture-decisions.md
  5. feature-inventory.md
- Incorporate all user corrections
- Ensure cross-references are valid

**Agent Input Contract**:

```json
{
  "mode": "generate_artifacts",
  "correction_files": [
    ".claude/memory/.tmp-corrections-initial.md",
    ".claude/memory/.tmp-corrections-conventions.md",
    ".claude/memory/.tmp-corrections-final.md"
  ]
}
```

**Agent Output Contract**:

```json
{
  "status": "complete",
  "artifacts_generated": [
    ".claude/memory/project-context.md",
    ".claude/memory/tech-stack-baseline.md",
    ".claude/memory/coding-conventions.md",
    ".claude/memory/architecture-decisions.md",
    ".claude/memory/feature-inventory.md"
  ],
  "artifacts_summary": {
    "total_size_kb": 245,
    "total_citations": 312,
    "total_adrs": 18,
    "total_features": 23
  }
}
```

**Quality Requirements**:

- All user corrections applied
- All claims cite source files (file:line)
- All inferences have confidence levels
- No placeholders or TODOs
- Cross-references between artifacts valid

**Invoke Agent**:

```bash
Task(
  subagent_type="codebase-archeologist",
  description="Generate final memory artifacts",
  prompt="Execute artifact generation following MODE 4 workflow. Incorporate ALL corrections from 3 checkpoints."
)
```

**Sub-task 3.1: Cleanup All Temporary Files**

```bash
rm .claude/memory/.tmp-corrections-initial.md
rm .claude/memory/.tmp-corrections-conventions.md
rm .claude/memory/.tmp-corrections-final.md
echo "Cleaned up all temporary correction files"
```

---

### Level 4: Validation and Summary (Orchestrator Responsibility)

#### Sub-task 4.1: Verify Final Artifacts

**Sub-task 4.1.1: Check All Files Exist**

```bash
REQUIRED_FILES=(
  ".claude/memory/project-context.md"
  ".claude/memory/tech-stack-baseline.md"
  ".claude/memory/coding-conventions.md"
  ".claude/memory/architecture-decisions.md"
  ".claude/memory/feature-inventory.md"
)

MISSING_COUNT=0
for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "ERROR: Required artifact missing: $file"
    MISSING_COUNT=$((MISSING_COUNT + 1))
  fi
done

if [ $MISSING_COUNT -eq 0 ]; then
  echo "All 5 memory artifacts verified"
else
  echo "$MISSING_COUNT artifact(s) missing"
  exit 1
fi
```

**Sub-task 4.1.2: Content Quality Validation**

Use Grep tool to validate artifact quality:

- Check for evidence citations ("According to", "Evidence:")
- Check for confidence levels ("Confidence: High", "Confidence: Medium")
- Detect placeholders (TODO, FIXME, XXX)

#### Sub-task 4.2: Generate Summary Report

Present comprehensive summary:

```markdown
## Memory Generation Complete: $PROJECT_NAME

**Analysis Duration**: [X] minutes
**Scope**: [Full codebase | Path]
**Depth**: [Deep | Medium | Quick]

### Generated Artifacts

1. **project-context.md** ([X] KB)
   - Overview, architecture, tech stack summary
   - Coding conventions summary
   - Constraints and NFRs

2. **tech-stack-baseline.md** ([X] KB)
   - [N] technologies documented
   - Rationale for each choice
   - Configuration details
   - Alternative technologies considered

3. **coding-conventions.md** ([X] KB)
   - File naming: [Pattern] ([X]% conformance)
   - Code style: [Pattern] ([X]% conformance)
   - Error handling: [Pattern] ([X]% conformance)
   - API design: [Pattern]
   - Testing: [Strategy]

4. **architecture-decisions.md** ([X] KB)
   - [N] ADRs generated
   - [x] High confidence, [X] Medium, [X] Low
   - Evidence cited for all decisions

5. **feature-inventory.md** ([X] KB)
   - [N] features identified
   - [X]% fully complete (frontend + backend + tests)
   - [X]% partially complete
   - [X]% in early development

### Key Findings

**Architecture**: [Pattern detected]
**Dominant Language**: [Detected language] ([X]% of code)
**Testing Coverage**: [X]% (estimated)
**Code Quality**: [High | Medium | Low]
**Consistency Score**: [X]% across naming, style, patterns

### Recommendations

[Recommendations based on findings]

### Next Steps

**For New Feature Development**:

1. All agents now load these memory artifacts automatically
2. New code follows existing conventions
3. New features integrate with existing architecture

**To Keep Memory Updated**:

- After major refactors: `/update-memory "architecture"`
- After dependency changes: `/update-memory "tech-stack"`
- After establishing new patterns: `/mine-patterns --type "[pattern]"`

**To Validate New Features**:

- Before implementation: `/validate-consistency "[feature]"`

### Files Ready for Use

All agents will now reference:

- `project-context.md` for high-level context
- `tech-stack-baseline.md` for technology decisions
- `coding-conventions.md` for style and patterns
- `architecture-decisions.md` for architectural context
- `feature-inventory.md` to avoid duplicate features

**Memory Baseline Established**: Complete
```

</task_decomposition>

<execution_workflow>

## Execution Flow Summary

### Phase Execution Timeline

**Phase 2.1: Initial Analysis + Checkpoint 1** (~10-15 min)

- Agent analyzes structure, config, tech stack
- Agent writes `.tmp-findings-initial.md`
- Orchestrator validates with user
- Orchestrator writes `.tmp-corrections-initial.md`
- Cleanup: Delete `.tmp-findings-initial.md`

**Phase 2.2: Convention Analysis + Checkpoint 2** (~15-20 min)

- Agent reads Checkpoint 1 corrections
- Agent mines conventions, patterns
- Agent writes `.tmp-findings-conventions.md`
- Orchestrator validates with user
- Orchestrator writes `.tmp-corrections-conventions.md`
- Cleanup: Delete `.tmp-findings-conventions.md`

**Phase 2.3: Final Analysis + Checkpoint 3** (~15-20 min)

- Agent reads Checkpoints 1-2 corrections
- Agent maps features, generates ADRs
- Agent writes `.tmp-findings-final.md`
- Orchestrator validates with user
- Orchestrator writes `.tmp-corrections-final.md`
- Cleanup: Delete `.tmp-findings-final.md`

**Phase 2.4: Artifact Generation** (~10-15 min)

- Agent reads ALL corrections from 3 checkpoints
- Agent generates 5 final memory artifacts
- Agent incorporates all user corrections
- Orchestrator verifies artifacts created
- Cleanup: Delete all 3 correction files

**Total Time**: 50-70 minutes for deep analysis

### Temporary Files Lifecycle

- `.tmp-findings-initial.md` - Created Phase 2.1, Deleted Checkpoint 1
- `.tmp-corrections-initial.md` - Created Checkpoint 1, Deleted Phase 2.4
- `.tmp-findings-conventions.md` - Created Phase 2.2, Deleted Checkpoint 2
- `.tmp-corrections-conventions.md` - Created Checkpoint 2, Deleted Phase 2.4
- `.tmp-findings-final.md` - Created Phase 2.3, Deleted Checkpoint 3
- `.tmp-corrections-final.md` - Created Checkpoint 3, Deleted Phase 2.4

</execution_workflow>

<error_handling>

## Error Scenarios and Resolution

### Error 1: No Code Files Found

```markdown
ERROR: No source files found in scope "[SCOPE]"

**Possible causes**:

- Incorrect path specified
- Empty repository
- All code is gitignored

**Solution**:

- Check scope path: `/generate-memory --scope "src"`
- Verify code exists: `ls -R [SCOPE]`
```

### Error 2: Insufficient Permissions

```markdown
ERROR: Cannot write to .claude/memory/

**Solution**:

- Check directory permissions
- Create directory: `mkdir -p .claude/memory`
- Verify write access: `touch .claude/memory/test`
```

### Error 3: Binary Files Only

```markdown
WARNING: Only binary files detected, no source code

**Detected**: node_modules/, dist/, build/
**Missing**: src/, lib/, app/

**Solution**:

- Ensure in project root
- Check if source in subdirectory
- Specify correct scope: `/generate-memory --scope "packages/app/src"`
```

### Error 4: Checkpoint Interrupted

```markdown
**Checkpoint Interrupted**

**Progress Saved**: Phase 1-2 complete

**To Resume**: Re-run `/generate-memory` (will detect partial artifacts)
```

### Error 5: Git History Unavailable

```markdown
WARNING: No git repository detected

**Impact**:

- Cannot generate ADR timeline
- Cannot attribute technology adoption

**Workaround**:

- ADRs generated without dates
- Technology choices inferred from current state
- Confidence levels may be lower
```

</error_handling>

<best_practices>

## Command Usage Best Practices

### First-Time Analysis

```bash
# Full deep analysis (recommended)
/generate-memory
```

### Targeted Analysis

```bash
# Analyze only frontend
/generate-memory --scope "src/frontend"

# Focus on architecture only
/generate-memory --focus "architecture"

# Quick analysis (faster, less detailed)
/generate-memory --depth "quick"
```

### Monorepo Analysis

```bash
# Analyze each package separately
/generate-memory --scope "packages/app1"
/generate-memory --scope "packages/app2"

# Or full monorepo (comprehensive but slower)
/generate-memory
```

### After Major Changes

```bash
# Regenerate specific aspects
/update-memory "tech-stack"
/update-memory "conventions"
/update-memory "architecture"
```

</best_practices>

---

**Begin execution**: Detect codebase structure and initiate Task Decomposition + Chain of Command workflow in scope: **$SCOPE**
