---
allowed-tools: Bash(code-tools:*), Read
argument-hint: [feature-slug]
description: Validate new feature plan against existing codebase conventions and architectural decisions using systematic comparison
---

# Consistency Validation Command

**System date assertion**: 2025-10-23
**Feature slug**: $1

Act as a product manager and scope management specialist with deep expertise in maintaining codebase consistency, enforcing architectural decisions, and preventing technical debt accumulation.

## Objective

Perform systematic validation of a new feature's implementation plan against existing codebase conventions, architectural decisions, and technology baseline to identify deviations before implementation begins. This is a critical quality gate that prevents drift and maintains codebase coherence.

## Methodology

### Phase 1: Context Retrieval

Load all baseline memory artifacts and feature plan:

```bash
# Load codebase baseline artifacts
code-tools read_file --path .claude/memory/coding-conventions.md
code-tools read_file --path .claude/memory/architecture-decisions.md
code-tools read_file --path .claude/memory/tech-stack-baseline.md

# Load feature-specific artifacts
code-tools read_file --path .claude/memory/implementation-plan-$1.md
code-tools read_file --path .claude/memory/requirements-$1.md
code-tools read_file --path .claude/memory/tech-analysis-$1.md

# Search for related features to check cross-feature consistency
code-tools search_memory --dir .claude/memory --query "$1 related features patterns" --topk 5
```

### Phase 2: Chain-of-Thought Comparison Reasoning

Before performing validation, reason through the comparison strategy:

```xml
<comparison_reasoning>
<baseline_understanding>
**Coding Conventions Summary**:
- {List 5-7 key conventions from coding-conventions.md}
- {Pattern}: {Dominance %} conformance
- {Exception cases}: {When deviations are acceptable}

**Architecture Decisions**:
- {Decision}: {Rationale} (ADR-001)
- {Decision}: {Rationale} (ADR-002)
- {Critical constraints}: {Non-negotiable patterns}

**Tech Stack Baseline**:
- {Framework/Library}: {Version} - {Usage pattern}
- {Approved dependencies}: {List with versions}
- {Prohibited dependencies}: {Why forbidden}
</baseline_understanding>

<feature_plan_analysis>
**Feature Components**:
- {Component}: {Technology choice} - {Implementation approach}
- {New dependencies introduced}: {List with justification}

**Deviation Candidates**:
- {Potential deviation 1}: {Why it might violate convention}
- {Potential deviation 2}: {Why it might violate ADR}

**Alignment Strengths**:
- {Aspect}: {How it aligns with baseline}
</feature_plan_analysis>

<validation_strategy>
**Comparison Dimensions**:
1. **File Naming & Structure**: Compare against conventions
2. **Architectural Patterns**: Validate against ADRs
3. **Technology Choices**: Check against tech-stack-baseline
4. **Error Handling**: Verify dominant pattern usage
5. **Testing Strategy**: Check test pyramid compliance
6. **API Design**: Validate against REST/GraphQL conventions
7. **State Management**: Check against established patterns
8. **Dependencies**: Verify no prohibited libraries

**Severity Classification Logic**:
- **CRITICAL**: Violates architectural decision OR uses prohibited technology
- **WARNING**: Deviates from convention with >80% conformance
- **INFO**: Minor deviation from convention with <80% conformance
- **COMPLIANT**: Matches established patterns
</validation_strategy>
</comparison_reasoning>
```

### Phase 3: Systematic Validation

Perform systematic comparison across all dimensions:

#### 3.1 File Naming & Directory Structure

**Validation Questions**:

- Does file naming match dominant pattern (camelCase, kebab-case, PascalCase)?
- Does directory structure follow feature-based or layer-based organization?
- Are files placed in correct directories per convention?
- Do new directories follow established hierarchy?

**Evidence Collection**:

```bash
# Extract file paths from implementation plan
grep -E "files_affected|file.*path" .claude/memory/implementation-plan-$1.md

# Compare against convention patterns
grep -E "file.*naming|directory.*structure" .claude/memory/coding-conventions.md
```

#### 3.2 Architectural Pattern Compliance

**Validation Questions**:

- Do planned components follow established architectural layers?
- Are separation of concerns principles maintained?
- Does data flow match architectural diagrams?
- Are integration patterns consistent with ADRs?
- Do new patterns contradict existing decisions?

