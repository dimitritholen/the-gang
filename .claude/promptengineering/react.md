# ReAct Prompting: 10 example prompts

ReAct (Reasoning + Acting) is a framework that interleaves reasoning traces with task-specific actions. The model generates thoughts about what to do, takes actions, observes results, and continues this cycle until the task is complete.

The pattern follows: Thought → Action → Observation → Thought → Action → ...

## 1. Basic Debugging

```text
Debug why the login form is not submitting.

Thought 1: I need to first understand what happens when the submit button is clicked.
Action 1: Read the form component code to examine the submit handler.
Observation 1: [code shows onSubmit handler calls handleLogin function]

Thought 2: The handler exists. Let me check if there are any errors in the console.
Action 2: Check browser console logs for JavaScript errors.
Observation 2: [Console shows "Uncaught TypeError: Cannot read property 'email' of undefined"]

Thought 3: The error suggests the form data is undefined. Let me verify how form data is being accessed.
Action 3: Examine the handleLogin function implementation.
Observation 3: [Code shows e.target.email.value but form uses controlled components with state]

Thought 4: The issue is clear - the code is trying to access form values incorrectly for controlled components.
Action 4: Update handleLogin to use state values instead of e.target.
Observation 4: [Form now submits successfully]

Final Answer: The bug was caused by incorrect form data access. Fixed by using state values instead of e.target for controlled components.
```

## 2. API Integration Investigation (Basic-Intermediate)

```text
Integrate a third-party payment API but the documentation is unclear about authentication.

Thought 1: I need to understand the authentication mechanism. Let me start with the official docs.
Action 1: Search the API documentation for authentication methods.
Observation 1: [Docs mention "API key authentication" but don't specify header format]

Thought 2: The header format is ambiguous. Let me check if there are code examples.
Action 2: Look for code examples in the documentation.
Observation 2: [Found a curl example: curl -H "Authorization: Bearer API_KEY"]

Thought 3: So it uses Bearer token format. Let me verify this works with a test request.
Action 3: Make a test API call with Bearer token authentication.
Observation 3: [Returns 401 Unauthorized]

Thought 4: Bearer format failed. Let me try the alternative format I've seen in other APIs.
Action 4: Try "Authorization: API_KEY" format.
Observation 4: [Returns 401 Unauthorized]

Thought 5: Maybe it uses a custom header. Let me check the community forums.
Action 5: Search Stack Overflow and GitHub issues for authentication examples.
Observation 5: [Found issue thread showing "X-API-Key: YOUR_KEY" format]

Thought 6: Custom header approach. Let me test this format.
Action 6: Make request with X-API-Key header.
Observation 6: [Returns 200 OK with expected response]

Final Answer: Authentication requires custom header "X-API-Key" with the API key value. The documentation was misleading about Bearer format.
```

## 3. Performance Optimization Investigation (Intermediate)

```text
The dashboard page loads slowly. Optimize it to load under 2 seconds.

Thought 1: First, I need to measure the current performance to identify bottlenecks.
Action 1: Run Lighthouse performance audit on the dashboard.
Observation 1: [Total load time: 5.2s, LCP: 4.1s, FCP: 2.3s, TBT: 890ms]

Thought 2: LCP is the biggest issue at 4.1s. Let me identify what element is the LCP.
Action 2: Check Chrome DevTools Performance tab to identify LCP element.
Observation 2: [LCP element is a large data table with 1000+ rows]

Thought 3: Rendering 1000+ rows is expensive. Let me check if virtualization is implemented.
Action 3: Examine the table component implementation.
Observation 3: [Table renders all rows in DOM, no virtualization]

Thought 4: Implementing virtual scrolling should significantly improve render time.
Action 4: Add react-virtual library and implement virtualized list.
Observation 4: [Re-test: LCP reduced to 2.1s, but still above target]

Thought 5: Still not at target. Let me check the bundle size - maybe code splitting can help.
Action 5: Analyze bundle with webpack-bundle-analyzer.
Observation 5: [Dashboard bundle is 850KB, includes heavy chart library used on other pages]

Thought 6: The chart library is being loaded but not used on dashboard. Let me implement code splitting.
Action 6: Use dynamic imports to lazy-load chart components.
Observation 6: [Bundle reduced to 320KB, re-test: LCP: 1.4s, TBT: 210ms]

Thought 7: We're under 2s but can optimize further. Let me check API response times.
Action 7: Measure API call duration in Network tab.
Observation 7: [Dashboard API takes 800ms, returns redundant data]

Thought 8: API is slow and over-fetching. Let me optimize the query.
Action 8: Add field selection to API query to fetch only needed data.
Observation 8: [API time reduced to 320ms, final test: Total load: 1.6s]

Final Answer: Optimized from 5.2s to 1.6s through: (1) Virtual scrolling for large table, (2) Code splitting to reduce bundle, (3) API query optimization. All targets met.
```

