---
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
argument-hint: [feature-slug]
description: Orchestrate feature implementation using CoT, CoVe, and anti-hallucination techniques from planning artifacts
---

# Feature Implementation Orchestration Command

**Feature slug**: $1

Act as a **Staff Engineer and Technical Lead** orchestrating the implementation of a feature that has already been planned. You will coordinate the development work, enforce quality gates, prevent hallucinations, and protect against scope creep.

## Objective

Transform the implementation plan into working, tested, production-ready code by:
1. Executing tasks in dependency order
2. Applying advanced prompt engineering at each step (CoT, CoVe, Step-Back)
3. Preventing hallucinations through context grounding
4. Maintaining scope boundaries
5. Ensuring quality through automated verification

## Prerequisites Check

Before starting implementation, verify all planning artifacts exist:

```bash
# Check for required artifacts
code-tools read_file --path .claude/memory/requirements-$1.md
code-tools read_file --path .claude/memory/tech-analysis-$1.md
code-tools read_file --path .claude/memory/implementation-plan-$1.md
code-tools read_file --path .claude/memory/scope-validation-$1.md
```

If ANY artifact is missing, **STOP** and run the appropriate planning command first:
- Missing requirements → `/gather-requirements`
- Missing tech analysis → `/research-tech $1`
- Missing implementation plan → `/plan-implementation $1`
- Missing scope validation → `/validate-scope $1`

## Methodology

### Phase 1: Implementation Context Preparation

Load ALL context into working memory:

```xml
<context_preparation>
  <requirements>
    {Summary of functional and non-functional requirements}
  </requirements>

  <tech_stack>
    {Technologies, frameworks, libraries from tech analysis}
    {Justifications for each choice}
  </tech_stack>

  <implementation_plan>
    <phases>
      {Phase 1, 2, 3, 4 with goals}
    </phases>
    <tasks>
      {Complete task list with IDs, dependencies, estimates}
    </tasks>
    <critical_path>
      {Tasks that block others}
    </critical_path>
  </implementation_plan>

  <scope_boundaries>
    <mvp_features>
      {What IS in scope}
    </mvp_features>
    <deferred_features>
      {What is NOT in scope}
    </deferred_features>
  </scope_boundaries>

  <coding_standards>
    {Language-specific standards}
    {Project conventions}
    {Security requirements}
  </coding_standards>
</context_preparation>
```

**Anti-Hallucination Measure**: This context forms the ONLY source of truth. Do not introduce information outside these artifacts.

### Phase 2: Dependency Graph Execution Plan

Analyze task dependencies and create execution order:

```
<execution_plan>
**Dependency Analysis**:
- Tasks with no dependencies (can start immediately): {T-1-1, T-1-2, ...}
- Tasks blocked waiting for dependencies: {T-2-1 waits for T-1-1}
- Critical path (longest chain): {T-1-1 → T-2-2 → T-3-1}

**Execution Order** (respecting dependencies):

Wave 1 (Parallel execution possible):
  - T-1-1: {Task name} [No dependencies]
  - T-1-2: {Task name} [No dependencies]

Wave 2 (After Wave 1 completes):
  - T-2-1: {Task name} [Depends on: T-1-1]
  - T-2-2: {Task name} [Depends on: T-1-1, T-1-2]

Wave 3 (After Wave 2 completes):
  - T-3-1: {Task name} [Depends on: T-2-2]

... {Continue for all tasks}

**Parallel Opportunities**:
- Wave 1: Can execute {N} tasks concurrently
- Wave 2: Can execute {M} tasks concurrently
- ...

**Estimated Duration**: {Sum of critical path estimates}
</execution_plan>
```

### Phase 3: Task-by-Task Implementation Loop

For EACH task in execution order:

#### Step 3.1: Pre-Implementation Validation

```
<pre_implementation_validation task_id="{T-X}">
**Scope Check**:
1. ✅ Is this task in the implementation plan? {Yes/No}
2. ✅ Does it implement a requirement from requirements doc? {REQ-ID}
3. ✅ Are all dependencies completed? {List with status}
4. ⚠️ Am I being asked to do anything beyond the task spec? {Flag if yes}

**Context Availability**:
1. ✅ Tech stack confirmed for this task? {Technology}
2. ✅ Coding standards known? {Standards reference}
3. ✅ Acceptance criteria clear? {List criteria}

**If ANY check fails**: STOP and resolve before coding.
</pre_implementation_validation>
```

#### Step 3.2: Invoke Senior Developer with Full Context

For each task, execute the senior-developer agent workflow:

```bash
# This is conceptual - the actual implementation would use the agent
# The agent follows its full methodology (CoT → Implementation → CoVe → Testing)
```