**Evidence Collection**:

```bash
# Extract architectural patterns from plan
grep -E "architecture|layer|pattern|design" .claude/memory/implementation-plan-$1.md

# Compare against ADRs
grep -E "ADR-|decision|pattern" .claude/memory/architecture-decisions.md
```

#### 3.3 Technology & Dependency Validation

**Validation Questions**:

- Are all libraries in tech-stack-baseline approved list?
- Are new dependencies justified and vetted?
- Do version constraints match baseline?
- Are prohibited dependencies avoided?
- Does technology choice align with stack strategy?

**Evidence Collection**:

```bash
# Extract dependencies from tech analysis
grep -E "dependency|library|framework|package" .claude/memory/tech-analysis-$1.md

# Compare against baseline
grep -E "approved|prohibited|dependency" .claude/memory/tech-stack-baseline.md
```

#### 3.4 Error Handling Pattern Validation

**Validation Questions**:

- Does error handling use dominant pattern (throw vs return, toast vs log)?
- Are error types consistent with convention?
- Is error propagation strategy aligned?
- Are error messages following template?

**Evidence Collection**:

```bash
# Extract error handling from plan
grep -E "error.*handl|exception|catch|throw" .claude/memory/implementation-plan-$1.md

# Compare against convention
grep -E "error.*pattern|exception.*handling" .claude/memory/coding-conventions.md
```

#### 3.5 Testing Strategy Validation

**Validation Questions**:

- Does testing match pyramid (unit > integration > E2E)?
- Are test locations following convention?
- Is coverage target met (per convention)?
- Are test naming patterns consistent?

**Evidence Collection**:

```bash
# Extract testing strategy
grep -E "test|coverage|unit|integration|e2e" .claude/memory/implementation-plan-$1.md

# Compare against convention
grep -E "test.*strategy|coverage|pyramid" .claude/memory/coding-conventions.md
```

#### 3.6 API Design Validation

**Validation Questions**:

- Do endpoints follow RESTful conventions?
- Is versioning strategy consistent?
- Are authentication/authorization patterns aligned?
- Do response formats match standard?

**Evidence Collection**:

```bash
# Extract API design
grep -E "endpoint|route|api|rest|graphql" .claude/memory/implementation-plan-$1.md

# Compare against convention
grep -E "api.*design|endpoint.*pattern|rest" .claude/memory/coding-conventions.md
```

#### 3.7 State Management Validation

**Validation Questions**:

- Does state management use established library?
- Are state patterns consistent with convention?
- Is global vs local state decision aligned?
- Do data flow patterns match architecture?

**Evidence Collection**:

```bash
# Extract state management
grep -E "state|redux|context|store" .claude/memory/implementation-plan-$1.md

# Compare against convention
grep -E "state.*management|store|context" .claude/memory/coding-conventions.md
```

### Phase 4: Chain-of-Verification

Validate findings before finalizing report:

```xml
<verification_checklist>
<question>Did I identify ALL deviations or only surface-level ones?</question>
<check>Re-scan plan for subtle inconsistencies</check>

<question>Are severity classifications justified by evidence?</question>
<check>Verify each CRITICAL has ADR violation or prohibited tech</check>
<check>Verify each WARNING has >80% conformance data</check>

<question>Are false positives excluded?</question>
<check>Acceptable deviations (justified in plan) marked INFO not WARNING</check>

<question>Is evidence cited with file:line or section references?</question>
<check>Each issue has traceable evidence</check>

<question>Are recommendations actionable and specific?</question>
<check>Not "fix error handling" but "replace throw with toast pattern (see coding-conventions.md:45)"</check>

<question>Is overall score calculated correctly?</question>
<check>Score = 100 - (CRITICAL × 10 + WARNING × 5 + INFO × 1)</check>

<question>Did I check for cross-feature consistency?</question>
<check>Compare against similar features in memory search results</check>

<question>Are there hidden assumptions in my validation?</question>
<check>State any assumed convention interpretations</check>

<question>Could any WARNING be a justified evolution of convention?</question>
<check>Note if deviation might be intentional improvement</check>

<question>Is the merge recommendation clear and justified?</question>
<check>CRITICAL → must fix before implementation</check>
<check>WARNING → should fix (or justify deviation)</check>
<check>INFO → optional consideration</check>
</verification_checklist>
```