## 4. Database Query Optimization with Testing (Intermediate)

```text
Optimize a slow user search query that times out with large datasets.

Thought 1: I need to see the current query and understand its performance characteristics.
Action 1: Read the search query implementation and execution plan.
Observation 1: [Query does LIKE '%search%' on multiple columns, full table scan, 12 seconds execution time]

Thought 2: LIKE with leading wildcard prevents index usage. Let me check existing indexes.
Action 2: Query database to show indexes on users table.
Observation 2: [Only primary key index exists, no indexes on searchable columns]

Thought 3: I should add indexes on search columns, but LIKE with wildcards won't use them efficiently.
Action 3: Research full-text search options for the database (PostgreSQL).
Observation 3: [PostgreSQL supports full-text search with GIN indexes and ts_vector]

Thought 4: Full-text search seems appropriate. Let me implement it.
Action 4: Add ts_vector column and GIN index, update query to use full-text search.
Observation 4: [Execution time: 1.2s for 1M rows, but searches for "john" miss "johnsmith"]

Thought 5: Tokenization is too aggressive. Let me adjust the search configuration.
Action 5: Use prefix matching with ts_vector for partial word matches.
Observation 5: [Now finds "johnsmith" but execution time increased to 2.8s]

Thought 6: Still too slow. Let me check if there's a way to combine approaches.
Action 6: Implement hybrid approach - exact prefix match with B-tree index for short queries, full-text for longer ones.
Observation 6: [Short queries: 120ms, long queries: 980ms]

Thought 7: Good performance but let me verify correctness with edge cases.
Action 7: Test with special characters, Unicode, and empty strings.
Observation 7: [Special characters cause errors in full-text mode]

Thought 8: Need to sanitize input for full-text search.
Action 8: Add input sanitization and escape special characters.
Observation 8: [All test cases pass, performance maintained]

Final Answer: Implemented hybrid search - B-tree prefix indexes for short queries (<3 chars), full-text search with GIN for longer queries. Performance improved from 12s to 120ms-980ms with proper handling of edge cases.
```

## 5. Security Vulnerability Assessment (Intermediate-Advanced)

```text
Audit the authentication system for security vulnerabilities.

Thought 1: I should start with the most critical aspects - password handling and session management.
Action 1: Examine password hashing implementation.
Observation 1: [Uses bcrypt with salt rounds of 10, looks secure]

Thought 2: Password hashing looks good. Let me check the session management.
Action 2: Review session token generation and storage.
Observation 2: [Uses JWT stored in localStorage, tokens don't expire]

Thought 3: Non-expiring tokens in localStorage is a security issue. Let me check if there's CSRF protection.
Action 3: Examine if CSRF tokens are implemented for state-changing operations.
Observation 3: [No CSRF tokens found, relies solely on JWT in localStorage]

Thought 4: This is vulnerable to XSS attacks. Let me verify the token validation.
Action 4: Test token validation by modifying token payload.
Observation 4: [Modified token is rejected, signature verification works]

Thought 5: Signature is validated but XSS could steal the token. Let me check Content Security Policy.
Action 5: Inspect HTTP headers for CSP and other security headers.
Observation 5: [No CSP header, no X-Frame-Options, no X-Content-Type-Options]

Thought 6: Missing security headers make XSS attacks easier. Let me check for XSS vulnerabilities.
Action 6: Test user-generated content rendering for XSS.
Observation 6: [User profile bio renders unescaped HTML - XSS vulnerability confirmed]

Thought 7: Found critical XSS vulnerability. Let me check authentication rate limiting.
Action 7: Test login endpoint with rapid requests.
Observation 7: [No rate limiting - vulnerable to brute force attacks]

Thought 8: Multiple vulnerabilities found. Let me prioritize and create remediation plan.
Action 8: Document all findings with severity levels and recommendations.
Observation 8: [List of vulnerabilities with CVSS scores and fix priorities]

Final Answer: Found 5 security issues:
1. CRITICAL: XSS in user-generated content (fix: implement DOMPurify)
2. HIGH: JWT in localStorage without expiration (fix: use httpOnly cookies with refresh tokens)
3. HIGH: No rate limiting on auth endpoints (fix: implement express-rate-limit)
4. MEDIUM: Missing security headers (fix: add helmet middleware)
5. LOW: No CSRF protection (fix: add CSRF tokens or SameSite cookie attribute)
```

