# Recursive Self-Improvement Prompting: 10 example prompts

Recursive Self-Improvement Prompting (RSIP) involves AI generating output, critiquing it from multiple perspectives, and recursively revising it through iterative cycles until quality thresholds are met. The key is diverse evaluation criteria at each recursion level.

## 1. Basic Function Refactoring

```text
Write a function to parse CSV data with error handling.

Recursion Level 1: Initial generation
[Generate code]

Self-critique Level 1 (Code Quality):
Identify 3 weaknesses in:
- Readability
- Error handling completeness
- Edge case coverage

Recursion Level 2: Address critique
[Generate improved version]

Self-critique Level 2 (Performance):
Identify 3 weaknesses in:
- Memory efficiency
- Processing speed
- Scalability

Recursion Level 3: Address critique
[Generate optimized version]

Self-critique Level 3 (Maintainability):
Identify 3 weaknesses in:
- Documentation
- Testability
- Code organization

Recursion Level 4: Final version
[Generate production-ready code]

Stopping condition: Zero critical issues across all three perspectives.
```

## 2. API Documentation Generation (Basic-Intermediate)

```text
Generate API documentation for this endpoint:

[paste code]

Cycle 1: Initial documentation
Generate comprehensive API docs.

Self-evaluation Cycle 1 (Completeness):
Score out of 10 for:
- Parameter descriptions
- Response examples
- Error scenarios
If any score <8, identify what's missing and regenerate.

Cycle 2: Enhanced documentation

Self-evaluation Cycle 2 (Usability):
Score out of 10 for:
- Clarity for junior developers
- Code examples quality
- Integration guidance
If any score <8, identify gaps and regenerate.

Cycle 3: Refined documentation

Self-evaluation Cycle 3 (Accuracy):
Verify:
- All edge cases documented
- Examples actually work
- Schema matches implementation
Fix any discrepancies and regenerate.

Cycle 4: Final documentation

Stopping condition: All scores >=8 and zero inaccuracies.
```

## 3. SQL Query Optimization Loop (Intermediate)

```text
Optimize this database query:

[paste query and schema]

Generation 1: Initial optimization
Apply basic indexing and query restructuring.

Self-audit 1 (Performance):
- Estimated query plan cost
- Index usage efficiency
- JOIN strategy effectiveness
Rate each 1-10. If any <7, identify issue and regenerate.

Generation 2: Performance-tuned query

Self-audit 2 (Correctness):
- Does it return same results as original?
- Are NULL values handled correctly?
- Edge cases covered?
If any issues found, fix and regenerate.

Generation 3: Correct optimized query

Self-audit 3 (Trade-offs):
- Write performance impact
- Index maintenance overhead
- Query complexity for maintainers
If trade-offs unacceptable, rebalance and regenerate.

Generation 4: Balanced optimized query

Stopping condition: Performance >7/10, correctness verified, trade-offs acceptable.
```

## 4. Component Design with Multi-Perspective Critique (Intermediate)

```text
Design a React component for a complex form with validation.

Iteration 0: Initial design
Create component structure and props interface.

Critique Lens 1 (Developer Experience):
Evaluate:
- API simplicity
- Type safety
- Documentation clarity
List 3 improvements. Apply and regenerate.

Iteration 1: DX-improved design

Critique Lens 2 (User Experience):
Evaluate:
- Accessibility (WCAG 2.1 AA)
- Performance (render efficiency)
- Error message quality
List 3 improvements. Apply and regenerate.

Iteration 2: UX-enhanced design

Critique Lens 3 (Engineering):
Evaluate:
- Testability
- State management complexity
- Bundle size impact
List 3 improvements. Apply and regenerate.

Iteration 3: Engineering-optimized design

Meta-critique:
Did recursive improvements introduce conflicts between perspectives?
If yes, find balanced solution and regenerate.

Iteration 4: Final harmonized design

Stopping condition: Scores >8/10 on all three lenses, no conflicts.
```

## 5. Error Handling Strategy Evolution (Intermediate-Advanced)

