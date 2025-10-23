# Multi-Objective Directional Prompting (MODP): 10 example prompts

## 1. Basic example

```text
Refactor this function to improve it along these three objectives:

Objective 1: Readability - Make it easier for junior developers to understand
Objective 2: Performance - Reduce time complexity where possible
Objective 3: Maintainability - Make it easier to add new validation rules

[paste code]

Direction: Prioritize readability first, then maintainability, then performance.
Only optimize performance if it doesn't significantly harm readability.

Show which changes address which objectives.
```

## 2. **Component Design with Balanced Constraints** (Basic-Intermediate)

```text
Design a notification component with these competing objectives:

Objective 1: User Experience - Notifications should be noticeable but not annoying
Objective 2: Accessibility - Must support screen readers and keyboard navigation
Objective 3: Performance - Minimal bundle size and render cost
Objective 4: Flexibility - Support different notification types (success, error, info, warning)

[describe current context]

Direction: UX and accessibility are non-negotiable - never compromise these.
For performance vs flexibility trade-offs, bias toward flexibility if the
performance cost is under 5KB and 16ms render time.

Provide the component API design and explain how each objective influenced your decisions.
```

## 3. **API Design with Multi-Stakeholder Needs** (Intermediate)

```text
Design a REST API endpoint for product search with these objectives:

Objective 1: Developer Experience - Intuitive and consistent with existing API patterns
Objective 2: Query Flexibility - Support filtering, sorting, pagination, and search
Objective 3: Performance - Response time under 200ms for 95th percentile
Objective 4: Future-Proofing - Extensible for upcoming features (faceted search, recommendations)
Objective 5: Security - Prevent data leaks and abuse (rate limiting, field filtering)

Current context:
- 100K products in catalog
- Existing API uses REST with JSON
- Team familiar with Express.js

Direction:
- Performance and security cannot be compromised
- If developer experience conflicts with future-proofing, choose the approach
  that allows iteration without breaking changes
- Flexibility is important but don't add complexity for hypothetical use cases

Design the endpoint specification and explain your trade-off decisions.
```

## 4. **Testing Strategy with Resource Constraints** (Intermediate)

```text
Design a testing strategy for our new authentication system with these objectives:

Objective 1: Coverage - Test all critical paths and edge cases
Objective 2: Speed - Test suite should run in under 3 minutes
Objective 3: Reliability - Tests should not be flaky
Objective 4: Maintainability - Tests should be easy to update when code changes
Objective 5: Development Velocity - Don't slow down feature development

Context:
- Team of 4 developers
- CI/CD pipeline runs on every PR
- Budget: 2 weeks for initial test implementation

Direction:
- Reliability is paramount - a flaky test is worse than no test
- Coverage for authentication must be 100% for happy paths, 80%+ for edge cases
- Speed vs coverage: prefer targeted high-value tests over exhaustive low-value tests
- If maintainability conflicts with coverage, choose maintainability for
  tests that change frequently

Provide test plan with test count breakdown by type and estimated execution time.
```

## 5. **Database Schema Design with Competing Concerns** (Intermediate-Advanced)

```text
Design a database schema for a multi-tenant SaaS application with these objectives:

Objective 1: Query Performance - Fast reads for dashboard queries
Objective 2: Data Integrity - Prevent orphaned records and maintain consistency
Objective 3: Tenant Isolation - Complete data separation for compliance
Objective 4: Cost Efficiency - Minimize storage and compute costs
Objective 5: Schema Evolution - Easy to add new features without migrations

Context:
- Expect 1000 tenants, ranging from 10 to 100,000 records each
- PostgreSQL database
- Most queries filter by tenant + date range
- Need to support tenant-specific customization of data model

Direction:
- Tenant isolation and data integrity are regulatory requirements (cannot compromise)
- Performance target: p95 queries under 100ms
- For cost vs performance: optimize for performance up to 2x cost, then prioritize cost
- Schema evolution vs query performance: prefer denormalization if it prevents
  complex migrations, except where it risks data integrity

Provide schema design with indexing strategy and explain key trade-off decisions.
```

## 6. **Code Review Process Design** (Advanced)

