---
allowed-tools: Bash(code-tools:*), Read, Grep
argument-hint: [feature-slug]
description: Validate new feature plan against existing codebase conventions and architectural decisions using systematic comparison with Chain of Verification
---

# Consistency Validation Command

**System date assertion**: Retrieve current system date before proceeding
**Feature slug**: $1

Act as a product manager and scope management specialist with deep expertise in maintaining codebase consistency, enforcing architectural decisions, and preventing technical debt accumulation.

## Objective

Perform systematic validation of a new feature's implementation plan against existing codebase conventions, architectural decisions, and technology baseline to identify deviations before implementation begins. Use Chain of Verification to ensure validation accuracy and eliminate false positives/negatives.

## Methodology with Chain of Verification

### Phase 1: Context Retrieval and Decomposition

**Task 1.1: Load baseline artifacts**

```bash
# Load codebase baseline artifacts
code-tools read_file --path .claude/memory/coding-conventions.md
code-tools read_file --path .claude/memory/architecture-decisions.md
code-tools read_file --path .claude/memory/tech-stack-baseline.md
```

**Task 1.2: Load feature-specific artifacts**

```bash
# Load feature-specific artifacts
code-tools read_file --path .claude/memory/implementation-plan-$1.md
code-tools read_file --path .claude/memory/requirements-$1.md
code-tools read_file --path .claude/memory/tech-analysis-$1.md

# Search for related features to check cross-feature consistency
code-tools search_memory --dir .claude/memory --query "$1 related features patterns" --topk 5
```

### Phase 2: Initial Validation - Generate Comparison Analysis

**Sub-task 2.1: Baseline understanding extraction**

```xml
<baseline_understanding>
**Coding Conventions Summary**:
- {Extract 5-7 key conventions from coding-conventions.md with line references}
- {Pattern}: {Dominance %} conformance (cite evidence)
- {Exception cases}: {When deviations are acceptable}

**Architecture Decisions**:
- {Decision}: {Rationale} (ADR-XXX with file:line reference)
- {Decision}: {Rationale} (ADR-XXX with file:line reference)
- {Critical constraints}: {Non-negotiable patterns}

**Tech Stack Baseline**:
- {Framework/Library}: {Version} - {Usage pattern with reference}
- {Approved dependencies}: {List with versions and references}
- {Prohibited dependencies}: {Why forbidden with reference}
</baseline_understanding>
```

**Sub-task 2.2: Feature plan analysis**

```xml
<feature_plan_analysis>
**Feature Components**:
- {Component}: {Technology choice} - {Implementation approach}
- {New dependencies introduced}: {List with justification}

**Potential Deviation Candidates**:
- {Deviation 1}: {Why it might violate convention} [reference: plan:line X]
- {Deviation 2}: {Why it might violate ADR} [reference: plan:line Y]

**Alignment Strengths**:
- {Aspect}: {How it aligns with baseline} [references]
</feature_plan_analysis>
```

**Sub-task 2.3: Systematic validation by dimension**

Execute validation across all dimensions:

**Dimension A: File Naming & Directory Structure**

Use Grep tool to extract file paths from implementation plan and compare against convention patterns:

- Search implementation plan for "files_affected|file.\*path"
- Search coding conventions for "file.*naming|directory.*structure"

**Validation questions**:

- Does file naming match dominant pattern (camelCase, kebab-case, PascalCase)?
- Does directory structure follow feature-based or layer-based organization?
- Are files placed in correct directories per convention?
- Do new directories follow established hierarchy?

**Dimension B: Architectural Pattern Compliance**

Use Grep tool to extract architectural patterns from plan and compare against ADRs:

- Search implementation plan for "architecture|layer|pattern|design"
- Search architecture decisions for "ADR-|decision|pattern"

**Validation questions**:

- Do planned components follow established architectural layers?
- Are separation of concerns principles maintained?
- Does data flow match architectural diagrams?
- Are integration patterns consistent with ADRs?
- Do new patterns contradict existing decisions?

