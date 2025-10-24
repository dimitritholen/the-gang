# Reflexion Prompting: 10 example prompts

## 1. Basic Bug Fix with Self-Reflection

```text
Fix this bug where the cart total is calculating incorrectly:

[paste code]

After providing your fix, reflect on:
1. What was my initial assumption about the bug?
2. Did I consider all calculation paths?
3. What did I miss in my first analysis?

If you find issues with your initial fix during reflection, provide an
improved solution.
```

## 2. API Design with Iterative Improvement (Basic-Intermediate)

```text
Design a REST API endpoint for uploading and processing images.

Initial design:
[provide your design]

Now reflect:
- What happens when the image is too large?
- How do I handle processing failures?
- Is this design synchronous or asynchronous? Which should it be?

Based on reflection, revise your design.

Second reflection:
- Did my revision introduce new problems?
- What edge cases still exist?

Final design after second reflection:
```

## 3. Test Writing with Coverage Reflection (Intermediate)

```text
Write unit tests for this authentication function:

[paste code]

After writing tests, reflect on your test coverage:

1. List all code paths in the function
2. Which paths did my tests cover?
3. Which paths did I miss?
4. What edge cases did I not consider?

Add additional tests based on your reflection.

Final reflection:
- Are there integration scenarios my unit tests don't cover?
- What would break in production that my tests wouldn't catch?
```

## 4. Performance Optimization + Learning Loop (Intermediate)

```text
Optimize this slow database query:

[paste query and schema]

Attempt 1: Provide your optimization.

Reflection after Attempt 1:
- Run EXPLAIN ANALYZE mentally - what's the query plan?
- Did I add appropriate indexes?
- What assumptions did I make about data distribution?

Attempt 2: Revise based on reflection.

Reflection after Attempt 2:
- Could this optimization hurt other queries?
- What's the write performance impact?
- Did I over-optimize?

Final solution with rationale for each decision.
```

## 5. Code Review with Meta-Analysis (Intermediate-Advanced)

```text
Review this PR:

[paste code and description]

Initial review:
[provide your feedback]

Now reflect on your own review:
1. Am I being too pedantic or not thorough enough?
2. Did I focus on what matters (correctness, security) or style nitpicks?
3. Is my feedback actionable with clear examples?
4. What biases am I bringing to this review?

Revised review incorporating your reflections:

Meta-reflection:
- If I received this review, would I find it helpful?
- What's one thing I could improve about how I give feedback?
```

## 6. Architecture Decision + Failure Analysis (Advanced)

```text
Design a caching strategy for a high-traffic e-commerce site.

Initial proposal:
[provide your design]

Failure scenario simulation:
Imagine your caching strategy has been in production for 3 months.
What are the 3 most likely ways it failed or caused issues?

For each failure:
1. What was the root cause?
2. What signal did I miss during design?
3. How would I have prevented this?

Revised design incorporating failure learnings:

Second-order reflection:
- What new failure modes did my revisions introduce?
- Am I over-engineering to prevent unlikely scenarios?
- What's the simplest design that solves 80% of problems?

Final design with explicit trade-off documentation.
```

## 7. Security Implementation + Adversarial Thinking (Advanced)

```text
Implement input validation for a user registration endpoint.

Initial implementation:
[provide your code]

Adversarial reflection - Put on attacker hat:
1. How would I bypass this validation?
2. What edge cases in encoding/escaping did the developer miss?
3. What happens if I send malformed data types?
4. Can I exploit the error messages?

Improved implementation addressing attack vectors:

Red team reflection:
Test your improved implementation against:
- OWASP Top 10 patterns
- Unicode/encoding exploits
- Rate limiting bypass
- Business logic abuse

Did you find new vulnerabilities? Iterate once more.

Final implementation:

Blue team reflection:
- How will I monitor for attacks against this endpoint?
- What logging is needed for security auditing?
- Is the code maintainable enough that future developers won't break security?
```

