---
allowed-tools: Task, Read, Bash, Glob, Grep
argument-hint: [--scope path] [--focus aspect] [--depth level]
description: Generate memory artifacts from existing codebase
---

<instructions>
You are orchestrating **codebase memory generation** to reverse-engineer an existing codebase and create comprehensive memory artifacts for future development.

Date assertion: Before starting ANY task/action, get the current system date to ground time-sensitive reasoning.

## Purpose

Generate 5 memory artifacts that document:

1. Project context (high-level overview)
2. Technology stack (with rationale)
3. Coding conventions (patterns to follow)
4. Architecture decisions (ADRs)
5. Feature inventory (existing features)

These artifacts will be used by all agents when adding new features to ensure consistency with existing codebase.

## Prerequisites

**Required**:

- Existing codebase with code to analyze
- Read/write access to `.claude/memory/` directory

**Optional**:

- Git repository (for commit history analysis)
- Package manifests (package.json, requirements.txt, etc.)
- Configuration files (tsconfig, eslint, etc.)

</instructions>

<generation_orchestration>

## Step 1: Parse Arguments and Detect Scope

Parse command arguments:

```bash
# Default: Full codebase analysis
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

**Scope Detection**:

- Check if monorepo (pnpm-workspace.yaml, lerna.json, nx.json)
- Check if microservices (multiple service directories)
- Detect primary language (count file extensions)
- Estimate size (LOC, file count)

Use Glob and Grep tools to:

```bash
# Detect project type
glob pattern="package.json" path="."
glob pattern="**/package.json" path="."  # Multiple = monorepo

# Detect languages
glob pattern="**/*.ts" path="."
glob pattern="**/*.py" path="."
glob pattern="**/*.java" path="."

# Count approximate LOC
find . -name "*.ts" -o -name "*.tsx" | xargs wc -l
```

Present scope summary:

```markdown
## Codebase Scope Detected

**Type**: Monorepo (detected pnpm-workspace.yaml)
**Languages**: TypeScript (80%), JavaScript (15%), CSS (5%)
**Size**: ~45,000 LOC across 420 files
**Packages**: 3 (apps/frontend, apps/backend, packages/shared)

**Scope for Analysis**: {SCOPE}
**Focus**: {FOCUS}
**Depth**: {DEPTH}

Proceeding with analysis...
```

---

## Step 2: Multi-Phase Analysis with Validation Checkpoints

This step uses a four-pass workflow with 3 validation checkpoints to enable interactive validation and correction.

### Phase 2a: Initial Analysis (Agent Pass 1)

**Invoke codebase-archeologist agent in initial analysis mode:**

```bash
# Use Task tool to invoke agent
Task(
  subagent_type="codebase-archeologist",
  description="Perform initial codebase analysis",
  prompt="""
**Mode:** analyze_phase1

**Scope:** $SCOPE
**Focus:** $FOCUS
**Depth:** $DEPTH

**Task:** Execute Phase 1 (Discovery) and Phase 2 (Technology Analysis)

**Context from Step 1:**
{Paste scope detection results}

**Instructions:**
1. Scan directory structure and detect project type
2. Parse configuration files (package.json, requirements.txt, etc.)
3. Identify tech stack, architecture, deployment model
4. Analyze why each technology was chosen
5. Document how each technology is used
6. Write findings to: .claude/memory/.tmp-findings-initial.md
7. Return confirmation with summary statistics

Follow MODE 1 workflow in your agent instructions.

**Quality Requirements:**
- All claims cite source files (file:line format)
- All inferences have confidence levels (High/Medium/Low)
- No invented features or patterns
- Flag contradictions explicitly
- Use "Unknown" instead of guessing
"""
)
```

**Expected Output:**

- Agent creates `.claude/memory/.tmp-findings-initial.md`
- Agent returns: "Initial analysis complete - ready for validation"

### Phase 2b: Checkpoint 1 Validation (Orchestrator Interaction)

**Read and validate initial findings:**

```bash
# Read findings file
FINDINGS_FILE=".claude/memory/.tmp-findings-initial.md"

if [ ! -f "$FINDINGS_FILE" ]; then
  echo "ERROR: Initial findings file not found at $FINDINGS_FILE"
  exit 1
fi

