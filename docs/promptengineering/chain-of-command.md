# Chain of Command: 10 example prompts

## 1. Basic example

```text
I need a code review for this pull request before merging.

Command chain:

Agent 1 (Style Reviewer):
- Check code formatting and style consistency
- Verify naming conventions
- Report style issues

Then pass to Agent 2 (Security Checker):
- Scan for security vulnerabilities
- Check for exposed secrets or API keys
- Validate input sanitization
- Report security concerns

Finally Agent 3 (Test Verifier):
- Verify test coverage meets 80% threshold
- Check that tests actually test the new code
- Ensure tests pass
- Report test quality

Each agent reports findings to the next. Final agent provides consolidated review.

[paste PR code]
```

## 2. **API Implementation Pipeline** (Basic-Intermediate)

```text
Build a REST API endpoint for user profile updates.

Delegate to specialized agents in sequence:

Agent 1 (API Designer):
- Design the endpoint structure (method, path, request/response schemas)
- Define validation rules
- Specify error responses
- Output: OpenAPI spec

Agent 2 (Implementation Engineer):
- Implement the endpoint based on the spec from Agent 1
- Add input validation
- Include error handling
- Output: Implementation code

Agent 3 (Test Engineer):
- Write unit tests for the implementation from Agent 2
- Write integration tests
- Test edge cases and error scenarios
- Output: Test suite

Agent 4 (Documentation Writer):
- Generate API documentation from Agent 1's spec
- Add usage examples
- Document authentication requirements
- Output: API docs

Each agent uses the previous agent's output as input.
```

## 3. **Bug Investigation Chain** (Intermediate)

```text
Users report that checkout fails intermittently (roughly 5% of attempts).

Deploy investigation team in sequence:

Agent 1 (Bug Reporter/Triage):
Your role: Gather and structure information
- Collect error logs for failed checkouts
- Identify patterns (time of day, user segments, cart contents)
- Classify severity and frequency
- Output: Structured bug report with reproduction steps

Pass to Agent 2 (Debugger/Investigator):
Your role: Find root cause
- Analyze logs from Agent 1
- Trace code execution path
- Identify the failing component
- Propose hypothesis for the bug
- Output: Root cause analysis

Pass to Agent 3 (Fix Engineer):
Your role: Implement solution
- Create fix based on Agent 2's analysis
- Ensure fix doesn't break other flows
- Add logging to prevent future similar issues
- Output: Code fix with explanation

Pass to Agent 4 (QA Validator):
Your role: Verify fix
- Test the fix from Agent 3
- Verify original bug is resolved
- Check for regressions
- Load test to ensure it handles volume
- Output: Validation report with approval/rejection

[paste error logs and checkout code]
```

## 4. **Documentation Generation Pipeline** (Intermediate)

```text
Generate comprehensive documentation for this codebase.

Agent 1 (Code Analyzer):
- Scan codebase structure
- Identify public APIs, functions, and classes
- Extract function signatures and types
- Map dependencies between modules
- Output: Code structure analysis JSON

Agent 2 (Documentation Writer):
- Take Agent 1's analysis
- Write clear explanations for each component
- Generate usage examples
- Create getting-started guide
- Output: Draft documentation

Agent 3 (Technical Reviewer):
- Review Agent 2's documentation for accuracy
- Verify code examples actually work
- Check for missing critical information
- Identify confusing sections
- Output: Review notes with required changes

Agent 4 (Documentation Editor):
- Apply Agent 3's feedback to Agent 2's draft
- Improve clarity and readability
- Ensure consistent tone and formatting
- Add diagrams where helpful
- Output: Final documentation

[paste codebase path or provide repo URL]
```

## 5. **Feature Implementation Pipeline with Structured Handoffs** (Intermediate-Advanced)