```text
Implement comprehensive error handling for a payment service.

Round 0: Basic implementation
Implement try-catch and error responses.

Self-improvement Round 1 (Security):
Critique for:
- Information leakage in errors
- PCI compliance issues
- Logging of sensitive data
Score each 1-10. Fix all <9 and regenerate.

Round 1: Security-hardened implementation

Self-improvement Round 2 (Reliability):
Critique for:
- Transient vs permanent failure distinction
- Retry logic appropriateness
- Idempotency guarantees
Score each 1-10. Fix all <8 and regenerate.

Round 2: Reliable implementation

Self-improvement Round 3 (Observability):
Critique for:
- Error categorization for metrics
- Trace context propagation
- Actionable error messages
Score each 1-10. Fix all <8 and regenerate.

Round 3: Observable implementation

Self-improvement Round 4 (Developer Experience):
Critique for:
- Error type discriminability
- Helper functions for common patterns
- Documentation completeness
Score each 1-10. Fix all <8 and regenerate.

Round 4: Production-ready implementation

Stopping condition: All scores >=8, compiles, passes static analysis.
```

## 6. Architecture Design with Recursive Validation (Advanced)

```text
Design a microservices architecture for an e-commerce platform.

Level 0: Initial architecture
Create high-level service boundaries and interactions.

Validation Level 1 (Technical Soundness):
Critique:
- Service coupling levels
- Data consistency strategy
- Scalability bottlenecks
Rate each dimension 1-10. If any <7, refactor and recurse.

Level 1: Technically sound architecture

Validation Level 2 (Operational Feasibility):
Critique:
- Deployment complexity
- Monitoring coverage
- Failure recovery procedures
Rate each 1-10. If any <7, simplify and recurse.

Level 2: Operationally feasible architecture

Validation Level 3 (Team Capability):
Critique against team profile:
- Technology stack familiarity
- Required headcount
- Learning curve
Rate each 1-10. If any <6, adjust and recurse.

Level 3: Team-appropriate architecture

Validation Level 4 (Business Alignment):
Critique:
- Time to market
- Cost within budget
- Competitive advantage
Rate each 1-10. If any <7, optimize and recurse.

Level 4: Business-aligned architecture

Meta-validation:
Are there conflicts between validation levels?
If yes, find optimal trade-offs and recurse.

Level 5: Final balanced architecture

Stopping condition: All validations >=7, no unresolved conflicts.
```

## 7. Test Suite with Recursive Coverage Improvement (Advanced)

```text
Create a comprehensive test suite for this authentication module:

[paste code]

Generation 0: Initial tests
Write tests for happy paths.

Self-analysis 0 (Coverage):
- Line coverage: X%
- Branch coverage: Y%
- Mutation score: Z%
If any <80%, identify gaps and recurse with added tests.

Generation 1: Expanded tests

Self-analysis 1 (Quality):
For each test, score:
- Clarity of intent
- Brittleness risk
- Execution speed
If average <8/10, improve and recurse.

Generation 2: Quality tests

Self-analysis 2 (Completeness):
Check for:
- Security vulnerability tests
- Performance regression tests
- Integration failure scenarios
If gaps found, add and recurse.

Generation 3: Comprehensive tests

Self-analysis 3 (Maintainability):
Evaluate:
- Test duplication
- Setup/teardown complexity
- Helper function reusability
If issues found, refactor and recurse.

Generation 4: Maintainable tests

Self-analysis 4 (Effectiveness):
Simulate:
- Would these catch the last 3 production bugs?
- Do they test behavior vs implementation?
- Are assertions meaningful?
If any "no", improve and recurse.

Generation 5: Effective tests

Stopping condition: Coverage >80%, quality >8/10, no gaps, maintainable, effective.
```

## 8. Code Review with Recursive Depth (Advanced-Expert)

```text
Review this pull request for a critical payment feature:

[paste code and description]

Review Depth 0: Surface-level review
Identify obvious issues (syntax, style, basic logic).

Recursive Deepening 1 (Correctness):
For each identified issue, ask:
- What's the root cause?
- Are there related issues?
- What test would catch this?
Generate new issues list. If >5 items, recurse to next depth.

Review Depth 1: Logic-level review
Analyze algorithms, data flow, state management.

Recursive Deepening 2 (System Impact):
For each logic issue, analyze:
- Downstream effects on other services
- Database consistency implications
- Performance characteristics at scale
Generate system-level concerns. If >3 items, recurse.

Review Depth 2: System-level review
Evaluate architecture fit, integration points, scalability.

Recursive Deepening 3 (Production Risk):
For each system concern, assess:
- Failure modes and blast radius
- Monitoring and debugging capability
- Rollback complexity
Generate risk assessment. If high-severity risks found, recurse.

Review Depth 3: Risk analysis
Detailed threat modeling and failure scenario analysis.

Meta-review:
- Is review feedback actionable?
- Am I being too pedantic or too lenient?
- Did I provide solutions, not just problems?
If any "no", refine review and recurse.

Review Depth 4: Final comprehensive review

Stopping condition: No critical issues, feedback actionable, appropriate depth.
```