## 6. Microservice Integration Debugging (Advanced)

```text
Debug intermittent 500 errors in production occurring between Order and Payment services.

Thought 1: Intermittent errors suggest timing or resource issues. Let me check recent deployment changes.
Action 1: Review deployment history for both services in the last 48 hours.
Observation 1: [Payment service deployed 36 hours ago with new retry logic]

Thought 2: New retry logic could be causing issues. Let me examine error logs.
Action 2: Query centralized logging for 500 errors between these services.
Observation 2: [Errors spike during high traffic periods, error message: "Connection pool exhausted"]

Thought 3: Connection pool exhaustion during high traffic. Let me check pool configuration.
Action 3: Examine database connection pool settings in Payment service.
Observation 3: [Pool size: 10, max wait time: 5000ms]

Thought 4: Pool of 10 seems small for production traffic. Let me check actual traffic patterns.
Action 4: Query metrics for concurrent request volume during error periods.
Observation 4: [Peak concurrent requests: 45-60, pool can't handle this]

Thought 5: Pool is undersized. But let me verify there are no connection leaks first.
Action 5: Check for unclosed connections in the code.
Observation 5: [Found async function not awaiting connection.release() in error path]

Thought 6: Connection leak in error handling! This would compound during high traffic.
Action 6: Fix connection leak and test in staging with load testing.
Observation 6: [Load test with 100 concurrent users: no errors, pool utilization: 40%]

Thought 7: Leak fixed but pool might still be undersized. Let me review the retry logic that was deployed.
Action 7: Examine the new retry implementation.
Observation 7: [Retries 3 times with exponential backoff, but doesn't release connection between retries]

Thought 8: Retries are holding connections! This multiplies the pool exhaustion problem.
Action 8: Modify retry logic to release and reacquire connections between attempts.
Observation 8: [Staging test successful, pool utilization remains healthy under load]

Thought 9: Fixes look good but let me verify end-to-end in production.
Action 9: Deploy fixes with gradual rollout and monitor error rates.
Observation 9: [Error rate dropped from 2.3% to 0.01% during peak traffic]

Final Answer: Root cause was combination of: (1) connection leak in error handling, (2) retry logic holding connections unnecessarily. Fixed by ensuring proper connection cleanup and releasing connections between retries. Error rate reduced from 2.3% to 0.01%.
```

## 7. Legacy Code Refactoring Strategy (Advanced)

```text
Refactor a 3000-line God Object class without breaking production.

Thought 1: I need to understand what this class does before refactoring.
Action 1: Analyze the class structure and identify distinct responsibilities.
Observation 1: [Class handles: user auth, data validation, API calls, logging, caching, email sending]

Thought 2: This violates single responsibility principle. Let me check test coverage first.
Action 2: Run test coverage analysis on this class.
Observation 2: [Test coverage: 34%, mostly happy path tests, no integration tests]

Thought 3: Low test coverage is risky for refactoring. Let me add characterization tests first.
Action 3: Write tests that document current behavior without modifying code.
Observation 3: [Added 45 tests, coverage increased to 78%]

Thought 4: Better test coverage. Now let me identify which responsibility to extract first.
Action 4: Analyze coupling between responsibilities using static analysis.
Observation 4: [Email sending has fewest dependencies, good extraction candidate]

Thought 5: Email sending is the safest to extract. Let me create the new class.
Action 5: Create EmailService class and move email methods.
Observation 5: [Extracted but tests fail - shared state dependencies found]

Thought 6: Shared state is blocking extraction. Let me identify the dependencies.
Action 6: Trace which state variables are used by email methods.
Observation 6: [Email methods access 3 global state variables and 2 helper methods]

Thought 7: I need to pass dependencies explicitly rather than accessing global state.
Action 7: Refactor email methods to accept dependencies as parameters.
Observation 7: [Tests pass, email methods are now pure functions]

Thought 8: Good progress. Let me deploy this change and validate in production.
Action 8: Deploy behind feature flag, route 10% of traffic to new implementation.
Observation 8: [Monitoring shows identical behavior, no errors]

Thought 9: First extraction successful. Let me repeat for next responsibility.
Action 9: Extract validation logic following same pattern.
Observation 9: [ValidationService created, 15% of original class extracted]

Thought 10: Making progress. Let me check if remaining code has clear ownership.
Action 10: Re-analyze remaining code for logical groupings.
Observation 10: [Remaining: auth (40%), API client (30%), caching (15%), misc (15%)]

Final Answer: Successfully extracted EmailService and ValidationService (30% of original class) using strangler fig pattern. Process: (1) Add characterization tests, (2) Identify loosely coupled responsibilities, (3) Extract dependencies explicitly, (4) Deploy behind feature flag, (5) Validate and iterate. Remaining responsibilities ready for next iteration.
```

