---
allowed-tools: Task, Bash(code-tools:*), Read
argument-hint: [feature description]
description: Orchestrate comprehensive requirements gathering by delegating to requirements-analyst agent
---

# Requirements Gathering Orchestrator

**System date assertion**: Retrieve current system date via `date +%Y-%m-%d` before proceeding
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

```
# Use Read tool for project context
Read .claude/memory/project-context.md (if exists)

# Use Grep tool to search for related requirements
Grep --pattern "related feature requirements|$ARGUMENTS" --path .claude/memory --output_mode content

# Use Glob tool to find similar features
Glob --pattern "requirements-*.md" --path .claude/memory
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

### Phase 2: Two-Pass Requirements Gathering

This phase uses a two-pass workflow to enable interactive requirements gathering through handoff files.

#### Phase 2a: Question Generation (Agent Pass 1)

**Invoke requirements-analyst agent in question generation mode:**

```
# Use Task tool to invoke agent
Task(
  subagent_type="requirements-analyst",
  description="Generate requirements questions",
  prompt="""
**Mode:** generate_questions

**Feature to analyze:** $ARGUMENTS

**Task:** Generate structured requirements questions

**Context from Phase 1:**
{Paste domain context and existing project context from Phase 1}

**Instructions:**
1. Use Read tool for documentation (docs/idea.md, .claude/memory/*)
2. Apply Chain-of-Thought reasoning to understand domain
3. Generate 20-30 questions following the 5-Level Framework
4. Use Write tool to save: .claude/memory/.tmp-questions-{feature-slug}.md
5. Use YAML format for easy parsing
6. Return confirmation message with question count

Follow MODE 1 workflow in your agent instructions.
"""
)
```

**Expected Output:**

- Agent creates `.claude/memory/.tmp-questions-{slug}.md`
- Agent returns: "Questions generated - ready for user input"

#### Phase 2b: Question Asking (Orchestrator Interaction)

**Read and parse questions file:**

```
# Extract feature slug (transform to kebab-case)
FEATURE_SLUG = {lowercase($ARGUMENTS) with spaces→hyphens, alphanumeric+hyphen only}

# Use Read tool
Read .claude/memory/.tmp-questions-{FEATURE_SLUG}.md
```

**Parse YAML questions and present to user:**

Extract questions from YAML structure and present using `AskUserQuestion` tool in batches:

**Batch 1: Purpose & Goals**

```
Use AskUserQuestion tool with questions from level1_purpose section
```

**Batch 2: Functional Requirements**

```
Use AskUserQuestion tool with questions from level2_functional section
```

**Batch 3: Non-Functional Requirements**

```
Use AskUserQuestion tool with questions from level3_nfr section
```

**Batch 4: Constraints & Dependencies**

```
Use AskUserQuestion tool with questions from level4_constraints section
```

**Batch 5: Acceptance Criteria**

```
Use AskUserQuestion tool with questions from level5_acceptance section
```

**Write answers file:**

```
# Use Write tool to create answers file in YAML format
Write .claude/memory/.tmp-answers-{FEATURE_SLUG}.md:
---
# Answers for {Feature Name}
# AUTO-DELETE after requirements generated
# Answered: {current-date}

answers:
  purpose-01: "{User's answer to purpose-01}"
  purpose-02: "{User's answer to purpose-02}"
  functional-01: "{User's answer to functional-01}"
  # ... continue for all questions
---
```

**Cleanup Phase 2a artifacts:**

```
# Delete questions file (no longer needed) - use Bash tool
Bash: rm .claude/memory/.tmp-questions-{FEATURE_SLUG}.md
```

#### Phase 2c: Requirements Generation (Agent Pass 2)

**Invoke requirements-analyst agent in requirements generation mode:**

```
# Use Task tool to invoke agent
Task(
  subagent_type="requirements-analyst",
  description="Generate requirements document",
  prompt="""
**Mode:** generate_requirements

**Feature slug:** {feature-slug}

**Task:** Generate comprehensive requirements document from user answers

**Instructions:**
1. Use Read tool for: .claude/memory/.tmp-answers-{feature-slug}.md
2. Parse and analyze all user responses
3. Apply Chain-of-Thought reasoning and Chain-of-Verification
4. Generate complete requirements document
5. Use Write tool to save: .claude/memory/requirements-{feature-slug}.md
6. Return confirmation with summary statistics

Follow MODE 2 workflow in your agent instructions.

**Quality Requirements:**
- Every requirement must have source attribution ("According to user response...")
- Every requirement must have confidence level
- Flag assumptions and open questions
- Use MoSCoW prioritization for MVP definition
"""
)
```

**Expected Output:**

- Agent creates `.claude/memory/requirements-{slug}.md`
- Agent returns: "Requirements document generated" with statistics

**Cleanup Phase 2b artifacts:**

```
# Delete answers file (no longer needed) - use Bash tool
Bash: rm .claude/memory/.tmp-answers-{FEATURE_SLUG}.md
```

**Verify final artifact:**

```
# Use Glob tool to verify requirements document was created
Glob --pattern "requirements-{FEATURE_SLUG}.md" --path .claude/memory
# Should return exactly one match
```

### Phase 3: Validation

After requirements document is generated, perform validation:

**Read and validate requirements document:**

```
# Use Read tool
Read .claude/memory/requirements-{FEATURE_SLUG}.md
```

**Validation Checklist**:

```xml
<orchestrator_validation>
<question>Did agent follow 5-level framework?</question>
<check>Verify all 5 levels covered (Purpose, Functional, NFR, Constraints, Acceptance)</check>

<question>Is output in correct structure?</question>
<check>Verify all required sections present (metadata, goals, FR, NFR, constraints, MVP, etc.)</check>

