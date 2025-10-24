---
allowed-tools: Task, Bash(code-tools:*), Read, WebFetch
argument-hint: [feature-slug]
description: Orchestrate technology research by delegating to tech-researcher agent
---

# Technology Research Orchestrator

**System date assertion**: Retrieve current system date via `date +%Y-%m-%d` before proceeding
**Feature slug**: $ARGUMENTS

Act as a technology research orchestrator coordinating evidence-based technology evaluation using systematic ReAct (Reasoning + Acting) cycles with Chain of Verification validation.

## Objective

Execute comprehensive technology research through iterative Thought-Action-Observation cycles, validating findings at each stage before delegating to specialized tech-researcher agent.

## Methodology: ReAct + Chain of Verification

### Phase 0: Architectural Context Discovery (ReAct Cycle 1)

**Thought 1**: Before evaluating specific technologies, I need architectural context to constrain research scope and identify relevant patterns.

**Action 1**: Execute context gathering
```bash
# System date
date +%Y-%m-%d

# Load feature requirements
code-tools read_file --path .claude/memory/requirements-$ARGUMENTS.md 2>/dev/null || echo "ERROR: Requirements not found. Run /gather-requirements first."

# Load existing tech baseline
code-tools read_file --path .claude/memory/tech-stack-baseline.md 2>/dev/null || echo "No tech baseline found"

# Load architecture decisions
code-tools read_file --path .claude/memory/architecture-decisions.md 2>/dev/null || echo "No ADRs found"

# Detect current stack
code-tools search_file --glob "package.json" --limit 1
code-tools search_file --glob "requirements.txt" --limit 1
code-tools search_file --glob "pom.xml" --limit 1
code-tools search_file --glob "Cargo.toml" --limit 1
code-tools search_file --glob "go.mod" --limit 1

# Search for related tech analysis
code-tools search_memory --dir .claude/memory --query "$ARGUMENTS technology stack dependencies" --topk 5
```

**Observation 1**: [Capture loaded context: requirements summary, current stack, ADRs, related decisions]

**Thought 2**: Based on requirements and existing stack, I can identify the architectural pattern and key technical challenges that will guide technology selection.

**Action 2**: Analyze requirements to extract:
- Fundamental architectural pattern (monolithic, microservices, serverless, event-driven, JAMstack, modular monolith, SOA)
- Key technical challenges (performance, scale, complexity, integration, security, reliability)
- Scale and performance requirements (concurrent users, throughput, latency targets, availability SLA)
- Industry standards applicable to this domain

**Observation 2**: [Document architectural pattern, challenges, scale requirements, industry standards]

**Verification Checkpoint 1**: Before proceeding to technology research, verify:
```xml
<verification_checkpoint_1>
<question>Do I have sufficient requirements to guide technology selection?</question>
<check>Confirm functional and non-functional requirements are documented with IDs</check>
<check>If missing: report error and recommend /gather-requirements first</check>

<question>Have I identified the architectural pattern correctly?</question>
<check>Pattern aligns with requirements (e.g., real-time needs suggest event-driven)</check>
<check>Pattern is explicit, not assumed</check>

<question>Are technical challenges prioritized by impact?</question>
<check>Challenges ranked High/Medium/Low based on requirements</check>
<check>Each challenge has "why it matters" justification</check>

<question>Do scale requirements provide concrete targets?</question>
<check>Numbers specified for: concurrent users, requests/sec, data volume, response times</check>
<check>Growth projections over 1-3 years documented</check>
<check>If vague: flag as open question for user clarification</check>
</verification_checkpoint_1>
```

**Action 3**: Present architectural context summary to user:
```
Based on analysis of requirements and existing codebase:

ARCHITECTURAL PATTERN: {identified pattern}
JUSTIFICATION: {why this pattern fits requirements}

KEY TECHNICAL CHALLENGES (prioritized):
1. {Challenge} - Priority: HIGH - Why: {impact on system}
2. {Challenge} - Priority: MEDIUM - Why: {impact on system}
...

SCALE REQUIREMENTS:
- Load: {concurrent users, requests/sec, data volume}
- Growth: {1-year, 3-year projections}
- Performance: {response time, throughput, latency targets}
- Availability: {uptime SLA}

INDUSTRY STANDARDS: {applicable reference architectures, compliance needs}

EXISTING CONSTRAINTS:
- Current stack: {detected technologies}
- Architectural decisions: {from ADRs}
- Team context: {skills, size if known}

Does this architectural understanding accurately represent the feature requirements? Any corrections or clarifications?
```

**Observation 3**: [User confirms or corrects architectural understanding]

**Thought 3**: With validated architectural context, I can now construct research parameters for the tech-researcher agent that will focus on relevant technology categories and evaluation criteria.

### Phase 1: Research Scope Definition (ReAct Cycle 2)

**Thought 4**: Given the architectural pattern and challenges, I need to identify which technology categories require research.

