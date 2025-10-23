---
allowed-tools: Task, Bash(code-tools:*), Read, WebFetch
argument-hint: [feature-slug]
description: Orchestrate technology research by delegating to tech-researcher agent
---

# Technology Research Orchestrator

**System date assertion**: 2025-10-23
**Feature slug**: $ARGUMENTS

Act as a technology research orchestrator responsible for coordinating the tech stack evaluation workflow and ensuring comprehensive, evidence-based analysis.

## Objective

Delegate technology research to the specialized tech-researcher agent while providing necessary context, validation checkpoints, and artifact structure enforcement.

## Methodology

### Phase 0: Step-Back Prompting (Architectural Context)

Before detailed technology research, understand the architectural context:

**Step-Back Questions**:

```xml
<architectural_context>
<question>What fundamental architectural pattern applies?</question>
<patterns>
- Monolithic application
- Microservices architecture
- Serverless/FaaS
- Event-driven architecture
- JAMstack
- Modular monolith
- Service-oriented architecture (SOA)
</patterns>
<purpose>Pattern dictates technology selection constraints and integration needs</purpose>

<question>What are the key technical challenges for this feature?</question>
<challenge_categories>
Performance: High throughput, low latency, real-time processing
Scale: Concurrent users, data volume, geographic distribution
Complexity: Business logic complexity, workflow orchestration, state management
Integration: Third-party APIs, legacy systems, data synchronization
Security: Authentication, authorization, data protection, compliance
Reliability: Fault tolerance, disaster recovery, uptime requirements
</challenge_categories>

<question>What industry standards or best practices apply?</question>
<purpose>Identify reference architectures and proven patterns for this domain</purpose>
<examples>
E-commerce: PCI-DSS compliance, checkout optimization, inventory management
SaaS: Multi-tenancy, subscription billing, data isolation
Real-time: WebSocket patterns, event streaming, CQRS
Mobile: Offline-first, sync strategies, push notifications
Data-intensive: ETL patterns, data lakes, batch vs streaming
</examples>

<question>What are the scale and performance requirements?</question>
<metrics>
- Expected load: {concurrent users, requests/sec, data volume}
- Growth projection: {1 year, 3 years}
- Performance targets: {response times, throughput, latency}
- Availability: {uptime SLA, geographic redundancy}
</metrics>
</architectural_context>
```

**Reason about architectural implications**:

```
Given this is a {pattern} architecture with {challenge} challenges, I should ensure tech research covers:
- {Architecture-specific consideration 1}
- {Architecture-specific consideration 2}
- {Scale-specific requirement 1}
```

### Phase 1: Prerequisites Validation

Check for existing context before delegating:

