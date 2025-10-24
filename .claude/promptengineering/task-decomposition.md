# Task Decomposition Prompting: 10 example prompts

Task decomposition breaks complex problems into simpler, manageable sub-tasks that can be solved independently and then composed into a complete solution. This technique is particularly effective for multi-step software engineering challenges.

## 1. Basic Feature Implementation

```text
Implement a user authentication feature with JWT tokens.

Decompose into sub-tasks:

Task 1: Design the authentication schema
- User model with email/password fields
- Token storage strategy
- Session management approach

Task 2: Implement password hashing
- Choose hashing algorithm (bcrypt/argon2)
- Implement hash generation
- Implement hash verification

Task 3: Create JWT token generation
- Configure JWT secret and expiration
- Implement token signing
- Include necessary claims (user ID, roles)

Task 4: Build login endpoint
- Validate credentials
- Generate token on success
- Return appropriate errors

Task 5: Create authentication middleware
- Extract token from request
- Verify token validity
- Attach user context to request

Execute each task in sequence, then integrate all components.
```

## 2. API Endpoint Development (Basic-Intermediate)

```text
Build a REST API endpoint for managing blog posts with pagination, filtering, and sorting.

Decomposition:

Sub-task A: Define data model and validation
- Post schema (title, content, author, tags, timestamps)
- Input validation rules
- Output serialization format

Sub-task B: Implement database queries
- Base query for posts
- Pagination logic (offset/limit or cursor-based)
- Filtering by author, tags, date range
- Sorting by date, popularity, relevance

Sub-task C: Build query parameter parser
- Extract pagination params (page, limit)
- Extract filter params (author, tags, date)
- Extract sort params (sortBy, order)
- Validate parameter values

Sub-task D: Create response formatter
- Structure paginated response
- Include metadata (total, pages, current)
- Add HATEOAS links for next/prev

Sub-task E: Implement error handling
- Invalid parameters
- Database errors
- Empty result sets

Sub-task F: Add caching layer
- Cache key generation
- Cache invalidation strategy
- TTL configuration

Integrate all sub-tasks into final endpoint implementation.
```

## 3. Database Migration with Decomposition (Intermediate)

```text
Migrate user data from MongoDB to PostgreSQL while maintaining zero downtime.

Phase 1: Pre-migration preparation
Step 1.1: Analyze MongoDB schema and data patterns
Step 1.2: Design equivalent PostgreSQL schema
Step 1.3: Create migration scripts for schema
Step 1.4: Set up PostgreSQL database

Phase 2: Dual-write implementation
Step 2.1: Implement write-through to both databases
Step 2.2: Add feature flag for dual-write mode
Step 2.3: Deploy and enable dual-write
Step 2.4: Monitor for write failures

Phase 3: Historical data migration
Step 3.1: Create data extraction scripts
Step 3.2: Implement data transformation logic
Step 3.3: Build batched data loader
Step 3.4: Execute migration with progress tracking

Phase 4: Validation and verification
Step 4.1: Compare record counts
Step 4.2: Validate data integrity (checksums)
Step 4.3: Test application against PostgreSQL
Step 4.4: Performance benchmark comparison

Phase 5: Cutover
Step 5.1: Enable PostgreSQL reads (behind feature flag)
Step 5.2: Monitor for errors and performance
Step 5.3: Gradually increase PostgreSQL traffic
Step 5.4: Disable MongoDB reads
Step 5.5: Remove dual-write logic

Execute each phase sequentially, with rollback plan for each step.
```

## 4. Performance Optimization with Hierarchical Decomposition (Intermediate)

```text
Optimize a slow-loading dashboard page (current load time: 5s, target: <1s).

Level 1: Problem identification
- Run performance profiling
- Identify bottlenecks (network, rendering, computation)

Level 2: Decompose by bottleneck type

Branch A: Network optimization
  A1: Analyze bundle size
    - Identify large dependencies
    - Find unused code
    - Check for duplicate modules
  A2: Implement code splitting
    - Split by route
    - Lazy load heavy components
    - Optimize chunk sizes
  A3: Optimize API calls
    - Batch multiple requests
    - Implement request caching
    - Add pagination where appropriate

Branch B: Rendering optimization
  B1: Identify expensive renders
    - Use React DevTools Profiler
    - Find unnecessary re-renders
    - Locate expensive computations
  B2: Apply rendering optimizations
    - Add React.memo to pure components
    - Implement useMemo for expensive calculations
    - Use useCallback for stable functions
  B3: Optimize DOM structure
    - Reduce DOM depth
    - Virtualize long lists
    - Minimize layout thrashing

Branch C: Data fetching optimization
  C1: Implement query optimization
    - Add database indexes
    - Reduce over-fetching
    - Use GraphQL field selection
  C2: Add caching layers
    - Server-side caching (Redis)
    - Client-side caching (React Query)
    - CDN for static assets
  C3: Implement prefetching
    - Prefetch on hover
    - Predictive prefetching
    - Service worker caching

Level 3: Integration and validation
- Apply all optimizations
- Measure final load time
- Verify functionality unchanged

Execute branches in parallel, then integrate and validate.
```