## 9. Migration Strategy with Recursive Risk Mitigation (Expert)

```text
Plan migration from monolith to microservices for a 500K LOC application.

Strategy 0: Initial plan
Outline migration approach and timeline.

Risk Recursion 1 (Technical Risks):
Identify top 5 technical risks.
For each risk:
- Mitigation strategy
- Residual risk level
If any residual risk is HIGH, revise plan and recurse.

Strategy 1: Risk-mitigated plan

Risk Recursion 2 (Business Risks):
Identify top 5 business risks.
For each risk:
- Impact on revenue/customers
- Mitigation strategy
If any HIGH impact risks, revise plan and recurse.

Strategy 2: Business-safe plan

Risk Recursion 3 (Team Risks):
Identify top 5 team/organizational risks.
For each risk:
- Capability gaps
- Mitigation through training/hiring
If critical gaps remain, revise plan and recurse.

Strategy 3: Team-feasible plan

Risk Recursion 4 (Integration Risks):
For each service boundary:
- Data consistency challenges
- Integration testing complexity
If complexity >7/10, simplify boundaries and recurse.

Strategy 4: Integration-optimized plan

Risk Recursion 5 (Operational Risks):
For deployment strategy:
- Zero-downtime feasibility
- Rollback complexity
- Monitoring coverage
If any HIGH risk, revise approach and recurse.

Strategy 5: Production-safe plan

Meta-analysis:
Run plan through pre-mortem:
"It's 12 months later. The migration failed. Why?"
If plausible failure scenarios emerge, address and recurse.

Strategy 6: Failure-hardened plan

Stopping condition: All risk categories <MEDIUM, pre-mortem shows no plausible failures.
```

## 10. System Design with Multi-Dimensional Recursive Optimization (Expert)

```text
Design a real-time collaborative editing system (like Google Docs).

Design 0: Initial architecture
Provide baseline design with technology choices.

Optimization Dimension 1 (Latency):
Current p95 latency estimate: Xms
Target: <50ms

Self-improve:
- Identify latency bottlenecks
- Apply optimizations
- Re-estimate latency
If target not met, recurse with new optimizations.

Design 1: Latency-optimized

Optimization Dimension 2 (Consistency):
Current consistency model: [eventual/strong/causal]
Conflict resolution quality: Y/10

Self-improve:
- Evaluate CRDT vs OT trade-offs
- Strengthen conflict resolution
- Re-evaluate consistency
If quality <8/10, recurse.

Design 2: Consistency-optimized

Optimization Dimension 3 (Scalability):
Current concurrent users: N
Target: 100K concurrent

Self-improve:
- Identify scaling bottlenecks
- Apply horizontal scaling strategies
- Re-estimate capacity
If target not met, recurse.

Design 3: Scale-optimized

Optimization Dimension 4 (Cost):
Current estimated cost at target scale: $X/month
Budget: $Y/month

Self-improve:
- Identify cost centers
- Apply cost optimizations
- Re-estimate costs
If over budget, recurse.

Design 4: Cost-optimized

Cross-Dimension Validation:
Check for conflicts:
- Did latency optimization hurt consistency?
- Did cost optimization reduce scalability?
- Did scale optimization increase latency?

If conflicts exist, find Pareto-optimal balance and recurse.

Design 5: Balanced design

Operational Dimension:
Evaluate:
- Deployment complexity: X/10
- Monitoring coverage: Y/10
- On-call burden: Z/10

If any <7/10, simplify and recurse.

Design 6: Operationally sound design

Resilience Dimension:
For each component:
- Failure probability
- Blast radius
- Recovery time

If any single point of failure with HIGH impact, add redundancy and recurse.

Design 7: Resilient design

Developer Experience Dimension:
Evaluate client library API:
- Integration complexity
- Learning curve
- Type safety

If DX score <8/10, improve API and recurse.

Design 8: DX-optimized design

Meta-Optimization:
Total system complexity score: X/10
If >7/10 (too complex), identify simplification opportunities and recurse.

Design 9: Simplified design

Final Validation:
Run design through all dimensions simultaneously.
Score each dimension.
If any <7/10 OR conflicts exist, perform multi-objective optimization and recurse.

Design 10: Final production-ready design

Stopping condition: All dimensions >=7/10, no conflicts, complexity acceptable.
```