**Dimension C: Technology & Dependency Validation**

Use Grep tool to extract dependencies from tech analysis and compare against baseline:

- Search tech analysis for "dependency|library|framework|package"
- Search tech stack baseline for "approved|prohibited|dependency"

**Validation questions**:

- Are all libraries in tech-stack-baseline approved list?
- Are new dependencies justified and vetted?
- Do version constraints match baseline?
- Are prohibited dependencies avoided?
- Does technology choice align with stack strategy?

**Dimension D: Error Handling Pattern Validation**

Use Grep tool to extract error handling from plan and compare against convention:

- Search implementation plan for "error.\*handl|exception|catch|throw"
- Search coding conventions for "error.*pattern|exception.*handling"

**Validation questions**:

- Does error handling use dominant pattern (throw vs return, toast vs log)?
- Are error types consistent with convention?
- Is error propagation strategy aligned?
- Are error messages following template?

**Dimension E: Testing Strategy Validation**

Use Grep tool to extract testing strategy from plan and compare against convention:

- Search implementation plan for "test|coverage|unit|integration|e2e"
- Search coding conventions for "test.\*strategy|coverage|pyramid"

**Validation questions**:

- Does testing match pyramid (unit > integration > E2E)?
- Are test locations following convention?
- Is coverage target met (per convention)?
- Are test naming patterns consistent?

**Dimension F: API Design Validation**

Use Grep tool to extract API design from plan and compare against convention:

- Search implementation plan for "endpoint|route|api|rest|graphql"
- Search coding conventions for "api.*design|endpoint.*pattern|rest"

**Validation questions**:

- Do endpoints follow RESTful conventions?
- Is versioning strategy consistent?
- Are authentication/authorization patterns aligned?
- Do response formats match standard?

**Dimension G: State Management Validation**

Use Grep tool to extract state management from plan and compare against convention:

- Search implementation plan for "state|redux|context|store"
- Search coding conventions for "state.\*management|store|context"

**Validation questions**:

- Does state management use established library?
- Are state patterns consistent with convention?
- Is global vs local state decision aligned?
- Do data flow patterns match architecture?

**Sub-task 2.4: Generate initial findings**

```xml
<initial_findings>
<critical_issues>
  <issue id="CRIT-001">
    <dimension>{Category}</dimension>
    <title>{Issue title}</title>
    <description>{What violation detected}</description>
    <evidence>
      <plan_ref>implementation-plan-{feature}.md:{line}</plan_ref>
      <baseline_ref>{baseline artifact}:{line}</baseline_ref>
      <conflict>
        Plan: "{excerpt}"
        Baseline: "{excerpt}"
      </conflict>
    </evidence>
    <severity_rationale>
      {Why classified as CRITICAL - must reference ADR violation or prohibited tech}
    </severity_rationale>
  </issue>
</critical_issues>

<warnings>
  <warning id="WARN-001">
    <dimension>{Category}</dimension>
    <title>{Warning title}</title>
    <description>{Deviation description}</description>
    <evidence>
      <plan_ref>implementation-plan-{feature}.md:{line}</plan_ref>
      <convention_ref>coding-conventions.md:{line}</convention_ref>
      <conformance_data>
        Dominant pattern: {Pattern} ({X}% of codebase - cite source)
        Plan uses: {Different pattern}
      </conformance_data>
    </evidence>
    <severity_rationale>
      {Why classified as WARNING - must have >80% conformance data}
    </severity_rationale>
  </warning>
</warnings>

<informational>
  <info id="INFO-001">
    <dimension>{Category}</dimension>
    <title>{Info title}</title>
    <description>{Minor deviation}</description>
    <evidence>
      <plan_ref>{Reference}</plan_ref>
      <note>{Why informational only}</note>
    </evidence>
  </info>
</informational>

<compliant_areas>
  <compliant dimension="{Category}">
    ✅ {What is compliant} (reference: {artifact}:{line})
  </compliant>
</compliant_areas>
</initial_findings>
```