## 5. Test Suite Creation with Decomposition (Intermediate-Advanced)

```text
Create comprehensive test suite for an e-commerce checkout flow.

Decompose by test type:

Layer 1: Unit tests
Module 1.1: Cart calculations
  - Test price calculations
  - Test discount application
  - Test tax calculations
  - Test shipping cost logic

Module 1.2: Validation functions
  - Test address validation
  - Test payment card validation
  - Test coupon code validation
  - Test inventory checks

Module 1.3: State management
  - Test cart state updates
  - Test checkout state machine
  - Test error state handling

Layer 2: Integration tests
Module 2.1: Payment processing
  - Test successful payment flow
  - Test payment failures
  - Test timeout handling
  - Test webhook processing

Module 2.2: Inventory management
  - Test stock reservation
  - Test stock release on failure
  - Test concurrent purchase handling

Module 2.3: Order creation
  - Test order record creation
  - Test email notification trigger
  - Test receipt generation

Layer 3: End-to-end tests
Scenario 3.1: Happy path
  - Add items to cart
  - Apply discount code
  - Enter shipping details
  - Complete payment
  - Verify order confirmation

Scenario 3.2: Error scenarios
  - Handle payment decline
  - Handle out-of-stock items
  - Handle timeout during checkout
  - Handle session expiration

Scenario 3.3: Edge cases
  - Zero-price items (free gift)
  - International shipping
  - Multiple concurrent checkouts

Layer 4: Performance tests
  - Load test checkout endpoint
  - Stress test payment processing
  - Concurrency test inventory locking

Implement each layer sequentially, building on previous layers.
```

## 6. Microservices Refactoring (Advanced)

```text
Refactor a monolithic order processing system into microservices.

Phase 1: Domain analysis and service boundary identification
Task 1.1: Map current system domains
  - Identify bounded contexts (orders, inventory, payments, shipping)
  - Map domain relationships
  - Identify shared vs domain-specific data

Task 1.2: Define service boundaries
  - Orders service responsibilities
  - Inventory service responsibilities
  - Payments service responsibilities
  - Notifications service responsibilities

Phase 2: Extract first service (Payments)
Task 2.1: Create new service scaffold
  - Set up service repository
  - Configure build and deployment
  - Implement health checks and monitoring

Task 2.2: Implement service logic
  - Extract payment processing code
  - Refactor for service independence
  - Add service API layer

Task 2.3: Establish communication patterns
  - Define REST/gRPC contracts
  - Implement event publishing
  - Add message queue integration

Task 2.4: Implement dual-write pattern
  - Write to both monolith and service
  - Validate consistency
  - Monitor for discrepancies

Task 2.5: Cutover to service
  - Route reads to new service
  - Remove monolith payment code
  - Clean up dual-write logic

Phase 3: Extract remaining services
- Repeat Phase 2 for Inventory service
- Repeat Phase 2 for Notifications service
- Extract Orders service last (depends on others)

Phase 4: Implement cross-cutting concerns
Task 4.1: Service discovery
Task 4.2: Distributed tracing
Task 4.3: Centralized logging
Task 4.4: API gateway
Task 4.5: Circuit breakers

Phase 5: Data consistency
Task 5.1: Implement saga pattern
Task 5.2: Add compensating transactions
Task 5.3: Event sourcing for order state

Execute phases sequentially, services within phase can be parallel.
```

## 7. Security Audit with Systematic Decomposition (Advanced)