## 8. Production Incident Response (Advanced-Expert)

```text
Production incident: Payment processing completely down, affecting all customers.

Thought 1: This is critical. I need immediate status of all payment-related services.
Action 1: Check health endpoints and monitoring dashboards for payment services.
Observation 1: [Payment API: DOWN, Payment DB: UP, Stripe webhook service: UP]

Thought 2: Payment API is down. Let me check if it's a deployment issue.
Action 2: Query deployment history and service logs from last 30 minutes.
Observation 2: [No recent deployments, logs show: "FATAL: database connection failed"]

Thought 3: Database connection issue despite DB being up. Let me verify connectivity.
Action 3: Test database connectivity from payment service host.
Observation 3: [Connection test succeeds from host, but fails from container]

Thought 4: Container networking issue. Let me check recent infrastructure changes.
Action 4: Review Kubernetes events and recent config changes.
Observation 4: [Security group rules updated 45 min ago, new egress restrictions]

Thought 5: Security group change likely broke DB access. Let me verify the rules.
Action 5: Compare current security group rules with previous working version.
Observation 5: [New rules block database port 5432 from payment service subnet]

Thought 6: Found root cause! I need to fix this immediately but safely.
Action 6: Prepare rollback of security group changes and get approval.
Observation 6: [Approval received, ready to rollback]

Thought 7: Before rolling back, let me ensure no other services depend on the new rules.
Action 7: Check if any other services were affected or if rules were intentional.
Observation 7: [No other services affected, change was accidental misconfiguration]

Thought 8: Safe to rollback. Let me execute and monitor.
Action 8: Rollback security group rules to previous version.
Observation 8: [Rules updated, payment service health endpoint now returns 200]

Thought 9: Service is up but let me verify end-to-end payment flow.
Action 9: Run synthetic transaction test through entire payment flow.
Observation 9: [Test payment completes successfully]

Thought 10: System recovered. Now I need to document and prevent recurrence.
Action 10: Write incident report and add alerting for DB connection failures.
Observation 10: [Report completed, new alert configured, runbook updated]

Final Answer:
- Root cause: Accidental security group rule change blocked payment service DB access
- Time to resolution: 18 minutes from detection
- Impact: 100% payment processing down for 18 minutes
- Fix: Rolled back security group rules
- Prevention: Added DB connection alerts, security group changes now require approval from two engineers
```

## 9. Architecture Decision with Trade-off Analysis (Expert)

```text
Choose database technology for a new high-throughput event logging service (100K events/second).

Thought 1: I need to understand the requirements in detail before making a decision.
Action 1: Gather detailed requirements - read patterns, write patterns, query complexity, retention.
Observation 1: [Write-heavy (99% writes), time-series data, simple queries, 90-day retention, need for aggregations]

Thought 2: Time-series data with heavy writes suggests specialized time-series databases.
Action 2: Research time-series database options: TimescaleDB, InfluxDB, ClickHouse, Cassandra.
Observation 2: [All can handle 100K writes/sec, differ in query capabilities and operational complexity]

Thought 3: Let me narrow down based on query requirements.
Action 3: List out specific query patterns needed for the service.
Observation 3: [Queries: count by time window, filter by event type, aggregate by user, 95th percentile calculations]

Thought 4: Aggregations and percentiles favor columnar databases. Let me compare ClickHouse vs TimescaleDB.
Action 4: Benchmark ClickHouse and TimescaleDB with realistic workload.
Observation 4: [ClickHouse: 120K writes/sec, 50ms p95 query. TimescaleDB: 95K writes/sec, 120ms p95 query]

Thought 5: ClickHouse performs better but let me consider operational complexity.
Action 5: Evaluate operational requirements - setup, maintenance, monitoring, backup.
Observation 5: [ClickHouse: steeper learning curve, complex cluster management. TimescaleDB: PostgreSQL-based, familiar ops]

Thought 6: Trade-off between performance and operational simplicity. Let me consider team expertise.
Action 6: Assess team's database experience and available time for learning.
Observation 6: [Team has strong PostgreSQL experience, limited time for learning new systems]

Thought 7: Team expertise favors TimescaleDB but performance is below ClickHouse. Let me check if TimescaleDB can be optimized.
Action 7: Research TimescaleDB optimization techniques and compare with baseline.
Observation 7: [With compression and proper chunk sizing, can achieve 110K writes/sec, 80ms p95]

Thought 8: Optimized TimescaleDB meets requirements. But let me consider cost at scale.
Action 8: Calculate infrastructure costs for both options at target scale.
Observation 8: [ClickHouse: $3.2K/month, TimescaleDB: $4.1K/month due to higher memory needs]

Thought 9: Cost difference is significant but not prohibitive. Let me consider failure modes.
Action 9: Analyze disaster recovery and failure scenarios for both.
Observation 9: [TimescaleDB: standard PostgreSQL backup/restore. ClickHouse: requires specialized backup strategies]

Thought 10: TimescaleDB has better operational fit despite higher cost. Let me validate this decision with a proof of concept.
Action 10: Run week-long POC with production-like traffic on TimescaleDB.
Observation 10: [POC successful: 115K events/sec sustained, 75ms p95 queries, zero downtime, team comfortable with ops]

Final Answer: Selected TimescaleDB because:
- Meets performance requirements (110K+ writes/sec, <100ms queries)
- Leverages team's PostgreSQL expertise (reduced operational risk)
- Standard backup/recovery procedures (simpler disaster recovery)
- Trade-off: 28% higher cost than ClickHouse acceptable given operational benefits
- POC validated decision with real-world workload
```

