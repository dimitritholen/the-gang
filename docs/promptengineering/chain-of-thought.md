# Chain of Thought: 10 example prompts

## 1. Basic example

```text
I have a React component where the state isn't updating correctly when users
click the increment button. Here's the code:

[paste code]

Let me think through this step by step:

Step 1: Identify what happens when the button is clicked.
Step 2: Trace the state update flow from event handler to re-render.
Step 3: Check if there are any asynchronous issues or stale closures.
Step 4: Determine the root cause based on this analysis.
Step 5: Provide the fix with explanation of why it works.

Walk through each step explicitly before giving the final solution.
```

## 2. **TypeScript Type Design with Incremental Reasoning** (Basic-Intermediate)

```text
I need to design TypeScript types for a multi-step form wizard with these requirements:

- 4 steps: Personal Info, Address, Payment, Review
- Each step has different required fields
- Need type-safe navigation between steps
- Must enforce that Review step can only access data if all previous steps are complete

Think through this incrementally:

First: Design types for individual step data.
Then: Consider how to represent the wizard state at each stage.
Next: Think about type-safe transitions between steps.
Finally: Design the type that enforces the completion requirement.

Show your reasoning at each stage, then provide the complete type system.
```

## 3. **Database Query Optimization with Analytical Reasoning** (Intermediate)

```text
This SQL query is taking 45 seconds on a table with 5M rows:

[paste query]

Analyze and optimize this step by step:

Step 1: Examine the query execution plan - what operations are most expensive?

Step 2: Identify which indexes exist and which are being used.

Step 3: Reason about why the query planner chose this execution path.

Step 4: Consider alternative query structures that could achieve the same result.

Step 5: Propose specific indexes or query rewrites with justification for each.

Step 6: Estimate the expected performance improvement for each suggestion.

Provide your analysis at each step before the final recommendations.
```

## 4. **State Management Library Selection with Comparison Reasoning** (Intermediate)

```text
We need to choose a state management solution for our React app.

Context:
- Medium complexity app (30+ components)
- Real-time updates from WebSocket
- Need offline support
- Team has mixed experience levels

Compare Zustand, Redux Toolkit, and Jotai by reasoning through:

Step 1: For each library, identify its core philosophy and mental model.

Step 2: Analyze how each handles our specific requirements:
   - Real-time updates
   - Offline persistence
   - Learning curve for junior developers
   - DevTools and debugging

Step 3: Consider integration complexity and boilerplate for each.

Step 4: Think through long-term maintenance implications.

Step 5: Make a recommendation with your complete reasoning chain visible.

Show your thought process for each library and criterion before concluding.
```

## 5. **Caching Strategy with Few-Shot Reasoning** (Intermediate-Advanced)

```text
Design a caching strategy for our API that serves product data.

Here are examples of good reasoning:

Example 1: "For user profile data that changes rarely, I'd use:
- Redis with 24h TTL because profiles update infrequently
- Cache invalidation on profile updates via pub/sub
- Fallback to database if cache miss
Reasoning: High read/write ratio (100:1) justifies aggressive caching."

Example 2: "For real-time stock prices, I'd use:
- Short TTL (10s) in application memory
- No persistent cache layer
Reasoning: Data stales quickly; memory cache avoids network overhead."

Now design caching for our product catalog:
- 50K products, updated hourly via batch job
- High read volume (10K req/min)
- Search and filter queries
- Price changes need to reflect within 5 minutes

Think through:
1. What are the access patterns and their characteristics?
2. What cache layers make sense (CDN, Redis, in-memory)?
3. How should TTL values be set for different query types?
4. What's the invalidation strategy?
5. How do we handle cache stampedes during the batch update?

Show your reasoning for each decision.
```

## 6. **Feature Flag System Design with Structured Thinking** (Advanced)

```text
Design a feature flag system for gradual rollout of new features.

Requirements:
- Support percentage-based rollouts (e.g., 5% of users)
- Target specific user segments (beta users, specific companies)
- Enable/disable flags without deployment
- Track flag evaluation for analytics

Think through the design systematically:

Part 1 - Data Model:
What entities do we need (flags, rules, users)?
How should flag evaluation rules be structured?
Where is this data stored?

Part 2 - Evaluation Logic:
How does the system determine if a flag is on for a given user?
What's the order of precedence for multiple rules?
How do we ensure consistent evaluation (same user always gets same result)?

Part 3 - Performance:
What's the latency requirement for flag evaluation?
Should we cache? At what level?
How do we handle flag changes propagating to multiple services?

Part 4 - Rollout Strategy:
How do we safely go from 0% to 100%?
What monitoring is needed during rollout?
How do we roll back quickly if issues arise?

Present your reasoning for each part, then provide the complete design.
```

## 7. **Container Orchestration Decision with Role Prompting** (Advanced)