```text
Conduct comprehensive security audit of a web application.

Decompose by security domain:

Domain A: Authentication and Authorization
  A1: Authentication mechanism review
    - Password policy enforcement
    - MFA implementation
    - Session management
    - Token security (JWT validation)

  A2: Authorization checks
    - RBAC implementation correctness
    - Privilege escalation vulnerabilities
    - Horizontal access control
    - API endpoint authorization

  A3: Credential management
    - Secrets storage (environment vs vault)
    - API key rotation
    - Password reset flow security

Domain B: Input Validation and Data Handling
  B1: Injection vulnerability scan
    - SQL injection testing
    - NoSQL injection testing
    - Command injection testing
    - LDAP injection testing

  B2: XSS prevention
    - Input sanitization review
    - Output encoding verification
    - CSP header configuration

  B3: File upload security
    - File type validation
    - Size limits
    - Virus scanning
    - Storage location security

Domain C: API Security
  C1: Rate limiting and throttling
    - Per-endpoint limits
    - Per-user limits
    - DDoS protection

  C2: CORS configuration
    - Allowed origins validation
    - Credential handling
    - Preflight request handling

  C3: API versioning and deprecation
    - Breaking change management
    - Sunset headers
    - Documentation accuracy

Domain D: Data Protection
  D1: Encryption at rest
    - Database encryption
    - File storage encryption
    - Encryption key management

  D2: Encryption in transit
    - TLS configuration
    - Certificate management
    - HSTS implementation

  D3: PII handling
    - Data minimization
    - Anonymization/pseudonymization
    - Right to deletion implementation

Domain E: Infrastructure Security
  E1: Dependency vulnerabilities
    - npm/pip audit results
    - Outdated dependency check
    - License compliance

  E2: Container security
    - Base image vulnerabilities
    - Secrets in images
    - Runtime security

  E3: Cloud configuration
    - IAM permissions audit
    - S3 bucket policies
    - Security group rules

Execute all domains in parallel, aggregate findings, prioritize by severity.
```

## 8. CI/CD Pipeline Setup with Modular Decomposition (Advanced)

```text
Build a complete CI/CD pipeline for a Node.js microservices application.

Module 1: Source control integration
  Step 1.1: Configure webhook triggers
  Step 1.2: Branch protection rules
  Step 1.3: PR validation requirements

Module 2: Build stage
  Step 2.1: Environment setup
    - Node.js version management
    - Dependency caching strategy
    - Parallel job configuration

  Step 2.2: Compilation and bundling
    - TypeScript compilation
    - Asset bundling
    - Source map generation

  Step 2.3: Artifact creation
    - Docker image building
    - Image tagging strategy
    - Registry push

Module 3: Test stage
  Step 3.1: Unit tests
    - Test execution with coverage
    - Coverage threshold enforcement
    - Results reporting

  Step 3.2: Integration tests
    - Service dependencies setup
    - Database migrations
    - Test execution

  Step 3.3: E2E tests
    - Environment provisioning
    - Test data seeding
    - Browser automation

  Step 3.4: Security scanning
    - Dependency vulnerability scan
    - SAST (Static Application Security Testing)
    - Container image scanning

Module 4: Deployment stage
  Step 4.1: Staging deployment
    - Infrastructure provisioning (Terraform)
    - Database migration execution
    - Application deployment
    - Smoke tests

  Step 4.2: Production deployment
    - Blue-green deployment setup
    - Canary release configuration
    - Rollback automation
    - Health check validation

Module 5: Post-deployment
  Step 5.1: Monitoring setup
    - Metrics collection
    - Log aggregation
    - Alert configuration

  Step 5.2: Notification
    - Slack/email notifications
    - Deployment tracking
    - Release notes generation

Module 6: Optimization
  Step 6.1: Pipeline parallelization
  Step 6.2: Cache optimization
  Step 6.3: Incremental builds

Implement modules sequentially, with steps within modules in parallel where possible.
```

## 9. Legacy Code Refactoring with Incremental Decomposition (Expert)

