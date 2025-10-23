# Chain of Verification: 10 example prompts

## 1. Basic  example

```text
I need to fix a bug where users can't submit forms in our React app.
First, diagnose the likely cause and provide a solution.

Then, verify your solution by answering:

1. Does this solution handle all edge cases (disabled buttons, network errors, validation)?
2. Are there any accessibility issues I've overlooked?
3. Could this fix introduce new bugs?

After verification, provide your final recommended fix.
```

## 2. **API Design with Self-Correction** (Basic-Intermediate)

```text
Design a REST API endpoint for a multi-tenant SaaS app that allows
users to export their data.

After your initial design, verify by checking:

1. Is the endpoint following REST best practices?
2. Have I properly handled tenant isolation and authorization?
3. What happens if the export is too large to generate synchronously?
4. Are there rate limiting considerations?

Revise your design based on the verification.
```

## 3. **Performance Optimization + Chain of Thought** (Intermediate)

```text
Our Next.js app has slow page load times. Here's the Lighthouse report:
[paste report data]

Step 1: Analyze the report and list 3-5 optimization strategies.

Step 2: For each strategy, verify:

- What's the expected impact on Core Web Vitals?
- Are there trade-offs or risks?
- Does this require code changes or configuration only?

Step 3: Think through implementation order - which should we tackle first and why?

Step 4: Provide a prioritized action plan with verified recommendations.
```

## 4. **Security Review with Role Prompting** (Intermediate)

```text
You are a senior security engineer reviewing code. Analyze this authentication flow:

[paste code]

Initial review: Identify potential security vulnerabilities.

Then perform verification:

1. Check each vulnerability against OWASP Top 10 2024
2. For each issue, verify: Is this exploitable in our specific context?
3. Are there modern security features I missed (e.g., Passkeys, WebAuthn)?
4. Have I considered both common and subtle attack vectors?

Provide a final security assessment with prioritized fixes.
```

## 5. **Architecture Decision + Few-Shot** (Intermediate-Advanced)

```text
We need to choose between microservices and modular monolith for our new
e-commerce platform. Team size: 8 developers. Expected scale: 100K users in year 1.

Example of good reasoning:
"For a fintech startup with 5 devs, I'd choose modular monolith because..."

Example of poor reasoning:
"Microservices are modern, so we should use them."

Now, provide your recommendation.

Then verify by answering:

1. Have I accurately assessed our team's capability to maintain this architecture?
2. Did I consider the operational complexity and costs?
3. What assumptions am I making about growth?
4. Am I falling for any "resume-driven development" biases?

Final recommendation after verification:
```

## 6. **Database Schema Design + XML Structure** (Advanced)

```text
Design a database schema for a real-time collaborative document editor
(think Google Docs).

<initial_design>
Provide your schema with tables, relationships, and indexes.
</initial_design>

<verification>
<question_1>How does this schema handle concurrent edits without conflicts?</question_1>
<question_2>What's the query pattern for loading a document with 10K edits?</question_2>
<question_3>Have I properly indexed for the most common queries?</question_3>
<question_4>Does this scale horizontally? What are the bottlenecks?</question_4>
<question_5>Are there modern approaches I'm missing (CRDT, OT, event sourcing)?</question_5>
</verification>

<revised_design>
Provide your final schema after addressing verification concerns.
Include migration strategy if switching from your initial design.
</revised_design>
```

## 7. **AI Integration Planning + Structured Output** (Advanced)

```text
We want to add AI features to our project management tool. Budget: $5K/month.

Phase 1: Brainstorm 5 AI features that would provide real value.

Phase 2: Verification round - for each feature:
{
  "feature": "name",
  "cost_estimate": "monthly cost",
  "implementation_complexity": "1-10",
  "user_value": "high/medium/low",
  "verification_questions": [
    "Is this technically feasible with current LLMs?",
    "What's the error rate and how do we handle mistakes?",
    "Does this create privacy/security concerns?",
    "Are we solving a real problem or adding AI for AI's sake?"
  ],
  "keep_or_discard": "decision after verification"
}

Phase 3: Provide final 2-3 recommended features with implementation roadmap.
```

## 8. **Code Review with Contextual Verification** (Advanced)

```text
Review this pull request for a payment processing feature:

[paste code and PR description]

Step 1: Initial review - identify issues with code quality, logic, tests.

Step 2: Context verification:

- Pull up similar code in the codebase - am I applying standards consistently?
- Check if this follows our team's established patterns
- Verify against our payment provider's latest docs (v2024.Q3)
- Are there recent CVEs related to any dependencies used?

Step 3: For each piece of feedback, verify:

- Is this a "must fix" or "nice to have"?
- Am I being pedantic or is this genuinely important?
- Have I explained WHY, not just WHAT?

Step 4: Final review with prioritized, verified feedback.
```

## 9. **Migration Strategy + Risk Assessment** (Expert)

```text
Plan migration from our monolithic PHP app to a modern stack.
Current: Laravel + MySQL, 50K daily active users, 500K LoC.

Phase 1: Propose a migration strategy (technology choices, approach, timeline).

Phase 2: Verification through multiple lenses:

Technical verification:

- Can we maintain feature parity?
- What's the data migration strategy?
- How do we handle the 200+ background jobs?

Business verification:

- What's the risk of user-facing downtime?
- Can we deliver new features during migration?
- What's the realistic timeline with our team of 6?

Historical verification:

- Research: What do post-mortems from similar migrations teach us?
- What could go catastrophically wrong?
- Am I being overconfident in estimates?

Alternative paths:

- Should we modernize in place instead?
- Could we strangle-fig pattern this?

Phase 3: After verification, revise your strategy if needed.

Phase 4: Final migration plan with go/no-go decision framework.
```

## 10. **Observability Strategy + Multi-Technique Combo** (Expert)

```text
Role: You are a Staff Engineer implementing observability for a growing startup.

Context:

- 12 microservices
- Kubernetes on AWS
- Currently only basic logging
- Recent incidents took hours to debug
- Budget: $3K/month for tooling

Task: Design a comprehensive observability strategy.

<step_1_initial_proposal>
Provide your strategy including:

- Tooling choices (tracing, metrics, logging)
- What to instrument and how
- Alert strategy
- Cost breakdown
</step_1_initial_proposal>

<step_2_verification>
Now verify your proposal by answering:

1. Tool selection verification:
   - Did I compare at least 3 options per category?
   - Am I biased toward tools I'm familiar with?
   - Are these tools right for our scale vs enterprise scale?

2. Practical verification:
   - Can our team actually maintain this?
   - How long will instrumentation take?
   - What's the performance overhead?

3. Cost verification:
   - Will we exceed budget as we scale?
   - Are there hidden costs (egress, retention)?
   - Should we use open-source alternatives?

4. Effectiveness verification:
   - Think of our last 3 incidents - would this strategy have helped?
   - What blind spots remain?
   - How do we measure if observability improves?

5. Industry check:
   - What are companies at our stage actually using?
   - Am I over-engineering or under-engineering?
</step_2_verification>

<step_3_revision>
Based on verification, revise your strategy.
Be specific about what changed and why.
</step_3_revision>

<step_4_implementation_plan>
Provide phased rollout plan (Weeks 1-4, 5-8, 9-12)
Include success metrics to evaluate if this is working.
</step_4_implementation_plan>
```