```bash
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

**Context Summary for Agent**:

```xml
<existing_context>
<requirements>
{Summary of functional and non-functional requirements from requirements-{feature}.md}
{Key constraints, performance targets, scale requirements}
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
{Any similar features' tech choices from memory search}
</related_tech_decisions>
</existing_context>
```

### Phase 2: Agent Invocation with Comprehensive Context

Delegate to tech-researcher agent via Task tool:

```
Perform comprehensive technology research for feature: $ARGUMENTS

**Role**: Act as a Senior Software Architect specializing in technology selection, evaluation, and justified recommendation with expertise in comparative analysis and evidence-based decision-making.

**Architectural Context**:
{Paste architectural understanding from Step-Back phase}

**Existing Project Context**:
{Paste context summary from Phase 1}

**Methodology**:

Use the systematic research and comparison framework:

**Phase 1: High-Level Analysis** (Step-Back Prompting)

Before evaluating specific technologies, analyze:

1. **Architectural Pattern Alignment**
   - What fundamental pattern applies? (monolith, microservices, serverless, event-driven, etc.)
   - Why is this pattern appropriate for the requirements?
   - What technologies are typically used in this pattern?

2. **Technical Challenge Identification**
   - What are the 3-5 key technical challenges?
   - For each challenge: Why does it matter? What makes it hard?
   - What types of technologies address these challenges?

3. **Industry Standards Research**
   - According to {industry/domain} best practices, what is the standard approach for {this type of feature}?
   - What are reference architectures or proven patterns?
   - What technologies do similar systems use?

4. **Scale & Performance Analysis**
   - Expected load characteristics
   - Growth projections
   - Performance requirements and how they constrain tech choices

**Phase 2: Technology Option Research**

For each relevant category (frontend, backend, database, caching, messaging, etc.):

**Research 2-3 Viable Options** per category:

For EACH option:

1. **Fetch Official Documentation** using WebFetch
   - Primary docs URL: {official-docs-url}
   - Key capabilities summary
   - Version recommendation

2. **Research Best Practices** using WebFetch
   - Best practices guides
   - Common pitfalls
   - Integration patterns

3. **Gather Performance Data** using WebFetch
   - Benchmarks (cite source)
   - Known performance characteristics
   - Scale limits

**Document Each Option in XML Structure**:

```xml
<technology_option>
  <name>{Technology Name}</name>
  <category>{Frontend|Backend|Database|Caching|Messaging|Infrastructure|Testing}</category>
  <version>{Recommended version with justification}</version>

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
      {Why this matters for our requirements}
    </strength>
    <!-- List 4-6 strengths, each with source -->
  </strengths>

  <weaknesses>
    <weakness source="{URL or known limitation}">
      {Specific weakness with explanation}
      {Impact on our use case}
    </weakness>
    <!-- List 3-5 weaknesses, each with source or reasoning -->
  </weaknesses>

  <requirements_alignment>
    <requirement id="{FR-XXX or NFR-XXX}" status="Fully Met|Partially Met|Not Met">
      {How this technology addresses the requirement}
      {Specific features or capabilities that provide this}
      {Source: documentation or benchmark citation}
    </requirement>
    <!-- Map ALL critical requirements -->
  </requirements_alignment>

  <fit_assessment>
    <learning_curve severity="Low|Medium|High">
      {Explanation based on team skills from context}
      {Time to productivity estimate}
    </learning_curve>

    <ecosystem_maturity>
      {Mature|Emerging|Experimental}
      {Age, stability, backward compatibility track record}
      {Source: release history, adoption metrics}
    </ecosystem_maturity>

    <community_support>
      {Size: GitHub stars, downloads, active contributors}
      {Activity: recent commits, issue resolution time}
      {Resources: tutorials, Stack Overflow questions}
      {Source: GitHub, npm, PyPI, etc.}
    </community_support>

    <integration_with_existing>
      {How it integrates with current stack from context}
      {Native|Official Adapter|Third-party|Custom Integration Required}
      {Integration complexity assessment}
    </integration_with_existing>

    <maintenance_burden>
      {Update frequency, breaking changes history}
      {Long-term support commitment}
      {Vendor lock-in risk}
    </maintenance_burden>
  </fit_assessment>

  <performance_characteristics>
    <metric name="{requests/sec, latency, throughput, memory, etc}">
      {Value with source citation}
      {Comparison to requirement target}
    </metric>
    <!-- Cite benchmarks: TechEmpower, official docs, case studies -->
  </performance_characteristics>

  <cost_analysis>
    <licensing>{Open source|Freemium|Commercial} - {License type}</licensing>
    <infrastructure_cost>{Estimate based on scale requirements}</infrastructure_cost>
    <operational_cost>{Maintenance, training, support}</operational_cost>
  </cost_analysis>

  <risk_assessment>
    <risk severity="High|Medium|Low">
      {Description of risk}
      {Mitigation strategy}
    </risk>
  </risk_assessment>
</technology_option>
```

**Phase 3: Comparative Analysis**

Create comparison matrix for each technology category:

| Criterion | Option A | Option B | Option C | Weight |
|-----------|----------|----------|----------|--------|
| Meets FR-001 | ✅ Full | ✅ Full | ⚠️ Partial | HIGH |
| Meets NFR-PERF-001 | ✅ (cite) | ⚠️ (cite) | ❌ (reason) | HIGH |
| Learning Curve | Medium | Low | High | MEDIUM |
| Ecosystem Maturity | Mature (source) | Emerging | Mature (source) | MEDIUM |
| Integration | Native | Adapter | Complex | HIGH |
| Cost | Free/OSS | Freemium | Enterprise | LOW |
| Performance | {metric source} | {metric source} | {metric source} | HIGH |
| Community Size | {data source} | {data source} | {data source} | LOW |
| Risk Level | Low | Medium | High | HIGH |

**Scoring Logic**:
- HIGH weight: 3x multiplier
- MEDIUM weight: 2x multiplier
- LOW weight: 1x multiplier
- ✅ = 3 points, ⚠️ = 2 points, ❌ = 0 points

Calculate weighted scores to inform recommendation.

**Phase 4: "According to..." Source Grounding**

For EVERY factual claim, use grounded language:

**Required Patterns**:
- "According to {official docs URL}, {claim}"
- "Based on {benchmark name} at {URL}, {performance claim}"
- "{Technology}'s official {guide type} states that {claim}"
- "A {date} {source type} shows that {trend}"

**Examples of Proper Grounding**:
- "According to the React documentation (react.dev/reference), concurrent features enable non-blocking rendering"
- "Based on TechEmpower benchmarks Round 22 (techempower.com/benchmarks), FastAPI achieves 28,000 req/s on JSON serialization"
- "MongoDB's official scaling guide (docs.mongodb.com/manual/sharding) recommends sharding at 2-5GB per shard"
- "The 2024 State of JS survey (stateofjs.com) shows Next.js with 75% satisfaction rating"

**Forbidden Ungrounded Claims**:
- ❌ "React is the best framework"
- ❌ "MongoDB is very scalable"
- ❌ "Everyone uses PostgreSQL"
- ❌ "FastAPI is faster" (without comparison data)

**Phase 5: Chain-of-Verification (CoVe)**

Before finalizing recommendations, verify:

```xml
<verification_checklist>
<question>Does each recommendation directly address stated requirements?</question>
<check>Cross-reference every recommended tech against FR/NFR IDs</check>

<question>Are all pros/cons backed by sources or clear reasoning?</question>
<check>Every strength/weakness has source URL or logical explanation</check>

<question>Have I provided at least 2 alternatives for key technology choices?</question>
<check>Each major category has 2-3 evaluated options</check>

<question>Are performance claims backed by benchmarks or documentation?</question>
<check>All performance metrics cite specific benchmarks or official docs</check>

<question>Have I considered the team's existing skills and stack?</question>
<check>Learning curve assessments reference current stack from context</check>
<check>Integration complexity considers existing tech baseline</check>

<question>Is the recommendation practical (not just theoretically optimal)?</question>
<check>Cost analysis includes infrastructure + operational costs</check>
<check>Risk assessment identifies blockers and mitigations</check>

<question>Have I identified integration challenges with existing systems?</question>
<check>Integration section addresses current stack compatibility</check>
<check>Migration path from current state outlined if applicable</check>

<question>Are there any "cool tech" biases I should check?</question>
<check>Justified preference for proven tech over bleeding edge unless compelling reason</check>
<check>Hype-driven choices flagged and evaluated objectively</check>

<question>Have I checked for hallucinated features or capabilities?</question>
<check>Every claimed feature verified against official documentation</check>
<check>No assumptions about what technology "probably supports"</check>

<question>Is version information current and accurate?</question>
<check>Recommended versions are latest stable (cite release date)</check>
<check>No recommendations for deprecated or EOL versions</check>
</verification_checklist>
```

Present summary to user and ask:
> "Based on the above research and analysis, have I covered all technology categories relevant to this feature? Are there additional integration points or constraints I should research?"

**Iterate** until user confirms completeness.

**Output Requirements**:

Generate technology analysis document in the following structure (render as markdown):

```xml
<tech_analysis>
  <metadata>
    <feature_slug>{feature}</feature_slug>
    <created>2025-10-23</created>
    <analyst>Tech Researcher Agent</analyst>
    <status>Draft</status>
  </metadata>

  <executive_summary>
    {2-3 sentence overview of recommended stack with primary justification}
    {Key trade-offs highlighted}
  </executive_summary>

  <current_context>
    <existing_stack>
      {Technologies currently in use from project context}
      {Versions, frameworks, libraries}
    </existing_stack>

    <team_context>
      {Skills, experience level with relevant technologies from context if available}
      {Size and structure if relevant to tech choices}
    </team_context>

    <constraints>
      {Architectural decisions that constrain tech choices}
      {Budget, timeline, compliance requirements}
    </constraints>
  </current_context>

  <step_back_analysis>
    <architectural_pattern>
      {Pattern identified: monolith, microservices, etc.}
      {Justification based on requirements}
      {Implications for tech selection}
    </architectural_pattern>

    <technical_challenges>
      <challenge priority="High|Medium|Low">
        <description>{Challenge}</description>
        <why_it_matters>{Impact on system}</why_it_matters>
        <tech_implications>{What types of tech address this}</tech_implications>
      </challenge>
    </technical_challenges>

    <industry_standards>
      <standard source="{URL or domain knowledge}">
        {Standard approach for this type of feature in this domain}
        {Rationale for why this is standard}
        {Common technology choices}
      </standard>
    </industry_standards>

    <scale_considerations>
      <load_profile>
        {Expected concurrent users, requests/sec, data volume}
        {Growth projection over 1-3 years}
      </load_profile>

      <performance_targets>
        {Response time requirements}
        {Throughput requirements}
        {Availability/uptime SLA}
      </performance_targets>
    </scale_considerations>
  </step_back_analysis>

  <technology_categories>
    <category name="{Frontend|Backend|Database|Caching|Messaging|Infrastructure|Testing}">
      <options_evaluated>
        <!-- Include full <technology_option> XML blocks from Phase 2 -->
        <!-- 2-3 options per category -->
      </options_evaluated>

      <comparative_matrix>
        <!-- Table from Phase 3 -->
        <!-- Include weighted scoring -->
      </comparative_matrix>

      <category_recommendation>
        <primary_choice>
          <technology>{Name}</technology>
          <justification>
            {Why this is the best fit based on scoring and analysis}
            {Key differentiators vs alternatives}
            {How it addresses critical requirements}
            {Sources supporting recommendation}
          </justification>
        </primary_choice>

        <alternative_choice>
          <technology>{Name}</technology>
          <use_case>
            {When to choose this instead}
            {Different trade-offs it offers}
          </use_case>
        </alternative_choice>

        <anti_recommendation>
          <technology>{Name}</technology>
          <reasons>
            {Why NOT to use this for this feature}
            {Specific gaps or risks}
          </reasons>
        </anti_recommendation>
      </category_recommendation>
    </category>
  </technology_categories>

  <overall_recommendation>
    <recommended_stack>
      <layer name="{Frontend|Backend|Database|etc}">
        <technology>{Name version}</technology>
        <role>{What it does in the stack}</role>
      </layer>
    </recommended_stack>

    <justification>
      {Comprehensive reasoning for the stack as a whole}
      {How components integrate}
      {How stack addresses all critical requirements}
      {Total cost of ownership estimate}
    </justification>

    <integration_strategy>
      {How recommended tech integrates with existing stack}
      {Migration path if replacing current tech}
      {Integration complexity and timeline}
    </integration_strategy>

    <implementation_risks>
      <risk severity="High|Medium|Low">
        <description>{Risk}</description>
        <probability>High|Medium|Low</probability>
        <impact>{Impact if occurs}</impact>
        <mitigation>{How to prevent or handle}</mitigation>
      </risk>
    </implementation_risks>

    <best_practices source="{URL}">
      {Practice 1 with source}
      {Practice 2 with source}
      {Practice 3 with source}
    </best_practices>
  </overall_recommendation>

  <alternative_stack>
    <stack_description>
      {Different set of choices with different trade-offs}
      {When this alternative would be better}
    </stack_description>

    <trade_offs>
      {What you gain vs primary recommendation}
      {What you lose vs primary recommendation}
    </trade_offs>
  </alternative_stack>

  <references>
    <documentation_sources>
      <source>{Technology}: {URL}</source>
    </documentation_sources>

    <benchmark_sources>
      <source>{Benchmark name}: {URL}</source>
    </benchmark_sources>

    <best_practice_guides>
      <source>{Guide name}: {URL}</source>
    </best_practice_guides>

    <community_resources>
      <source>{Resource name}: {URL}</source>
    </community_resources>
  </references>

  <verification_confirmation>
    {Confirmation that all CoVe checks passed}
    {Any assumptions or uncertainties flagged}
  </verification_confirmation>

  <open_questions>
    <question priority="High|Medium|Low">
      {Question requiring user input or further research}
      {Why this question matters}
    </question>
  </open_questions>
</tech_analysis>
```

**Anti-Hallucination Safeguards**:

1. **Source Everything**: Every claim must cite URL or documented reasoning
2. **No Assumptions**: If unsure about capability, mark as "UNCERTAIN - requires verification"
3. **Version Accuracy**: Only recommend versions verified in official docs
4. **Benchmark Honesty**: Only cite benchmarks you've actually fetched and read
5. **Feature Verification**: Every claimed feature verified in official documentation
6. **Avoid Absolutes**: Replace "X is the best" with "According to {source}, X performs better in {context}"

**Best Practices**:

- **Evidence-Based**: Every recommendation grounded in sources
- **Balanced**: Present pros AND cons for all options
- **Practical**: Consider real-world constraints (cost, team skills, timeline)
- **Risk-Aware**: Identify and mitigate implementation risks
- **Integration-Focused**: Address how new tech works with existing stack
- **Testable**: Recommendations include verification/validation approach

**Iterative Refinement**:

After presenting initial analysis:
1. Ask user to confirm completeness and accuracy
2. Refine based on feedback
3. Re-verify with CoVe checklist
4. Iterate until user approves

Return final technology analysis document content ready to write to file.
```

### Phase 3: Validation and Artifact Creation

After agent completes technology research:

**Validation Checklist**:

```xml
<orchestrator_validation>
<question>Did agent perform Step-Back analysis?</question>
<check>Verify architectural pattern, challenges, industry standards, scale analysis present</check>

<question>Did agent research 2-3 options per major category?</question>
<check>Count technology_option blocks - should have multiple per category</check>

<question>Are all options documented in XML structure?</question>
<check>Verify each option has: name, category, version, docs, strengths, weaknesses, requirements alignment, fit assessment</check>

<question>Did agent create comparative matrices?</question>
<check>Verify tables with weighted scoring for each category</check>

<question>Are all claims source-grounded ("According to...")?</question>
<check>Spot-check 10 random factual claims for source citations</check>
<check>No ungrounded claims like "X is the best" without justification</check>

<question>Did agent perform CoVe validation?</question>
<check>Verify verification_confirmation section present</check>
<check>Verify all 10 CoVe questions addressed</check>

<question>Is output in correct XML structure?</question>
<check>Verify all required sections: metadata, executive_summary, current_context, step_back_analysis, technology_categories, overall_recommendation, references</check>

<question>Are recommendations practical and justified?</question>
<check>Recommendations address actual requirements with IDs</check>
<check>Risk assessment includes mitigations</check>
<check>Integration strategy addresses existing stack</check>

<question>Are references comprehensive?</question>
<check>All cited sources listed in references section</check>
<check>URLs are valid (spot-check 5 random URLs)</check>

<question>Did agent avoid "cool tech" bias?</question>
<check>Bleeding-edge choices have compelling justification</check>
<check>Mature, proven technologies preferred unless good reason</check>
</orchestrator_validation>
```

**Write to Memory**:

```bash
# Write tech analysis to memory
code-tools create_file \
  --file .claude/memory/tech-analysis-$ARGUMENTS.md \
  --content @- \
  --add-last-line-newline <<EOF
{Agent's tech analysis document content}
EOF
```

### Phase 4: Quality Gates

Before considering tech research complete, verify:

**Completeness Gates**:

- [ ] Step-back analysis addresses architectural pattern, challenges, standards, scale
- [ ] At least 2 viable options researched per major technology category
- [ ] Each option has complete XML structure with all required fields
- [ ] Comparative matrices with weighted scoring for each category
- [ ] Primary recommendation with comprehensive justification
- [ ] Alternative recommendation with different trade-offs
- [ ] Anti-recommendations (what NOT to use and why)
- [ ] Integration strategy addressing existing stack
- [ ] Risk assessment with mitigations
- [ ] Best practices with sources
- [ ] All references listed with URLs
- [ ] User confirmed completeness

**Quality Gates**:

- [ ] All factual claims source-grounded ("According to...")
- [ ] No hallucinated features or capabilities
- [ ] Version recommendations are current and accurate
- [ ] Performance claims cite specific benchmarks
- [ ] No "cool tech" bias without justification
- [ ] Requirements alignment explicitly shown with FR/NFR IDs
- [ ] Learning curve assessments reference team context
- [ ] Cost analysis includes infrastructure + operational costs

**Evidence Gates**:

- [ ] Every strength/weakness has source citation
- [ ] Every performance metric cites benchmark or official docs
- [ ] Every best practice has source URL
- [ ] Integration assessments reference current tech baseline
- [ ] Risk mitigations are specific and actionable

## Error Handling

**Agent Returns Incomplete Analysis**:

```
If missing required sections or options:
  - Report: "Tech analysis incomplete - missing {sections/categories}"
  - Re-invoke agent with specific instruction to complete missing parts
  - Do NOT accept incomplete output
```

**Agent Makes Ungrounded Claims**:

```
If spot-checking finds unsourced claims:
  - Identify specific claims lacking sources
  - Re-invoke agent: "Please provide source citations for: {claims}"
  - Do NOT accept ungrounded analysis
```

**Missing Prerequisites**:

```
If requirements-{feature}.md not found:
  - Cannot research without requirements
  - Recommend: /gather-requirements {feature} first
  - Exit with error message
```

**User Unable to Clarify Constraints**:

```
If user doesn't know tech constraints:
  - Document as open question with HIGH priority
  - Research based on general best practices
  - Note assumption in tech analysis
```

**Validation Fails**:

```
If orchestrator validation checklist fails:
  - Identify specific failures
  - Re-invoke agent with corrective instructions
  - Do NOT write to memory until validation passes
```

## Success Criteria

Technology research is successful when:

- ✅ All recommendations are evidence-based with source citations
- ✅ Requirements alignment explicitly shown with FR/NFR mapping
- ✅ At least 2 viable alternatives presented per major category
- ✅ Trade-offs clearly articulated with pros/cons
- ✅ Integration with existing stack addressed
- ✅ Implementation risks identified with mitigations
- ✅ User can make informed decision from analysis
- ✅ No hallucinated features or capabilities
- ✅ Document written to .claude/memory/tech-analysis-{slug}.md

## Output

Comprehensive technology analysis artifact in `.claude/memory/tech-analysis-{slug}.md` ready for implementation planning phase.

**Next Steps**: Run `/plan-implementation {feature-slug}` to create detailed implementation plan.