**Action 4**: Map architectural pattern and challenges to technology categories:
```
Pattern: {monolithic|microservices|serverless|event-driven|JAMstack|modular monolith|SOA}
→ Categories: {Frontend, Backend, Database, Caching, Messaging, Infrastructure, Testing, etc.}

Challenges:
- {Challenge 1} → Requires evaluation of: {specific tech category}
- {Challenge 2} → Requires evaluation of: {specific tech category}
```

**Observation 4**: [List of technology categories requiring research: Frontend, Backend, Database, Caching, Messaging, Infrastructure, Testing, etc.]

**Verification Checkpoint 2**: Validate research scope:
```xml
<verification_checkpoint_2>
<question>Have I identified all relevant technology categories?</question>
<check>Each key challenge maps to at least one technology category</check>
<check>Integration points with existing stack considered</check>
<check>No critical categories missed (e.g., authentication, monitoring, deployment)</check>

<question>Is the research scope manageable?</question>
<check>Focused on 3-6 major categories (not trying to research everything)</check>
<check>Prioritized by impact on critical requirements</check>

<question>Are evaluation criteria clear for each category?</question>
<check>Success criteria tied to specific FR/NFR IDs</check>
<check>Trade-off dimensions identified (performance vs complexity, cost vs scalability)</check>
</verification_checkpoint_2>
```

**Thought 5**: Research scope is validated. Now I'll delegate to tech-researcher agent with comprehensive context and structured verification requirements.

### Phase 2: Agent Delegation with ReAct Framework (ReAct Cycle 3)

**Action 5**: Invoke tech-researcher agent with structured research protocol:

````
Perform comprehensive technology research for feature: $ARGUMENTS

**Role**: Senior Software Architect specializing in evidence-based technology evaluation and comparative analysis.

**Architectural Context**:
{Paste validated architectural understanding from Phase 0}

**Existing Project Context**:
```xml
<existing_context>
<requirements>
{Functional and non-functional requirements from requirements-{feature}.md}
{Key constraints, performance targets, scale requirements with FR/NFR IDs}
</requirements>

<current_tech_stack>
{Detected stack from package.json/requirements.txt/etc}
{Existing frameworks, libraries, versions}
</current_tech_stack>

<architectural_constraints>
{From architecture-decisions.md if available}
{Patterns that must be followed, prohibited technologies}
</architectural_constraints>

<tech_baseline>
{From tech-stack-baseline.md if available}
{Approved dependencies, version constraints, prohibited libraries}
</tech_baseline>

<related_tech_decisions>
{Similar features' tech choices from memory search}
</related_tech_decisions>
</existing_context>
```

**Research Protocol**: Execute ReAct cycles for each technology category

### ReAct Research Template (Apply to each category)

**CATEGORY**: {Frontend|Backend|Database|Caching|Messaging|Infrastructure|Testing}

**Thought 1**: I need to identify 2-3 viable technology options for this category based on industry standards and requirements.

**Action 1**: Research viable options
- Query industry standards: "According to {domain} best practices, what are standard technologies for {use case}?"
- WebFetch official documentation for candidate technologies
- Identify version recommendations from official sources

**Observation 1**: [List of 2-3 candidate technologies with official docs URLs]

**Thought 2**: For each candidate, I need to gather evidence about capabilities, performance, and fit.

**Action 2**: For EACH candidate technology, execute research actions:
```
Action 2a: WebFetch official documentation
- URL: {official-docs-url}
- Extract: key capabilities, main use cases, core features relevant to requirements

Action 2b: WebFetch performance benchmarks
- Search for: "{technology} benchmark {use case}"
- Cite sources: TechEmpower, official docs, case studies
- Record: specific metrics (req/s, latency, throughput, memory)

Action 2c: WebFetch best practices guides
- URL: {official best practices or authoritative guides}
- Extract: common pitfalls, integration patterns, optimization techniques

Action 2d: WebFetch ecosystem information
- GitHub repo: stars, active contributors, recent commits, issue resolution time
- Package registry: downloads, version history, breaking changes
- Community: Stack Overflow questions, tutorial availability
```

**Observation 2**: [For each candidate, document research findings with source URLs]

**Thought 3**: I have gathered evidence. Now I need to evaluate each technology against specific requirements.

**Action 3**: Map technologies to requirements
```
For each candidate:
  For each critical requirement (FR-XXX, NFR-XXX):
    - Status: Fully Met|Partially Met|Not Met
    - Evidence: {specific feature or capability from docs}
    - Source: {URL citation}
```

**Observation 3**: [Requirements alignment matrix for all candidates]

**Thought 4**: I need to assess practical fit considering team context, integration complexity, and operational burden.