### Phase 5: Report Generation

Create comprehensive consistency validation report:

```xml
<consistency_report>
<metadata>
  <feature_slug>{feature}</feature_slug>
  <validation_date>2025-10-23</validation_date>
  <artifacts_validated>
    <artifact>implementation-plan-{feature}.md</artifact>
    <artifact>requirements-{feature}.md</artifact>
    <artifact>tech-analysis-{feature}.md</artifact>
  </artifacts_validated>
  <baseline_artifacts>
    <artifact>coding-conventions.md</artifact>
    <artifact>architecture-decisions.md</artifact>
    <artifact>tech-stack-baseline.md</artifact>
  </baseline_artifacts>
</metadata>

<validation_summary>
  <overall_score>{0-100}</overall_score>
  <status>PASS|PASS_WITH_WARNINGS|FAIL</status>
  <critical_count>{number}</critical_count>
  <warning_count>{number}</warning_count>
  <info_count>{number}</info_count>
  <compliant_count>{number}</compliant_count>
</validation_summary>

<critical_issues>
  <issue id="CRIT-001">
    <dimension>Architectural Pattern | Technology | {Category}</dimension>
    <title>{Concise issue title}</title>
    <description>
      {Detailed description of violation}
    </description>
    <evidence>
      <plan_reference>implementation-plan-{feature}.md:{section or line}</plan_reference>
      <baseline_reference>architecture-decisions.md:{ADR-XXX or line}</baseline_reference>
      <conflict>
        Plan says: "{Excerpt from plan}"
        Baseline requires: "{Excerpt from baseline}"
      </conflict>
    </evidence>
    <impact>
      {Why this is critical - technical debt, security, maintainability}
    </impact>
    <recommendation>
      {Specific, actionable fix}
    </recommendation>
  </issue>
</critical_issues>

<warnings>
  <warning id="WARN-001">
    <dimension>{Category}</dimension>
    <title>{Concise warning title}</title>
    <description>
      {Detailed description of deviation}
    </description>
    <evidence>
      <plan_reference>implementation-plan-{feature}.md:{section}</plan_reference>
      <convention_reference>coding-conventions.md:{section}</convention_reference>
      <conformance_data>
        Dominant pattern: {Pattern} ({X}% of codebase)
        Plan uses: {Different pattern}
      </conformance_data>
    </evidence>
    <impact>
      {Why this matters - consistency, readability, onboarding}
    </impact>
    <recommendation>
      {Specific fix OR justification for deviation}
    </recommendation>
  </warning>
</warnings>

<informational>
  <info id="INFO-001">
    <dimension>{Category}</dimension>
    <title>{Concise info title}</title>
    <description>
      {Minor deviation or consideration}
    </description>
    <evidence>
      <plan_reference>{Reference}</plan_reference>
      <note>{Why this is informational only}</note>
    </evidence>
    <suggestion>
      {Optional improvement suggestion}
    </suggestion>
  </info>
</informational>

<compliant_areas>
  <compliant dimension="File Structure">
    ✅ All files follow feature-based organization (coding-conventions.md:12)
  </compliant>
  <compliant dimension="API Design">
    ✅ Endpoints follow /api/v1/{resource} pattern (coding-conventions.md:67)
  </compliant>
  <compliant dimension="TypeScript">
    ✅ Strict mode enabled, all types defined (tech-stack-baseline.md:34)
  </compliant>
  <!-- List 5-10 compliant areas -->
</compliant_areas>

<cross_feature_analysis>
  <similar_features>
    <feature>{Related feature 1}</feature>
    <consistency_note>
      {How current plan compares to this feature's implementation}
    </consistency_note>
  </similar_features>
</cross_feature_analysis>

<scoring_breakdown>
  <calculation>
    Base score: 100
    Critical deductions: -{critical_count × 10} = {total}
    Warning deductions: -{warning_count × 5} = {total}
    Info deductions: -{info_count × 1} = {total}
    Final score: {overall_score}/100
  </calculation>
  <interpretation>
    90-100: Excellent consistency, proceed with implementation
    80-89: Good consistency, address warnings before implementation
    70-79: Moderate consistency, must fix critical issues
    0-69: Poor consistency, significant rework required
  </interpretation>
</scoring_breakdown>

<recommendations>
  <immediate_actions>
    {List critical items that must be fixed}
  </immediate_actions>
  <before_implementation>
    {List warnings that should be addressed}
  </before_implementation>
  <future_considerations>
    {List info items and evolution suggestions}
  </future_considerations>
  <merge_decision>
    APPROVE | REQUEST_CHANGES | BLOCK
    {Justification based on score and critical count}
  </merge_decision>
</recommendations>

<validation_notes>
  <assumptions>
    {Any assumptions made during validation}
  </assumptions>
  <edge_cases>
    {Any special cases or exceptions noted}
  </edge_cases>
  <convention_evolution>
    {Any suggestions for updating conventions based on this validation}
  </convention_evolution>
</validation_notes>
</consistency_report>
```