# Display findings to orchestrator
cat "$FINDINGS_FILE"
```

**Present findings to user for validation:**

Use structured questions to validate key aspects:

**Validation Questions:**

1. "Tech Stack Detection: Does the identified technology stack match your project?"
2. "Architecture Assessment: Is the detected architecture (e.g., monolith/microservices, client-server) accurate?"
3. "Deployment Model: Does the identified deployment model (e.g., serverless, containerized) match reality?"
4. "Technology Rationale: Are there any technologies where the inferred rationale is incorrect?"
5. "Corrections Needed: Any other inaccuracies or missing information in the initial analysis?"

**Write corrections file:**

```bash
cat > .claude/memory/.tmp-corrections-initial.md <<EOF
# Corrections for Initial Analysis
# AUTO-DELETE after artifacts generated
# Created: $(date +%Y-%m-%d)

## User Corrections

### Tech Stack
{User's corrections to technology stack if any}

### Architecture
{User's corrections to architecture assessment if any}

### Deployment Model
{User's corrections to deployment model if any}

### Technology Rationale
{User's corrections to technology rationale if any}

### Additional Notes
{Any other corrections or clarifications from user}

## Validation Status
- Initial analysis validated: {YES/NO}
- Corrections provided: {YES/NO}
- Ready for next phase: {YES}
EOF

echo "✓ Corrections written to .claude/memory/.tmp-corrections-initial.md"
```

**Cleanup Phase 2a artifacts:**

```bash
# Delete initial findings file (no longer needed)
rm .claude/memory/.tmp-findings-initial.md
echo "✓ Cleaned up temporary findings file"
```

### Phase 2c: Convention Analysis (Agent Pass 2)

**Invoke codebase-archeologist agent in convention analysis mode:**

```bash
# Use Task tool to invoke agent
Task(
  subagent_type="codebase-archeologist",
  description="Analyze coding conventions and patterns",
  prompt="""
**Mode:** analyze_phase2

**Task:** Execute Phase 3 (Pattern Extraction)

**Instructions:**
1. Read corrections from: .claude/memory/.tmp-corrections-initial.md
2. Mine naming conventions (files, variables, functions)
3. Extract code organization patterns
4. Identify error handling conventions
5. Analyze API design patterns
6. Determine testing strategy
7. Write findings to: .claude/memory/.tmp-findings-conventions.md
8. Return confirmation with summary statistics

Follow MODE 2 workflow in your agent instructions.

**Incorporate User Corrections:**
- Apply all corrections from initial analysis
- Adjust analysis based on validated tech stack
- Focus pattern mining on validated architecture
"""
)
```

**Expected Output:**

- Agent creates `.claude/memory/.tmp-findings-conventions.md`
- Agent returns: "Convention analysis complete - ready for validation"

### Phase 2d: Checkpoint 2 Validation (Orchestrator Interaction)

**Read and validate convention findings:**

```bash
# Read findings file
FINDINGS_FILE=".claude/memory/.tmp-findings-conventions.md"

if [ ! -f "$FINDINGS_FILE" ]; then
  echo "ERROR: Convention findings file not found at $FINDINGS_FILE"
  exit 1
fi

# Display findings to orchestrator
cat "$FINDINGS_FILE"
```

**Present findings to user for validation:**

**Validation Questions:**

1. "Naming Conventions: Do the identified file/variable naming patterns match your standards?"
2. "Code Organization: Is the detected code organization pattern accurate?"
3. "Error Handling: Does the identified error handling approach match your practices?"
4. "API Design: Are the identified API design patterns correct?"
5. "Testing Strategy: Does the detected testing strategy match reality?"
6. "Pattern Conformance: Do the conformance percentages seem accurate?"
7. "Corrections Needed: Any other inaccuracies in the pattern analysis?"

**Write corrections file:**

```bash
cat > .claude/memory/.tmp-corrections-conventions.md <<EOF
# Corrections for Convention Analysis
# AUTO-DELETE after artifacts generated
# Created: $(date +%Y-%m-%d)

## User Corrections

### Naming Conventions
{User's corrections to naming patterns if any}

### Code Organization
{User's corrections to organization patterns if any}

### Error Handling
{User's corrections to error handling if any}

### API Design
{User's corrections to API patterns if any}

### Testing Strategy
{User's corrections to testing approach if any}

### Pattern Conformance
{User's corrections to conformance percentages if any}

### Additional Notes
{Any other corrections or clarifications from user}

## Validation Status
- Convention analysis validated: {YES/NO}
- Corrections provided: {YES/NO}
- Ready for next phase: {YES}
EOF

echo "✓ Corrections written to .claude/memory/.tmp-corrections-conventions.md"
```

**Cleanup Phase 2c artifacts:**

```bash
# Delete convention findings file (no longer needed)
rm .claude/memory/.tmp-findings-conventions.md
echo "✓ Cleaned up temporary findings file"
```

### Phase 2e: Final Analysis (Agent Pass 3)

**Invoke codebase-archeologist agent in final analysis mode:**

```bash
# Use Task tool to invoke agent
Task(
  subagent_type="codebase-archeologist",
  description="Complete feature inventory and ADR generation",
  prompt="""
**Mode:** analyze_phase3

**Task:** Execute Phase 4 (Feature Inventory) and Phase 5 (ADR Inference)

**Instructions:**
1. Read corrections from: .claude/memory/.tmp-corrections-conventions.md
2. Map backend endpoints to features
3. Map frontend routes to features
4. Cross-reference with database schema
5. Assess feature completeness
6. Generate Architecture Decision Records with evidence
7. Assign confidence levels to all ADRs
8. Write findings to: .claude/memory/.tmp-findings-final.md
9. Return confirmation with summary statistics

Follow MODE 3 workflow in your agent instructions.

**Incorporate All Previous Corrections:**
- Apply corrections from initial analysis
- Apply corrections from convention analysis
- Ensure consistency across all analysis phases
"""
)
```

**Expected Output:**

- Agent creates `.claude/memory/.tmp-findings-final.md`
- Agent returns: "Final analysis complete - ready for validation"

### Phase 2f: Checkpoint 3 Validation (Orchestrator Interaction)

**Read and validate final findings:**

```bash
# Read findings file
FINDINGS_FILE=".claude/memory/.tmp-findings-final.md"

if [ ! -f "$FINDINGS_FILE" ]; then
  echo "ERROR: Final findings file not found at $FINDINGS_FILE"
  exit 1
fi

# Display findings to orchestrator
cat "$FINDINGS_FILE"
```

**Present findings to user for validation:**

**Validation Questions:**

1. "Feature Inventory: Are all identified features accurate and complete?"
2. "Feature Completeness: Do the completeness percentages (frontend+backend+tests) match reality?"
3. "Architecture Decisions: Do the inferred ADRs accurately reflect actual decisions made?"
4. "ADR Confidence Levels: Are the confidence levels (High/Medium/Low) appropriate?"
5. "Missing Features: Are there any features not identified that should be included?"
6. "Corrections Needed: Any other inaccuracies in the final analysis?"

**Write corrections file:**

```bash
cat > .claude/memory/.tmp-corrections-final.md <<EOF
# Corrections for Final Analysis
# AUTO-DELETE after artifacts generated
# Created: $(date +%Y-%m-%d)

## User Corrections

### Feature Inventory
{User's corrections to feature list if any}

### Feature Completeness
{User's corrections to completeness assessments if any}

### Architecture Decisions
{User's corrections to ADRs if any}

### Confidence Levels
{User's corrections to confidence assessments if any}

### Missing Features
{Any features user wants to add}

### Additional Notes
{Any other corrections or clarifications from user}

## Validation Status
- Final analysis validated: {YES/NO}
- Corrections provided: {YES/NO}
- Ready for artifact generation: {YES}
EOF

echo "✓ Corrections written to .claude/memory/.tmp-corrections-final.md"
```

**Cleanup Phase 2e artifacts:**

```bash
# Delete final findings file (no longer needed)
rm .claude/memory/.tmp-findings-final.md
echo "✓ Cleaned up temporary findings file"
```

### Phase 2g: Artifact Generation (Agent Pass 4)

**Invoke codebase-archeologist agent in artifact generation mode:**

```bash
# Use Task tool to invoke agent
Task(
  subagent_type="codebase-archeologist",
  description="Generate final memory artifacts",
  prompt="""
**Mode:** generate_artifacts

**Task:** Generate 5 memory artifacts incorporating all user corrections

**Instructions:**
1. Read ALL correction files:
   - .claude/memory/.tmp-corrections-initial.md
   - .claude/memory/.tmp-corrections-conventions.md
   - .claude/memory/.tmp-corrections-final.md
2. Generate 5 memory artifacts in .claude/memory/:
   - project-context.md
   - tech-stack-baseline.md
   - coding-conventions.md
   - architecture-decisions.md
   - feature-inventory.md
3. Incorporate ALL user corrections from all 3 checkpoints
4. Return confirmation with artifact summary

Follow MODE 4 workflow in your agent instructions.

**Quality Requirements:**
- All user corrections applied
- All claims cite source files (file:line)
- All inferences have confidence levels
- No placeholders or TODOs
- Cross-references between artifacts are valid
"""
)
```

**Expected Output:**

- Agent creates 5 final artifacts in `.claude/memory/`
- Agent returns: "Memory artifacts generated"

**Cleanup all temporary correction files:**

```bash
# Delete all correction files (no longer needed)
rm .claude/memory/.tmp-corrections-initial.md
rm .claude/memory/.tmp-corrections-conventions.md
rm .claude/memory/.tmp-corrections-final.md

echo "✓ Cleaned up all temporary correction files"
```

**Verify final artifacts:**

```bash
# Verify all 5 artifacts were created
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
  echo "✅ All 5 memory artifacts verified"
else
  echo "❌ $MISSING_COUNT artifact(s) missing"
  exit 1
fi
```

---

## Step 3: Analysis Progress Summary

The multi-phase workflow executes as follows:

**Phase 2a-2b: Initial Analysis + Checkpoint 1** (~10-15 minutes)

- Agent analyzes directory structure, config files, tech stack
- Agent writes findings to `.tmp-findings-initial.md`
- Orchestrator validates with user
- Orchestrator writes corrections to `.tmp-corrections-initial.md`
- Cleanup: Delete `.tmp-findings-initial.md`

**Phase 2c-2d: Convention Analysis + Checkpoint 2** (~15-20 minutes)

- Agent reads corrections from Checkpoint 1
- Agent mines naming conventions, patterns, error handling, API design, testing
- Agent writes findings to `.tmp-findings-conventions.md`
- Orchestrator validates with user
- Orchestrator writes corrections to `.tmp-corrections-conventions.md`
- Cleanup: Delete `.tmp-findings-conventions.md`

**Phase 2e-2f: Final Analysis + Checkpoint 3** (~15-20 minutes)

- Agent reads corrections from Checkpoints 1-2
- Agent maps features (endpoints, routes, database)
- Agent generates ADRs with confidence levels
- Agent writes findings to `.tmp-findings-final.md`
- Orchestrator validates with user
- Orchestrator writes corrections to `.tmp-corrections-final.md`
- Cleanup: Delete `.tmp-findings-final.md`

**Phase 2g: Artifact Generation** (~10-15 minutes)

- Agent reads ALL corrections from 3 checkpoints
- Agent generates 5 final memory artifacts
- Agent incorporates all user corrections
- Orchestrator verifies artifacts created
- Cleanup: Delete all 3 correction files

**Total Time**: 50-70 minutes for deep analysis with 3 validation checkpoints

**Temporary Files Lifecycle:**

- `.tmp-findings-initial.md` - Created Phase 2a, Deleted Phase 2b
- `.tmp-corrections-initial.md` - Created Phase 2b, Deleted Phase 2g
- `.tmp-findings-conventions.md` - Created Phase 2c, Deleted Phase 2d
- `.tmp-corrections-conventions.md` - Created Phase 2d, Deleted Phase 2g
- `.tmp-findings-final.md` - Created Phase 2e, Deleted Phase 2f
- `.tmp-corrections-final.md` - Created Phase 2f, Deleted Phase 2g

---

## Step 4: Validate Generated Artifacts

After Phase 2g completes, verify all artifacts exist and temporary files are cleaned up:

<validation_checklist>
**Artifact Verification**:
✅ File created: `.claude/memory/project-context.md`
✅ File created: `.claude/memory/tech-stack-baseline.md`
✅ File created: `.claude/memory/coding-conventions.md`
✅ File created: `.claude/memory/architecture-decisions.md`
✅ File created: `.claude/memory/feature-inventory.md`

**Content Validation**:
✅ All files have evidence citations (file:line format)
✅ All inferences have confidence levels
✅ No "TODO" or placeholder sections
✅ Cross-references between artifacts are valid
✅ No hallucinated features or technologies

**Cleanup Verification**:
✅ Temporary findings files deleted (`.tmp-findings-*.md`)
✅ Temporary corrections files deleted (`.tmp-corrections-*.md`)
✅ Only permanent artifacts remain in `.claude/memory/`
</validation_checklist>

Use Read tool to spot-check artifacts:

```bash
# Check for evidence citations
grep -c "According to" .claude/memory/*.md
grep -c "Evidence:" .claude/memory/*.md

# Check for confidence levels
grep -c "Confidence: High" .claude/memory/*.md
grep -c "Confidence: Medium" .claude/memory/*.md

# Check for placeholders
grep "TODO\|FIXME\|XXX" .claude/memory/*.md
```

If validation fails, request agent to revise specific sections.

---

## Step 5: Summary Report

Present comprehensive summary to user:

```markdown
## Memory Generation Complete: $PROJECT_NAME

**Analysis Duration**: {X minutes}
**Scope**: {Full codebase | Specific path}
**Depth**: {Deep | Medium | Quick}

### Generated Artifacts

1. **project-context.md** ({X KB})
   - Overview, architecture, tech stack summary
   - Coding conventions summary
   - Constraints and NFRs

2. **tech-stack-baseline.md** ({X KB})
   - {N} technologies documented
   - Rationale for each choice
   - Configuration details
   - Alternative technologies considered

3. **coding-conventions.md** ({X KB})
   - File naming: {Pattern} ({X}% conformance)
   - Code style: {Pattern} ({X}% conformance)
   - Error handling: {Pattern} ({X}% conformance)
   - API design: {Pattern}
   - Testing: {Strategy}

4. **architecture-decisions.md** ({X KB})
   - {N} ADRs generated
   - {X} High confidence, {X} Medium, {X} Low
   - Evidence cited for all decisions

5. **feature-inventory.md** ({X KB})
   - {N} features identified
   - {X}% fully complete (frontend + backend + tests)
   - {X}% partially complete
   - {X}% in early development

### Key Findings

**Architecture**: {Pattern detected}
**Dominant Language**: {Language} ({X}% of code)
**Testing Coverage**: {X}% (estimated from test files)
**Code Quality**: {High | Medium | Low} (based on linting, consistency)

**Consistency Score**: {X}% across naming, style, patterns

### Recommendations

{If low consistency:}
- Consider standardizing {specific inconsistency}
- Run `/mine-patterns` to identify dominant conventions

{If missing tests:}
- {X}% of features lack tests
- Consider implementing test coverage for critical paths

{If architectural drift:}
- Some modules don't follow {pattern}
- Consider refactoring {specific modules}

### Next Steps

**For New Feature Development**:
1. All agents will now load these memory artifacts automatically
2. New code will follow existing conventions
3. New features will integrate with existing architecture

**To Keep Memory Updated**:
- After major refactors: `/update-memory "architecture"`
- After dependency changes: `/update-memory "tech-stack"`
- After establishing new patterns: `/mine-patterns --type "{pattern}"`

**To Validate New Features**:
- Before implementation: `/validate-consistency "{feature}"`
- This checks if new feature aligns with conventions

### Files Ready for Use

All agents (Requirements Analyst, Tech Researcher, Implementation Planner, Senior Developer, Code Review Specialist) will now automatically reference:
- `project-context.md` for high-level context
- `tech-stack-baseline.md` for technology decisions
- `coding-conventions.md` for style and patterns
- `architecture-decisions.md` for architectural context
- `feature-inventory.md` to avoid duplicate features

**Memory Baseline Established**: ✅
```

</generation_orchestration>

<error_handling>

## Error Scenarios

**Issue: No code files found in scope**

```markdown
❌ Error: No source files found in scope "{SCOPE}"

**Possible causes**:
- Incorrect path specified
- Empty repository
- All code is gitignored

**Solution**:
- Check scope path: `/generate-memory --scope "src"`
- Verify code exists: `ls -R {SCOPE}`
```

**Issue: Insufficient permissions**

```markdown
❌ Error: Cannot write to .claude/memory/

**Solution**:
- Check directory permissions
- Create directory: `mkdir -p .claude/memory`
- Verify write access: `touch .claude/memory/test`
```

**Issue: Binary files only**

```markdown
⚠️ Warning: Only binary files detected, no source code

**Detected**: node_modules/, dist/, build/
**Missing**: src/, lib/, app/

**Solution**:
- Ensure you're in project root
- Check if source code is in subdirectory
- Specify correct scope: `/generate-memory --scope "packages/app/src"`
```

**Issue: User stops at checkpoint**

```markdown
**Checkpoint Interrupted**

**Progress Saved**:
- Phase 1-2 complete
- Partial artifacts generated

**To Resume**:
- Re-run `/generate-memory` (will detect partial artifacts)
- Or manually complete remaining phases
```

**Issue: Git history unavailable**

```markdown
⚠️ Warning: No git repository detected

**Impact**:
- Cannot generate ADR timeline
- Cannot attribute technology adoption to commits

**Workaround**:
- ADRs will be generated without dates
- Technology choices inferred from current state only
- Confidence levels may be lower
```

</error_handling>

<best_practices>

## Command Usage Best Practices

### First-Time Analysis

```bash
# Full deep analysis (recommended for comprehensive baseline)
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

# Or full monorepo (slower but comprehensive)
/generate-memory
```

### After Major Changes

```bash
# Regenerate specific aspects
/update-memory "tech-stack"  # After adding dependencies
/update-memory "conventions"  # After style changes
/update-memory "architecture"  # After refactoring
```

</best_practices>

---

Generate memory artifacts from codebase in scope: **$SCOPE**

Begin by detecting codebase structure and invoking codebase-archeologist agent.