**Action 4**: Evaluate fit dimensions
```
For each candidate:
  - Learning curve: {Low|Medium|High} based on team skills
  - Ecosystem maturity: {Mature|Emerging|Experimental} with evidence
  - Community support: {size metrics, activity metrics, resource availability}
  - Integration with existing stack: {Native|Adapter|Custom} with complexity assessment
  - Maintenance burden: {update frequency, breaking changes history, LTS commitment}
  - Cost: {licensing, infrastructure, operational}
```

**Observation 4**: [Fit assessment for all candidates with justifications]

**Thought 5**: I have comprehensive data on all candidates. Now I'll create comparative analysis with weighted scoring.

**Action 5**: Generate comparison matrix
```
| Criterion          | Option A        | Option B        | Option C        | Weight |
| ------------------ | --------------- | --------------- | --------------- | ------ |
| Meets FR-001       | ✅ Full (cite)  | ✅ Full (cite)  | ⚠️ Partial (cite) | HIGH   |
| Meets NFR-PERF-001 | ✅ (cite)       | ⚠️ (cite)       | ❌ (reason)     | HIGH   |
| Learning Curve     | Medium          | Low             | High            | MEDIUM |
| Ecosystem Maturity | Mature (source) | Emerging        | Mature (source) | MEDIUM |
| Integration        | Native          | Adapter         | Complex         | HIGH   |
| Cost               | {$ source}      | {$ source}      | {$ source}      | LOW    |
| Performance        | {metric source} | {metric source} | {metric source} | HIGH   |
| Community Size     | {data source}   | {data source}   | {data source}   | LOW    |
| Risk Level         | Low (why)       | Medium (why)    | High (why)      | HIGH   |

SCORING LOGIC:
- HIGH weight: 3x multiplier
- MEDIUM weight: 2x multiplier
- LOW weight: 1x multiplier
- ✅ = 3 points, ⚠️ = 2 points, ❌ = 0 points

WEIGHTED SCORES:
Option A: {calculated score}
Option B: {calculated score}
Option C: {calculated score}
```

**Observation 5**: [Comparison matrix with weighted scores]

**Thought 6**: Based on scores and qualitative factors, I can recommend the best-fit technology for this category.

**Action 6**: Formulate category recommendation
```xml
<category_recommendation>
  <primary_choice>
    <technology>{Name version}</technology>
    <justification>
      {Why best fit based on weighted scoring}
      {Key differentiators vs alternatives}
      {How it addresses critical requirements with FR/NFR IDs}
      {Sources supporting recommendation}
    </justification>
    <score>{weighted score}</score>
  </primary_choice>

  <alternative_choice>
    <technology>{Name version}</technology>
    <use_case>
      {When to choose this instead}
      {Different trade-offs it offers}
    </use_case>
    <score>{weighted score}</score>
  </alternative_choice>

  <anti_recommendation>
    <technology>{Name}</technology>
    <reasons>
      {Why NOT to use for this feature}
      {Specific gaps or risks with evidence}
    </reasons>
  </anti_recommendation>
</category_recommendation>
```

**Observation 6**: [Category recommendation with primary, alternative, and anti-recommendation]

**REPEAT ReAct Research Template for all technology categories**

### Chain of Verification: Pre-Finalization Validation

**Thought N**: Before finalizing recommendations, I must verify the analysis for completeness, accuracy, and bias.

**Action N**: Execute comprehensive verification checklist

```xml
<verification_checklist>
<verification_1>
  <question>Does each recommendation directly address stated requirements?</question>
  <action>Cross-reference every recommended tech against FR/NFR IDs</action>
  <status>PASS|FAIL: {findings}</status>
</verification_1>

<verification_2>
  <question>Are all pros/cons backed by sources or clear reasoning?</question>
  <action>Audit 100% of strength/weakness claims for source URLs or logical explanations</action>
  <status>PASS|FAIL: {findings}</status>
</verification_2>

<verification_3>
  <question>Have I provided at least 2 alternatives for key technology choices?</question>
  <action>Count options per category - verify 2-3 options evaluated</action>
  <status>PASS|FAIL: {findings}</status>
</verification_3>

<verification_4>
  <question>Are performance claims backed by benchmarks or documentation?</question>
  <action>Verify all performance metrics cite specific benchmarks with URLs</action>
  <status>PASS|FAIL: {findings}</status>
</verification_4>

<verification_5>
  <question>Have I considered team's existing skills and stack?</question>
  <action>Verify learning curve assessments reference current stack from context</action>
  <action>Verify integration complexity considers existing tech baseline</action>
  <status>PASS|FAIL: {findings}</status>
</verification_5>

<verification_6>
  <question>Is the recommendation practical (not just theoretically optimal)?</question>
  <action>Verify cost analysis includes infrastructure + operational costs</action>
  <action>Verify risk assessment identifies blockers with mitigations</action>
  <status>PASS|FAIL: {findings}</status>
</verification_6>

<verification_7>
  <question>Have I identified integration challenges with existing systems?</question>
  <action>Verify integration section addresses current stack compatibility</action>
  <action>Verify migration path outlined if replacing current tech</action>
  <status>PASS|FAIL: {findings}</status>
</verification_7>

<verification_8>
  <question>Are there any "cool tech" biases I should check?</question>
  <action>Flag bleeding-edge choices - verify compelling justification exists</action>
  <action>Verify preference for proven tech over hype-driven choices</action>
  <status>PASS|FAIL: {findings}</status>
</verification_8>

<verification_9>
  <question>Have I checked for hallucinated features or capabilities?</question>
  <action>Verify every claimed feature against official documentation</action>
  <action>Confirm no assumptions about what technology "probably supports"</action>
  <status>PASS|FAIL: {findings}</status>
</verification_9>

<verification_10>
  <question>Is version information current and accurate?</question>
  <action>Verify recommended versions are latest stable with release dates</action>
  <action>Confirm no deprecated or EOL versions recommended</action>
  <status>PASS|FAIL: {findings}</status>
</verification_10>
</verification_checklist>
```

