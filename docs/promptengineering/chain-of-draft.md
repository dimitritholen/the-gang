# Chain of Draft: 10 example prompts

## 1. Basic example

```text
Write an error message for when a user's credit card is declined.

Draft 1: Write the initial version focusing on clarity.

Review Draft 1: Evaluate for tone, clarity, and helpfulness. What's missing?

Draft 2: Revise based on review, improving empathy and providing actionable steps.

Review Draft 2: Is it now user-friendly and professionally written?

Final: Deliver the polished error message.
```

## 2. **API Response Schema Design** (Basic-Intermediate)

```text
Design a JSON response schema for a user profile endpoint.

Required fields: id, email, name, created_at, preferences

Draft 1: Create initial schema
- Design basic structure
- Include all required fields
- Add types

Critique Draft 1:
- Is the structure consistent with REST best practices?
- Are field names intuitive?
- Is nested structure appropriate?
- What about optional fields and null handling?

Draft 2: Revise schema
- Apply feedback from critique
- Improve naming conventions
- Add proper null handling
- Consider versioning

Critique Draft 2:
- Does this handle edge cases?
- Is it extensible for future fields?
- Are there any security concerns?

Final Draft: Deliver production-ready schema with documentation.
```

## 3. **Database Query Optimization** (Intermediate)

```text
Optimize this slow SQL query that retrieves user orders with product details:

[paste slow query]

Draft 1: Initial optimization attempt
- Analyze the query structure
- Propose first set of optimizations
- Rewrite the query

Review Draft 1:
- What's the expected performance improvement?
- Did we miss any obvious optimizations?
- Are there any new issues introduced?
- Check index usage

Draft 2: Second optimization pass
- Apply review feedback
- Add any missed optimizations
- Consider query restructuring
- Add appropriate indexes

Review Draft 2:
- Validate query correctness
- Check for edge cases
- Verify index recommendations are practical
- Consider maintenance implications

Draft 3: Final optimization
- Incorporate all feedback
- Add execution plan analysis
- Document the changes

Final: Provide optimized query with before/after metrics.
```

## 4. **React Component Refactoring** (Intermediate)

```text
Refactor this React component that has performance issues and poor structure:

[paste component code]

Draft 1: Initial refactoring
- Identify issues (prop drilling, unnecessary re-renders, etc.)
- Propose component structure
- Refactor with basic improvements

Critique Draft 1:
- Are there still performance issues?
- Is the component tree optimal?
- Have we addressed prop drilling?
- Are hooks used correctly?
- Is the code testable?

Draft 2: Second refactoring iteration
- Split into smaller components
- Implement proper memoization
- Add custom hooks for logic extraction
- Improve state management

Critique Draft 2:
- Is the component hierarchy too deep or too shallow?
- Are we over-optimizing?
- Is the code more readable?
- Have we introduced new complexity?

Draft 3: Final refinement
- Balance performance and readability
- Ensure components are reusable
- Add proper TypeScript types
- Verify no regressions

Final: Provide refactored component with explanation of improvements.
```

## 5. **System Design Document with Iterative Refinement** (Intermediate-Advanced)

```text
Create a system design document for a real-time chat application.

Requirements:
- Support 100K concurrent users
- Message persistence
- Typing indicators
- Read receipts
- File sharing

Draft 1: High-level design
- Architecture overview
- Component breakdown
- Technology choices
- Data flow

Review Draft 1:
- Is the architecture scalable to 100K users?
- Are technology choices justified?
- What about failure scenarios?
- Are there single points of failure?
- What's missing in the design?

Draft 2: Detailed design
- Address scalability concerns
- Add redundancy and failover
- Detail data models
- Include infrastructure diagram
- Add monitoring strategy

Review Draft 2:
- How do we handle message ordering at scale?
- What's the latency for message delivery?
- Are costs reasonable?
- Is the design over-engineered or under-engineered?
- What about security and privacy?

Draft 3: Security and optimization pass
- Add authentication/authorization
- Include encryption strategy
- Optimize for cost
- Add rate limiting
- Address privacy concerns

Review Draft 3:
- Are there any gaps in security?
- Is the design practically implementable?
- What's the migration strategy?
- Are we following industry best practices?

Final Draft: Complete system design with all sections polished and comprehensive.
```

## 6. **Algorithm Implementation with Performance Tuning** (Advanced)