```text
Role: You are a platform engineer evaluating container orchestration solutions.

Context:
- Team of 8 developers, 1 DevOps engineer
- 15 microservices, expect to grow to 30
- Currently using Docker Compose in production (yes, really)
- Budget: $2K/month for infrastructure
- No Kubernetes experience on team

Evaluate: Kubernetes, Nomad, AWS ECS, and Cloud Run.

Reason through your evaluation:

Phase 1 - Operational Complexity:
For each option, think through:
- What's the day-to-day operational burden?
- What breaks at 3am and how hard is it to fix?
- What's the learning curve given our team's skills?

Phase 2 - Feature Fit:
- Which features do we actually need vs nice-to-have?
- Which solution provides these with least complexity?
- What are we giving up with each choice?

Phase 3 - Cost Analysis:
- Direct costs (compute, control plane)
- Hidden costs (training, maintenance, tooling)
- Opportunity cost of engineering time

Phase 4 - Future Considerations:
- What happens when we scale to 50 services?
- How locked-in are we to each option?
- Can we migrate later if needed?

Walk through each phase explicitly, then provide your recommendation.
```

## 8. **Event-Driven Architecture Design with Structured Output** (Advanced)

```text
Design an event-driven architecture for an e-commerce order processing system.

Requirements:
- Order placement triggers inventory check, payment, and notifications
- Each step can fail and needs retry logic
- Need audit trail of all events
- Some processes take minutes (fraud check)

Design the system by reasoning through these aspects and output as JSON:

For each event type you identify, provide:

{
  "event_name": "string",
  "reasoning": {
    "why_needed": "explain the business need",
    "triggers": "what causes this event",
    "consumers": "which services need this event",
    "timing_requirements": "sync vs async and why"
  },
  "schema": {
    "required_fields": [],
    "optional_fields": []
  },
  "failure_handling": {
    "retry_strategy": "describe approach",
    "compensation": "how to undo if needed",
    "dead_letter": "what happens after max retries"
  },
  "ordering_requirements": "does order matter?",
  "idempotency": "how is it ensured?"
}

First, think through the complete order flow and identify all events.
Then, for each event, reason through the JSON structure above.
Finally, provide the complete event catalog as JSON array.
```

## 9. **Zero-Downtime Deployment Strategy with Multi-Lens Analysis** (Expert)

```text
Plan a zero-downtime deployment strategy for migrating our API from v1 to v2.

Context:
- 5M requests/day
- Mobile apps take 2-3 months for users to update
- Breaking changes in v2 (different response structure)
- Database schema changes required
- 3 regions (US, EU, ASIA)

Analyze through multiple reasoning lenses:

Technical Reasoning:
- How do we run v1 and v2 simultaneously?
- What's the database migration strategy with zero downtime?
- How do we route traffic between versions?
- What's the rollback mechanism if v2 has issues?

Risk Reasoning:
- What's the blast radius if something goes wrong?
- Which components are most likely to fail?
- How do we detect problems early?
- What's our rollback time if we discover issues after 50% rollout?

Timeline Reasoning:
- What's the minimum safe rollout period?
- What are the discrete phases?
- How long should we observe at each phase?
- When can we sunset v1?

User Impact Reasoning:
- How do we ensure old mobile apps keep working?
- What happens to in-flight requests during deployment?
- How do we communicate changes to API consumers?
- What's the support burden during transition?

Go through each reasoning lens, then synthesize into a complete deployment plan
with specific steps, timelines, and success criteria.
```

## 10. **Legacy Codebase Refactoring with Risk Assessment** (Expert)

```text
We need to refactor a critical legacy service that's become unmaintainable.

Context:
- 15K lines of JavaScript (no TypeScript)
- No tests
- Handles payment processing (business-critical)
- 8 years old, original authors gone
- Frequent production bugs
- Team wants to rewrite in TypeScript with proper architecture

Plan the refactoring by reasoning through these dimensions:

<phase_1_understanding>
Before touching code, think through:
- What are the actual business rules implemented here?
- What are the hidden dependencies we need to discover?
- What parts do we understand vs don't understand?
- How do we build confidence in our understanding?
</phase_1_understanding>

<phase_2_risk_analysis>
For each possible approach (big rewrite vs incremental refactor), reason about:
- What can go catastrophically wrong?
- How would we detect problems before users do?
- What's the rollback strategy?
- What's the blast radius of a mistake?
- Historical context: Why do big rewrites usually fail?
</phase_2_risk_analysis>

<phase_3_incremental_strategy>
Design a step-by-step refactoring approach:
- What's the absolute smallest first step?
- How do we add tests to untested code?
- What order should we tackle different modules?
- How do we maintain feature parity while refactoring?
- What metrics tell us if we're improving or making things worse?
</phase_3_incremental_strategy>

<phase_4_safety_mechanisms>
What safety nets do we build:
- Feature flags for new code paths?
- Shadow mode to compare old vs new behavior?
- Automated validation between versions?
- Gradual rollout strategy?
</phase_4_safety_mechanisms>

<phase_5_organizational>
Non-technical reasoning:
- How do we justify the engineering time?
- How do we prevent new features being added during refactor?
- What's the communication plan to stakeholders?
- How long can we realistically dedicate to this?
</phase_5_organizational>

Reason through each phase explicitly, then provide:
1. Go/no-go recommendation with reasoning
2. If go: detailed first 4 weeks of work
3. Success metrics to evaluate progress
4. Criteria for stopping if this isn't working
</phase_5_organizational>
```
