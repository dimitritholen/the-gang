---
allowed-tools: Task, Read, Bash, Glob, Grep
argument-hint: [--scope path] [--focus aspect] [--depth level]
description: Generate memory artifacts from existing codebase
---

<instructions>
You are orchestrating **codebase memory generation** to reverse-engineer an existing codebase and create comprehensive memory artifacts for future development.

Date assertion: Before starting ANY task/action, retrieve or affirm current system date (e.g., "System date: YYYY-MM-DD") to ground time-sensitive reasoning.

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

## Step 2: Invoke Codebase Archeologist

Use Task tool to invoke codebase-archeologist subagent:

<agent_prompt_template>
You are analyzing an existing codebase to generate memory artifacts for future development.

**Scope**: $SCOPE
**Focus**: $FOCUS
**Depth**: $DEPTH

**Context**:
{Paste scope detection results}

**Your Task**:

Execute the 5-phase analysis framework:

### Phase 1: Discovery (Step-Back)
- Detect project type, tech stack, architecture
- **Checkpoint 1**: Present findings, ask user to validate

### Phase 2: Technology Analysis (CoT)
- Analyze why each technology was chosen
- Document how each is used
- Identify configuration and patterns

### Phase 3: Pattern Extraction (Systematic)
- Mine naming conventions (files, variables, functions)
- Extract code organization patterns
- Identify error handling conventions
- Analyze API design patterns
- Determine testing strategy
- **Checkpoint 2**: Present patterns, ask user to validate

### Phase 4: Feature Inventory
- Map backend endpoints to features
- Map frontend routes to features
- Cross-reference with database schema
- Assess feature completeness
- Infer non-functional requirements

### Phase 5: ADR Inference
- Generate Architecture Decision Records
- Assign confidence levels (High/Medium/Low)
- Cite evidence for each decision
- **Checkpoint 3**: Present ADRs, ask user final validation

**Output**:

Generate 5 memory artifacts in `.claude/memory/`:
1. `project-context.md` - High-level overview
2. `tech-stack-baseline.md` - Technologies with rationale
3. `coding-conventions.md` - Patterns for future code
4. `architecture-decisions.md` - ADRs with confidence levels
5. `feature-inventory.md` - Complete feature list

**Quality Gates**:
- All claims cite source files (file:line)
- All inferences have confidence levels
- No invented features or patterns
- Contradictions flagged, not hidden
- "Unknown" used instead of guessing

**Anti-Hallucination**:
- Use "According to {file}..." for all factual claims
- Use "Inferred from {pattern analysis}..." for inferences
- Run CoVe validation before finalizing
- Flag uncertainties explicitly

**Hybrid Interaction**:
- Present 3 checkpoints for user validation
- Incorporate user corrections at each checkpoint
- Ask clarifying questions when evidence is ambiguous

Proceed with systematic codebase archaeology.
</agent_prompt_template>

---

## Step 3: Monitor Analysis Progress

The codebase-archeologist agent will:

### Phase 1: Discovery (~5-10 minutes)
- Scan directory structure
- Parse configuration files
- Detect tech stack
- **Checkpoint 1: User validates tech stack**

### Phase 2: Technology Analysis (~10-15 minutes)
- Analyze dependencies
- Infer technology choices
- Document usage patterns

### Phase 3: Pattern Extraction (~15-20 minutes)
- Mine 500+ code samples
- Extract conventions
- Identify dominant patterns
- **Checkpoint 2: User validates patterns**

### Phase 4: Feature Inventory (~10-15 minutes)
- Map endpoints and routes
- Cross-reference features
- Assess completeness

### Phase 5: ADR Inference (~10-15 minutes)
- Generate ADRs with evidence
- Assign confidence levels
- **Checkpoint 3: User final validation**

**Total Time**: 50-75 minutes for deep analysis

---

## Step 4: Validate Generated Artifacts

After agent completes, verify all artifacts exist and are complete:

<validation_checklist>
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