**Observation N**: [Verification results - PASS/FAIL for each check with specific findings]

**Thought N+1**: If any verification checks FAIL, I must revise the analysis before presenting to user.

**Action N+1**: [If FAIL found] Correct identified issues:
- Re-research claims lacking sources
- Remove or qualify unverified statements
- Add missing alternatives
- Strengthen requirements alignment
- Address bias or hallucination issues

**Observation N+1**: [Revised analysis with corrections applied]

**Thought N+2**: Verification complete (all PASS). Now I'll structure the comprehensive technology analysis document.

**Action N+2**: Generate final technology analysis document

```xml
<tech_analysis>
  <metadata>
    <feature_slug>{feature}</feature_slug>
    <created>{current date}</created>
    <analyst>Tech Researcher Agent</analyst>
    <status>Draft</status>
  </metadata>

  <executive_summary>
    {2-3 sentence overview of recommended stack with primary justification}
    {Key trade-offs highlighted}
  </executive_summary>

  <architectural_context>
    <pattern>
      {Identified pattern: monolith, microservices, etc.}
      {Justification based on requirements}
    </pattern>

    <technical_challenges>
      <challenge priority="High|Medium|Low">
        <description>{Challenge}</description>
        <why_matters>{Impact on system}</why_matters>
        <tech_implications>{What types of tech address this}</tech_implications>
      </challenge>
    </technical_challenges>

    <industry_standards source="{URL or domain knowledge}">
      {Standard approach for this feature type in this domain}
      {Rationale for standard}
      {Common technology choices}
    </industry_standards>

    <scale_requirements>
      <load_profile>
        {Expected: concurrent users, requests/sec, data volume}
        {Growth: 1-year, 3-year projections}
      </load_profile>
      <performance_targets>
        {Response time, throughput, availability SLA}
      </performance_targets>
    </scale_requirements>
  </architectural_context>

  <current_context>
    <existing_stack>
      {Technologies currently in use}
      {Versions, frameworks, libraries}
    </existing_stack>

    <constraints>
      {Architectural decisions constraining choices}
      {Budget, timeline, compliance requirements}
    </constraints>
  </current_context>

  <technology_categories>
    <category name="{Frontend|Backend|Database|Caching|Messaging|Infrastructure|Testing}">
      <research_summary>
        {Brief summary of research process for this category}
        {Number of options evaluated, sources consulted}
      </research_summary>

      <options_evaluated>
        <technology_option>
          <name>{Technology Name}</name>
          <version>{Recommended version with release date}</version>

          <official_documentation>
            <url>{Primary documentation URL}</url>
            <summary>
              {Key capabilities from official docs}
              {Main use cases}
              {Core features relevant to requirements}
            </summary>
          </official_documentation>

          <strengths>
            <strength source="{URL or 'official docs:{page}'}">
              {Specific strength with feature citation}
              {Why matters for requirements}
            </strength>
            <!-- 4-6 strengths, each with source -->
          </strengths>

          <weaknesses>
            <weakness source="{URL or known limitation}">
              {Specific weakness with explanation}
              {Impact on use case}
            </weakness>
            <!-- 3-5 weaknesses, each with source or reasoning -->
          </weaknesses>

          <requirements_alignment>
            <requirement id="{FR-XXX or NFR-XXX}" status="Fully Met|Partially Met|Not Met">
              {How technology addresses requirement}
              {Specific features providing this}
              {Source: documentation or benchmark citation}
            </requirement>
            <!-- Map ALL critical requirements -->
          </requirements_alignment>

          <fit_assessment>
            <learning_curve severity="Low|Medium|High">
              {Explanation based on team skills}
              {Time to productivity estimate}
            </learning_curve>

            <ecosystem_maturity>
              {Mature|Emerging|Experimental}
              {Age, stability, backward compatibility record}
              {Source: release history, adoption metrics}
            </ecosystem_maturity>

            <community_support>
              {Size: GitHub stars, downloads, contributors}
              {Activity: recent commits, issue resolution}
              {Resources: tutorials, Stack Overflow}
              {Source: GitHub, npm, PyPI, etc.}
            </community_support>

            <integration_with_existing>
              {How integrates with current stack}
              {Native|Official Adapter|Third-party|Custom}
              {Integration complexity assessment}
            </integration_with_existing>

            <maintenance_burden>
              {Update frequency, breaking changes history}
              {Long-term support commitment}
              {Vendor lock-in risk}
            </maintenance_burden>
          </fit_assessment>

          <performance_characteristics>
            <metric name="{requests/sec, latency, throughput, memory}">
              {Value with source citation}
              {Comparison to requirement target}
            </metric>
            <!-- Cite benchmarks: TechEmpower, official docs, case studies -->
          </performance_characteristics>

          <cost_analysis>
            <licensing>{Open source|Freemium|Commercial} - {License type}</licensing>
            <infrastructure_cost>{Estimate based on scale}</infrastructure_cost>
            <operational_cost>{Maintenance, training, support}</operational_cost>
            <total_monthly_estimate>{$X,XXX/month}</total_monthly_estimate>
          </cost_analysis>

          <risk_assessment>
            <risk severity="High|Medium|Low">
              <description>{Risk}</description>
              <probability>High|Medium|Low</probability>
              <impact>{Impact if occurs}</impact>
              <mitigation>{How to prevent or handle}</mitigation>
            </risk>
          </risk_assessment>
        </technology_option>
        <!-- 2-3 options per category -->
      </options_evaluated>

      <comparative_analysis>
        {Comparison matrix with weighted scoring from Action 5}
      </comparative_analysis>

      <category_recommendation>
        {Category recommendation from Action 6}
      </category_recommendation>
    </category>
  </technology_categories>

  <overall_recommendation>
    <recommended_stack>
      <layer name="{Frontend|Backend|Database|etc}">
        <technology>{Name version}</technology>
        <role>{What it does in stack}</role>
        <justification>{Why chosen for this layer}</justification>
      </layer>
    </recommended_stack>

    <stack_justification>
      {Comprehensive reasoning for stack as whole}
      {How components integrate}
      {How stack addresses all critical requirements}
      {Total cost of ownership estimate}
    </stack_justification>

    <integration_strategy>
      {How recommended tech integrates with existing stack}
      {Migration path if replacing current tech}
      {Integration complexity and timeline}
      {Fallback strategies if integration issues arise}
    </integration_strategy>

    <implementation_risks>
      <risk severity="High|Medium|Low">
        <description>{Risk}</description>
        <probability>High|Medium|Low</probability>
        <impact>{Impact if occurs}</impact>
        <mitigation>{How to prevent or handle}</mitigation>
        <contingency>{What to do if mitigation fails}</contingency>
      </risk>
    </implementation_risks>

    <best_practices>
      <practice source="{URL}">
        {Practice with detailed explanation}
        {Why important for this stack}
      </practice>
    </best_practices>

    <rollout_strategy>
      <phase number="1" duration="{timeframe}">
        {What to implement}
        {Success criteria}
        {Validation approach}
      </phase>
      <!-- Phased rollout with validation gates -->
    </rollout_strategy>
  </overall_recommendation>

  <alternative_stack>
    <stack_description>
      {Different set of choices with different trade-offs}
      {When this alternative would be better}
    </stack_description>

    <trade_offs>
      <gains>{What you gain vs primary recommendation}</gains>
      <losses>{What you lose vs primary recommendation}</losses>
    </trade_offs>

    <use_cases>
      {Scenarios where alternative is superior}
    </use_cases>
  </alternative_stack>

  <references>
    <documentation_sources>
      <source technology="{name}">{URL}</source>
    </documentation_sources>

    <benchmark_sources>
      <source name="{benchmark name}">{URL}</source>
    </benchmark_sources>

    <best_practice_guides>
      <source name="{guide name}">{URL}</source>
    </best_practice_guides>

    <community_resources>
      <source name="{resource name}">{URL}</source>
    </community_resources>
  </references>

  <verification_confirmation>
    {Confirmation all CoVe checks passed}
    {Summary of verification process}
    {Any assumptions or uncertainties flagged}
  </verification_confirmation>

  <open_questions>
    <question priority="High|Medium|Low">
      {Question requiring user input or further research}
      {Why this question matters}
      {Impact on recommendation if answered differently}
    </question>
  </open_questions>
</tech_analysis>
```