## 8. Migration Strategy + Premortem (Expert)

```text
Plan a migration from MongoDB to PostgreSQL for a production system.

Initial migration plan:
[provide detailed plan]

Premortem reflection:
It's 6 months from now. The migration was a disaster. What went wrong?

Generate 5 realistic failure scenarios:
1. [scenario]
2. [scenario]
3. [scenario]
4. [scenario]
5. [scenario]

For each scenario, reflect:
- What warning signs existed that I ignored?
- What could I have done differently in planning?

Revised migration plan incorporating premortem learnings:

Success criteria reflection:
- How will I measure if the migration is successful?
- What's my rollback strategy?
- What's the worst case timeline and cost?

Reality check reflection:
- Am I being overconfident in estimates?
- What hidden complexity am I not seeing?
- Have I talked to teams who've done similar migrations?

Final migration plan with risk mitigation strategies.
```

## 9. Debugging Complex Issue + Hypothesis Evolution (Expert)

```text
Debug this production issue: Random 500 errors occurring in payment processing,
affecting ~5% of transactions, no clear pattern in logs.

Available data:
[paste logs, metrics, timing data]

Hypothesis 1:
[state your initial hypothesis]

Test Hypothesis 1:
[describe how you'd test it]

Reflection on Hypothesis 1:
- What evidence supports this hypothesis?
- What evidence contradicts it?
- What assumptions am I making?

Hypothesis 2 (based on reflection):
[revised or alternative hypothesis]

Test Hypothesis 2:

Reflection on testing approach:
- Am I testing in a way that could disprove my hypothesis?
- Or am I only looking for confirming evidence?
- What would I see if I'm completely wrong about the cause?

Pattern reflection:
Step back and reflect on the debugging process itself:
- Am I in a confirmation bias loop?
- Have I considered systemic issues vs. code bugs?
- What would a fresh pair of eyes notice that I'm missing?

New hypothesis incorporating systemic thinking:

Final diagnosis with confidence level and evidence:

Post-resolution reflection:
- What clues did I miss early on?
- How can I improve my debugging process?
- What tooling/monitoring would have made this easier?
```

## 10. System Design + Iterative Refinement + Stakeholder Perspectives (Expert)

```text
Design a real-time notification system for a social platform (1M+ daily active users).

Round 1 - Initial design:
[provide architecture, tech choices, data flow]

Technical reflection:
- What's my scaling ceiling with this design?
- Where are the single points of failure?
- What's the latency budget and did I meet it?

Round 2 - Revised technical design:

Operational reflection:
Put on SRE hat:
- How do I monitor this system?
- What alerts do I need?
- What breaks at 2 AM and how do I fix it quickly?
- What's the runbook for common failures?

Round 3 - Operationally aware design:

Cost reflection:
Put on finance hat:
- What's the monthly infrastructure cost at current scale?
- At 10x scale?
- Where are the cost optimization opportunities?
- What's the trade-off between cost and reliability?

Round 4 - Cost-optimized design:

User experience reflection:
Put on product hat:
- What happens to notifications when system is degraded?
- How do users perceive reliability?
- What's the failure mode UX?
- Are we solving the right problem with technology?

Round 5 - User-centric refinement:

Integration reflection:
Put on client team hat:
- How easy is this to integrate for mobile/web developers?
- What's the learning curve?
- Where will they make mistakes?
- Is the API intuitive or do I need extensive documentation?

Round 6 - Developer experience improvements:

Meta-reflection on design process:
- Which perspective revealed the most critical issues?
- What did I initially over-prioritize?
- What did I initially under-prioritize?
- If I had to cut scope, what's the MVP that's still valuable?

Final design:
Present simplified architecture with explicit trade-offs documented.

Include:
- What I optimized for and why
- What I explicitly chose NOT to solve
- Decision points where different trade-offs make sense
- Evolution path for future requirements
```