### Phase 3: Chain of Verification - Validate Initial Findings

**Critical verification checklist - answer each question and revise findings if needed**:

```xml
<verification_round_1>
<question_1>Did I identify ALL deviations or only surface-level ones?</question_1>
<verification_1>
  <action>Re-scan implementation plan for subtle inconsistencies</action>
  <action>Check for implicit patterns not explicitly stated</action>
  <action>Review dependencies graph for hidden tech choices</action>
  <finding>
    {Did this reveal additional issues? If yes, add them. If no, state "No additional issues found"}
  </finding>
</verification_1>

<question_2>Are severity classifications justified by concrete evidence?</question_2>
<verification_2>
  <check>Each CRITICAL must cite specific ADR violation OR prohibited technology</check>
  <check>Each WARNING must cite quantitative conformance data (>80% threshold)</check>
  <check>Each INFO must explain why it's not higher severity</check>
  <finding>
    {Review each issue classification}
    {Reclassify any issues with insufficient evidence}
    {List any reclassifications: ISSUE-ID: {OLD} → {NEW} because {reason}}
  </finding>
</verification_2>

<question_3>Are false positives excluded?</question_3>
<verification_3>
  <check>Acceptable deviations (justified in plan) marked INFO not WARNING</check>
  <check>Intentional architectural evolution distinguished from drift</check>
  <check>Context-appropriate exceptions recognized</check>
  <finding>
    {Identify any false positives}
    {Remove or downgrade false positives: ISSUE-ID removed/downgraded because {reason}}
  </finding>
</verification_3>

<question_4>Is evidence cited with traceable file:line references?</question_4>
<verification_4>
  <check>Every issue has plan_reference with file:line or section</check>
  <check>Every issue has baseline_reference with file:line or section</check>
  <check>Conflicting excerpts are quoted verbatim</check>
  <finding>
    {List issues with incomplete evidence}
    {Add missing references: ISSUE-ID: added reference {artifact}:{line}}
  </finding>
</verification_4>

<question_5>Are recommendations actionable and specific?</question_5>
<verification_5>
  <check>Not generic "fix error handling" but specific "replace lines X-Y with toast pattern (see coding-conventions.md:45)"</check>
  <check>Each recommendation includes concrete example or reference</check>
  <check>Recommendations are feasible within feature scope</check>
  <finding>
    {Review recommendation quality}
    {Enhance vague recommendations: ISSUE-ID: improved recommendation to "{specific guidance}"}
  </finding>
</verification_5>

<question_6>Is overall score calculated correctly?</question_6>
<verification_6>
  <calculation>
    Base score: 100
    Critical count: {N} → -{N × 10} = {deduction}
    Warning count: {N} → -{N × 5} = {deduction}
    Info count: {N} → -{N × 1} = {deduction}
    Final score: {total}/100
  </calculation>
  <check>Verify arithmetic is correct</check>
  <check>Score interpretation matches rubric</check>
  <finding>
    {Confirm score or state correction}
  </finding>
</verification_6>

<question_7>Did I check cross-feature consistency?</question_7>
<verification_7>
  <check>Compare against similar features from memory search results</check>
  <check>Are patterns consistent with related features?</check>
  <check>If different, is there valid evolution rationale?</check>
  <finding>
    {Cross-feature consistency assessment}
    {Any new issues discovered from cross-feature comparison}
  </finding>
</verification_7>

<question_8>Are there hidden assumptions in my validation?</question_8>
<verification_8>
  <check>State any assumed convention interpretations</check>
  <check>Note any ambiguous baseline requirements</check>
  <check>Identify gaps in baseline documentation</check>
  <finding>
    {List all assumptions made}
    {Note any validation limitations due to assumptions}
  </finding>
</verification_8>

<question_9>Could any WARNING be justified evolution of convention?</question_9>
<verification_9>
  <check>Does deviation introduce better pattern?</check>
  <check>Is there industry best practice justification?</check>
  <check>Would adopting this improve codebase?</check>
  <finding>
    {Identify potential convention evolution opportunities}
    {Note in findings if deviation might be intentional improvement}
  </finding>
</verification_9>

<question_10>Is the merge recommendation clear and justified?</question_10>
<verification_10>
  <check>CRITICAL count > 0 → BLOCK or REQUEST_CHANGES</check>
  <check>Score < 70 → must fix before implementation</check>
  <check>Score 70-89 → address warnings before implementation</check>
  <check>Score >= 90 → proceed with implementation</check>
  <finding>
    {State merge decision}
    {Justify based on score and critical count}
  </finding>
</verification_10>
</verification_round_1>
```

