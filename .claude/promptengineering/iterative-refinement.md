# Iterative Refinement Prompting: 10 example prompts

Iterative refinement involves progressively improving outputs through multiple rounds of feedback, analysis, and prompt adjustment. Each iteration builds on the previous one to converge on an optimal solution.

## 1. Basic Function Optimization

```text
Write a function to validate email addresses.

Iteration 1: Initial implementation
[AI provides code]

Feedback for Iteration 2:
- Add RFC 5322 compliance
- Handle edge cases (Unicode domains, plus addressing)

Iteration 2: Enhanced implementation
[AI provides improved code]

Feedback for Iteration 3:
- Optimize performance for bulk validation
- Add detailed error messages

Iteration 3: Final optimized version
[AI provides final code]
```

## 2. API Response Design with Progressive Enhancement (Basic-Intermediate)

```text
Design a JSON response structure for a user profile API endpoint.

Version 1: Basic structure
Provide initial design with essential fields.

Refinement Round 1:
Review output. Does it handle:
- Pagination for nested collections?
- HATEOAS links?
- Field filtering capabilities?

Add these requirements and regenerate.

Version 2: Enhanced structure

Refinement Round 2:
Evaluate against real-world constraints:
- Response size for mobile clients
- Versioning strategy
- Backward compatibility

Apply optimizations and regenerate.

Version 3: Production-ready structure

Final validation:
- OpenAPI 3.0 compliance check
- Performance characteristics
- Developer experience assessment
```

## 3. Database Query Optimization Loop (Intermediate)

```text
Optimize this slow PostgreSQL query:

[paste query and schema]

Round 1: Initial optimization
Provide your first optimization approach.

Self-critique Round 1:
- What's the query execution plan?
- Which indexes are actually used?
- What's the estimated cost reduction?

Round 2: Refined optimization
Based on self-critique, provide improved version.

Self-critique Round 2:
- Did optimization help write performance?
- Are there query patterns this breaks?
- What's the index maintenance overhead?

Round 3: Balanced optimization
Provide final query considering all trade-offs.

Stopping criteria:
- Query time reduced by >50%
- No negative impact on writes
- Index size remains reasonable
```

## 4. Error Handling Strategy Evolution (Intermediate)

```text
Implement error handling for a payment processing service.

Draft 1: Basic error handling
Implement try-catch blocks and error responses.

Iteration feedback:
- Are errors distinguishable by type?
- Can clients programmatically handle errors?
- Are errors properly logged for debugging?

Draft 2: Structured error handling
Implement error types, codes, and structured responses.

Iteration feedback:
- Do errors leak sensitive information?
- Are transient vs permanent failures distinguished?
- Is there proper context for debugging?

Draft 3: Production-grade error handling
Add security, retry logic, and observability.

Final review:
- Test against error scenarios
- Validate error response schema
- Ensure monitoring integration
```

## 5. Component Architecture Refinement (Intermediate-Advanced)

```text
Design a React component for a data table with sorting, filtering, and pagination.

Iteration 1: Component structure
Provide initial component architecture and props interface.

Review prompt:
Analyze for:
- State management complexity
- Reusability across different data types
- Performance with large datasets
- Accessibility compliance

Iteration 2: Refined architecture
Address identified issues in new design.

Review prompt:
Evaluate:
- Does it handle async data loading?
- Is virtualization needed for performance?
- How does it integrate with form state?
- What's the testing strategy?

Iteration 3: Optimized architecture
Incorporate performance and testing considerations.

Self-refine prompt:
- Code split opportunities
- Server component vs client component decisions
- Memoization strategy
- Bundle size impact

Iteration 4: Production-ready architecture
Final design with all considerations balanced.
```

## 6. API Design with Feedback Loops (Advanced)

```text
Design a GraphQL API for a multi-tenant SaaS application.

Phase 1: Initial schema design
Create schema with core types, queries, and mutations.

Self-review Phase 1:
- N+1 query vulnerabilities
- Authorization at field level
- Pagination strategy
- Real-time subscription needs

Phase 2: Security-hardened schema
Incorporate authorization and query complexity limits.

Self-review Phase 2:
- Performance under load
- Caching strategy
- Deprecation handling
- Versioning approach

Phase 3: Performance-optimized schema
Add DataLoader patterns and optimistic queries.

External validation:
Run schema against:
- GraphQL best practices checklist
- Security audit requirements
- Performance benchmarks
- DX evaluation criteria

Phase 4: Iteration based on validation
Address any gaps found in external validation.

Stopping criteria:
- All security requirements met
- Sub-100ms p95 latency target
- Zero breaking changes path exists
- Developer satisfaction score >8/10
```

## 7. Test Suite Development with Coverage Iteration (Advanced)

