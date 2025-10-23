---
allowed-tools: Task, Bash(code-tools:*), Read
argument-hint: [feature description]
description: Orchestrate comprehensive requirements gathering by delegating to requirements-analyst agent
---

# Requirements Gathering Orchestrator

**System date assertion**: 2025-10-23
**Feature**: $ARGUMENTS

Act as a requirements gathering orchestrator responsible for coordinating the requirements analysis workflow and ensuring completeness.

## Objective

Delegate requirements gathering to the specialized requirements-analyst agent while providing necessary context, validation checkpoints, and artifact structure enforcement.

## Methodology

### Phase 0: Step-Back Prompting (Domain Context)

Before detailed requirements gathering, understand the domain context:

**Step-Back Questions**:

```xml
<domain_context>
<question>What category of software/system is this?</question>
<examples>
- E-commerce platform
- Internal tool/admin system
- Public-facing application
- Data pipeline/ETL system
- Mobile app
- API/service
- Enterprise SaaS
</examples>
<purpose>Understanding domain helps identify relevant non-functional requirements (NFRs) and constraints</purpose>

<question>What are key factors in this domain?</question>
<domain_specific_considerations>
If e-commerce: Payment security, cart abandonment, checkout flow, inventory
If internal tool: Permissions, audit logs, bulk operations, admin workflows
If public app: Scalability, SEO, social integration, user onboarding
If data pipeline: Data quality, transformation rules, error handling, idempotency
If mobile: Offline support, battery/data usage, push notifications, app store guidelines
If API: Rate limiting, versioning, backward compatibility, documentation
If SaaS: Multi-tenancy, billing, subscription management, white-labeling
</domain_specific_considerations>

<question>What similar features or systems might inform this?</question>
<purpose>Identify analogous implementations to reference for completeness</purpose>
</domain_context>
```

**Reason about domain-specific requirements**:

```
Given this is a {domain} feature, I should ensure requirements cover:
- {Domain-specific NFR 1}
- {Domain-specific NFR 2}
- {Domain-specific constraint 1}
```

### Phase 1: Prerequisites Validation

Check for existing context before delegating:

```bash
# Load existing project context
code-tools read_file --path .claude/memory/project-context.md 2>/dev/null || echo "No project context found"

# Search for related requirements
code-tools search_memory --dir .claude/memory --query "$ARGUMENTS related feature requirements" --topk 5

# Check for similar features
code-tools list_dir --path .claude/memory --depth 1 | grep -E "requirements-.*\.md"
```

**Context Summary for Agent**:

```xml
<existing_context>
<project_overview>
{Summary from project-context.md if available}
</project_overview>

<related_features>
{List any related features found in memory search}
</related_features>

<similar_implementations>
{Any similar requirements-*.md files that might inform this}
</similar_implementations>

<technology_constraints>
{From tech-stack-baseline.md if exists - what stack must be used}
</technology_constraints>
</existing_context>
```

### Phase 2: Agent Invocation with Comprehensive Context

Delegate to requirements-analyst agent via Task tool:

```
Perform comprehensive requirements gathering for feature: $ARGUMENTS

**Role**: Act as a Requirements Gathering Specialist with expertise in structured elicitation, ambiguity resolution, and testable specification creation.

**Domain Context**:
{Paste domain understanding from Step-Back phase}

**Existing Project Context**:
{Paste context summary from Phase 1}

**Methodology**:

Use the 5-level structured questioning framework:

**Level 1: Purpose & Goals** (3-5 questions)
- What is the primary objective of this feature?
- What problem does it solve for users?
- Who are the target users/personas?
- How will success be measured?

**Level 2: Functional Requirements** (5-8 questions)
- What specific actions must users be able to perform?
- What are the key user workflows?
- What data inputs are required?
- What outputs/results are expected?
- What are the happy path scenarios?
- What are edge cases and error scenarios?

**Level 3: Non-Functional Requirements** (4-6 questions)
- Performance expectations? (response time, throughput)
- Scalability requirements? (concurrent users, data volume)
- Security/privacy requirements?
- Availability/reliability expectations?
- Accessibility requirements?
- Usability/UX expectations?

**Level 4: Constraints & Dependencies** (3-5 questions)
- Timeline or deadline constraints?
- Budget limitations?
- Technology stack preferences/constraints?
- Integration with existing systems?
- Regulatory/compliance requirements?
- Resource constraints (team size, skills)?

**Level 5: Acceptance Criteria** (2-3 questions)
- How will we know this feature is complete?
- What are the must-have vs. nice-to-have capabilities?
- What would constitute a minimum viable implementation?

**Chain-of-Verification (CoVe)**:

After gathering all requirements, verify by asking yourself:

1. ✅ Have I identified all stakeholders?
2. ✅ Are all workflows fully described?
3. ✅ Are there any ambiguous terms that need definition?
4. ✅ Have I captured measurable acceptance criteria?
5. ✅ Are there any unstated assumptions I should clarify?
6. ✅ Have I identified dependencies on other systems/features?

Present summary to user and ask:
> "Based on the above, have I captured all requirements completely? Are there any aspects I've missed or misunderstood?"

**Iterate** until user confirms completeness.

**Output Requirements**:

Generate requirements document in the following XML structure (render as markdown):

```xml
<requirements>
  <metadata>
    <feature_name>{Name}</feature_name>
    <created>2025-10-23</created>
    <analyst>Requirements Analyst Agent</analyst>
    <status>Draft</status>
  </metadata>

  <executive_summary>
    {2-3 sentence overview of the feature and its purpose}
  </executive_summary>

  <stakeholders>
    <stakeholder role="{role}">{description}</stakeholder>
  </stakeholders>

  <goals>
    <primary_goal>{goal}</primary_goal>
    <secondary_goals>
      <goal>{goal}</goal>
    </secondary_goals>
  </goals>

  <functional_requirements>
    <requirement id="FR-001" priority="High|Medium|Low">
      <description>{What the system must do}</description>
      <acceptance_criteria>
        <criterion>{Testable criterion}</criterion>
      </acceptance_criteria>
      <user_story>As a {user}, I want {capability} so that {benefit}</user_story>
    </requirement>
  </functional_requirements>

  <non_functional_requirements>
    <performance>
      <requirement id="NFR-PERF-001">
        <description>{requirement}</description>
        <target_metric>{measurable target}</target_metric>
      </requirement>
    </performance>

    <security>
      <requirement id="NFR-SEC-001">{requirement}</requirement>
    </security>

    <scalability>
      <requirement id="NFR-SCALE-001">{requirement}</requirement>
    </scalability>

    <accessibility>
      <requirement id="NFR-ACC-001">{requirement}</requirement>
    </accessibility>

    <usability>
      <requirement id="NFR-UX-001">{requirement}</requirement>
    </usability>
  </non_functional_requirements>

  <constraints>
    <constraint type="timeline">{description}</constraint>
    <constraint type="budget">{description}</constraint>
    <constraint type="technical">{description}</constraint>
    <constraint type="regulatory">{description}</constraint>
  </constraints>

  <dependencies>
    <dependency type="system">{existing system/service}</dependency>
    <dependency type="feature">{other feature}</dependency>
    <dependency type="external">{third-party service}</dependency>
  </dependencies>

  <out_of_scope>
    <item>{Explicitly what will NOT be included}</item>
  </out_of_scope>

  <assumptions>
    <assumption confidence="High|Medium|Low">{Stated assumption}</assumption>
  </assumptions>

  <open_questions>
    <question priority="High|Medium|Low">{Question requiring clarification}</question>
  </open_questions>

  <success_criteria>
    <criterion measurable="true">{How success will be measured}</criterion>
  </success_criteria>

  <mvp_definition>
    <must_have>
      <feature>{Minimum viable feature}</feature>
    </must_have>
    <should_have>
      <feature>{Important but not blocking}</feature>
    </should_have>
    <could_have>
      <feature>{Nice to have for future}</feature>
    </could_have>
  </mvp_definition>
</requirements>
```

**Anti-Hallucination Safeguards**:

1. **Ground in User Input**: Only document what the user explicitly states or confirms
2. **Flag Assumptions**: Mark anything inferred with "ASSUMPTION:" tag and confidence level
3. **Avoid Industry Jargon**: Use clear language unless user introduced specific terms
4. **Request Clarification**: If uncertain, ask rather than guess
5. **Cross-Reference**: Use existing project context to inform questions
6. **Quantify Vagueness**: Replace "fast" with "responds within 200ms" (after confirming with user)

**Best Practices**:

- **Be Specific**: Every requirement should be unambiguous
- **Be Testable**: Every requirement should have measurable acceptance criteria
- **Be Traceable**: Use unique IDs (FR-001, NFR-PERF-001, etc.)
- **Be Concise**: Avoid redundancy and unnecessary detail
- **Be Complete**: Cover all aspects (functional, non-functional, constraints)
- **Be Domain-Aware**: Include domain-specific NFRs and constraints

**Iterative Refinement**:

After presenting initial requirements:
1. Ask user to confirm completeness
2. Refine based on feedback
3. Re-verify with CoVe checklist
4. Iterate until user approves

Return final requirements document content ready to write to file.
```