**Observation N+2**: [Complete technology analysis document]

**Thought N+3**: Analysis is complete and verified. I'll present summary to user for confirmation before finalizing.

**Action N+3**: Present analysis summary to user
```
TECHNOLOGY RESEARCH COMPLETE

RECOMMENDED STACK:
- {Layer 1}: {Technology} - {Justification}
- {Layer 2}: {Technology} - {Justification}
...

KEY TRADE-OFFS:
- {Trade-off 1}: {Explanation}
- {Trade-off 2}: {Explanation}

INTEGRATION COMPLEXITY: {Low|Medium|High}
TOTAL ESTIMATED COST: ${X,XXX}/month
IMPLEMENTATION TIMELINE: {estimate}

CRITICAL REQUIREMENTS COVERAGE:
- {FR-001}: ✅ {How addressed}
- {NFR-001}: ✅ {How addressed}

OPEN QUESTIONS (require your input):
1. {Question 1} - Priority: HIGH
2. {Question 2} - Priority: MEDIUM

Have I covered all technology categories relevant to this feature? Are there additional integration points or constraints I should research?
```

**Observation N+3**: [User confirms completeness or requests additional research]

**Thought N+4**: [If user requests changes] I need to iterate on specific areas based on feedback.
**Thought N+4**: [If user confirms] Research is complete and validated. Ready to write artifact.