### Phase 4: Revise Findings Based on Verification

**Generate revised findings incorporating verification insights**:

```xml
<revised_findings>
<changes_from_verification>
  - {List all changes made based on verification}
  - {Issues added: ISSUE-ID with rationale}
  - {Issues removed: ISSUE-ID with rationale}
  - {Issues reclassified: ISSUE-ID from {OLD} to {NEW} with rationale}
  - {Evidence added: ISSUE-ID with added references}
  - {Recommendations enhanced: ISSUE-ID with improvements}
</changes_from_verification>

<verified_critical_issues>
  {Same structure as initial_findings but with verified, evidence-backed issues}
</verified_critical_issues>

<verified_warnings>
  {Same structure as initial_findings but with verified, evidence-backed warnings}
</verified_warnings>

<verified_informational>
  {Same structure as initial_findings but with verified info items}
</verified_informational>

<verified_compliant_areas>
  {List 5-10 areas where plan demonstrates strong compliance}
</verified_compliant_areas>

<cross_feature_analysis>
  <similar_features>
    <feature>{Related feature}</feature>
    <consistency_note>
      {How current plan compares to this feature's implementation}
    </consistency_note>
  </similar_features>
</cross_feature_analysis>

<assumptions_and_limitations>
  {Document all assumptions made during validation}
  {Note any limitations due to missing/ambiguous baseline documentation}
</assumptions_and_limitations>

<convention_evolution_suggestions>
  {If any warnings suggest beneficial evolution, document here}
  {Suggest baseline updates for future consideration}
</convention_evolution_suggestions>
</revised_findings>
```

### Phase 5: Final Report Generation

Create comprehensive consistency validation report with verified findings:

```xml
<consistency_report>
<metadata>
  <feature_slug>{feature}</feature_slug>
  <validation_date>{current date}</validation_date>
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
  <verification_completed>true</verification_completed>
</metadata>

<validation_summary>
  <overall_score>{0-100}</overall_score>
  <status>PASS|PASS_WITH_WARNINGS|FAIL</status>
  <critical_count>{number}</critical_count>
  <warning_count>{number}</warning_count>
  <info_count>{number}</info_count>
  <compliant_count>{number}</compliant_count>
</validation_summary>

{Include verified_critical_issues, verified_warnings, verified_informational, verified_compliant_areas}

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
    {List critical items that MUST be fixed before implementation}
  </immediate_actions>
  <before_implementation>
    {List warnings that SHOULD be addressed before implementation}
  </before_implementation>
  <future_considerations>
    {List info items and convention evolution suggestions}
  </future_considerations>
  <merge_decision>
    APPROVE | REQUEST_CHANGES | BLOCK
    {Justification based on verified score and critical count}
  </merge_decision>
</recommendations>

<verification_summary>
  <verification_rounds_completed>1</verification_rounds_completed>
  <issues_added_during_verification>{count}</issues_added_during_verification>
  <issues_removed_during_verification>{count}</issues_removed_during_verification>
  <issues_reclassified_during_verification>{count}</issues_reclassified_during_verification>
  <false_positives_eliminated>{count}</false_positives_eliminated>
  <assumptions_documented>{list key assumptions}</assumptions_documented>
</verification_summary>

<validation_notes>
  <assumptions>
    {All assumptions made during validation}
  </assumptions>
  <edge_cases>
    {Special cases or exceptions noted}
  </edge_cases>
  <convention_evolution>
    {Suggestions for updating conventions based on this validation}
  </convention_evolution>
  <baseline_gaps>
    {Missing or ambiguous baseline documentation that limited validation}
  </baseline_gaps>
</validation_notes>
</consistency_report>
```