### Phase 3: Validation and Artifact Creation

After agent completes requirements gathering:

**Validation Checklist**:

```xml
<orchestrator_validation>
<question>Did agent follow 5-level framework?</question>
<check>Verify all 5 levels covered (Purpose, Functional, NFR, Constraints, Acceptance)</check>

<question>Did agent perform CoVe validation?</question>
<check>Verify agent presented verification checklist to user</check>

<question>Is output in correct XML structure?</question>
<check>Verify all required sections present (metadata, goals, FR, NFR, constraints, etc.)</check>

<question>Are requirements testable and specific?</question>
<check>Spot-check acceptance criteria for measurability</check>
<check>No vague terms like "fast" or "user-friendly" without quantification</check>

<question>Are assumptions and open questions documented?</question>
<check>Verify assumptions have confidence levels</check>
<check>Verify open questions are prioritized</check>

<question>Is MVP clearly defined?</question>
<check>Verify MoSCoW prioritization (must/should/could have)</check>

<question>Did agent use Step-Back domain context?</question>
<check>Verify domain-specific NFRs included</check>
</orchestrator_validation>
```

**Write to Memory**:

```bash
# Extract feature slug from feature name
FEATURE_SLUG=$(echo "$ARGUMENTS" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')

# Write requirements to memory
code-tools create_file \
  --file .claude/memory/requirements-$FEATURE_SLUG.md \
  --content @- \
  --add-last-line-newline <<EOF
{Agent's requirements document content}
EOF
```

### Phase 4: Quality Gates

Before considering requirements complete, verify:

**Completeness Gates**:

- [ ] All 5 levels of questioning addressed
- [ ] Functional requirements have acceptance criteria
- [ ] Non-functional requirements have target metrics
- [ ] Out-of-scope explicitly listed
- [ ] Dependencies identified
- [ ] MVP defined with MoSCoW prioritization
- [ ] User confirmed completeness

**Quality Gates**:

- [ ] No ambiguous terms (or defined in glossary)
- [ ] All requirements are testable
- [ ] All requirements have unique IDs
- [ ] Assumptions documented with confidence levels
- [ ] Open questions prioritized

**Traceability Gates**:

- [ ] Feature name matches argument
- [ ] Created date is today (2025-10-23)
- [ ] Status is Draft (will be updated after review)
- [ ] File saved to .claude/memory/requirements-{slug}.md

## Error Handling

**Agent Returns Incomplete Requirements**:

```
If missing required sections:
  - Report: "Requirements incomplete - missing {sections}"
  - Re-invoke agent with specific instruction to complete missing sections
  - Do NOT accept incomplete output
```

**Agent Asks Unclear Questions**:

```
If agent's questions are confusing to user:
  - Intervene and rephrase questions for clarity
  - Guide agent to use simpler language
```

**User Unable to Answer Questions**:

```
If user doesn't know answer:
  - Document as open question with HIGH priority
  - Continue with remaining questions
  - Note assumption if necessary to proceed
```

**Validation Fails**:

```
If orchestrator validation checklist fails:
  - Identify specific failures
  - Re-invoke agent with corrective instructions
  - Do NOT write to memory until validation passes
```

## Success Criteria

Requirements gathering is successful when:

- ✅ All requirements are clear, testable, and unambiguous
- ✅ User confirms completeness and accuracy
- ✅ No assumptions are undocumented
- ✅ Acceptance criteria are measurable
- ✅ Out-of-scope items are explicitly listed
- ✅ MVP is clearly defined
- ✅ Domain-specific considerations included
- ✅ Document written to .claude/memory/requirements-{slug}.md

## Output

Comprehensive requirements artifact in `.claude/memory/requirements-{slug}.md` ready for tech research phase.

**Next Steps**: Run `/research-tech {feature-slug}` to analyze technology options.
