---
allowed-tools: Task, Bash(code-tools:*), Read
argument-hint: [feature-slug]
description: Orchestrate scope validation and feature creep prevention by delegating to scope-guardian agent
---

# Scope Validation Orchestrator

**System date assertion**: 2025-10-23
**Feature slug**: $ARGUMENTS

Act as a scope validation orchestrator responsible for coordinating the scope management workflow and ensuring ruthless MVP prioritization.

## Objective

Delegate scope validation to the specialized scope-guardian agent while providing necessary context, validation checkpoints, and artifact structure enforcement.

**Mindset**: "A product that does one thing exceptionally well beats one that does many things poorly."

## Methodology

### Phase 0: Step-Back Prompting (Product Context)

Before detailed scope validation, understand the product context:

**Step-Back Questions**:

```xml
<product_context>
<question>What is the fundamental user problem being solved?</question>
<purpose>Identify the ONE core value proposition to anchor scope decisions</purpose>
<framework>
- What pain point are users experiencing?
- What is the current workaround?
- What would success look like for users?
- How will users measure if this solves their problem?
</framework>

<question>What category of product/feature is this?</question>
<categories>
- Core workflow: Essential to primary user journey
- Enhancement: Improves existing functionality
- Experimental: Testing new hypothesis or approach
- Technical debt: Replacing/refactoring existing system
- Nice-to-have: Convenience or polish feature
</categories>
<purpose>Category dictates MVP scope tolerance (core workflow = tight scope, experimental = flexible)</purpose>

<question>What are the real constraints?</question>
<constraints>
- Hard deadline: Specific date requirement (e.g., conference launch, regulatory)
- Soft deadline: Flexible timeline
- Fixed resources: Team size/skills cannot change
- Budget cap: Fixed cost limit
- Technical constraint: Must integrate with X, must use Y
</constraints>
<purpose>Constraints determine what can realistically be included in MVP</purpose>

<question>What is the competition or alternative?</question>
<purpose>Identify minimum feature set to be competitive or viable alternative</purpose>
<framework>
- What do competitors offer?
- What is the minimum feature set to compete?
- What differentiator makes this valuable vs alternatives?
</framework>
</product_context>
```

**Reason about MVP scope**:

```
Given this solves {user problem} as a {category} with {constraints}, MVP scope should:
- Include: {Minimum to solve core problem}
- Exclude: {Nice-to-haves that can wait}
- Differentiate on: {Key value proposition}
```

### Phase 1: Prerequisites Validation

Check for existing artifacts before delegating:

```bash
# Load feature requirements
code-tools read_file --path .claude/memory/requirements-$ARGUMENTS.md 2>/dev/null || echo "ERROR: Requirements not found. Run /gather-requirements first."

# Load technology analysis
code-tools read_file --path .claude/memory/tech-analysis-$ARGUMENTS.md 2>/dev/null || echo "WARN: Tech analysis not found. Limited scope validation possible."

# Load implementation plan
code-tools read_file --path .claude/memory/implementation-plan-$ARGUMENTS.md 2>/dev/null || echo "WARN: Implementation plan not found. Limited scope validation possible."

# Search for related scope decisions
code-tools search_memory --dir .claude/memory --query "$ARGUMENTS mvp scope priorities" --topk 5
```

**Context Summary for Agent**:

```xml
<existing_context>
<requirements>
{Summary from requirements-{feature}.md}
{Original goals, stakeholders, must-have vs should-have from mvp_definition}
{Constraints: timeline, budget, resources}
{Explicitly out-of-scope items}
</requirements>

<technology_choices>
{Technologies recommended in tech-analysis-{feature}.md if available}
{Complexity introduced by tech choices}
</technology_choices>

<implementation_scope>
{Task count and total effort from implementation-plan-{feature}.md if available}
{Phases and deliverables}
{Requirements traceability}
</implementation_scope>

<related_decisions>
{Similar features' scope decisions from memory search}
</related_decisions>
</existing_context>
```

### Phase 2: Agent Invocation with Comprehensive Context

Delegate to scope-guardian agent via Task tool:

```
Perform comprehensive scope validation for feature: $ARGUMENTS

**Role**: Act as a Product Manager and Scope Management Specialist with expertise in identifying and preventing feature creep, defining MVP boundaries, and ruthlessly prioritizing must-haves vs. nice-to-haves.

**Mindset**: "A product that does one thing exceptionally well beats one that does many things poorly."

**Product Context**:
{Paste product understanding from Step-Back phase}

**Existing Artifacts Context**:
{Paste context summary from Phase 1}

**Methodology**:

Use the systematic scope validation and MVP prioritization framework:

**Phase 1: Core Scope Extraction**

From requirements document, identify the **essential core**:

```xml
<core_scope>
  <primary_goal>{The ONE main thing this feature must achieve}</primary_goal>

  <user_problem>
    {The fundamental problem users are experiencing}
    {Current workaround or pain point}
  </user_problem>

  <must_have_capabilities>
    <!-- ONLY capabilities explicitly requested by user -->
    <capability id="{FR-XXX}" source="{Exact user statement or requirement text}">
      {Capability description}
    </capability>
  </must_have_capabilities>

  <success_criteria_mvp>
    <!-- Minimum metrics to declare MVP success -->
    <criterion measurable="true">{Criterion from requirements}</criterion>
  </success_criteria_mvp>

  <constraints>
    <timeline>{As stated in requirements - hard vs soft deadline}</timeline>
    <budget>{As stated in requirements - fixed vs flexible}</budget>
    <resources>{Team size, skills, availability from requirements}</resources>
    <technical>{Must-use technologies or integrations}</technical>
  </constraints>

  <explicitly_out_of_scope>
    <!-- Items user explicitly said are NOT included -->
    <item source="{requirements section}">{Item}</item>
  </explicitly_out_of_scope>
</core_scope>
```

**Phase 2: Scope Creep Detection**

For EACH artifact (requirements doc, tech analysis, implementation plan), apply systematic validation:

**2A. Requirements Document Validation**

For EACH requirement (FR-XXX, NFR-XXX), ask:

```xml
<requirement_validation id="{REQ-ID}">
  <question_1>Is this explicitly requested by the user?</question_1>
  <answer_1>{Yes: cite exact user statement | No: this is inferred/assumed}</answer_1>

  <question_2>Is this necessary for core functionality?</question_2>
  <answer_2>{Yes: explain why | No: this is enhancement}</answer_2>

  <question_3>Is this part of MVP or nice-to-have?</question_3>
  <answer_3>{Must-Have: essential | Should-Have: important but deferrable | Could-Have: nice-to-have}</answer_3>

  <question_4>Is this an assumption without user confirmation?</question_4>
  <answer_4>{No assumptions | Assumption: {what we assumed}}</answer_4>

  <question_5>Is this "gold-plating" (exceeding needs)?</question_5>
  <answer_5>{No | Yes: {how it exceeds stated needs}}</answer_5>

  <question_6>Does this fit within stated constraints?</question_6>
  <answer_6>{Yes: aligns with timeline/budget | No: conflicts with {constraint}}</answer_6>

  <mvp_litmus_test>
    Question: "Can we ship without this and still solve the core problem?"
    Answer: {Yes: defer it | No: must-have}
  </mvp_litmus_test>

  <verdict>Keep|Flag for Clarification|Defer to Phase 2|Remove</verdict>
  <reasoning>{Justification for verdict}</reasoning>
