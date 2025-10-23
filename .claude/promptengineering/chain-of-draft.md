# Chain of Draft: 10 example prompts

## 1. Basic example

```text
I need to write an error message for when users exceed their API rate limit.

Draft 1: Write an initial error message for this scenario.

Review Draft 1: Critique this message considering:
- Clarity for developers
- Actionability (what can they do about it?)
- Technical accuracy
- Tone

Draft 2: Rewrite the error message addressing the critiques from the review.

Final output: Present Draft 2 as the recommended error message.
```

## 2. **Function Naming with Iterative Refinement** (Basic-Intermediate)

```text
I have this function that fetches user data, validates permissions,
caches the result, and logs the activity:

[paste code]

Draft 1: Suggest a function name and explain your reasoning.

Critique Draft 1: Evaluate the name against these criteria:
- Does it accurately describe all the function's responsibilities?
- Is it too long or too short?
- Does it follow project conventions?
- Does it suggest the function might be doing too much?

Draft 2: Based on the critique, either:
- Propose an improved function name, OR
- Suggest refactoring the function into multiple functions with appropriate names

Explain your final recommendation.
```

## 3. **Git Commit Message Refinement** (Intermediate)

```text
I made changes to our authentication system that:
- Fixed a bug where sessions expired too early
- Added logging for failed login attempts
- Refactored the token validation logic

Draft 1: Write a git commit message following conventional commits format.

Review Draft 1: Critique considering:
- Does the subject line accurately summarize the primary change?
- Are related changes grouped logically or should they be separate commits?
- Is the body descriptive enough for future developers?
- Are breaking changes or important details highlighted?

Draft 2: Revise the commit message (or split into multiple commits if needed)
addressing the review feedback.

Draft 3: Review Draft 2 and make final refinements for clarity and conciseness.

Provide the final commit message(s).
```

## 4. **API Endpoint Design with Critique Loop** (Intermediate)

```text
Design a REST API endpoint for users to search products with filters.

Requirements:
- Full-text search on name and description
- Filter by category, price range, availability
- Support sorting
- Pagination required
- Need to return facet counts for filters

Draft 1: Design the endpoint (method, path, request/response format).

Critique Draft 1: Evaluate against:
- RESTful best practices
- Query parameter vs request body appropriateness
- Response structure clarity
- Performance considerations (are we over-fetching?)
- Extensibility (can we add filters later?)

Draft 2: Redesign the endpoint addressing the critiques.

Critique Draft 2: Review for any remaining issues or edge cases:
- How does it handle invalid filter combinations?
- Is the pagination approach sound?
- Are there any security concerns?

Draft 3: Finalize the endpoint design with any last refinements.

Provide the final API specification with example requests/responses.
```

## 5. **Database Schema Design with Evolutionary Drafts** (Intermediate-Advanced)

```text
Design database schema for a task management system.

Requirements:
- Tasks have title, description, due date, priority
- Tasks belong to projects
- Tasks can have subtasks (nested)
- Tasks can be assigned to multiple users
- Need to track task history/changes

Draft 1: Create initial schema design (tables, columns, relationships).

Review Draft 1: Analyze for:
- Normalization issues
- How well does it handle the nested subtasks requirement?
- Query performance for common operations
- Is task history approach scalable?
- Missing indexes or constraints?

Draft 2: Revise the schema addressing the review points.

Review Draft 2: Consider additional concerns:
- How does this handle deep nesting (10+ levels of subtasks)?
- What happens when reassigning tasks between projects?
- Are there any data integrity risks?
- Is the history tracking approach efficient for auditing?

Draft 3: Create final schema incorporating all feedback.

Present the final schema with:
- Table definitions with all constraints
- Explanation of design decisions
- Potential optimization strategies
```

## 6. **Error Handling Strategy Design** (Advanced)

```text
Design error handling strategy for a distributed microservices system.

Context:
- 12 microservices
- Services communicate via REST and message queues
- Need consistent error responses
- Must support retry logic and circuit breakers
- Need observability into failures

Draft 1: Design the error handling approach including:
- Error classification (retriable vs non-retriable)
- Error response format
- Propagation strategy across service boundaries
- Logging and monitoring approach

Critique Draft 1: Challenge the design:
- Does this approach create tight coupling between services?
- How do we handle cascading failures?
- Is there enough context in errors for debugging?
- What happens to errors in async message processing?
- Are we leaking sensitive information in error messages?

Draft 2: Revise the strategy addressing the critique points.

Critique Draft 2: Evaluate operational aspects:
- How does on-call engineer diagnose issues with this approach?
- What's the alert fatigue risk?
- Are there edge cases in the retry logic (idempotency)?
- How do we version error formats as the system evolves?

Draft 3: Finalize the error handling strategy with all refinements.

Provide:
- Complete error handling specification
- Code examples for implementation
- Operational runbook snippets
```

## 7. **Component API Design with User Perspective** (Advanced)