```text
Implement "dark mode" feature for the React application.

Stage 1 - Planning (Requirements Analyst):
{
  "role": "requirements_analyst",
  "tasks": [
    "Analyze user stories and acceptance criteria",
    "Identify all UI components that need dark mode",
    "Define color palette and design tokens",
    "List technical requirements (localStorage, theme context, etc.)"
  ],
  "output_format": "requirements_doc",
  "pass_to": "architect"
}

Stage 2 - Architecture (Technical Architect):
{
  "role": "technical_architect",
  "input": "requirements_doc from Stage 1",
  "tasks": [
    "Design theme system architecture",
    "Plan component modification strategy",
    "Define theme context and hooks structure",
    "Identify integration points"
  ],
  "output_format": "technical_design",
  "pass_to": "implementer"
}

Stage 3 - Implementation (Senior Developer):
{
  "role": "senior_developer",
  "input": "technical_design from Stage 2",
  "tasks": [
    "Implement theme context and provider",
    "Create theme toggle component",
    "Update all components identified in Stage 1",
    "Add persistence to localStorage"
  ],
  "output_format": "code_implementation",
  "pass_to": "test_engineer"
}

Stage 4 - Testing (QA Engineer):
{
  "role": "qa_engineer",
  "input": "code_implementation from Stage 3",
  "tasks": [
    "Write unit tests for theme logic",
    "Create integration tests for theme switching",
    "Test accessibility (contrast ratios, etc.)",
    "Verify persistence across sessions"
  ],
  "output_format": "test_results",
  "pass_to": "reviewer"
}

Stage 5 - Review (Code Reviewer):
{
  "role": "code_reviewer",
  "input": "code_implementation from Stage 3 + test_results from Stage 4",
  "tasks": [
    "Review implementation quality",
    "Check test coverage",
    "Verify accessibility standards",
    "Approve or request changes"
  ],
  "output_format": "review_decision"
}

Execute this chain with each agent only starting after receiving input from previous agent.
```

## 6. **CI/CD Pipeline Orchestration** (Advanced)

```text
Set up complete CI/CD pipeline for a Node.js microservice.

Pipeline Commander coordinates these specialized agents:

Agent 1 (Build Engineer):
Role: Set up build process
- Configure Node.js version and dependencies
- Set up build scripts
- Configure environment variables
- Output: Build configuration (Dockerfile, package.json scripts)
Status: START → Build Engineer

Agent 2 (Test Orchestrator):
Role: Configure all testing layers
Input: Build config from Agent 1
- Set up unit test runner (Jest)
- Configure integration tests
- Set up test database
- Configure code coverage reporting
- Output: Test configuration
Status: WAIT for Agent 1 → Test Orchestrator

Agent 3 (Security Scanner):
Role: Security validation
Input: Build artifacts from Agent 1
Run in parallel with Agent 2:
- Scan dependencies for vulnerabilities (npm audit)
- Run SAST tools (Semgrep, SonarQube)
- Check for secrets in code
- Output: Security report
Status: WAIT for Agent 1 → Security Scanner (parallel)

Agent 4 (Quality Gate):
Role: Decision maker
Input: Test results from Agent 2 + Security report from Agent 3
- Evaluate if tests pass
- Check coverage threshold (>80%)
- Review security findings
- Decision: PROCEED or BLOCK
Status: WAIT for Agent 2 AND Agent 3 → Quality Gate

Agent 5 (Container Builder):
Role: Build and push container
Input: PROCEED decision from Agent 4
- Build Docker image
- Tag with commit SHA and version
- Push to container registry
- Output: Image URL and tags
Status: WAIT for Agent 4 PROCEED → Container Builder

Agent 6 (Deployment Manager):
Role: Deploy to environments
Input: Image URL from Agent 5
- Deploy to staging first
- Run smoke tests
- If pass, deploy to production with blue-green strategy
- Output: Deployment status
Status: WAIT for Agent 5 → Deployment Manager

Agent 7 (Monitor):
Role: Post-deployment validation
Input: Deployment status from Agent 6
- Check application health
- Monitor error rates for 15 minutes
- Alert if issues detected
- Output: Validation report
Status: WAIT for Agent 6 → Monitor

Execute this command chain with proper ordering and parallelization where noted.
```

## 7. **Multi-Service Deployment with Error Handling** (Advanced)

```text
Deploy 5 microservices with dependencies in correct order.

Service dependency graph:
- auth-service (no dependencies)
- user-service (depends on auth-service)
- product-service (depends on auth-service)
- order-service (depends on user-service, product-service)
- notification-service (depends on order-service)

Deployment Commander orchestrates:

Phase 1 (Dependency Resolver):
- Analyze dependency graph
- Calculate deployment order
- Output: [auth, [user, product], order, notification]

Phase 2 (Parallel Deployment Group 1):
Deploy Agent for auth-service:
- Deploy auth-service
- Wait for health check
- If FAIL → ABORT all, rollback
- If SUCCESS → Signal ready

Phase 3 (Parallel Deployment Group 2):
Only start after Phase 2 SUCCESS.

Deploy Agent A for user-service:
- Deploy user-service
- Health check
- Report status

Deploy Agent B for product-service:
- Deploy product-service
- Health check
- Report status

Synchronization Point:
- Wait for BOTH Agent A and B to succeed
- If ANY fail → Rollback all of Phase 2 and 3

Phase 4 (Deploy order-service):
Only start after Phase 3 SUCCESS.
- Deploy order-service
- Verify it can reach user-service and product-service
- Health check
- If FAIL → Rollback Phases 2, 3, 4

Phase 5 (Deploy notification-service):
Only start after Phase 4 SUCCESS.
- Deploy notification-service
- Verify end-to-end flow
- If FAIL → Rollback Phases 2, 3, 4, 5

Phase 6 (Validation):
- Run integration tests across all services
- Monitor for 10 minutes
- If issues → Full rollback
- If success → Mark deployment complete

Error Handling Protocol:
- Any phase failure triggers rollback of that phase + all subsequent phases
- Rollback preserves previous working versions
- Notification sent to team on any failure

[provide service configurations and current versions]
```