Return final technology analysis document content ready to write to file.

````

**Observation 5**: [Tech-researcher agent returns complete technology analysis document]

### Phase 3: Orchestrator Validation (ReAct Cycle 4)

**Thought 7**: Agent has returned analysis. Before accepting it, I must validate against quality gates to ensure completeness, accuracy, and adherence to methodology.

**Action 7**: Execute orchestrator validation checklist

```xml
<orchestrator_validation>
<validation_1>
  <check>Did agent perform Step-Back analysis?</check>
  <action>Verify architectural pattern, challenges, industry standards, scale analysis present</action>
  <pass_criteria>All architectural context sections populated with evidence</pass_criteria>
  <status>PASS|FAIL: {findings}</status>
</validation_1>

<validation_2>
  <check>Did agent research 2-3 options per major category?</check>
  <action>Count technology_option blocks per category</action>
  <pass_criteria>Minimum 2 options per critical category, 1 option acceptable for minor categories</pass_criteria>
  <status>PASS|FAIL: {findings}</status>
</validation_2>

<validation_3>
  <check>Are all options documented in complete XML structure?</check>
  <action>Verify each option has: name, category, version, docs URL, strengths (4+), weaknesses (3+), requirements alignment, fit assessment, performance data, cost, risks</action>
  <pass_criteria>All required fields present for every technology_option</pass_criteria>
  <status>PASS|FAIL: {findings}</status>
</validation_3>

<validation_4>
  <check>Did agent create comparative matrices with weighted scoring?</check>
  <action>Verify tables exist for each category with weights and scores calculated</action>
  <pass_criteria>Comparison matrices present with explicit scoring methodology</pass_criteria>
  <status>PASS|FAIL: {findings}</status>
</validation_4>

<validation_5>
  <check>Are all claims source-grounded with "According to..." pattern?</check>
  <action>Spot-check 10 random factual claims for source citations (URLs or explicit reasoning)</action>
  <pass_criteria>100% of checked claims have sources; no ungrounded assertions</pass_criteria>
  <status>PASS|FAIL: {findings}</status>
</validation_5>

<validation_6>
  <check>Did agent perform Chain of Verification validation?</check>
  <action>Verify verification_confirmation section present with all 10 CoVe questions addressed</action>
  <pass_criteria>Verification checklist completed with PASS/FAIL status for each check</pass_criteria>
  <status>PASS|FAIL: {findings}</status>
</validation_6>

<validation_7>
  <check>Is output in correct XML structure?</check>
  <action>Verify all required sections present: metadata, executive_summary, architectural_context, current_context, technology_categories (with nested options), overall_recommendation, alternative_stack, references, verification_confirmation, open_questions</action>
  <pass_criteria>All required XML sections present and properly nested</pass_criteria>
  <status>PASS|FAIL: {findings}</status>
</validation_7>

<validation_8>
  <check>Are recommendations practical and justified?</check>
  <action>Verify recommendations address actual requirements with FR/NFR IDs</action>
  <action>Verify risk assessments include specific mitigations and contingencies</action>
  <action>Verify integration strategy addresses existing stack compatibility</action>
  <pass_criteria>Every recommendation maps to requirements; risks have mitigations; integration path clear</pass_criteria>
  <status>PASS|FAIL: {findings}</status>
</validation_8>

<validation_9>
  <check>Are references comprehensive and valid?</check>
  <action>Verify all cited sources listed in references section</action>
  <action>Spot-check 5 random URLs for validity</action>
  <pass_criteria>All sources catalogued; spot-checked URLs are valid</pass_criteria>
  <status>PASS|FAIL: {findings}</status>
</validation_9>

<validation_10>
  <check>Did agent avoid "cool tech" bias?</check>
  <action>Check if bleeding-edge choices have compelling justification tied to requirements</action>
  <action>Verify mature, proven technologies preferred unless specific reason</action>
  <pass_criteria>No unjustified hype-driven recommendations; trade-offs explicitly stated</pass_criteria>
  <status>PASS|FAIL: {findings}</status>
</validation_10>
</orchestrator_validation>
```

