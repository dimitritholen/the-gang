# Active Prompting: 10 example prompts

Active prompting involves dynamically adapting follow-up questions and prompts based on responses, uncertainty, context, and feedback. Unlike static prompts, active prompts evolve through the interaction to refine understanding and solutions.

## 1. Basic Debugging with Uncertainty Detection

```text
I'm getting a "Cannot read property of undefined" error in my React component.

[Initial response from AI]

Follow-up questions based on your confidence level:
- If you're confident about the cause: Show me the exact fix
- If you're uncertain (50-80% confidence): Ask me clarifying questions about
  component state, props, or lifecycle
- If you're very uncertain (<50%): Request the component code and relevant
  context

Adapt your next response based on the information gathered.
```

## 2. API Integration with Context Building (Basic-Intermediate)

```text
Help me integrate Stripe payments into my Next.js app.

Start with: What's your current experience level with Stripe and Next.js?

Then adapt:
- If beginner: Provide step-by-step tutorial with explanations
- If intermediate: Focus on architecture patterns and error handling
- If advanced: Discuss edge cases, webhook security, and testing strategies

After your initial response, ask a follow-up question that addresses the
biggest risk or gap you identified in the implementation.
```

## 3. Code Review with Dynamic Depth (Intermediate)

```text
Review this pull request:

[paste code]

Phase 1: Initial scan
Identify your top 3 concerns ranked by severity.

Phase 2: Uncertainty-based follow-up
For each concern, rate your confidence (high/medium/low).
For LOW confidence items: Ask me specific questions to clarify before
making recommendations.

Phase 3: Context adaptation
Based on my answers, adjust your review focus:
- If I'm unclear about concepts: Provide educational explanations
- If I'm experienced but overlooked something: Point to specific patterns
- If there's architectural context missing: Ask about system constraints

Phase 4: Tailored recommendations
Provide final review adapted to my knowledge level and project context.
```

## 4. Performance Optimization with Iterative Refinement (Intermediate)

```text
My web app is slow. Here's a Lighthouse report:

[paste report]

Step 1: Initial analysis
What are the top 3 performance bottlenecks?

Step 2: Confidence check
For each bottleneck, indicate:
- High confidence: Provide solution immediately
- Medium confidence: Ask 1-2 clarifying questions
- Low confidence: Request additional profiling data

Step 3: Dynamic adaptation
Based on my responses, if you discover:
- The issue is infrastructure-related → shift to deployment/CDN questions
- The issue is code-related → dive into framework-specific optimizations
- Multiple root causes → help me prioritize by impact vs effort

Step 4: Iterative validation
After each optimization suggestion, ask: "What result did you get?" and
adapt next recommendations based on the actual impact measured.
```

## 5. Architecture Design with Feedback Loops (Intermediate-Advanced)

```text
Design a microservices architecture for an e-commerce platform.

Round 1: Initial proposal
Provide your architecture design.

Round 2: Constraint discovery
Ask me 3-5 questions to uncover constraints you're uncertain about:
- Team size and skills
- Budget limitations
- Existing infrastructure
- Compliance requirements
- Scale expectations

Round 3: Adaptive redesign
Based on my answers, if you discover:
- Small team → simplify to modular monolith or fewer services
- Limited budget → suggest cost-effective alternatives
- High compliance needs → emphasize security boundaries
- Uncertain scale → design for flexibility

Round 4: Challenge your assumptions
Ask me: "What concerns you most about this design?"
Adapt your architecture to address the specific concern.

Round 5: Final design
Present refined architecture with explicit trade-offs based on our conversation.
```

## 6. Test Strategy with Dynamic Example Selection (Advanced)

```text
Help me write tests for this authentication module:

[paste code]

Phase 1: Complexity assessment
Analyze the code and rate its testing complexity (simple/moderate/complex).

Phase 2: Adaptive examples
Based on complexity:
- Simple: Provide 2-3 basic test examples
- Moderate: Show 5-7 examples covering edge cases
- Complex: Provide comprehensive test suite with integration tests

Phase 3: Coverage gaps
After showing examples, ask: "Which test case is most confusing?"

Phase 4: Targeted clarification
Based on my answer:
- If mocking is confusing → explain mocking strategy in detail
- If assertions are unclear → provide assertion pattern examples
- If test setup is complex → break down arrange-act-assert pattern

Phase 5: Custom examples
Generate 2-3 new test examples specifically addressing the confusion point.
```

## 7. Migration Planning with Risk Adaptation (Advanced)

```text
Plan migration from JavaScript to TypeScript for our codebase (500 files).

Step 1: Initial assessment
Ask questions to gauge:
- Codebase complexity (frameworks, patterns, dependencies)
- Team TypeScript experience
- Timeline pressure
- Risk tolerance

Step 2: Uncertainty identification
Based on answers, identify your top 3 uncertainties about the migration.
For each uncertainty, ask a specific follow-up question.

Step 3: Adaptive strategy
After gathering information, if you detect:
- Low TS experience + tight timeline → incremental adoption strategy
- High complexity + risk averse → extensive testing and gradual rollout
- Experienced team + flexible timeline → aggressive migration with refactoring

Step 4: Challenge scenario
Ask: "What's the one thing that would make you cancel this migration?"
Adapt your plan to specifically mitigate that risk.

Step 5: Dynamic milestones
Create migration milestones that adapt to:
- My answers about blockers
- Detected team capabilities
- Identified technical constraints

Provide final plan with adaptive checkpoints.
```