```text
Implement an autocomplete search feature for a product catalog with 1M products.

Draft 1: Naive implementation
- Basic string matching algorithm
- Simple data structure
- Focus on correctness first

Benchmark Draft 1:
- Measure search latency
- Check memory usage
- Identify bottlenecks
- What's the time complexity?

Draft 2: First optimization
- Implement Trie data structure
- Add basic caching
- Optimize string matching

Benchmark Draft 2:
- Compare performance with Draft 1
- Is memory usage acceptable?
- What's the improvement percentage?
- Where are remaining bottlenecks?

Draft 3: Advanced optimization
- Add fuzzy matching for typos
- Implement ranking algorithm
- Use precomputed indexes
- Add debouncing

Benchmark Draft 3:
- Measure latency at various loads
- Check ranking quality
- Validate fuzzy matching accuracy
- Is it production-ready?

Draft 4: Production hardening
- Add error handling
- Implement fallback mechanisms
- Optimize for mobile devices
- Add telemetry

Final: Production-ready implementation with benchmarks and documentation.
```

## 7. **Technical Specification with Stakeholder Iterations** (Advanced)

```text
Write a technical specification for migrating from REST API to GraphQL.

Current state: 50 REST endpoints, 3 client applications

Draft 1: Initial specification
- Migration rationale
- Proposed GraphQL schema
- Migration phases
- Timeline estimate

Stakeholder Review Round 1:
From Engineering perspective:
- Is the migration plan realistic?
- What about backward compatibility?
- Resource requirements?

From Product perspective:
- Customer impact?
- Feature velocity during migration?

From DevOps perspective:
- Infrastructure changes?
- Monitoring and observability?

Draft 2: Revised specification
- Address backward compatibility with API gateway
- Add detailed phase breakdown
- Include risk mitigation strategies
- Adjust timeline based on feedback
- Add resource allocation plan

Stakeholder Review Round 2:
From Security:
- Authentication/authorization changes?
- Query depth limiting?
- Rate limiting strategy?

From Frontend team:
- Client migration complexity?
- Breaking changes?
- Developer experience improvements?

Draft 3: Comprehensive revision
- Add security considerations
- Detail client migration guides
- Include training plan
- Add rollback procedures
- Provide cost-benefit analysis

Technical Review:
- Are all technical concerns addressed?
- Is the spec implementable as written?
- Are success metrics defined?
- What could go wrong?

Final Draft: Complete technical specification ready for approval and implementation.
```

## 8. **Code Architecture Redesign with Multiple Review Cycles** (Advanced)

```text
Redesign the architecture of a monolithic e-commerce application for better maintainability.

Current issues:
- 200K lines of code in one codebase
- Tightly coupled modules
- Difficult to test
- Deployment takes 2 hours
- Frequent merge conflicts

Draft 1: Initial architecture proposal
- Propose modular monolith or microservices
- Define module boundaries
- Outline migration strategy

Architecture Review Panel 1:
Performance Architect reviews:
- Are the module boundaries optimal?
- What's the communication overhead?
- Latency concerns?

Maintainability Expert reviews:
- Is this more maintainable than current?
- Developer experience improvements?
- Testing strategy?

Draft 2: Refined architecture
- Adjust boundaries based on feedback
- Add detailed communication patterns
- Include testing strategy
- Define deployment pipeline
- Add observability plan

Architecture Review Panel 2:
Operations Engineer reviews:
- Deployment complexity?
- Monitoring requirements?
- Scaling strategy?

Staff Engineer reviews:
- Code organization standards?
- Dependency management?
- Technical debt migration plan?

Draft 3: Detailed implementation plan
- Phase-by-phase migration
- Team structure recommendations
- Technology choices with justifications
- Risk assessment
- Success metrics

Final Review:
Security Team:
- Security implications of new architecture?

Cost Analyst:
- Infrastructure cost changes?

Engineering Manager:
- Resource requirements realistic?
- Timeline achievable?

Final Draft: Approved architecture design with implementation roadmap.
```

## 9. **API Documentation with User Feedback Iterations** (Expert)