**Observation 7**: [Validation results - PASS/FAIL for each check]

**Thought 8**: Based on validation results, I need to determine if analysis is acceptable or requires agent to revise.

**Decision Branch**:
- **IF all validations PASS**: Proceed to Phase 4 (write artifact)
- **IF any validation FAILS**: Execute corrective action

**Action 8a** [If FAIL]: Re-invoke agent with corrective instructions
```
Your technology analysis has validation issues that must be corrected:

FAILED VALIDATIONS:
{List specific validation failures with details}

REQUIRED CORRECTIONS:
{Specific instructions for each failure}

Please revise the analysis to address these issues and resubmit.
```

**Observation 8a**: [Agent returns revised analysis - loop back to Action 7 for re-validation]

**Action 8b** [If PASS]: Proceed to artifact creation

**Observation 8b**: [All validations passed - ready to write memory artifact]

### Phase 4: Artifact Creation and Final Verification

**Thought 9**: Validation complete. I'll write the technology analysis to memory for use in implementation planning.

**Action 9**: Write artifact to memory
```bash
code-tools create_file \
  --file .claude/memory/tech-analysis-$ARGUMENTS.md \
  --content @- \
  --add-last-line-newline <<EOF
{Agent's verified tech analysis document content}
EOF
```

**Observation 9**: [File written to .claude/memory/tech-analysis-{slug}.md]

**Thought 10**: Artifact created. I'll perform final completeness check before reporting success.

**Action 10**: Final quality gate verification
```xml
<final_quality_gates>
<completeness_check>
  <gate>Step-back analysis addresses architectural pattern, challenges, standards, scale</gate>
  <gate>At least 2 viable options researched per major technology category</gate>
  <gate>Each option has complete XML structure with all required fields</gate>
  <gate>Comparative matrices with weighted scoring for each category</gate>
  <gate>Primary recommendation with comprehensive justification</gate>
  <gate>Alternative recommendation with different trade-offs</gate>
  <gate>Anti-recommendations (what NOT to use and why)</gate>
  <gate>Integration strategy addressing existing stack</gate>
  <gate>Risk assessment with mitigations and contingencies</gate>
  <gate>Best practices with sources</gate>
  <gate>All references listed with URLs</gate>
  <gate>User confirmed completeness</gate>
</completeness_check>

<quality_check>
  <gate>All factual claims source-grounded with "According to..." pattern</gate>
  <gate>No hallucinated features or capabilities</gate>
  <gate>Version recommendations current and accurate (checked against official releases)</gate>
  <gate>Performance claims cite specific benchmarks with URLs</gate>
  <gate>No "cool tech" bias without compelling requirement-based justification</gate>
  <gate>Requirements alignment explicitly shown with FR/NFR IDs</gate>
  <gate>Learning curve assessments reference team context from existing stack</gate>
  <gate>Cost analysis includes infrastructure + operational costs</gate>
</quality_check>

<evidence_check>
  <gate>Every strength/weakness has source citation or logical reasoning</gate>
  <gate>Every performance metric cites benchmark or official documentation</gate>
  <gate>Every best practice has source URL</gate>
  <gate>Integration assessments reference current tech baseline</gate>
  <gate>Risk mitigations are specific, actionable, and testable</gate>
</evidence_check>
</final_quality_gates>
```

**Observation 10**: [Final quality gates status - all PASS required to declare success]

**Thought 11**: All quality gates passed. Technology research is complete and artifact is ready for next phase.

**Action 11**: Report success to user
```
✓ TECHNOLOGY RESEARCH COMPLETE

ARTIFACT: .claude/memory/tech-analysis-{slug}.md

RESEARCH SUMMARY:
- Categories evaluated: {count}
- Technologies researched: {count}
- Sources cited: {count}
- Requirements mapped: {count FR + count NFR}

RECOMMENDED STACK:
{Brief summary of primary recommendations per category}

KEY INSIGHTS:
- {Insight 1}
- {Insight 2}
- {Insight 3}

NEXT STEPS:
Run /plan-implementation {feature-slug} to create detailed implementation plan based on this technology analysis.
```

**Observation 11**: [User informed of successful completion]

## Error Handling Protocols

### Error: Missing Prerequisites

**Thought**: Cannot research without requirements.
**Action**: Report error and recommend prerequisite command.
```
ERROR: Requirements not found for feature: {slug}

Technology research requires validated requirements to guide evaluation criteria.

RECOMMENDED ACTION:
Run: /gather-requirements {slug}

This will create requirements-{slug}.md which provides:
- Functional requirements (FR-XXX)
- Non-functional requirements (NFR-XXX)
- Constraints and priorities

After requirements are gathered, re-run: /research-tech {slug}
```

### Error: Agent Returns Incomplete Analysis