**Write verified report to memory**:

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

**Evidence-Based Validation**: Every issue MUST cite specific file:line references from both plan and baseline. Verification phase eliminates any findings without proper evidence.

**Conformance Data Required**: Warnings require quantitative conformance data (e.g., "80% of codebase uses pattern X"). Verification phase checks this requirement and downgrades/removes issues lacking data.

**"According to..." Prompting**: When stating conventions, use: "According to coding-conventions.md:{line}, the dominant pattern is {pattern}".

**No Invented Conventions**: If convention is not documented in baseline artifacts, mark as INFO with note "No established convention found - comparing to similar features". Verification phase checks for hallucinated conventions.

**Severity Justification**: Each CRITICAL must reference specific ADR or prohibited technology list. Each WARNING must have >80% conformance data. Verification phase enforces these requirements strictly.

**Verification Loop Prevents False Findings**: The Chain of Verification phase systematically checks for false positives, missing evidence, incorrect severity classifications, and unarticulated assumptions before finalizing the report.

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
  - Document in verification_summary
```

## Validation Checklist

Before finalizing report, verify:

- [ ] All baseline artifacts loaded successfully
- [ ] All feature artifacts loaded successfully
- [ ] Phase 3 verification completed with all 10 questions answered
- [ ] Each CRITICAL has ADR/prohibited-tech reference (verified in Phase 3)
- [ ] Each WARNING has conformance percentage (verified in Phase 3)
- [ ] Each issue has plan_reference and baseline_reference (verified in Phase 3)
- [ ] Overall score calculation is correct (verified in Phase 3)
- [ ] Merge decision matches score interpretation (verified in Phase 3)
- [ ] No hallucinated conventions - all cited from artifacts (verified in Phase 3)
- [ ] Cross-feature consistency checked (verified in Phase 3)
- [ ] Assumptions stated explicitly (verified in Phase 3)
- [ ] False positives eliminated (verified in Phase 3)
- [ ] Verification summary included in report
- [ ] Report written to .claude/memory/consistency-report-{feature}.md

## Best Practices

1. **Verification Over Initial Judgment**: Initial findings are provisional - verification phase determines final report
2. **Evidence-Based Only**: Never claim "convention is X" without citing source and verifying during Phase 3
3. **Quantify Deviations**: Use conformance percentages verified against actual baseline data
4. **Distinguish Convention from Preference**: Only enforce documented conventions verified in Phase 3
5. **Suggest Convention Evolution**: If plan introduces better pattern, note in verification phase
6. **Provide Actionable Recommendations**: Verify during Phase 3 that recommendations are specific and feasible
7. **Cross-Reference Similar Features**: Verification phase checks consistency with past implementations
8. **Balance Consistency with Innovation**: Verification phase identifies justified improvements vs drift
9. **Document Assumptions**: Verification phase forces explicit assumption documentation
10. **Eliminate False Positives**: Dedicated verification question ensures false positives are removed

## Output

Generate markdown-formatted consistency report in `.claude/memory/consistency-report-{feature}.md` with:

- Overall score (0-100) and status (PASS/PASS_WITH_WARNINGS/FAIL)
- Verified critical issues (MUST fix before implementation)
- Verified warnings (SHOULD fix or justify)
- Verified informational notes (CONSIDER)
- Compliant areas (positive reinforcement)
- Actionable, specific recommendations
- Merge decision (APPROVE/REQUEST_CHANGES/BLOCK)
- Verification summary showing validation quality
- Documented assumptions and limitations

**Success**: Feature plan validated against codebase baseline with verified, evidence-based consistency report generated. Verification phase ensures report accuracy and eliminates hallucinations/false positives.