<question>Are requirements testable and specific?</question>
<check>Spot-check acceptance criteria for measurability</check>
<check>No vague terms like "fast" or "user-friendly" without quantification</check>

<question>Are assumptions and open questions documented?</question>
<check>Verify assumptions have confidence levels</check>
<check>Verify open questions are prioritized</check>

<question>Is MVP clearly defined?</question>
<check>Verify MoSCoW prioritization (must/should/could have)</check>

<question>Are sources attributed?</question>
<check>Verify each requirement references user answers</check>

<question>Are temporary files cleaned up?</question>
<check>Verify .tmp-questions-{slug}.md deleted</check>
<check>Verify .tmp-answers-{slug}.md deleted</check>
</orchestrator_validation>
```

**If validation passes:**

```
Report:
- Requirements validation passed
- All temporary handoff files cleaned up
- Requirements document ready: .claude/memory/requirements-{FEATURE_SLUG}.md
```

**If validation fails:**

```
Report:
- Validation failed: {specific issues}
- Action: Review requirements document and address issues
- Keep temporary files for debugging if validation fails
```

### Phase 4: Quality Gates and Completion

Before considering requirements complete, verify:

**Completeness Gates**:

- [ ] All 5 levels of questioning addressed
- [ ] Functional requirements have acceptance criteria
- [ ] Non-functional requirements have target metrics
- [ ] Out-of-scope explicitly listed
- [ ] Dependencies identified
- [ ] MVP defined with MoSCoW prioritization
- [ ] All user answers incorporated

**Quality Gates**:

- [ ] No ambiguous terms (or defined in glossary)
- [ ] All requirements are testable
- [ ] All requirements have unique IDs (FR-001, NFR-PERF-001, etc.)
- [ ] Assumptions documented with confidence levels
- [ ] Open questions prioritized
- [ ] Every requirement has source attribution

**Traceability Gates**:

- [ ] Feature name matches argument: $ARGUMENTS
- [ ] Created date matches current system date retrieved earlier
- [ ] Status is Draft (will be updated after review)
- [ ] File saved to .claude/memory/requirements-{slug}.md

**Cleanup Verification**:

- [ ] .tmp-questions-{slug}.md deleted
- [ ] .tmp-answers-{slug}.md deleted
- [ ] Only requirements-{slug}.md remains in memory

**Present Summary to User**:

```
Requirements Gathering Complete

Feature: $ARGUMENTS
Artifact: .claude/memory/requirements-{slug}.md

Statistics:
- Functional Requirements: {N}
- Non-Functional Requirements: {N}
- Constraints: {N}
- Dependencies: {N}
- Open Questions: {N}
- Assumptions: {N}

Confidence:
- High: {N}%
- Medium: {N}%
- Low: {N}%

Next Steps:
1. Review requirements document
2. Resolve open questions if needed
3. Run /research-tech {slug} for technology analysis
```

## Error Handling

**Phase 2a Fails (Question Generation)**:

```
If agent fails to generate questions:
  - Use Read tool to verify docs/idea.md exists and is readable
  - Retry agent invocation with more explicit instructions
  - No cleanup needed (no files created yet)
```

**Phase 2b Fails (Question Asking)**:

```
If questions file not found or malformed:
  - Report: "Questions file missing or invalid"
  - Check .claude/memory/.tmp-questions-{slug}.md exists
  - If exists but malformed, ask agent to regenerate

If user unable to answer questions:
  - Mark answer as "Unknown - requires investigation"
  - Document as HIGH priority open question
  - Continue with remaining questions
  - Agent will flag this in requirements document
```

**Phase 2c Fails (Requirements Generation)**:

```
If agent fails to generate requirements:
  - Keep .tmp-answers-{slug}.md for debugging
  - Retry agent invocation
  - If retry fails, user can inspect answers file manually

If requirements document incomplete:
  - Report: "Requirements incomplete - missing {sections}"
  - Keep temporary files for debugging
  - Re-invoke agent with corrective instructions
```

**Validation Fails**:

```
If orchestrator validation checklist fails:
  - Identify specific failures
  - Keep temporary files if they still exist
  - Options:
    1. Re-run Phase 2c with corrected instructions
    2. Manually edit requirements-{slug}.md
    3. Re-run entire workflow with clarifications
```

**Cleanup Failures**:

```
If temporary files not deleted:
  - Log warning but don't fail workflow
  - User can manually run /cleanup-memory {slug}
  - Temporary files are prefixed with .tmp- for easy identification
```

## Success Criteria

Requirements gathering is successful when:

- Agent successfully generated questions (Phase 2a)
- All 20-30 questions asked to user (Phase 2b)
- User provided answers to all questions (Phase 2b)
- Agent successfully generated requirements document (Phase 2c)
- All requirements are clear, testable, and unambiguous
- No assumptions are undocumented
- Acceptance criteria are measurable
- Out-of-scope items are explicitly listed
- MVP is clearly defined with MoSCoW
- Domain-specific considerations included
- Every requirement has source attribution
- Temporary handoff files cleaned up
- Final document at .claude/memory/requirements-{slug}.md

## Output

**Primary Artifact:**
`.claude/memory/requirements-{slug}.md` - Comprehensive requirements document ready for tech research phase

**Temporary Files (deleted after completion):**

- `.claude/memory/.tmp-questions-{slug}.md` - Agent-generated questions (deleted after Phase 2b)
- `.claude/memory/.tmp-answers-{slug}.md` - User answers (deleted after Phase 2c)

**Next Steps**:

1. Review requirements document
2. Resolve any open questions flagged by agent
3. Run `/research-tech {feature-slug}` to analyze technology options