The senior-developer agent will:
1. **Chain-of-Thought Reasoning**: Plan the implementation approach
2. **Grounded Implementation**: Write code using only verified APIs/patterns
3. **Chain-of-Verification**: Self-check the implementation
4. **Automated Testing**: Generate and run tests
5. **Documentation**: Create implementation log

**Pass to agent**:
- Task ID and specification
- All context artifacts
- Dependencies outputs (if any)
- Acceptance criteria
- Coding standards

**Receive from agent**:
- Implementation files (code)
- Test suite (passing tests)
- CoVe verification results
- Implementation documentation
- Any assumptions flagged

#### Step 3.3: Quality Gate Validation

After agent completes task, run quality gates:

```xml
<quality_gate task_id="{T-X}">
  <code_quality>
    <standards_compliance>
      ✅ Naming conventions followed?
      ✅ Formatting correct?
      ✅ Comments present where needed?
    </standards_compliance>

    <best_practices>
      ✅ DRY principle applied?
      ✅ SOLID principles respected?
      ✅ Error handling comprehensive?
    </best_practices>
  </code_quality>

  <test_coverage>
    <unit_tests>
      ✅ Tests exist? {Count}
      ✅ Tests passing? {Pass rate}
      ✅ Coverage adequate? {%}
    </unit_tests>

    <edge_cases>
      ✅ Boundary conditions tested?
      ✅ Error paths tested?
      ✅ Integration points tested?
    </edge_cases>
  </test_coverage>

  <security_review>
    ✅ Input validation present?
    ✅ No injection vulnerabilities?
    ✅ Auth/authz correctly applied?
    ✅ No hardcoded secrets?
  </security_review>

  <scope_compliance>
    ✅ Implements exactly the task spec (no more)?
    ✅ No features outside requirements added?
    ✅ Matches acceptance criteria?
  </scope_compliance>

  <anti_hallucination_check>
    ✅ All libraries used are in tech analysis?
    ✅ All APIs used are verified (no invented methods)?
    ✅ No assumptions made without flagging?
  </anti_hallucination_check>

  <verdict>{Pass|Fail|Needs Revision}</verdict>

  <issues_found>
    {List any issues that need correction}
  </issues_found>
</quality_gate>
```

**If verdict is "Fail" or "Needs Revision"**: Send back to agent for fixes before proceeding.

#### Step 3.4: Integration Verification

After quality gate passes:

```bash
# Run integration tests if this task connects to other components
code-tools run_tests --suite integration --filter "{feature-name}"

# Verify the system still works end-to-end
code-tools run_tests --suite e2e --filter "{critical-flows}"
```

**If integration tests fail**: Investigate and fix before marking task complete.

#### Step 3.5: Task Completion Documentation

```bash
# Mark task as complete in tracking
code-tools create_file --file .claude/memory/tasks-$1.md --content @task-status.txt

# Update: Task T-X: [Complete] {timestamp}
```

### Phase 4: Cross-Phase Validation

After completing each implementation phase (Foundation, Core, Integration, Polish):

```xml
<phase_completion_check phase="{Phase-N}">
  <exit_criteria>
    <!-- From implementation plan -->
    <criterion>{What must be true to proceed}</criterion>
    <status>{Met|Not Met}</status>
  </exit_criteria>

  <deliverable>
    <what>{What can be demoed/tested}</what>
    <verification>{How to verify it works}</verification>
    <demo_performed>{Yes|No}</demo_performed>
  </deliverable>

  <scope_drift_check>
    <features_added>{List any features added this phase}</features_added>
    <cross_reference>
      {For each feature, confirm it's in requirements}
      {Flag any not in original scope}
    </cross_reference>
  </scope_drift_check>

  <technical_debt>
    <shortcuts_taken>{Any temporary solutions}</shortcuts_taken>
    <refactoring_needed>{Items to improve later}</refactoring_needed>
  </technical_debt>

  <recommendation>{Proceed to next phase | Fix issues | Scope review needed}</recommendation>
</phase_completion_check>
```

**Do not proceed to next phase until exit criteria are met.**

### Phase 5: Final Implementation Verification

After all tasks complete, comprehensive validation:

```xml
<final_verification>
  <requirements_coverage>
    <functional_requirements>
      <!-- For each REQ-ID in requirements doc -->
      <requirement id="{REQ-ID}">
        <description>{Requirement text}</description>
        <implemented_by>{Task IDs}</implemented_by>
        <tested>{Yes|No}</tested>
        <status>{Complete|Incomplete}</status>
      </requirement>
    </functional_requirements>

    <non_functional_requirements>
      <!-- Performance, security, scalability, etc. -->
      <requirement id="{NFR-ID}">
        <description>{Requirement text}</description>
        <verification_method>{How verified}</verification_method>
        <result>{Pass|Fail with metrics}</result>
      </requirement>
    </non_functional_requirements>

    <coverage_summary>
      {X/Y requirements fully implemented}
      {Z requirements partially implemented (list)}
      {W requirements not implemented (list with reason)}
    </coverage_summary>
  </requirements_coverage>

  <test_suite_validation>
    <unit_tests>
      <total>{Count}</total>
      <passing>{Count}</passing>
      <coverage>{%}</coverage>
    </unit_tests>

    <integration_tests>
      <total>{Count}</total>
      <passing>{Count}</passing>
    </integration_tests>

    <e2e_tests>
      <critical_flows_tested>{List}</critical_flows_tested>
      <all_passing>{Yes|No}</all_passing>
    </e2e_tests>
  </test_suite_validation>

  <performance_validation>
    <!-- If NFRs specify performance requirements -->
    <metric name="{e.g., Response Time}">
      <required>{Target from NFRs}</required>
      <measured>{Actual performance}</measured>
      <status>{Meets|Exceeds|Fails}</status>
    </metric>
  </performance_validation>

  <security_audit>
    <owasp_top_10_check>
      {Address each of OWASP Top 10 relevant to this feature}
    </owasp_top_10_check>
    <vulnerabilities_found>{Count}</vulnerabilities_found>
    <all_resolved>{Yes|No}</all_resolved>
  </security_audit>

  <scope_final_check>
    <mvp_features>
      {All MVP features from scope validation implemented? Yes/No}
    </mvp_features>
    <deferred_features>
      {Confirm no deferred features were implemented}
    </deferred_features>
    <scope_creep_detected>{Yes|No - list if yes}</scope_creep_detected>
  </scope_final_check>

  <code_quality_metrics>
    <standards_violations>{Count}</standards_violations>
    <complexity_issues>{Count}</complexity_issues>
    <maintainability_score>{A-F grade}</maintainability_score>
  </code_quality_metrics>

  <documentation_completeness>
    ✅ Implementation docs for all tasks?
    ✅ API documentation (if applicable)?
    ✅ README updated?
    ✅ Deployment instructions (if changed)?
  </documentation_completeness>
</final_verification>
```

### Phase 6: Implementation Summary and Handoff

Create comprehensive summary document:

```bash
code-tools create_file --file .claude/memory/implementation-summary-$1.md --content @summary.txt
```

#### Summary Document Structure

```markdown
# Implementation Summary: {Feature Name}

## Status: {Complete|Partial|Blocked}

## Overview

**Implementation Period**: {Start date} to {End date}
**Total Tasks**: {Completed} / {Planned}
**Test Coverage**: {%}
**Requirements Met**: {X/Y}

## What Was Built

{High-level description of the implemented feature}

### Components Delivered

1. **{Component Name}** ({Language/Framework})
   - Files: {List of files}
   - Purpose: {What it does}
   - Tests: {Test count}

2. **{Component Name}**
   ...

## Requirements Coverage

| Requirement ID | Description | Status | Tasks | Tests |
|----------------|-------------|--------|-------|-------|
| REQ-001 | {Text} | ✅ Complete | T-1-1, T-2-3 | 15 tests |
| REQ-002 | {Text} | ⚠️ Partial | T-2-4 | 8 tests |

## Quality Metrics

- **Test Coverage**: {%} (Target: 80%+)
- **Code Quality**: {Grade}
- **Security Issues**: {Count} ({Resolved count} resolved)
- **Performance**: {Meets|Exceeds|Below} NFR targets

## Scope Compliance

✅ **No Scope Creep Detected** - All implemented features were in original plan

OR

⚠️ **Scope Deviations**:
- {Feature X}: Added because {justification}
- {Feature Y}: Deferred to Phase 2 due to {reason}

## Technical Decisions Made

### Key Architectural Choices

1. **{Decision}**
   - **Why**: {Rationale based on requirements/constraints}
   - **Alternatives Considered**: {What else was evaluated}
   - **Trade-offs**: {What we gained vs. what we lost}

## Known Limitations / Technical Debt

1. **{Limitation}**
   - **Impact**: {How it affects the feature}
   - **Mitigation**: {Workaround or future fix plan}

## Testing Summary

### Unit Tests
- Total: {Count}
- Coverage: {%}
- Key areas: {List}

### Integration Tests
- Scenarios covered: {List}
- All passing: {Yes/No}

### E2E Tests
- Critical user flows tested: {List}
- Status: {All passing | Issues found}

## Deployment Readiness

- [ ] All tests passing
- [ ] Security audit complete
- [ ] Performance validated
- [ ] Documentation updated
- [ ] Code reviewed (if process requires)
- [ ] Deployment scripts updated
- [ ] Monitoring/logging in place

## Next Steps

### Immediate
1. {Action item}
2. {Action item}

### Phase 2 / Future Enhancements
1. {Deferred feature}
2. {Optimization opportunity}

## Lessons Learned

### What Went Well
- {Positive observation}

### What Could Be Improved
- {Area for improvement}

## Reference Artifacts

- Requirements: `.claude/memory/requirements-{feature}.md`
- Tech Analysis: `.claude/memory/tech-analysis-{feature}.md`
- Implementation Plan: `.claude/memory/implementation-plan-{feature}.md`
- Scope Validation: `.claude/memory/scope-validation-{feature}.md`
- Task Logs: `.claude/memory/implementation-{feature}-*.md`
```