```text
Design a code review process that optimizes for these objectives:

Objective 1: Code Quality - Catch bugs, design issues, and maintain standards
Objective 2: Learning - Junior developers grow from review feedback
Objective 3: Velocity - PRs merge within 1 business day
Objective 4: Team Morale - Process feels collaborative, not adversarial
Objective 5: Knowledge Sharing - Prevent knowledge silos
Objective 6: Consistency - Similar code gets similar feedback

Context:
- Team: 2 senior, 3 mid-level, 3 junior developers
- 15-25 PRs per week
- Mix of features, bugs, and refactors
- Remote team across 3 time zones

Direction:
- Code quality baseline is non-negotiable (tests required, no known bugs merged)
- Velocity vs quality: block PRs for correctness issues, not style preferences
- Learning vs velocity: invest extra time in junior developer PRs (up to 2x review time)
- If knowledge sharing conflicts with velocity: prioritize velocity for hot fixes,
  knowledge sharing for architectural changes
- Team morale trumps all other objectives if tension arises

Design the complete review process including:
- Review assignment algorithm
- Required checks before human review
- Guidelines for reviewers
- Escalation path for disagreements
- Metrics to track process health

Explain how each element serves the objectives and where trade-offs were made.
```

## 7. **Microservices Migration Strategy** (Advanced)

```text
Plan migration from monolith to microservices with these objectives:

Objective 1: Zero Downtime - No service interruptions during migration
Objective 2: Team Autonomy - Teams can deploy services independently
Objective 3: System Reliability - Maintain or improve current 99.9% uptime
Objective 4: Development Velocity - Don't slow down feature development during migration
Objective 5: Cost Control - Infrastructure costs increase by max 30%
Objective 6: Reversibility - Can roll back if approach isn't working

Context:
- Current monolith: 200K lines, 6 teams contributing
- Deploy weekly currently
- No container experience on team
- 18-month timeline for migration
- Revenue-critical system (e-commerce)

Direction:
- Zero downtime and reliability are absolute constraints
- Development velocity should not drop below 70% of current pace
- Team autonomy vs reliability: choose reliability, but provide tooling to make
  autonomous deployments safe
- Cost vs team autonomy: willing to pay extra 30% for autonomy, not more
- If any objective is at risk after 6 months, must have option to pause and
  consolidate progress

Design migration strategy including:
- Service decomposition approach
- Migration sequence and timeline
- Team structure evolution
- Infrastructure architecture
- Risk mitigation for each phase
- Go/no-go criteria at key milestones

For each major decision, explicitly state which objectives it optimizes for
and which it compromises.
```

## 8. **SaaS Pricing Model Design** (Advanced)

```text
Design a pricing model that balances these objectives:

Objective 1: Revenue Maximization - Capture willingness to pay across segments
Objective 2: Customer Satisfaction - Perceived as fair and predictable
Objective 3: Sales Efficiency - Easy to explain and quick to close deals
Objective 4: Product-Led Growth - Support free/trial users converting organically
Objective 5: Margin Preservation - Price correlates with infrastructure costs
Objective 6: Competitive Positioning - Attractive vs competitors

Context:
- B2B project management SaaS
- Target: SMBs (10-50 employees) and Mid-market (50-500 employees)
- Core costs scale with: active users and storage
- Competitors: Freemium models and per-seat pricing
- Current beta: 200 users, mix of free and paid

Data from beta:
- Free users: 10% convert to paid after 30 days
- Paid users: $15/user/month, 3.2% churn monthly
- High-value features: reporting (30% usage), integrations (45% usage), custom fields (60% usage)

Direction:
- Customer satisfaction > revenue in year 1 (building reputation)
- Revenue > customer satisfaction starting year 2
- Sales efficiency is critical - no custom pricing for deals under $10K annually
- Product-led growth: must have free tier, but limit to prevent abuse
- Margin: acceptable to lose money on free tier if conversion rate > 8%
- Competitive positioning: match or undercut on base tier, charge premium for advanced features

Design complete pricing structure including:
- Tier definitions and prices
- Feature distribution across tiers
- Free tier limitations
- Overage/upgrade policies
- Expected revenue model and customer distribution

For each pricing decision, map it to the objectives and explain trade-offs.
```

## 9. **Platform Team Charter and Priorities** (Expert)