## 10. Complex System Integration (Expert)

```text
Integrate a new ML recommendation service into existing e-commerce platform without disrupting user experience.

Thought 1: This is a complex integration with multiple touchpoints. Let me map out all integration points.
Action 1: Identify where recommendation service needs to integrate - product pages, cart, search, email.
Observation 1: [4 integration points, different latency requirements, fallback strategies needed]

Thought 2: Different latency requirements suggest different integration patterns. Let me define SLAs.
Action 2: Document latency requirements and acceptable fallback behavior for each integration point.
Observation 2: [Product page: <200ms (show old algo), Cart: <500ms (skip), Search: <300ms (use defaults), Email: async]

Thought 3: Email is async so easier. Let me start there to validate the ML service works.
Action 3: Implement email recommendations integration with the ML service.
Observation 3: [Integration successful, ML service responds in 1.2s average, acceptable for async]

Thought 4: Email works but too slow for synchronous pages. Let me investigate why.
Action 4: Profile ML service to identify latency bottlenecks.
Observation 4: [Model inference: 80ms, database queries: 900ms, serialization: 220ms]

Thought 5: Database queries are the bottleneck. Let me check if caching can help.
Action 5: Implement Redis caching layer for user features and item metadata.
Observation 5: [With caching: p50: 95ms, p95: 180ms, p99: 310ms]

Thought 6: Much better! But p99 still exceeds product page requirement. Let me implement timeout and fallback.
Action 6: Add circuit breaker pattern with 150ms timeout and fallback to rule-based recommendations.
Observation 6: [Fallback triggers on 5% of requests, user experience unaffected]

Thought 7: Single integration point working well. Let me implement gradual rollout strategy.
Action 7: Deploy behind feature flag with percentage-based rollout.
Observation 7: [10% of users seeing ML recommendations, monitoring shows positive engagement metrics]

Thought 8: Positive results but let me verify no bias or quality issues.
Action 8: Run A/B test comparing ML recommendations vs existing algorithm.
Observation 8: [ML: +8% CTR, +5% conversion, but -12% for new users (cold start problem)]

Thought 9: Cold start problem for new users. Let me implement hybrid approach.
Action 9: Use rule-based for users with <5 interactions, ML for established users.
Observation 9: [Hybrid approach: +6% CTR overall, no drop for new users]

Thought 10: Hybrid works well. Now let me implement remaining integration points using same pattern.
Action 10: Roll out to search and cart pages with same architecture (caching, circuit breaker, hybrid logic).
Observation 10: [All integration points live, 40% of traffic on ML recommendations, metrics positive]

Thought 11: Integration successful but let me ensure observability for ongoing operations.
Action 11: Add comprehensive monitoring - latency, cache hit rate, fallback rate, ML service health, recommendation quality metrics.
Observation 11: [Dashboards created, alerts configured for SLA violations and quality degradation]

Final Answer: Successfully integrated ML recommendation service using:
1. Phased rollout starting with async use case (email)
2. Performance optimization through Redis caching (1.2s → 95ms p50)
3. Circuit breaker pattern with intelligent fallbacks
4. Hybrid approach solving cold start problem
5. Gradual rollout with A/B testing validation
6. Comprehensive observability for production operations
Result: +6% CTR, +5% conversion, 40% traffic on ML with <200ms latency and robust fallback strategy.
```
