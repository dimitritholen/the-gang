# Self-Consistency: 10 example prompts

## 1. Basic example

```text
I'm getting a TypeError in this JavaScript function but I'm not sure why:

[paste code]

Generate 3 different explanations for what might be causing this error,
each using a different debugging approach:

Approach 1: Analyze the type flow through the function
Approach 2: Consider the input data and how it's used
Approach 3: Look at the surrounding context and how the function is called

Then identify which explanation appears most consistent across all approaches
and provide the fix.
```

## 2. **SQL Query Debugging with Multiple Perspectives** (Basic-Intermediate)

```text
This SQL query returns unexpected results:

[paste query]

Solve this by reasoning through it 3 different ways:

Path 1: Start from the innermost subquery and work outward
Path 2: Start from the WHERE clauses and trace the filtering logic
Path 3: Start from the JOIN conditions and analyze the relationships

After completing all three reasoning paths, identify which issues
appear in multiple paths (these are most likely the real problems).
Provide the corrected query.
```

## 3. **Component Architecture Decision** (Intermediate)

```text
We need to decide how to structure a complex filtering component in React.

Requirements:
- 8 different filter types (text, date range, multi-select, etc.)
- Filters can be combined with AND/OR logic
- Need URL sync for sharing filtered views
- Must be reusable across 5 different pages

Generate 3 independent solutions using different architectural approaches:

Solution A: Using React Context + Custom Hooks approach
Solution B: Using State Management Library (Zustand/Redux) approach
Solution C: Using Compound Components pattern approach

For each solution, think through:
- State management strategy
- Reusability mechanism
- URL synchronization approach
- Performance considerations

Then compare all three solutions and identify:
- Which concerns are addressed consistently across solutions?
- Which approach handles the most requirements elegantly?
- What is the consensus choice?
```

## 4. **API Rate Limit Implementation** (Intermediate)

```text
Design a rate limiting system for our API (100 requests per minute per user).

Approach this problem from 3 different algorithmic perspectives:

Perspective 1: Token Bucket Algorithm
- How would you implement this?
- What are the data structures needed?
- How does it handle bursts?

Perspective 2: Sliding Window Log
- How would you implement this?
- What are the data structures needed?
- How does it handle edge cases?

Perspective 3: Fixed Window Counter
- How would you implement this?
- What are the data structures needed?
- What are the trade-offs?

After exploring all three:
- Which aspects are consistent across approaches?
- Which algorithm best fits our use case?
- Are there hybrid approaches combining strengths of multiple methods?

Provide final recommendation with implementation outline.
```

## 5. **Test Strategy Design with Multiple Frameworks** (Intermediate-Advanced)

```text
We need a testing strategy for a new checkout flow feature.

Feature complexity:
- Multi-step form with validation
- Payment integration
- Inventory checking
- Email notifications
- Analytics tracking

Create 3 independent test plans using different testing philosophies:

Philosophy A: Testing Trophy approach (focus on integration tests)
Philosophy B: Testing Pyramid approach (focus on unit tests)
Philosophy C: Testing Diamond approach (focus on integration + E2E)

For each philosophy, specify:
- What percentage of tests at each level?
- Which specific scenarios to test at which level?
- Mocking strategy
- Expected test count and coverage

After generating all three plans:
- Which scenarios appear critical in all three plans?
- What's the overlapping consensus on test distribution?
- Can we create a hybrid plan taking the best from each?

Provide final synthesized test strategy.
```

## 6. **Performance Bottleneck Analysis** (Advanced)

```text
Our dashboard loads slowly (5-8 seconds). Here's the performance profile:

[paste performance data]

Diagnose this using 3 different analytical methods:

Method 1: Critical Rendering Path Analysis
- Identify blocking resources
- Analyze render timeline
- Find layout thrashing
- Conclusion: Primary bottleneck?

Method 2: JavaScript Execution Analysis
- Profile function call times
- Identify heavy computations
- Find unnecessary re-renders
- Conclusion: Primary bottleneck?

Method 3: Network and Data Flow Analysis
- Analyze request waterfalls
- Identify redundant requests
- Check bundle sizes
- Conclusion: Primary bottleneck?

After completing all three analyses:
- Which bottleneck appears in multiple methods?
- What's the consistent diagnosis across approaches?
- Which optimizations have consensus priority?

Provide final optimization plan based on consistent findings.
```

## 7. **Database Scaling Strategy with Multiple Scenarios** (Advanced)

