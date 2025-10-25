---
allowed-tools: Bash(code-tools:*), Read, Grep, Glob, Write, Edit, WebFetch, mcp__sequential-thinking__sequentialthinking
argument-hint: [vague prompt to enhance]
description: Transform vague prompts into advanced prompt-engineered versions (multi-pattern optimizer)
---

# Multi-Pattern Prompt Optimizer

Transform user prompts using layered technique combinations, semantic intent detection, and quality validation.

## User's Prompt

$ARGUMENTS

## CRITICAL: Load Supporting Data First

Before analysis, read these files (try local first, fallback to home):

1. `Read .claude/promptengineering/intent-taxonomy.json` (or `~/.claude/promptengineering/`)
2. `Read .claude/promptengineering/pattern-layering.json` (or `~/.claude/promptengineering/`)
3. `Read .claude/promptengineering/combination-templates.json` (or `~/.claude/promptengineering/`)
4. `Read .claude/promptengineering/patterns.json` (or `~/.claude/promptengineering/`)

If files missing, generate error with installation instructions.

## Optimization Flow

### Step 1: Intent Taxonomy Detection

**Goal Classification:**

- CREATE: Build new functionality/features
- DEBUG: Fix bugs, troubleshoot issues
- OPTIMIZE: Improve performance, efficiency, quality
- DESIGN: Architecture, planning, structure
- ANALYZE: Understand, investigate, explain
- MIGRATE: Refactor, modernize, port
- VALIDATE: Test, verify, audit, review
- DOCUMENT: Explain, write guides, API docs

**Quality Requirements Detection:**

- CORRECTNESS: "critical", "production", "reliable", "robust"
- PERFORMANCE: "fast", "optimize", "bottleneck", "latency"
- SECURITY: "secure", "audit", "vulnerable", "exploit"
- MAINTAINABILITY: "clean", "readable", "modular", "scalable"
- COMPLETENESS: "comprehensive", "thorough", "all cases", "edge cases"

**Output Type:**

- CODE: Implementation files
- ARCHITECTURE: Design docs, diagrams
- TESTS: Test suites, validation
- DOCUMENTATION: Guides, explanations
- CONFIGURATION: Setup, deployment scripts
- ANALYSIS: Reports, findings

### Step 2: Multi-Pattern Selection

Use loaded `intent-taxonomy.json` and `patterns.json` data.

**Selection Strategy:**

1. **Foundation Pattern** (choose 1):
   - Maps directly to primary goal
   - CREATE → ReAct (13) or Task Decomposition (12)
   - DEBUG → Chain of Thought (1) + Chain of Verification (2)
   - OPTIMIZE → Chain of Thought (1) + Self-Consistency (4)
   - DESIGN → Multi-Objective Directional (5) or Role-Based (7)
   - ANALYZE → Chain of Thought (1)
   - VALIDATE → Chain of Verification (2)

2. **Enhancement Patterns** (choose 0-2):
   - Quality requirements → additional techniques
   - CORRECTNESS → Chain of Verification (2)
   - PERFORMANCE → Self-Consistency (4) for approach comparison
   - SECURITY → Chain of Verification (2) + Role-Based (7, security expert)
   - MAINTAINABILITY → Chain of Draft (6) for refinement
   - COMPLETENESS → Recursive Self-Improvement (11)

3. **Formatter Pattern** (choose 0-1):
   - Chain of Command (3) if multi-stage workflow needed
   - Agile/Scrum (14) if team/sprint context
   - Iterative Refinement (10) if convergence needed

**Compatibility Rules:**

- Max 3 patterns total (1 foundation + 2 enhancements/formatters)
- Check canCombineWith for compatibility
- Priority: Foundation > Quality requirements > Formatter

### Step 3: Complexity Detection

Analyze user prompt for complexity level:

- **basic**: Simple, single-file, "fix this bug"
- **intermediate**: Multi-file, "implement feature X"
- **advanced**: Architecture, "design system for Y"
- **expert**: Migration, "refactor entire Z to use W"

Use complexity to select pattern level from patterns.json.