**Write report to memory**:

```bash
code-tools create_file \
  --file .claude/memory/consistency-report-$1.md \
  --content @- \
  --add-last-line-newline <<EOF
# Consistency Validation Report: {feature}

{Render consistency_report XML as markdown}
EOF
```

## Anti-Hallucination Safeguards

**Evidence-Based Validation**: Every issue MUST cite specific file:line references from both plan and baseline. No generic claims.

**Conformance Data Required**: Warnings require quantitative conformance data (e.g., "80% of codebase uses pattern X"). Do NOT claim dominance without evidence.

**"According to..." Prompting**: When stating conventions, use: "According to coding-conventions.md:{line}, the dominant pattern is {pattern}".

**No Invented Conventions**: If convention is not documented in baseline artifacts, mark as INFO with note "No established convention found - comparing to similar features".

**Severity Justification**: Each CRITICAL must reference specific ADR or prohibited technology list. Each WARNING must have >80% conformance data.

## Error Handling

**Missing Baseline Artifacts**:

```
If coding-conventions.md not found:
  - Cannot perform validation without baseline
  - Recommend: /generate-memory first
  - Exit with error message

If architecture-decisions.md not found:
  - Mark architectural validations as INFO only
  - Note: "No ADRs found, architectural validation limited"

If tech-stack-baseline.md not found:
  - Mark tech validations as INFO only
  - Note: "No tech baseline, dependency validation limited"
```

**Missing Feature Artifacts**:

```
If implementation-plan-{feature}.md not found:
  - Cannot validate without plan
  - Recommend: /plan-implementation {feature} first
  - Exit with error message
```

**Empty or Malformed Artifacts**:

```
If artifact exists but is empty or unparseable:
  - Report artifact issue
  - Attempt validation with available data
  - Note limitation in validation_notes
```

## Validation Checklist

Before finalizing report, verify:

- [ ] All baseline artifacts loaded successfully
- [ ] All feature artifacts loaded successfully
- [ ] Each CRITICAL has ADR/prohibited-tech reference
- [ ] Each WARNING has conformance percentage
- [ ] Each issue has plan_reference and baseline_reference
- [ ] Overall score calculation is correct
- [ ] Merge decision matches score interpretation
- [ ] No hallucinated conventions (all cited from artifacts)
- [ ] Cross-feature consistency checked
- [ ] Assumptions stated explicitly
- [ ] Report written to .claude/memory/consistency-report-{feature}.md

## Best Practices

1. **Be Evidence-Based**: Never claim "convention is X" without citing source
2. **Quantify Deviations**: Use conformance percentages, not subjective terms
3. **Distinguish Convention from Preference**: Only enforce documented conventions
4. **Suggest Convention Evolution**: If plan introduces better pattern, note it
5. **Provide Actionable Recommendations**: Not "fix error handling" but "replace lines X-Y with toast pattern"
6. **Cross-Reference Similar Features**: Learn from past implementations
7. **Balance Consistency with Innovation**: Don't block justified improvements
8. **Document Assumptions**: State interpretation when conventions are ambiguous

## Output

Generate markdown-formatted consistency report in `.claude/memory/consistency-report-{feature}.md` with:

- Overall score (0-100) and status (PASS/PASS_WITH_WARNINGS/FAIL)
- Critical issues (MUST fix before implementation)
- Warnings (SHOULD fix or justify)
- Informational notes (CONSIDER)
- Compliant areas (positive reinforcement)
- Actionable recommendations
- Merge decision (APPROVE/REQUEST_CHANGES/BLOCK)

**Success**: Feature plan validated against codebase baseline with evidence-based consistency report generated.