```text
Our PostgreSQL database is approaching capacity. Current: 2TB data, 10K writes/sec peak.

Model 3 different growth scenarios and solution approaches:

Scenario A: Linear growth (2x in 12 months)
- How would you scale this?
- What's the architecture evolution?
- Cost and complexity assessment?

Scenario B: Exponential growth (5x in 6 months)
- How would you scale this?
- What's the architecture evolution?
- Cost and complexity assessment?

Scenario C: Unpredictable spiky growth
- How would you scale this?
- What's the architecture evolution?
- Cost and complexity assessment?

For each scenario, independently determine:
- Sharding strategy
- Read replica approach
- Caching layer design
- Migration path

After modeling all three scenarios:
- Which strategies appear robust across all scenarios?
- What's the common foundation we should build?
- Which scenario should we optimize for?

Provide a solution that maintains consistency across scenarios while
being practical for our most likely growth path.
```

## 8. **Microservices Decomposition Strategy** (Advanced)

```text
Break down our monolithic e-commerce application into microservices.

Current monolith modules:
- User management
- Product catalog
- Shopping cart
- Order processing
- Inventory
- Payment
- Shipping
- Notifications

Create 3 different decomposition strategies using different principles:

Strategy 1: Decompose by Business Capability
- How do you group these modules?
- What are the service boundaries?
- How do services communicate?
- What are the data ownership rules?

Strategy 2: Decompose by Subdomain (DDD approach)
- How do you identify bounded contexts?
- What are the service boundaries?
- How do services communicate?
- What are the data ownership rules?

Strategy 3: Decompose by Transaction/Workflow
- How do you group these modules?
- What are the service boundaries?
- How do services communicate?
- What are the data ownership rules?

After creating all three strategies:
- Which modules are consistently grouped together?
- Which service boundaries appear in multiple strategies?
- What communication patterns are consistent?

Synthesize a final microservices architecture that incorporates
the consistent patterns from all three strategies.
```

## 9. **Security Architecture Review with Multiple Threat Models** (Expert)

```text
Review the security architecture for our multi-tenant SaaS application.

Architecture:
- React frontend (S3 + CloudFront)
- Node.js API (ECS)
- PostgreSQL (RDS)
- Redis cache (ElastiCache)
- Background jobs (Lambda)

Analyze security from 3 different attacker perspectives:

Perspective 1: External Attacker (Internet-facing threats)
- What are the attack vectors?
- Which components are vulnerable?
- What's the attack priority order?
- Required defenses?

Perspective 2: Malicious Tenant (Insider threat)
- What are the attack vectors?
- Which components are vulnerable?
- What's the attack priority order?
- Required defenses?

Perspective 3: Compromised Dependencies (Supply chain attack)
- What are the attack vectors?
- Which components are vulnerable?
- What's the attack priority order?
- Required defenses?

For each perspective, independently identify:
- Top 5 security risks
- Existing controls
- Missing controls
- Remediation priority

After completing all three analyses:
- Which vulnerabilities appear across multiple perspectives?
- What are the highest consensus priority fixes?
- Which controls provide defense-in-depth across threat models?

Provide final security roadmap focusing on consistently identified risks.
```

## 10. **Legacy System Modernization with Risk-Adjusted Paths** (Expert)

```text
Plan modernization of our core billing system.

Current state:
- 20-year-old Java 8 codebase
- 200K lines of code
- Processes $10M monthly
- No automated tests
- Original team departed
- Critical to business
- Frequent production issues

Generate 3 independent modernization strategies with different risk profiles:

Strategy A: Conservative (Minimum risk)
- What's the approach?
- What's the timeline?
- What are the phases?
- How do we ensure safety?
- What's the success criteria?

Strategy B: Moderate (Balanced risk/reward)
- What's the approach?
- What's the timeline?
- What are the phases?
- How do we ensure safety?
- What's the success criteria?

Strategy C: Aggressive (Maximum modernization)
- What's the approach?
- What's the timeline?
- What are the phases?
- How do we ensure safety?
- What's the success criteria?

For each strategy, independently determine:
- Technical approach (strangler fig, rewrite, refactor-in-place)
- Testing strategy
- Rollout plan
- Rollback mechanisms
- Resource requirements
- Business continuity plan

After developing all three strategies:
- Which safety mechanisms appear in all strategies?
- What phases are consistently prioritized first?
- What's the consensus on minimum viable modernization?

Synthesize a final strategy that:
- Takes mandatory safety measures from all three
- Balances risk/reward based on consistent findings
- Provides decision points to shift between strategies
- Includes objective go/no-go criteria
```