```text
Design the API for a React data table component.

Requirements:
- Display tabular data with sorting and filtering
- Virtualization for large datasets (10K+ rows)
- Column resizing and reordering
- Row selection (single and multi)
- Custom cell renderers
- Export functionality

Draft 1: Design the component API (props, callbacks, ref methods).

Review Draft 1 from Developer Experience perspective:
- Is the API intuitive for common use cases?
- Are there too many required props?
- Is it flexible enough for advanced use cases?
- How does composition work (can users extend it)?
- Are there any performance footguns?

Draft 2: Redesign the API addressing DX concerns.

Review Draft 2 from Implementation perspective:
- Can this API be implemented efficiently?
- Are there any props that would cause excessive re-renders?
- How does this handle controlled vs uncontrolled patterns?
- What's the testing story for consumers?
- Is the TypeScript type experience good?

Draft 3: Final API design balancing DX and implementation concerns.

Provide:
- Complete TypeScript interface
- Usage examples for common scenarios
- Implementation notes for complex aspects
```

## 8. **System Architecture Design with Multi-Round Review** (Advanced)

```text
Design architecture for a real-time collaboration platform (think Google Docs).

Requirements:
- Multiple users editing simultaneously
- Conflict resolution
- Offline support with sync
- Version history
- 100ms latency requirement
- Must scale to 100 concurrent users per document

Draft 1: Propose initial architecture including:
- Client-side architecture
- Server-side architecture
- Communication protocol
- Conflict resolution approach
- Data persistence strategy

Critique Draft 1 - Technical Feasibility:
- Will the conflict resolution approach work at scale?
- Can we achieve 100ms latency with this design?
- How does offline sync handle conflicts?
- What happens during network partitions?

Draft 2: Revise architecture addressing feasibility concerns.

Critique Draft 2 - Operational Concerns:
- How do we deploy updates without disrupting active sessions?
- What's the monitoring and debugging story?
- How do we handle service degradation gracefully?
- What are the cost implications at scale?

Draft 3: Refine architecture with operational considerations.

Critique Draft 3 - Edge Cases:
- What if a user makes 1000 edits offline then syncs?
- How do we handle malicious users?
- What's the data retention and GDPR compliance story?
- How do we recover from total data loss of a document?

Draft 4: Finalize architecture with edge cases handled.

Provide:
- Complete architecture diagram
- Detailed component descriptions
- Failure mode analysis
- Scalability roadmap
```

## 9. **Code Review Feedback with Iterative Refinement** (Expert)

```text
I need to provide code review feedback on a pull request that has several issues.

The PR:
- Implements a new feature correctly
- Has poor variable naming
- Missing error handling in 3 places
- Adds 400 lines to an already 800-line file
- No tests included
- Doesn't follow team's TypeScript conventions

Draft 1: Write initial code review feedback.

Self-Review Draft 1: Critique your own feedback:
- Is the tone constructive or could it be discouraging?
- Are you explaining the "why" behind each suggestion?
- Are you prioritizing feedback (critical vs nice-to-have)?
- Are you offering specific solutions or just pointing out problems?
- Is any feedback subjective that should be acknowledged as such?

Draft 2: Rewrite the feedback addressing your self-critique.

Self-Review Draft 2: Consider the human element:
- How would you feel receiving this feedback?
- Are you acknowledging the good aspects of the PR?
- Are you inviting discussion rather than dictating changes?
- Is the feedback actionable with clear next steps?
- Have you considered the author's context (junior dev, time pressure, etc.)?

Draft 3: Final refined feedback that is constructive, clear, and respectful.

Provide the complete code review comment.
```

## 10. **Technical Design Document with Stakeholder Iterations** (Expert)

```text
Write a technical design document for migrating our monolithic app to microservices.

Context:
- Current monolith: 300K lines, 8 years old
- Team: 20 engineers, mixed experience
- Stakeholders: Engineering, Product, Executive leadership
- Timeline pressure: 12 months
- Business impact: High risk

Draft 1: Write initial design doc with:
- Executive summary
- Current state analysis
- Proposed architecture
- Migration strategy
- Timeline
- Risks and mitigations

Review Draft 1 - Technical Leadership perspective:
- Is the technical approach sound?
- Are the architectural decisions justified?
- Is the migration strategy realistic?
- What technical risks are underestimated?
- Are there alternative approaches worth considering?

Draft 2: Revise incorporating technical leadership feedback.

Review Draft 2 - Product/Business perspective:
- Is the business value clear?
- How does this impact feature delivery during migration?
- What happens if we need to pause/extend the timeline?
- Are success metrics defined?
- What's the rollback plan?

Draft 3: Revise balancing technical and business concerns.

Review Draft 3 - Team/Implementation perspective:
- Is this achievable with our current team skills?
- What knowledge gaps need to be filled?
- How is work distributed across team members?
- Are there dependencies that could block progress?
- What happens if key people leave during this project?

Draft 4: Refine with team capacity and risk management.

Review Draft 4 - Communication perspective:
- Can executives understand the tradeoffs from the summary?
- Can engineers understand what they need to build?
- Are open questions clearly marked?
- Is it clear what decisions need to be made and by whom?
- Does it invite feedback or feel like a done deal?

Draft 5: Final polish for clarity and audience appropriateness.

Provide the final design document ready for review.
```