</requirement_validation>
```

**Flag as scope creep if**:
- Requirement not explicitly requested by user
- Requirement is "should-have" or "could-have" rather than "must-have"
- Requirement adds complexity without proportional value
- Requirement conflicts with constraints (timeline, budget, resources)
- Passes MVP litmus test (can ship without it)

**2B. Technology Analysis Validation**

For EACH major technology choice in tech-analysis doc:

```xml
<tech_validation technology="{name}">
  <question_1>Does this directly address a stated requirement?</question_1>
  <answer_1>{Requirement FR-XXX or NFR-XXX it addresses | No direct requirement}</answer_1>

  <question_2>Is this the simplest viable option?</question_2>
  <answer_2>{Yes: why | No: simpler alternative is {X} that also meets requirements}</answer_2>

  <question_3>Does this introduce unnecessary complexity?</question_3>
  <answer_3>{No: appropriate complexity | Yes: {how it's complex beyond needs}}</answer_3>

  <question_4>Is this "resume-driven" or "hype-driven" selection?</question_4>
  <answer_4>{No: practical, justified choice | Yes: choosing for novelty/trendiness}</answer_4>

  <question_5>Does this require skills/time not available?</question_5>
  <answer_5>{No: team has skills | Yes: requires {skills/time} we don't have}</answer_5>

  <question_6>Could a simpler alternative meet requirements?</question_6>
  <answer_6>{No: this is the simplest option | Yes: {alternative} is simpler and sufficient}</answer_6>

  <verdict>Appropriate|Over-engineered|Recommend Simpler Alternative</verdict>
  <reasoning>{Justification with specific requirements cited}</reasoning>
  <alternative>{If over-engineered, suggest specific simpler option with justification}</alternative>
</tech_validation>
```

**Flag as over-engineering if**:
- Technology is more complex than requirements necessitate
- Simpler alternative exists that fully meets requirements
- Chosen for "coolness factor" rather than practical fit
- Adds learning curve or integration complexity without sufficient benefit
- No clear requirement justifying the complexity

**2C. Implementation Plan Validation**

For EACH task in implementation plan:

```xml
<task_validation task_id="{T-X-Y}">
  <question_1>Does this implement a core requirement?</question_1>
  <answer_1>{Requirement FR-XXX or NFR-XXX | No direct requirement}</answer_1>

  <question_2>Is this on the critical path to MVP?</question_2>
  <answer_2>{Yes: MVP-essential | No: can be deferred}</answer_2>

  <question_3>Is this implementing a "nice-to-have"?</question_3>
  <answer_3>{No: must-have | Yes: implements {REQ-ID} which is should/could-have}</answer_3>

  <question_4>Could this be deferred to Phase 2/future?</question_4>
  <answer_4>{No: MVP-critical because {reason} | Yes: can defer because {reason}}</answer_4>

  <question_5>Is this adding capability not requested?</question_5>
  <answer_5>{No: matches requirements | Yes: adds {capability} not in requirements}</answer_5>

  <question_6>Is this "while we're at it" scope expansion?</question_6>
  <answer_6>{No | Yes: {description of expansion}}</answer_6>

  <mvp_litmus_test>
    Question: "Can we launch MVP without this task?"
    Answer: {Yes: defer | No: critical}
  </mvp_litmus_test>

  <verdict>MVP-Critical|Defer to Phase 2|Remove Entirely</verdict>
  <reasoning>{Justification with requirement traceability}</reasoning>
</task_validation>
```

**Flag as scope expansion if**:
- Task doesn't map to a must-have core requirement
- Task implements should-have or could-have feature
- Task can be deferred without blocking MVP functionality
- Task adds unrequested capability or "future-proofing"
- Task fails MVP litmus test

**Phase 3: MVP Definition (Ruthless Prioritization)**

Define the TRUE MVP using MoSCoW method:

```xml
<mvp_definition>
  <must_have>
    <!-- Without these, product is useless for core problem -->
    <feature id="{FR-XXX}">
      <description>{Feature description}</description>
      <rationale>{Why absolutely essential - cite core goal}</rationale>
      <litmus_test>Cannot ship without this; core problem unsolved</litmus_test>
    </feature>
  </must_have>

  <should_have>
    <!-- Important but not critical for initial launch -->
    <feature id="{FR-XXX}">
      <description>{Feature description}</description>
      <deferral_impact>{What happens if we launch without this}</deferral_impact>
      <recommendation>Defer to Phase 2 (post-MVP iteration)</recommendation>
      <litmus_test>Can ship without this; users can work around limitation</litmus_test>
    </feature>
  </should_have>

  <could_have>
    <!-- Nice-to-have, low priority enhancement -->
    <feature id="{FR-XXX}">
      <description>{Feature description}</description>
      <value>{Why this would be nice}</value>
      <recommendation>Defer to backlog for future consideration</recommendation>
      <litmus_test>Purely enhancement; no impact on core value</litmus_test>
    </feature>
  </could_have>

  <wont_have>
    <!-- Explicitly out of scope for MVP and near-term -->
    <feature>
      <description>{Feature description}</description>
      <reasoning>{Why excluding - complexity, constraints, or out-of-scope}</reasoning>
    </feature>
  </wont_have>

  <mvp_summary>
    {1-2 sentence summary of what MVP includes and excludes}
    {Core value proposition of MVP}
  </mvp_summary>
</mvp_definition>
```

**MVP Litmus Test** (apply to every feature):

Ask: "Can we ship without this feature and still solve the core problem?"

- If YES → Not MVP must-have; defer to should/could-have
- If NO → Must-have; keep in MVP

**Phase 4: Alignment Matrix**

Cross-reference requirements ↔ tech ↔ tasks:

| Requirement ID | Priority (MoSCoW) | Tech Choice | Implementation Tasks | Aligned? | Issue |
|----------------|-------------------|-------------|---------------------|----------|-------|
| FR-001 | Must-Have | ✅ Appropriate | T-1-1, T-2-3 (MVP) | ✅ | None |
| FR-005 | Should-Have | ✅ Appropriate | T-3-7, T-3-8 | ⚠️ | Defer to Phase 2 |
| NFR-PERF-002 | Could-Have | ⚠️ Over-engineered | T-2-5 | ❌ | Tech exceeds needs |
| N/A | N/A | N/A | T-4-2 | ❌ | No requirement for this task |

**Phase 5: Red Flag Analysis**

Identify scope creep red flags:

```xml
<red_flags>
  <feature_bloat>
    🚩 {Specific requirement/task} doesn't align with core goal of {goal}
  </feature_bloat>

  <gold_plating>
    🚩 {Requirement} asks for X, but {implementation/tech} provides X+Y+Z unnecessarily
  </gold_plating>

  <perfectionism>
    🚩 {Acceptance criteria} goes beyond "good enough for MVP"
    Example: {Specific criterion that's excessive}
  </perfectionism>

  <tech_showboating>
    🚩 {Technology} is impressive but overkill for stated needs
    Simpler option: {Alternative}
  </tech_showboating>

  <while_were_at_it>
    🚩 {Task/requirement} uses phrases like "while we're at it" or "it would be nice if"
    Source: {Where found}
  </while_were_at_it>

  <future_proofing>
    🚩 {Feature/tech} justified by "we might need it later" without concrete requirement
  </future_proofing>
</red_flags>
```

**Phase 6: Chain-of-Verification (CoVe)**

Before finalizing validation, verify:

```xml
<verification_checklist>
<question>Have I validated EVERY requirement against original user request?</question>
<check>Each FR-XXX and NFR-XXX has requirement_validation block</check>

<question>Is MVP definition ruthlessly minimal?</question>
<check>Every must-have passes "cannot ship without this" litmus test</check>
<check>Should-haves and could-haves are clearly deferrable</check>

<question>Are all scope creep items identified?</question>
<check>Requirements not explicitly requested are flagged</check>
<check>Tasks without requirement mapping are flagged</check>
<check>Over-engineered tech choices are flagged</check>

<question>Is alignment matrix complete?</question>
<check>Every requirement has tech and task mapping</check>
<check>Misalignments are identified with issues</check>

<question>Are recommendations specific and actionable?</question>
<check>Each recommendation has clear keep/simplify/defer/remove/clarify action</check>
<check>Justifications cite specific requirements or constraints</check>

<question>Are constraints validated?</question>
<check>Timeline: Sum of MVP tasks ≤ deadline</check>
<check>Budget: Effort × rate ≤ budget cap</check>
<check>Resources: Required skills match available team</check>

<question>Have I applied the "No" framework?</question>
<check>Feature bloat called out with specific examples</check>
<check>Gold-plating identified and simplified</check>
<check>Technology showboating flagged with alternatives</check>

<question>Are all red flags documented?</question>
<check>Specific instances of scope creep patterns listed in red_flags section</check>

<question>Is scope creep risk level justified?</question>
<check>Low: <10% of items flagged</check>
<check>Medium: 10-30% flagged</check>
<check>High: >30% flagged or major must-have bloat</check>

<question>Can stakeholders understand what is/isn't in MVP?</question>
<check>MVP summary is clear and concise</check>
<check>MoSCoW categories are unambiguous</check>
</verification_checklist>
```

Present summary to user and ask:
> "Based on the above validation, do you agree with the MVP definition and scope recommendations? Are there any must-haves I've incorrectly flagged as deferrable, or any should-haves you'd like to promote to must-have?"

**Iterate** until user confirms MVP scope.

**Output Requirements**:

Generate scope validation document in the following structure (render as markdown):

```xml
<scope_validation>
  <metadata>
    <feature_slug>{feature}</feature_slug>
    <validation_date>2025-10-23</validation_date>
    <validator>Scope Guardian Agent</validator>
    <status>Draft</status>
  </metadata>

  <validation_summary>
    <overall_status>APPROVED|REVISE_REQUIRED|SIGNIFICANT_SCOPE_CREEP</overall_status>
    <scope_creep_risk>Low|Medium|High</scope_creep_risk>

    <key_findings>
      <must_have_count>{Number of validated must-haves}</must_have_count>
      <should_have_count>{Number deferred to Phase 2}</should_have_count>
      <could_have_count>{Number deferred to backlog}</could_have_count>
      <removed_count>{Number removed entirely}</removed_count>
      <over_engineered_count>{Number of over-engineered tech choices}</over_engineered_count>
      <orphaned_tasks_count>{Tasks without requirement mapping}</orphaned_tasks_count>
    </key_findings>

    <executive_summary>
      {2-3 sentence summary of validation findings}
      {Overall recommendation: approve as-is, revise scope, or major rework needed}
    </executive_summary>
  </validation_summary>

  <core_scope_baseline>
    <!-- Include full <core_scope> XML from Phase 1 -->
  </core_scope_baseline>

  <scope_creep_analysis>
    <requirements_validation>
      <!-- Include ALL <requirement_validation> blocks from Phase 2A -->
    </requirements_validation>

    <technology_validation>
      <!-- Include ALL <tech_validation> blocks from Phase 2B -->
    </technology_validation>

    <implementation_validation>
      <!-- Include ALL <task_validation> blocks from Phase 2C -->
    </implementation_validation>
  </scope_creep_analysis>

  <mvp_definition>
    <!-- Include full <mvp_definition> XML from Phase 3 -->
  </mvp_definition>

  <alignment_matrix>
    <!-- Include table from Phase 4 -->
    <!-- List all misalignments with severity and recommendation -->
  </alignment_matrix>

  <red_flag_analysis>
    <!-- Include full <red_flags> XML from Phase 5 -->

    <red_flag_count>{Total number of red flags}</red_flag_count>
    <severity>
      {Low: <5 flags, Medium: 5-10 flags, High: >10 flags}
    </severity>
  </red_flag_analysis>

  <recommendations>
    <keep>
      <item id="{REQ-ID|TECH|TASK-ID}" type="requirement|tech|task">
        <description>{What to keep}</description>
        <justification>{Why it's essential - cite core goal and litmus test}</justification>
      </item>
    </keep>

    <simplify>
      <item id="{ID}" type="requirement|tech|task">
        <current>{Current over-engineered state}</current>
        <simplified>{Simpler alternative that meets requirements}</simplified>
        <justification>{Why simplification is better - cost/complexity/timeline}</justification>
        <effort_saved>{Hours/cost saved by simplification}</effort_saved>
      </item>
    </simplify>

    <defer>
      <item id="{ID}" type="requirement|tech|task">
        <description>{What to defer}</description>
        <to_phase>Phase 2|Backlog</to_phase>
        <justification>{Why it can wait - litmus test result, constraints}</justification>
        <deferral_impact>{Impact of launching without this}</deferral_impact>
      </item>
    </defer>

    <remove>
      <item id="{ID}" type="requirement|tech|task">
        <description>{What to remove entirely}</description>
        <justification>{Why it's scope creep - no requirement, gold-plating, etc.}</justification>
        <effort_saved>{Hours/cost saved by removal}</effort_saved>
      </item>
    </remove>

    <clarify>
      <item id="{ID}" type="requirement|tech|task">
        <description>{What needs clarification}</description>
        <question>{Specific question for user/stakeholder}</question>
        <reason>{Why clarification is needed}</reason>
        <decision_impact>{How answer affects MVP scope}</decision_impact>
      </item>
    </clarify>
  </recommendations>

  <constraint_validation>
    <timeline_check>
      <original_constraint>{Deadline from requirements}</original_constraint>
      <current_scope_effort>{Total hours for current scope}</current_scope_effort>
      <mvp_scope_effort>{Total hours for recommended MVP}</mvp_scope_effort>
      <aligned>{Yes|No - exceeds constraint by X hours/weeks}</aligned>
    </timeline_check>

    <budget_check>
      <original_constraint>{Budget from requirements}</original_constraint>
      <current_scope_cost>{Estimated cost for current scope}</current_scope_cost>
      <mvp_scope_cost>{Estimated cost for recommended MVP}</mvp_scope_cost>
      <aligned>{Yes|No - exceeds budget by $X}</aligned>
    </budget_check>

    <resource_check>
      <original_constraint>{Team size/skills from requirements}</original_constraint>
      <current_scope_needs>{Skills/team needed for current scope}</current_scope_needs>
      <mvp_scope_needs>{Skills/team needed for recommended MVP}</mvp_scope_needs>
      <aligned>{Yes|No - requires {missing skills/people}}</aligned>
    </resource_check>
  </constraint_validation>

  <risk_assessment>
    <scope_creep_risk_level>Low|Medium|High</scope_creep_risk_level>

    <risk_factors>
      <factor>{Factor contributing to scope creep risk}</factor>
      <mitigation>{How recommendations address this}</mitigation>
    </risk_factors>

    <if_no_action>
      {Consequences of not addressing scope creep}
      {Timeline impact, budget impact, quality impact}
    </if_no_action>
  </risk_assessment>

  <sign_off>
    <decision>APPROVE|REVISE_REQUIRED|REJECT</decision>

    <justification>
      APPROVE: MVP is well-defined, minimal scope creep, constraints aligned
      REVISE_REQUIRED: Moderate scope creep, recommendations must be addressed
      REJECT: Significant scope creep, major rework needed before proceeding
    </justification>

    <next_steps>
      {Specific actions to take based on decision}
      {e.g., "Remove tasks T-3-7, T-3-8, simplify tech choice for database"}
    </next_steps>
  </sign_off>

  <verification_confirmation>
    {Confirmation that all CoVe checks passed}
    {Any assumptions or edge cases noted}
  </verification_confirmation>
</scope_validation>
```

**Anti-Hallucination Safeguards**:

1. **User Request Grounding**: Only "must-have" if explicitly stated by user in requirements
2. **Litmus Test Everything**: Apply "can we ship without this?" to every feature
3. **Cite Sources**: Every validation references specific requirement IDs or user statements
4. **No Invented Requirements**: If not in requirements doc, flag as scope creep
5. **Conservative MVP**: When uncertain, defer to should-have; user can promote if critical

**Best Practices**:

- **Ruthless Prioritization**: Default to "defer" unless clear must-have
- **Evidence-Based**: Every validation cites specific requirements or constraints
- **User-Centric**: Focus on solving core user problem, not building perfect system
- **Constraint-Aware**: Respect timeline/budget limits; cut scope to fit
- **Iterative**: MVP is first step; Phase 2 exists for enhancements

**Iterative Refinement**:

After presenting initial validation:
1. User reviews MVP definition and recommendations
2. User can promote should-haves to must-haves (with justification)
3. User can accept deferrals or request re-evaluation
4. Re-verify with CoVe checklist
5. Iterate until user approves final MVP scope

Return final scope validation document content ready to write to file.
```

### Phase 3: Validation and Artifact Creation

After agent completes scope validation:

**Validation Checklist**:

```xml
<orchestrator_validation>
<question>Did agent extract core scope from requirements?</question>
<check>Verify core_scope section with primary_goal, must_have_capabilities, constraints</check>

<question>Did agent validate ALL requirements?</question>
<check>Every FR-XXX and NFR-XXX has requirement_validation block</check>

<question>Did agent validate technology choices?</question>
<check>Each major tech has tech_validation block with simplification check</check>

<question>Did agent validate implementation tasks?</question>
<check>Tasks have task_validation blocks with MVP litmus test</check>

<question>Is MVP definition ruthlessly minimal?</question>
<check>Must-haves all pass "cannot ship without" litmus test</check>
<check>Should-haves and could-haves are genuinely deferrable</check>

<question>Is alignment matrix complete?</question>
<check>Every requirement has tech and task mapping</check>
<check>Misalignments identified with specific issues</check>

<question>Are red flags documented?</question>
<check>Specific instances of feature bloat, gold-plating, tech showboating, etc.</check>

<question>Did agent perform CoVe validation?</question>
<check>verification_confirmation section present</check>
<check>All 10 CoVe questions addressed</check>

<question>Are recommendations actionable?</question>
<check>Each recommendation has specific action (keep/simplify/defer/remove/clarify)</check>
<check>Justifications cite requirements, constraints, or litmus tests</check>

<question>Is constraint validation present?</question>
<check>Timeline, budget, resource checks with aligned/not-aligned status</check>

<question>Is sign-off decision justified?</question>
<check>APPROVE/REVISE/REJECT matches scope creep risk level and findings</check>
</orchestrator_validation>
```

**Write to Memory**:

```bash
# Write scope validation to memory
code-tools create_file \
  --file .claude/memory/scope-validation-$ARGUMENTS.md \
  --content @- \
  --add-last-line-newline <<EOF
{Agent's scope validation document content}
EOF
```

### Phase 4: Quality Gates

Before considering scope validation complete, verify:

**Completeness Gates**:

- [ ] Core scope baseline extracted from requirements
- [ ] All requirements validated with 7-question framework
- [ ] All technology choices validated with 6-question framework
- [ ] All tasks validated with 7-question framework
- [ ] MVP defined with MoSCoW prioritization
- [ ] Alignment matrix shows requirement ↔ tech ↔ task relationships
- [ ] Red flags documented with specific examples
- [ ] Recommendations categorized (keep/simplify/defer/remove/clarify)
- [ ] Constraint validation (timeline, budget, resources)
- [ ] Sign-off decision with justification
- [ ] User confirmed MVP scope

**Quality Gates**:

- [ ] Every must-have passes "cannot ship without" litmus test
- [ ] Should-haves and could-haves are genuinely deferrable
- [ ] No requirements flagged as must-have without user explicit request
- [ ] Over-engineered tech has simpler alternative suggested
- [ ] Orphaned tasks (no requirement) are flagged for removal
- [ ] Scope creep risk level justified by data
- [ ] Recommendations have effort/cost savings estimates

**Evidence Gates**:

- [ ] Every validation cites specific requirement IDs
- [ ] Verdicts justified with litmus test results
- [ ] Red flags have specific examples (not generic claims)
- [ ] Alignment issues have clear problem descriptions
- [ ] Constraint violations have quantitative data (hours, cost)

## Error Handling

**Agent Returns Incomplete Validation**:

```
If missing required validations:
  - Report: "Scope validation incomplete - missing {requirement/tech/task validations}"
  - Re-invoke agent with specific instruction to validate all items
  - Do NOT accept incomplete validation
```

**Agent Flags Everything as Must-Have**:

```
If >80% of requirements are must-have:
  - Report: "MVP definition not ruthless enough - too many must-haves"
  - Re-invoke agent: "Apply stricter litmus test: can we ship without this?"
  - Do NOT accept bloated MVP
```

**Missing Prerequisites**:

```
If requirements-{feature}.md not found:
  - Cannot validate scope without requirements
  - Recommend: /gather-requirements {feature} first
  - Exit with error message
```

**Agent Doesn't Apply Litmus Test**:

```
If validation blocks missing mvp_litmus_test:
  - Re-invoke agent: "Apply MVP litmus test to ALL requirements and tasks"
  - Do NOT accept validation without litmus tests
```

**Validation Fails**:

```
If orchestrator validation checklist fails:
  - Identify specific failures
  - Re-invoke agent with corrective instructions
  - Do NOT write to memory until validation passes
```

## Success Criteria

Scope validation is successful when:

- ✅ Every item verified against original user request
- ✅ MVP is clearly defined and ruthlessly minimal
- ✅ Scope creep items identified and categorized
- ✅ Recommendations are specific and actionable
- ✅ Timeline/budget alignment validated
- ✅ User knows exactly what is/isn't included in MVP
- ✅ Development team has clear boundaries
- ✅ Document written to .claude/memory/scope-validation-{slug}.md

## Output

Comprehensive scope validation artifact in `.claude/memory/scope-validation-{slug}.md` ready for implementation.

**Next Steps**:
- If APPROVED: Proceed to `/implement-feature {feature-slug}`
- If REVISE_REQUIRED: Address recommendations, update artifacts, re-run validation
- If REJECT: Major rework of requirements/plan needed