```text
Define charter and priorities for a new platform engineering team with these objectives:

Objective 1: Developer Productivity - Reduce friction for product engineers
Objective 2: System Reliability - Improve uptime and reduce incidents
Objective 3: Cost Optimization - Reduce infrastructure spend by 25%
Objective 4: Security Posture - Meet SOC2 and ISO 27001 requirements
Objective 5: Innovation Enablement - Don't block new technology adoption
Objective 6: Team Sustainability - Avoid burnout, maintain on-call rotation

Context:
- 40 product engineers across 8 teams
- Current pain points: slow CI/CD (20min builds), complex deployments, frequent outages
- Infrastructure spend: $80K/month (target: $60K/month)
- Security audit in 6 months
- Platform team: 5 engineers (2 senior, 3 mid-level)

Current metrics:
- Mean deployment time: 45 minutes
- Deployment success rate: 78%
- P95 build time: 23 minutes
- Monthly incidents: 8 (avg)
- On-call pages: 15/week

Direction:
- Security compliance is a deadline (6 months) - must be met
- Developer productivity has highest long-term ROI - prioritize when possible
- Cost optimization: achieve through efficiency, not by degrading reliability
- Reliability vs innovation: allow experimentation in non-critical paths
- Team sustainability: if velocity requires unsustainable on-call burden,
  reduce scope or hire
- First 90 days: focus on quick wins for developer productivity to build trust

Design platform team strategy including:
- 18-month roadmap with quarterly milestones
- Prioritized project list with effort estimates
- Success metrics for each objective
- Resource allocation across objectives
- Dependencies and sequencing
- Risk mitigation for conflicts between objectives

For each quarter, specify:
- Primary objective being optimized
- Secondary objectives being maintained
- Objectives being explicitly deprioritized
- Trade-off rationale
```

## 10. **Technical Architecture Decision Framework** (Expert)

```text
Create a decision framework for technical architecture choices that optimizes for these objectives:

Objective 1: Execution Speed - Deliver features to market quickly
Objective 2: Scalability - Handle 10x growth without rewrite
Objective 3: Team Skill Alignment - Use technologies team knows or can learn quickly
Objective 4: Operational Excellence - System is observable, debuggable, maintainable
Objective 5: Cost Efficiency - Minimize infrastructure and tooling costs
Objective 6: Vendor Independence - Avoid lock-in to single cloud/vendor
Objective 7: Innovation Currency - Stay current with industry practices

Context:
- Series A startup, 15 engineers
- Product: Real-time collaboration platform
- Current: Monolithic Rails app, PostgreSQL, Redis, deployed on Heroku
- Next 12 months: expect 5x user growth, 10x data growth
- Recent incidents: database CPU spikes, WebSocket connection limits

Technical constraints:
- Team expertise: Strong in Rails/JavaScript, moderate in Python, weak in Go/Java
- Budget: $15K/month infrastructure, $50K/year for tooling/licenses
- Compliance: Must support SOC2 within 12 months

Decisions needed:
1. Database strategy (scale PostgreSQL vs migrate to distributed DB)
2. Real-time infrastructure (WebSockets vs cloud service like Pusher)
3. Deployment platform (stay on Heroku vs Kubernetes vs serverless)
4. Monitoring/observability stack
5. CI/CD evolution

Direction for trade-offs:
- Execution speed is critical for next 6 months (pre-Series B fundraising)
- Scalability: must handle 10x, but 100x can wait until later
- Team skills: prefer extending current knowledge over new paradigms, unless
  current approach fundamentally won't scale
- Operational excellence: non-negotiable for user-facing services, can be
  rough for internal tools
- Cost efficiency: stay within budget, but willing to pay for managed services
  that save engineering time at rate of $10K/month = 1 engineer week saved
- Vendor independence: acceptable for non-core components, avoid for core data/logic
- Innovation currency: adopt proven practices from last 2-3 years, avoid
  bleeding edge unless it solves critical problem

Design decision framework including:
1. Evaluation criteria for each decision type
2. Weighted scoring model reflecting objective priorities
3. Specific recommendations for the 5 decisions above with trade-off analysis
4. Guidance on when to revisit architectural choices
5. Process for future architectural decisions

For each recommendation:
- List which objectives it optimizes for (with expected impact)
- List which objectives it compromises (with mitigation strategy)
- Identify assumptions that would invalidate the choice
- Specify metrics to validate the decision is working
- Define criteria for when to reverse the decision

Structure the framework to be reusable for future decisions beyond these specific choices.
```