```text
Create comprehensive API documentation for a payment processing API.

Audience: Third-party developers integrating our payment system

Draft 1: Technical draft
- API reference for all endpoints
- Request/response schemas
- Authentication guide
- Error codes

Internal Developer Review:
- Is the documentation technically accurate?
- Are all endpoints covered?
- Are examples correct?
- What's confusing?

Draft 2: Improved technical content
- Fix technical inaccuracies
- Add more code examples in multiple languages
- Improve error code descriptions
- Add rate limiting documentation
- Include webhook documentation

Technical Writer Review:
- Is the language clear for non-native speakers?
- Is the structure logical?
- Are there gaps in the user journey?
- Is it scannable and easy to navigate?

Draft 3: Structural and clarity improvements
- Reorganize by user journey (not just endpoint list)
- Add quick-start guide
- Create tutorials for common use cases
- Improve navigation and search
- Add diagrams for complex flows

Beta User Testing:
Provide Draft 3 to 5 partner developers and gather feedback:
- What was confusing?
- What took longest to understand?
- What was missing?
- What was most helpful?

Draft 4: User-informed revision
- Add FAQ section based on common questions
- Expand troubleshooting guide
- Add more real-world examples
- Include best practices section
- Add security best practices
- Create migration guides

Support Team Review:
- Does this reduce support ticket volume?
- Are common issues addressed?
- Is troubleshooting guidance clear?

Draft 5: Support-informed refinement
- Add common error scenarios with solutions
- Include debugging checklist
- Add monitoring and logging recommendations
- Create "What to do when things go wrong" section

Final Review Committee:
- Product Manager: Business goals met?
- Engineering Lead: Technical accuracy confirmed?
- Developer Relations: Developer experience optimal?
- Legal: Compliance and terms clear?

Final Draft: Production documentation published to developer portal.
```

## 10. **Enterprise Software Proposal with Multi-Round Refinement** (Expert)

```text
Develop a proposal to replace our legacy inventory management system.

Context:
- Current system is 15 years old
- 200 daily users across 5 warehouses
- Critical to operations
- Budget: $500K
- Timeline: 12 months

Draft 1: Initial proposal
- Problem statement
- Proposed solution (build vs buy)
- High-level architecture
- Estimated costs
- Timeline
- Team requirements

Executive Review Round 1:
CFO questions:
- Total cost of ownership?
- ROI calculation?
- Risk of cost overruns?

CTO questions:
- Technical feasibility?
- Team capability?
- Integration complexity?

COO questions:
- Operational disruption during transition?
- Training requirements?
- Fallback plan if system fails?

Draft 2: Executive feedback incorporation
- Add detailed TCO analysis (5-year projection)
- Include ROI with conservative and optimistic scenarios
- Add detailed risk assessment with mitigation plans
- Break timeline into milestones with go/no-go gates
- Add contingency plans
- Detail change management process

Department Head Review Round 2:
Warehouse Managers:
- Will this actually improve our workflows?
- What's the learning curve?
- What if we need custom features?

IT Director:
- Infrastructure requirements?
- Support and maintenance plan?
- Security and compliance?

Finance Director:
- Budget breakdown by phase?
- Payment terms?
- Cost vs current system?

Draft 3: Operational feasibility refinement
- Add user workflow analysis showing improvements
- Include phased rollout plan (one warehouse at a time)
- Detail training program (in-person + online)
- Add customization budget and process
- Include detailed infrastructure requirements
- Add security audit plan
- Phase budget allocation

Vendor Evaluation (if buying):
Evaluate 3 vendor solutions against requirements:
- Feature comparison matrix
- Cost comparison (licensing, implementation, maintenance)
- Reference checks
- Demo feedback from end users

Build vs Buy Analysis:
In-house build assessment:
- Development timeline
- Required team size
- Ongoing maintenance cost
- Flexibility and control

Commercial solution assessment:
- Implementation timeline
- Vendor lock-in risk
- Customization limitations
- Support quality

Draft 4: Recommendation with full justification
- Clear build vs buy recommendation with reasoning
- If buy: Vendor selection with justification
- If build: Technology stack and team plan
- Detailed implementation roadmap
- Comprehensive risk register
- Success metrics and KPIs
- Change management plan
- Communication strategy

Board Presentation Review:
Legal:
- Contract terms reviewed?
- IP considerations?
- Liability and warranty?

HR:
- Organizational change impact?
- Headcount changes?

Procurement:
- Vendor due diligence complete?
- Terms negotiable?

Final Draft Review:
Independent consultant review:
- Is this proposal realistic?
- Are costs accurate?
- Timeline achievable?
- Risks adequately addressed?

Draft 5: Final refinement
- Address any remaining concerns
- Polish executive summary
- Ensure all appendices are complete
- Add lessons learned from similar projects
- Include testimonials or case studies
- Finalize budget with contingency

Board Approval Package:
- Executive summary (2 pages)
- Full proposal (30 pages)
- Financial models (spreadsheet)
- Risk analysis (detailed)
- Implementation Gantt chart
- Vendor contracts (if applicable)
- Governance structure

Final Proposal: Ready for board presentation and approval vote.
```