## 8. **Architecture Design Review Board** (Advanced)

```text
Evaluate this proposed microservices architecture for approval.

Convene review board with specialist roles:

Reviewer 1 (Performance Architect):
Focus: Performance and scalability
- Analyze expected load patterns
- Identify bottlenecks
- Review caching strategy
- Check database query patterns
- Output: Performance assessment (APPROVE/CONCERNS/REJECT)

Reviewer 2 (Security Architect):
Focus: Security posture
- Review authentication/authorization flows
- Check data encryption (in transit, at rest)
- Validate API security
- Assess attack surface
- Output: Security assessment (APPROVE/CONCERNS/REJECT)

Reviewer 3 (Operations Engineer):
Focus: Operational complexity
- Evaluate monitoring and observability
- Review deployment complexity
- Check disaster recovery plan
- Assess maintenance burden
- Output: Ops assessment (APPROVE/CONCERNS/REJECT)

Reviewer 4 (Cost Analyst):
Focus: Resource efficiency
- Estimate infrastructure costs
- Identify over-provisioning
- Suggest cost optimizations
- Calculate ROI
- Output: Cost assessment (APPROVE/CONCERNS/REJECT)

Reviewer 5 (Staff Engineer):
Focus: Technical excellence
- Review code organization
- Check design patterns usage
- Evaluate testability
- Assess technical debt
- Output: Technical assessment (APPROVE/CONCERNS/REJECT)

Review Coordinator (Final Decision Maker):
Receives all 5 assessments:
- If ALL approve → Architecture APPROVED
- If ANY reject → Architecture REJECTED, return for revision
- If concerns but no reject → Request mitigation plan for concerns

Each reviewer works independently, then coordinator synthesizes.

[paste architecture diagram and design doc]
```

## 9. **Incident Response Coordination with Escalation** (Expert)

```text
Production incident: API response times spiked to 30s, affecting 80% of requests.

Incident Commander activates response chain:

Level 1 - First Response (On-Call Engineer):
Immediate actions (0-5 minutes):
- Acknowledge incident
- Check monitoring dashboards
- Identify affected services
- Quick diagnosis: Is this a known issue?
- Decision: Can I resolve? YES → proceed, NO → escalate to Level 2

If Level 1 escalates:

Level 2 - Service Owner (Senior Engineer):
Actions (5-15 minutes):
Input: Level 1's initial findings
- Deep dive into service logs
- Check recent deployments
- Review database performance
- Identify root cause hypothesis
- Decision: Can rollback fix this?
  - If YES → execute rollback, monitor
  - If NO → escalate to Level 3

If Level 2 escalates:

Level 3 - Infrastructure Team:
Actions (15-30 minutes):
Input: Level 2's analysis
- Check infrastructure metrics (CPU, memory, network)
- Review auto-scaling events
- Investigate database performance
- Check for platform issues
- Decision: Infrastructure problem or application?
  - If infrastructure → fix and report
  - If application → escalate to Level 4

If Level 3 escalates:

Level 4 - War Room (Multiple Specialists):
Parallel investigation by:
- Backend Lead: Application code review
- DBA: Database query analysis
- DevOps: Infrastructure deep dive
- Product: Customer impact assessment

War Room Coordinator:
- Synthesizes findings from all specialists
- Decides on mitigation strategy
- Coordinates implementation
- Monitors resolution

Level 5 - Executive Escalation:
If incident >1 hour with no resolution:
- CTO notified
- Customer communication prepared
- Stakeholder updates coordinated

Post-Incident (After Resolution):
Incident Commander assigns:
- Post-mortem owner
- Timeline documentation
- Root cause analysis
- Prevention measures design

Each level has authority to resolve OR escalate. Clear handoff protocol required.
```