## Hallucination Prevention Strategy

Throughout implementation, enforce these safeguards:

### 1. Context Injection
**Every agent invocation** must include:
- Full requirements context
- Tech stack from analysis
- Task specification
- Coding standards
- Previous task outputs (if dependencies)

**Never** let agent operate without context.

### 2. "According to..." Verification
**Every** library/framework usage must be verified:
- Is it in tech analysis? → Approved
- Is it in official docs? → Fetch and confirm
- Is it a hallucination? → Reject and find alternative

### 3. API Method Validation
Before using ANY API method:
```bash
# Check if it exists in official docs
code-tools fetch_content --url {official-docs-url} | grep "{method-name}"

# Or check if it's used in existing codebase
code-tools grep_code --pattern "{method-name}" --limit 10
```

**If not found**: It's likely a hallucination. Use alternative or verify first.

### 4. Assumption Flagging
**Require** agent to flag assumptions:
```
<assumptions_made>
  <assumption status="needs_validation">
    {What was assumed because it wasn't specified}
  </assumption>
</assumptions_made>
```

**Review** all flagged assumptions and either:
- Validate with user
- Look up in documentation
- Reject if unsupported

### 5. Cross-Artifact Verification
**Before implementing**: Verify consistency
```
<consistency_check>
  Requirements say: {X}
  Tech analysis recommends: {Y to implement X}
  Task spec describes: {Z approach}

  ✅ Are X, Y, Z consistent?
  ⚠️ If not, which is authoritative?
</consistency_check>
```

## Scope Protection Mechanisms

### Continuous Scope Monitoring

**Before each task**:
```
Is this task in the plan? {Yes → Proceed | No → Reject}
```

**During implementation**:
```
Agent wants to add feature F.
Is F in requirements? {Yes → Allow | No → Reject as scope creep}
```

**After each phase**:
```
Compare implemented features to scope validation doc.
Flag any extras for review.
```

### Scope Creep Triggers

**Immediately flag and halt if**:
- Agent mentions "let's also add..."
- Agent implements features not in task spec
- Agent uses libraries not in tech analysis
- Agent creates files not described in plan

### Recovery from Scope Violations

```xml
<scope_violation_detected>
  <violation>{What was added/changed outside scope}</violation>
  <source>{Which task or agent}</source>

  <assessment>
    <is_it_necessary>{Critical|Nice-to-have|Unnecessary}</is_it_necessary>
    <impact_if_removed>{How it affects feature}</impact_if_removed>
  </assessment>

  <resolution>
    <option_1>Remove it - not in MVP</option_1>
    <option_2>Get approval to expand scope</option_2>
    <option_3>Defer to Phase 2</option_3>
  </resolution>

  <action_taken>{What we decided}</action_taken>
</scope_violation_detected>
```

## Success Criteria

Implementation orchestration is successful when:

- ✅ All planned tasks completed (or explicitly deferred with reason)
- ✅ All requirements met (functional and non-functional)
- ✅ All tests passing (unit, integration, E2E)
- ✅ No hallucinated code (all APIs verified)
- ✅ No scope creep (only planned features implemented)
- ✅ Coding standards followed throughout
- ✅ Security audit passed
- ✅ Documentation complete
- ✅ Feature is deployable

## Error Handling

If implementation cannot complete:

```xml
<implementation_blocked>
  <phase>{Which phase}</phase>
  <task_id>{Where stuck}</task_id>

  <blocker>
    <type>{Technical|Requirements|Dependency|Resource}</type>
    <description>{What's blocking}</description>
  </blocker>

  <attempted_resolutions>
    <attempt>{What was tried}</attempt>
    <result>{Why it didn't work}</result>
  </attempted_resolutions>

  <recommendation>
    {What needs to happen to unblock}
  </recommendation>
</implementation_blocked>
```

**Escalation**: Create detailed blocker report for human intervention.

## Summary

This orchestration command bridges the gap between **planning** and **delivery** by:

1. **Structuring** the implementation as a series of verified, tested steps
2. **Preventing** hallucinations through context grounding and verification
3. **Protecting** scope through continuous validation against requirements
4. **Ensuring** quality through automated gates and testing
5. **Documenting** every decision and implementation detail

The result: **Production-ready code** that implements exactly what was planned, nothing more, nothing less, with full traceability from requirement to implementation.

Begin implementation now, following this orchestration methodology.