```text
Create comprehensive test suite for authentication module:

[paste code]

Round 1: Happy path tests
Write tests for successful authentication flows.

Coverage analysis 1:
- Current line coverage: X%
- Current branch coverage: Y%
- Untested code paths: [list]

Round 2: Edge case tests
Add tests for identified untested paths.

Coverage analysis 2:
- Updated line coverage: X%
- Updated branch coverage: Y%
- Error scenarios covered: Z%

Round 3: Integration tests
Add tests for external dependencies and race conditions.

Quality analysis:
- Are tests brittle or robust?
- Do tests document behavior?
- Test execution time acceptable?
- Flakiness assessment

Round 4: Test refinement
Improve test quality based on analysis.

Self-refine:
- Remove redundant tests
- Improve test names and organization
- Add missing assertions
- Optimize slow tests

Final validation:
- Coverage targets met (>90% line, >80% branch)
- No flaky tests
- Clear failure messages
- Fast execution time (<5s)
```

## 8. Migration Script with Risk Mitigation (Advanced-Expert)

```text
Write a database migration script to rename a critical table used across 50+ queries.

Version 1: Direct approach
Write migration with simple table rename.

Risk assessment 1:
- Zero-downtime possible?
- Rollback strategy?
- Data integrity guarantees?
- Application compatibility during migration?

Version 2: Phased approach
Implement migration with transition period.

Risk assessment 2:
- What happens if migration pauses mid-way?
- How long is the transition period?
- Monitoring and validation strategy?
- Performance impact during transition?

Version 3: Production-safe approach
Add validation, rollback triggers, and monitoring.

Dry-run simulation:
Test migration script against:
- Empty database
- Small dataset (1K rows)
- Large dataset (1M rows)
- Concurrent write scenarios

Version 4: Battle-tested approach
Incorporate learnings from simulation.

Final checklist:
- Idempotent execution
- Progress tracking
- Automatic rollback on failure
- Complete validation suite
- Runbook for operators

Iterate until all checklist items satisfied.
```

## 9. System Design with Constraint Satisfaction (Expert)

```text
Design a real-time multiplayer game backend supporting 10K concurrent players.

Iteration 1: Initial architecture
Provide high-level architecture with technology choices.

Constraint evaluation 1:
Check against:
- Latency budget (<50ms for player actions)
- Cost ceiling ($5K/month at target scale)
- Team capabilities (5 backend engineers, Go/TypeScript)
- Time to market (6 months)

Iteration 2: Constraint-aware architecture
Adjust design to meet constraints.

Performance modeling:
Calculate:
- Messages per second at peak load
- Database write/read patterns
- Network bandwidth requirements
- Infrastructure costs at scale

Iteration 3: Performance-optimized architecture
Optimize based on modeling results.

Failure mode analysis:
For each component, analyze:
- What happens when it fails?
- What's the blast radius?
- How fast can we recover?
- What's the monitoring strategy?

Iteration 4: Resilient architecture
Add redundancy, circuit breakers, and graceful degradation.

Operational complexity review:
- How many services to maintain?
- Deployment complexity?
- On-call burden?
- Observability coverage?

Iteration 5: Operationally simplified architecture
Balance reliability with maintainability.

Final validation:
Run architecture through:
- Latency budget verification
- Cost modeling at 1x, 5x, 10x scale
- Team capability assessment
- Timeline feasibility check

Iterate until all validations pass.
```

## 10. Code Generation with Self-Improvement Loop (Expert)

```text
Generate a production-ready REST API handler for file uploads with virus scanning.

Generation 1: Basic implementation
Create initial handler code.

Self-critique 1:
Review code for:
- Error handling completeness
- Input validation coverage
- Security vulnerabilities
- Resource cleanup
- Logging and observability

Generation 2: Hardened implementation
Fix issues identified in self-critique.

Self-critique 2:
Deeper analysis:
- Concurrent upload handling
- Memory leak possibilities
- Timeout configurations
- Retry logic for virus scanning
- Rate limiting

Generation 3: Robust implementation
Address concurrency and resource management.

Static analysis simulation:
Run mental checks for:
- SonarQube critical issues
- OWASP Top 10 compliance
- TypeScript strict mode violations
- ESLint errors
- Security audit flags

Generation 4: Quality-assured implementation
Fix all static analysis issues.

Integration test perspective:
What tests would fail? Consider:
- Malicious file uploads
- Oversized files
- Network failures during upload
- Virus scanner unavailability
- Concurrent upload limits

Generation 5: Test-informed implementation
Add defensive code for test scenarios.

Performance profiling:
Analyze:
- Memory allocation patterns
- CPU usage for large files
- Database query efficiency
- API response times

Generation 6: Performance-optimized implementation
Apply optimizations based on profiling.

Production readiness checklist:
- Graceful shutdown handling
- Health check endpoints
- Metrics emission
- Structured logging
- Configuration externalization
- Documentation completeness

Generation 7: Production-ready implementation

Stopping criteria met when:
- Zero critical/high severity issues
- All edge cases handled
- Performance targets achieved
- Observable and maintainable
- Fully documented
```