### Step 4: Semantic Intent Extraction

Beyond keywords, detect:

- Multiple concurrent goals (e.g., "debug AND document")
- Implicit constraints (e.g., "production" implies CORRECTNESS)
- Stakeholder context (e.g., "team review" implies Chain of Command)
- Uncertainty signals (e.g., "not sure how" triggers Active Prompting)

### Step 5: Layered Prompt Construction

First check `combination-templates.json` for pre-built template match. If match found, use that template. Otherwise, build from scratch:

**Layer 1: Foundation (from primary pattern template)**

```
{foundation_template}
```

**Layer 2: Enhancement Integration**
Use `pattern-layering.json` integration points. For each enhancement pattern, inject:

- Verification steps (if CoVe)
- Reflection cycles (if Reflexion)
- Multiple approaches (if Self-Consistency)
- Role context (if Role-Based)

**Layer 3: Output Formatting**
Add structured output requirements:

```
## Success Criteria
- [ ] {criterion_1}
- [ ] {criterion_2}

## Output Format
{specific_structure}

## Constraints
- {constraint_1}
- {constraint_2}
```

### Step 6: Quality Validation (Chain of Verification)

**Verification Checklist:**

- [ ] Removed vague terms (good, better, optimize without metrics)
- [ ] Defined measurable success criteria
- [ ] Specified output format/structure
- [ ] Included validation/verification steps
- [ ] Added edge case considerations
- [ ] Used imperative verbs (analyze, generate, verify)
- [ ] Set clear constraints (scope, length, format)

**If any item fails → revise enhanced prompt**

### Step 7: Self-Critique & Alternatives

**Critique enhanced prompt:**

- Potential weaknesses?
- Missing context?
- Ambiguities remaining?

**Generate alternative pattern combination** (if primary score <80%):

- Different foundation technique
- Same validation criteria
- Compare which is clearer/more actionable

### Step 8: Present Results

## ANALYSIS SUMMARY

**Detected Intents:**

- Goal: {CREATE/DEBUG/OPTIMIZE/etc}
- Quality needs: {CORRECTNESS/PERFORMANCE/etc}
- Output type: {CODE/ARCHITECTURE/etc}

**Selected Patterns:**

- Foundation: {technique_name} (ID {id}) - {complexity} level
- Enhancement 1: {technique_name} (ID {id}) - {reason}
- Enhancement 2: {technique_name} (ID {id}) - {reason}
- Formatter: {technique_name} (ID {id}) - {reason}

**Pattern Compatibility:**

- Foundation canCombineWith: {ids}
- All selected patterns compatible: {yes/no}
- Combination rationale: {why these work together}

**Quality Score:** {0-100}% match confidence

---

## ENHANCED PROMPT

```
{full_layered_prompt_with_all_patterns_integrated}
```

---

## VALIDATION RESULTS

**Checklist:**

- [x/blank] Removed vague terms
- [x/blank] Defined success criteria
- [x/blank] Specified output format
- [x/blank] Included verification steps
- [x/blank] Edge cases addressed
- [x/blank] Imperative verbs used
- [x/blank] Clear constraints

**Weaknesses Identified:**

- {weakness_1}
- {weakness_2}

**Revisions Made:**

- {revision_1}
- {revision_2}

---

## ALTERNATIVE PATTERN COMBINATION

*Only if primary score <80%*

**Alternative:** {different_foundation} + {different_enhancements}
**Comparison:** {why primary is better OR recommend alternative}

---

## IMPROVEMENT SUMMARY

This enhanced prompt provides:

- {benefit_1: e.g., multi-stage reasoning with verification}
- {benefit_2: e.g., layered quality checks at each step}
- {benefit_3: e.g., structured output with measurable criteria}
- {benefit_4: e.g., explicit pattern techniques for AI to follow}

## FINALLY

Ask the user the following questions in an interactive way:

<questions>
  <question>Run this enhanced prompt now?</question>
  <question>Save to file? (if yes, ask for path)</question>
  <question>Show alternative pattern combination?</question>
  <question>Explain specific pattern integration?</question>
</questions>