```text
Refactor a 10K line legacy JavaScript file into maintainable modules.

Phase 1: Analysis and planning
  Task 1.1: Static analysis
    - Identify all functions and their dependencies
    - Map global state usage
    - Detect circular dependencies

  Task 1.2: Create dependency graph
    - Visualize function call hierarchy
    - Identify highly coupled components
    - Find potential module boundaries

  Task 1.3: Define refactoring strategy
    - Prioritize by coupling/cohesion
    - Plan extraction order
    - Define success metrics

Phase 2: Extract pure utility functions (lowest risk)
  Task 2.1: Identify pure functions (no side effects)
  Task 2.2: Group by responsibility
  Task 2.3: Create utility modules
    - utils/string.js
    - utils/date.js
    - utils/validation.js
  Task 2.4: Replace usage with imports
  Task 2.5: Test equivalence

Phase 3: Extract data models and types
  Task 3.1: Identify data structures
  Task 3.2: Convert to classes/types
  Task 3.3: Create model modules
  Task 3.4: Update references
  Task 3.5: Add validation methods

Phase 4: Extract business logic (medium risk)
  Task 4.1: Identify business rules
  Task 4.2: Create service modules
    - services/user.js
    - services/order.js
    - services/payment.js
  Task 4.3: Inject dependencies
  Task 4.4: Comprehensive testing

Phase 5: Extract UI components (higher risk)
  Task 5.1: Identify rendering logic
  Task 5.2: Create component hierarchy
  Task 5.3: Implement components with tests
  Task 5.4: Replace inline rendering
  Task 5.5: Visual regression testing

Phase 6: Refactor global state (highest risk)
  Task 6.1: Identify all global variables
  Task 6.2: Create state management module
  Task 6.3: Migrate to centralized state
  Task 6.4: Remove globals incrementally
  Task 6.5: Extensive integration testing

Phase 7: Clean up and optimization
  Task 7.1: Remove dead code
  Task 7.2: Consolidate duplicate logic
  Task 7.3: Optimize imports
  Task 7.4: Add documentation
  Task 7.5: Performance validation

Execute phases sequentially, with regression testing after each phase.
```

## 10. Full-Stack Feature with Cross-Layer Decomposition (Expert)

```text
Implement a real-time collaborative document editing feature (like Google Docs).

Layer 1: Requirements and architecture
  Module 1.1: Define functional requirements
    - Real-time sync (<100ms latency)
    - Conflict resolution strategy
    - Presence indicators
    - Cursor sharing

  Module 1.2: Technology selection
    - Conflict resolution: CRDTs vs OT
    - Real-time transport: WebSocket vs Server-Sent Events
    - Data structure: Rope vs Array
    - Storage: PostgreSQL with JSONB vs MongoDB

Layer 2: Data model and algorithms
  Module 2.1: Document representation
    - Design data structure for efficient operations
    - Implement insertion/deletion primitives
    - Add indexing for fast access

  Module 2.2: CRDT implementation
    - Implement Yjs or Automerge
    - Define character-level operations
    - Implement convergence guarantees

  Module 2.3: Operational transformation (alternative)
    - Implement OT algorithm
    - Handle concurrent operations
    - Implement transformation functions

Layer 3: Backend implementation
  Module 3.1: WebSocket server
    - Connection management
    - Room-based message routing
    - Heartbeat and reconnection

  Module 3.2: Conflict resolution service
    - Apply CRDT operations
    - Broadcast changes to clients
    - Handle late-joining clients

  Module 3.3: Persistence layer
    - Snapshot strategy (periodic saves)
    - Operation log for replay
    - Garbage collection for old operations

  Module 3.4: Presence service
    - Track active users per document
    - Cursor position tracking
    - User activity status

Layer 4: Frontend implementation
  Module 4.1: Editor component
    - Rich text editor integration (ProseMirror/Slate)
    - Local operation capture
    - Operation application from remote

  Module 4.2: WebSocket client
    - Connection lifecycle management
    - Automatic reconnection with exponential backoff
    - Message queue for offline operations

  Module 4.3: Local state management
    - Pending operations queue
    - Optimistic UI updates
    - Conflict resolution on reconciliation

  Module 4.4: Presence UI
    - Collaborator avatars
    - Remote cursor rendering
    - Activity indicators

Layer 5: Optimizations
  Module 5.1: Performance
    - Debounce operation sending
    - Batch multiple operations
    - Virtual scrolling for large documents

  Module 5.2: Conflict prevention
    - Operational transformation optimization
    - Last-write-wins for metadata
    - Manual conflict resolution UI

  Module 5.3: Scalability
    - Horizontal scaling with Redis pub/sub
    - Document sharding strategy
    - CDN for static assets

Layer 6: Testing strategy
  Module 6.1: Unit tests
    - CRDT operations correctness
    - Transformation functions
    - Data structure operations

  Module 6.2: Integration tests
    - Multi-client simulation
    - Conflict scenarios
    - Network failure handling

  Module 6.3: E2E tests
    - Real-time collaboration flows
    - Offline/online transitions
    - Performance benchmarks

Layer 7: Deployment and monitoring
  Module 7.1: Infrastructure
    - Kubernetes deployment
    - Load balancer configuration
    - Auto-scaling policies

  Module 7.2: Monitoring
    - WebSocket connection metrics
    - Operation latency tracking
    - Conflict resolution success rate
    - Document size and performance correlation

Execute layers sequentially with each layer's modules in parallel where independent.
Continuously test integration between layers as they complete.
```
