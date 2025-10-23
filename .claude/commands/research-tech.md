---
allowed-tools: Bash, Read, WebFetch, Write
argument-hint: [feature-slug]
description: Research and recommend technology stack with Step-Back prompting and source grounding
---

# Technology Research Command

Date assertion: Before starting ANY task/action, retrieve or affirm current system date (e.g., "System date: YYYY-MM-DD") to ground time-sensitive reasoning.

**Feature slug**: $ARGUMENTS

Act as a senior software architect specializing in technology selection and evaluation.

## Objective

Conduct comprehensive technology research that produces justified, comparison-based recommendations grounded in actual documentation and best practices.

## Methodology

### Phase 1: Context Gathering

Use code-tools to understand the project:

```bash
# Retrieve requirements
code-tools read_file --path .claude/memory/requirements-$1.md

# Analyze existing stack
code-tools search_file --glob "package.json" --limit 5
code-tools search_file --glob "requirements.txt" --limit 5
code-tools search_file --glob "pom.xml" --limit 5
code-tools search_file --glob "Cargo.toml" --limit 5
code-tools search_file --glob "go.mod" --limit 5

# Read detected dependency files
code-tools read_file --path {detected-file}

# Check past tech decisions
code-tools search_memory --dir .claude/memory --query "technology architecture decisions" --topk 5
```

### Phase 2: Step-Back Prompting

Before diving into specific technologies, answer these abstract questions:

```
<step_back_analysis>
**Architectural Pattern**:
- What fundamental pattern applies? (monolith, microservices, serverless, event-driven, etc.)
- Why is this pattern appropriate for the requirements?

**Technical Challenges**:
1. {Challenge}: {Why it matters}
2. {Challenge}: {Why it matters}

**Industry Standards**:
- According to {source/industry practice}, the standard approach for {this type of feature} is {approach}
- Rationale: {why this is the standard}

**Scale Considerations**:
- Expected load: {concurrent users, requests/sec, data volume}
- Growth projection: {how this might scale}
- Performance requirements: {response times, throughput}
</step_back_analysis>
```

### Phase 3: Technology Research (For Each Category)

For relevant categories (frontend, backend, database, infrastructure):

#### Research 2-3 Viable Options

For each option:

```bash
# Fetch official documentation
code-tools fetch_content --url {official-docs-url}

# Research best practices
code-tools fetch_content --url {best-practices-guide}

# Check community resources (if applicable)
code-tools fetch_content --url {benchmarks or community-discussions}
```

#### Document Each Option with XML Structure

```xml
<technology_option>
  <name>{Technology Name}</name>
  <category>{Frontend|Backend|Database|Infrastructure}</category>
  <version>{Recommended version}</version>

  <official_documentation>
    <url>{URL}</url>
    <summary>{Key capabilities from docs}</summary>
  </official_documentation>

  <strengths>
    <strength source="{URL or 'official docs'}">
      {Strength with specific feature citation}
    </strength>
  </strengths>

  <weaknesses>
    <weakness source="{URL or known limitation}">
      {Weakness with explanation}
    </weakness>
  </weaknesses>

  <requirements_alignment>
    <requirement id="{REQ-ID}" status="Met|Partial|Not Met">
      {How this technology addresses the requirement}
    </requirement>
  </requirements_alignment>

  <fit_assessment>
    <learning_curve>{Low|Medium|High} - {explanation}</learning_curve>
    <ecosystem_maturity>{Assessment}</ecosystem_maturity>
    <community_size>{Size and activity level}</community_size>
    <integration_with_existing>{How it integrates}</integration_with_existing>
  </fit_assessment>

  <performance_characteristics>
    {Benchmarks, known performance traits, citations}
  </performance_characteristics>
</technology_option>
```

### Phase 4: Comparative Analysis

Create comparison matrix:

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Meets FR-001 | ✅ | ✅ | ⚠️ |
| Meets NFR-PERF-001 | ✅ (cite) | ⚠️ (cite) | ❌ |
| Learning Curve | Medium | Low | High |
| Ecosystem Maturity | Mature (cite) | Emerging | Mature |
| Integration | Native | Adapter needed | Complex |
| Cost | Open source | Freemium | Enterprise |
| Performance | {metric} | {metric} | {metric} |
| Community | {size} | {size} | {size} |

### Phase 5: "According to..." Prompting

For EVERY factual claim, use grounded language:

**Good Examples**:

- "According to the React documentation (react.dev), concurrent features enable..."
- "Based on TechEmpower benchmarks (techempower.com/benchmarks), FastAPI achieves..."
- "MongoDB's official scaling guide states that..."
- "A 2024 Stack Overflow survey shows that..."

**Avoid Ungrounded Claims**:

- ❌ "React is the best framework"
- ❌ "MongoDB is very scalable"
- ❌ "Everyone uses PostgreSQL"

### Phase 6: Chain-of-Verification (CoVe)

Verify your analysis by checking:

```
<verification_questions>
1. ✅ Does each recommendation directly address stated requirements?
2. ✅ Are all pros/cons backed by sources or clear reasoning?
3. ✅ Have I provided at least 2 alternatives for key technology choices?
4. ✅ Are performance claims backed by benchmarks or documentation?
5. ✅ Have I considered the team's existing skills and stack?
6. ✅ Is the recommendation practical (not just theoretically optimal)?
7. ✅ Have I identified integration challenges with existing systems?
8. ✅ Are there any "cool tech" biases I should check?
</verification_questions>
```

### Phase 7: Create Technology Analysis Document

```bash
code-tools create_file --file .claude/memory/tech-analysis-$1.md --content @tech-analysis.txt
```

#### Document Structure

Include all of:

- Executive summary (2-3 sentences)
- Current context (existing stack, team context)
- Step-back analysis from Phase 2
- Technology options evaluated (with XML blocks from Phase 3)
- Comparative matrix from Phase 4
- Primary recommendation with full justification
- Alternative recommendation with different trade-offs
- Anti-recommendation (what NOT to use and why)
- Best practices with sources
- References (all URLs used)
- Verification checklist confirmation

## Hallucination Prevention Strategies

1. **Always Cite Sources**: Use WebFetch to retrieve actual documentation
2. **Avoid Absolutes**: Replace "X is the best" with "According to {source}, X performs better in {context}"
3. **Acknowledge Uncertainty**: If you can't verify a claim, say so
4. **Compare Fairly**: Present balanced pros/cons
5. **Check Recency**: Note if information might be outdated

## Success Criteria

Your analysis is successful if:

- ✅ Every recommendation is grounded in sources
- ✅ Requirements alignment is explicitly shown
- ✅ At least 2 viable alternatives are presented
- ✅ Trade-offs are clearly articulated
- ✅ Integration with existing stack is addressed
- ✅ Implementation risks are identified with mitigations
- ✅ User can make informed decision from your analysis

Begin research now using Step-Back prompting and "According to..." grounding.