## 10. **Release Management Orchestration with Approval Gates** (Expert)

```text
Orchestrate v2.0.0 release across development, staging, and production.

Release Manager coordinates multi-stage approval pipeline:

Stage 1 - Release Preparation (Release Engineer):
<preparation>
Tasks:
- Create release branch from main
- Generate changelog from commits
- Update version numbers
- Create release notes
- Build release artifacts
Output: Release package + documentation
Gate: Self-approved (procedural)
</preparation>

Stage 2 - Automated Validation (QA Automation):
<validation>
Input: Release package from Stage 1
Tasks:
- Run full test suite (unit, integration, e2e)
- Execute performance benchmarks
- Run security scans
- Validate backward compatibility
Decision: PASS/FAIL
Gate: Must PASS to proceed
If FAIL → Return to development, block release
</validation>

Stage 3 - QA Approval (QA Lead):
<qa_review>
Input: Test results from Stage 2
Tasks:
- Review test coverage
- Manual exploratory testing
- Verify known issues are documented
- Check regression tests pass
Decision: APPROVE/REJECT/REQUEST_CHANGES
Gate: Must APPROVE to proceed
Escalation: If REJECT, notify Engineering Manager
</qa_review>

Stage 4 - Staging Deployment (DevOps Engineer):
<staging_deploy>
Input: Approved package from Stage 3
Tasks:
- Deploy to staging environment
- Run smoke tests
- Verify all features work
- Load test with production-like traffic
Output: Staging deployment report
Gate: Health checks must pass
</staging_deploy>

Stage 5 - Product Approval (Product Manager):
<product_review>
Input: Working staging from Stage 4
Tasks:
- Verify features match requirements
- Review user-facing changes
- Approve release notes
- Confirm release timing
Decision: APPROVE/DELAY/REQUEST_CHANGES
Gate: Must APPROVE to proceed
Authority: Can DELAY release for business reasons
</product_review>

Stage 6 - Security Review (Security Team):
<security_review>
Input: Full release package + staging environment
Tasks:
- Review security scan results from Stage 2
- Verify no critical vulnerabilities
- Check compliance requirements met
- Validate data handling changes
Decision: APPROVE/CONDITIONAL_APPROVE/BLOCK
Gate: Must APPROVE or CONDITIONAL_APPROVE
Authority: Can BLOCK release for security issues
</security_review>

Stage 7 - Engineering Approval (Engineering Manager):
<engineering_approval>
Input: All previous stage results
Tasks:
- Review overall quality
- Assess risk level
- Verify team is prepared for support
- Check documentation completeness
Decision: APPROVE/REJECT
Gate: Final engineering sign-off
Authority: Ultimate veto power
</engineering_approval>

Stage 8 - Production Deployment (Release Manager):
<production_deploy>
Input: All approvals from Stages 3-7
Preconditions: ALL must be APPROVED
Tasks:
- Execute blue-green deployment
- Deploy to 10% of production (canary)
- Monitor for 1 hour
- If healthy → scale to 50%
- Monitor for 2 hours
- If healthy → scale to 100%
- Complete deployment

Rollback triggers:
- Error rate >1%
- Response time >2s p95
- Any critical errors
- Manual rollback request from any Stage 6-7 approver
</production_deploy>

Stage 9 - Post-Release Validation (SRE Team):
<post_release>
Input: Production deployment status from Stage 8
Tasks:
- Monitor metrics for 24 hours
- Track error rates
- Monitor customer feedback
- Verify rollback procedure works
Output: Release health report
Gate: Issues trigger investigation, not rollback
</post_release>

Stage 10 - Release Closure (Release Manager):
<closure>
Input: All stage results
Tasks:
- Archive release artifacts
- Document any issues encountered
- Schedule post-mortem if needed
- Close release ticket
- Notify stakeholders of completion
Output: Final release report
</closure>

Approval Gate Matrix:
- Stage 2 (Automation): Must PASS (automatic gate)
- Stage 3 (QA): Must APPROVE (manual gate)
- Stage 5 (Product): Must APPROVE (manual gate)
- Stage 6 (Security): Must APPROVE (manual gate)
- Stage 7 (Engineering): Must APPROVE (manual gate)

Any REJECT or BLOCK stops the pipeline. Release cannot proceed until issue resolved.

Emergency Override:
- CTO can override any gate except Security
- Security BLOCK requires VP Engineering + CTO joint approval to override

Execute this release chain with all gates and approvals tracked.
</closure>
```