**Thought**: Analysis missing required sections violates quality gates.
**Action**: Identify gaps and re-invoke agent with specific completion instructions.
```
Analysis incomplete. Missing: {list of missing sections/categories}

Re-invoking agent with instruction to complete: {specific missing parts}

Do NOT accept incomplete output.
```

### Error: Agent Makes Ungrounded Claims

**Thought**: Ungrounded claims violate evidence-based methodology and risk hallucination.
**Action**: Identify unsourced claims and demand source citations.
```
Validation failed: Found {count} ungrounded claims:
- {Claim 1} - No source cited
- {Claim 2} - No source cited

Re-invoking agent with instruction:
"Please provide source citations (URLs) for the following claims: {list claims}
For each claim, either cite a URL or explain the logical reasoning if it's a deduction."

Do NOT accept ungrounded analysis.
```

### Error: User Unable to Clarify Constraints

**Thought**: Lack of clarity on constraints creates risk but shouldn't block research.
**Action**: Document as open questions, proceed with general best practices, note assumptions.
```
User unable to clarify: {constraint type}

PROCEEDING WITH ASSUMPTIONS:
- {Assumption 1} - based on: {reasoning}
- {Assumption 2} - based on: {reasoning}

DOCUMENTED IN ANALYSIS:
- open_questions section: HIGH priority for clarification before implementation
- Assumption impacts: {which recommendations depend on assumptions}

Note: Recommendations may need revision once constraints clarified.
```

### Error: Orchestrator Validation Fails

**Thought**: Validation failure indicates quality issues that could impact downstream implementation planning.
**Action**: Identify specific failures, provide corrective guidance, re-invoke agent.
```
Orchestrator validation failed on {count} checks:

VALIDATION FAILURE 1: {description}
- What's wrong: {specific issue}
- Required correction: {what agent must fix}

VALIDATION FAILURE 2: {description}
- What's wrong: {specific issue}
- Required correction: {what agent must fix}

Re-invoking agent with corrective instructions.

Do NOT write to memory until all validations pass.
```

### Error: Technology Research Inconclusive

**Thought**: If research doesn't yield clear recommendations, multiple paths may be viable.
**Action**: Present multiple viable options with equal weight, defer decision to user.
```
Research inconclusive - multiple technologies have similar fitness scores:

OPTION A: {Technology}
- Score: {X.XX}
- Best for: {scenario}
- Trade-offs: {trade-offs}

OPTION B: {Technology}
- Score: {X.XX}
- Best for: {scenario}
- Trade-offs: {trade-offs}

RECOMMENDATION:
Both options are viable. Decision depends on:
{Key decision factors}

USER INPUT NEEDED:
{Specific questions to guide final selection}
```

## Success Criteria

Technology research is complete when:

- ✅ All requirements loaded and validated (or error reported if missing)
- ✅ Architectural pattern identified with justification
- ✅ Technical challenges prioritized by impact
- ✅ Scale requirements quantified (concurrent users, throughput, latency, availability)
- ✅ 2-3 technology options evaluated per major category
- ✅ Each option documented with complete evidence (docs, benchmarks, community data)
- ✅ Requirements alignment explicitly mapped with FR/NFR IDs
- ✅ Comparative matrices created with weighted scoring
- ✅ All claims source-grounded with "According to..." pattern and URL citations
- ✅ No hallucinated features or capabilities
- ✅ Chain of Verification validation completed (all 10 checks PASS)
- ✅ Orchestrator validation completed (all 10 checks PASS)
- ✅ Primary, alternative, and anti-recommendations provided with justifications
- ✅ Integration strategy addresses existing stack compatibility
- ✅ Risk assessment includes mitigations and contingencies
- ✅ Cost analysis includes infrastructure + operational estimates
- ✅ User confirmed completeness (or open questions documented)
- ✅ All quality gates passed (completeness, quality, evidence)
- ✅ Artifact written to .claude/memory/tech-analysis-{slug}.md

## Anti-Hallucination Safeguards

Critical rules enforced throughout research process:

1. **Source Everything**: Every claim MUST cite URL or explicit reasoning - no exceptions
2. **No Assumptions**: Mark uncertain capabilities as "UNCERTAIN - requires verification"
3. **Version Accuracy**: Only recommend versions verified in official documentation with release dates
4. **Benchmark Honesty**: Only cite benchmarks actually fetched and read via WebFetch
5. **Feature Verification**: Every claimed feature verified against official documentation
6. **Avoid Absolutes**: Replace "X is the best" with "According to {source}, X performs better in {context}"
7. **Explicit Uncertainty**: Flag gaps in research rather than making up information
8. **Evidence Audit**: 100% of strength/weakness claims must have source or reasoning

## Output

Comprehensive, evidence-based technology analysis artifact ready for implementation planning phase.

**Final Artifact**: `.claude/memory/tech-analysis-{slug}.md`

**Next Command**: `/plan-implementation {feature-slug}`
