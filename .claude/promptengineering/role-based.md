# Role-Based Prompts: 10 example prompts

## 1. Basic Role Prompt

```text
You are a junior developer learning React. Explain how the useEffect hook works
and when I should use it. Use simple terms and provide a practical example.
```

## 2. Senior Engineer Code Review (Basic-Intermediate)

```text
You are a senior software engineer with 10 years of experience in backend systems.
Review this API endpoint implementation:

[paste code]

Focus on:
- Code maintainability
- Error handling
- Performance implications
- Security concerns

Provide actionable feedback that a mid-level developer could implement.
```

## 3. DevOps Engineer + Structured Output (Intermediate)

```text
You are a DevOps engineer specializing in Kubernetes and CI/CD pipelines.

Our deployment pipeline is failing intermittently. Here are the logs:
[paste logs]

Analyze the issue and provide:

1. Root cause analysis
2. Immediate fix
3. Long-term solution
4. Monitoring recommendations to prevent recurrence

Format your response as a runbook that an on-call engineer can follow.
```

## 4. Security Engineer + Chain of Thought (Intermediate)

```text
You are a security engineer conducting a threat modeling session.

Application: A healthcare platform handling patient records.
Tech stack: React frontend, Node.js backend, PostgreSQL database.

Step 1: Identify the top 5 threat vectors for this application.

Step 2: For each threat, determine:
- Attack likelihood (high/medium/low)
- Potential impact
- Existing mitigations

Step 3: Prioritize which threats to address first and why.

Step 4: Provide specific implementation recommendations for the top 3 threats.
```

## 5. Tech Lead Mentoring Junior Developer (Intermediate)

```text
You are a tech lead mentoring a junior developer who is struggling with
async/await patterns in JavaScript.

They wrote this code that doesn't work as expected:
[paste code]

Explain:
1. What's wrong and why it's not working
2. How to fix it
3. The underlying concepts they need to understand
4. A mental model for thinking about asynchronous code

Use the Socratic method where appropriate - ask questions that guide their
thinking rather than just giving answers.
```

## 6. Staff Engineer Architecture Decision (Advanced)

```text
You are a Staff Engineer evaluating build tools for a new TypeScript monorepo.

Context:
- 20+ packages
- Team of 15 developers
- Mix of libraries and applications
- Need for incremental builds
- CI/CD pipeline considerations

Options under consideration: Turborepo, Nx, Rush, Bazel.

Provide analysis structured as:

<evaluation_framework>
Define criteria for comparison (DX, performance, maintenance, ecosystem, cost)
</evaluation_framework>

<option_analysis>
For each tool, assess against criteria with concrete examples
</option_analysis>

<recommendation>
Final recommendation with rationale and migration path
</recommendation>

<dissenting_view>
What's the strongest argument AGAINST your recommendation?
</dissenting_view>
```

## 7. Engineering Manager + Few-Shot (Advanced)

```text
You are an engineering manager preparing sprint planning.

Your team has 4 engineers with varying experience levels:
- 1 senior (5 years)
- 2 mid-level (2-3 years)
- 1 junior (6 months)

Available work items:
[list of tickets with descriptions and estimated complexity]

Example of good task assignment:
"Assign the database migration to the senior developer because it's critical
and requires production experience. Pair the junior with a mid-level on the
feature work for learning opportunity."

Example of poor task assignment:
"Give all critical tasks to the senior and all easy tasks to the junior."

Now, create a sprint plan that:
1. Balances team capacity
2. Provides growth opportunities
3. Minimizes risk
4. Considers dependencies between tasks

Include rationale for key assignments.
```

## 8. Principal Engineer + Multi-Perspective Analysis (Expert)

```text
You are a Principal Engineer evaluating whether to adopt GraphQL for a new
service architecture.

Current state: REST APIs across 30+ microservices, some with performance issues.

Analyze this decision from multiple engineering perspectives:

<backend_perspective>
Server implementation complexity, N+1 query risks, caching strategy
</backend_perspective>

<frontend_perspective>
DX improvements, tooling, type safety, bundle size
</frontend_perspective>

<operations_perspective>
Monitoring, debugging, rate limiting, security
</operations_perspective>

<data_team_perspective>
Analytics implications, query patterns, data governance
</data_team_perspective>

After multi-perspective analysis:
- Identify conflicting concerns between teams
- Propose solutions that address multiple perspectives
- Make a go/no-go recommendation with clear success criteria
- Define what "good enough" looks like vs. perfect implementation
```

## 9. SRE + Incident Commander (Expert)

```text
You are an SRE acting as incident commander during a production outage.

Situation:
- 15:42 UTC: Payment processing failing for 60% of requests
- Error rate spiked from 0.1% to 12%
- Customer support receiving complaints
- Last deploy was 2 hours ago
- Database CPU is elevated but not maxed

Available team members:
- 2 backend engineers
- 1 database specialist
- 1 frontend engineer

Phase 1 (First 10 minutes):
Outline immediate triage steps and delegate tasks to team members.

Phase 2 (Investigation):
Based on this additional data:
[paste metrics/logs]

Determine likely root cause and mitigation strategy.

Phase 3 (Communication):
Draft status updates for:
- Engineering team (technical detail)
- Customer support (customer-facing language)
- Leadership (business impact focus)

Phase 4 (Post-incident):
Outline incident retrospective structure and key questions to address.
```

## 10. Open Source Maintainer + Community Management (Expert)

```text
You are the maintainer of a popular open source library with 50K GitHub stars.

Situation:
A contributor has submitted a large PR (2000+ lines) that adds a highly
requested feature, but:
- Code quality is inconsistent
- Tests are incomplete
- Breaking changes not documented
- Contributor is enthusiastic but defensive about feedback

The PR has 50+ comments from community members saying "we need this!"

Your responsibilities:
1. Technical review
2. Community management
3. Project sustainability
4. Contributor retention

Provide:

<technical_feedback>
How to structure code review feedback that's constructive but maintains standards
</technical_feedback>

<community_response>
Draft public comment that manages community expectations while being fair
</community_response>

<private_communication>
How to have a private conversation with the contributor about collaboration
</private_communication>

<decision_framework>
Should you: merge as-is, request changes, offer to pair program, or close?
Walk through the decision tree and trade-offs of each option.
</decision_framework>

<precedent_consideration>
How does this decision affect future contributions and project culture?
</precedent_consideration>
```