## 8. Security Audit with Threat Modeling Adaptation (Expert)

```text
Conduct a security audit of our authentication system:

[paste architecture and code]

Phase 1: Threat surface mapping
Identify potential attack vectors with confidence levels:
- High confidence threats (known vulnerabilities)
- Medium confidence threats (potential weaknesses)
- Low confidence threats (need more context)

Phase 2: Context-driven questions
For medium/low confidence items, ask targeted questions:
- About deployment environment
- About user data sensitivity
- About existing security controls
- About threat model (script kiddies vs nation-state)

Phase 3: Adaptive threat prioritization
Based on answers, if you discover:
- High-value target + sophisticated threats → focus on advanced attacks
- Consumer app + basic threats → focus on common vulnerabilities
- Regulated industry → emphasize compliance requirements

Phase 4: Dynamic testing recommendations
Adapt testing approach based on findings:
- If SQL injection possible → provide specific SQLi test cases
- If session management weak → focus on session fixation tests
- If crypto issues found → provide crypto validation tests

Phase 5: Iterative remediation
For each vulnerability:
1. Propose fix
2. Ask: "What constraints prevent this fix?"
3. Adapt recommendation based on constraints
4. Provide alternative if needed

Phase 6: Final report
Security assessment adapted to your specific context, threat model, and constraints.
```

## 9. Debugging Production Issues with Hypothesis Evolution (Expert)

```text
Production issue: Payment processing fails intermittently (5-10% of transactions).

[paste initial logs and metrics]

Phase 1: Initial hypothesis generation
Based on available data, generate 3 hypotheses ranked by likelihood.
For each hypothesis, state your confidence level.

Phase 2: Dynamic data requests
For hypotheses with <70% confidence, request specific additional data:
- Logs from specific timeframes
- Metrics from particular services
- Database query performance
- Network traces

Phase 3: Adaptive investigation
As I provide data, continuously update:
- Hypothesis probability rankings
- New questions to ask
- Different data sources to examine

If new data contradicts your hypothesis → immediately pivot and explain why.

Phase 4: Pattern recognition
Ask: "Have you made any recent changes to: [most likely culprit based on data]?"

Phase 5: Contextual adaptation
Based on my answer about recent changes:
- If deployment change → focus on rollback vs fix-forward
- If config change → investigate environment differences
- If dependency update → check version compatibility
- If no changes → look for external factors

Phase 6: Experiment design
Propose targeted experiments to test remaining hypotheses.
Adapt experiment based on: risk tolerance, traffic volume, business impact.

Phase 7: Solution validation
After fix proposal, ask: "What monitoring exists for this code path?"
Adapt solution to include observability if missing.

Provide final diagnosis with confidence level and recommended fix adapted
to your operational constraints.
```

## 10. System Design with Multi-Stakeholder Adaptation (Expert)

```text
Design a real-time analytics dashboard for a SaaS product.

Round 1: Stakeholder identification
Ask: "Who are the primary stakeholders?" (engineers, product, customers, executives)

Round 2: Requirements discovery
Based on stakeholders mentioned, ask targeted questions:
- For engineers: Scale, tech stack, maintenance burden
- For product: Features, user experience, time to market
- For customers: Performance, reliability, cost
- For executives: ROI, competitive advantage, risk

Round 3: Constraint uncertainty resolution
Identify what you're least confident about and ask specific follow-ups:
- "What's the acceptable latency for dashboard updates?"
- "What's the budget ceiling for infrastructure?"
- "Are there existing systems this must integrate with?"

Round 4: Adaptive design
Create initial design, then ask: "What's the most controversial part of this design?"

Round 5: Controversy resolution
Based on the controversial element:
- If performance vs cost → provide cost-performance trade-off analysis
- If complexity vs features → suggest MVP and phased approach
- If tech choice vs team skills → propose learning path or alternatives

Round 6: Iterative refinement
Present refined design, then ask: "What would make you say 'no' to this design?"

Round 7: Objection handling
Adapt design to address specific objection:
- Technical risk → add more validation and proof of concepts
- Cost concerns → provide cost optimization strategies
- Timeline worries → break into smaller deliverable chunks
- Operational complexity → simplify or add automation

Round 8: Validation questions
For each major component, ask:
"On a scale of 1-10, how confident are you that this will work?"
For scores <7, dig into specific concerns and adapt design.

Round 9: Meta-adaptation
Ask: "Looking at this whole conversation, what did I not ask about that I should have?"
Incorporate that perspective into final design.

Round 10: Final design delivery
Present comprehensive design adapted through:
- Stakeholder priorities discovered
- Constraints uncovered
- Risks identified and mitigated
- Objections addressed
- Missing perspectives integrated

Include decision log showing how design evolved through our conversation.
```
