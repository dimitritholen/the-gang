# Prompt Engineering Reference for AI Coding Models (Context7 Style)

- Scope: 80% software development prompting, 20% general prompting
- Audience: Engineers integrating LLMs into coding workflows and tools
- Date: October 23, 2025
- Style: Context7 reference — structured, example‑heavy, concise

## 1) Role, Objective, and Constraints (ROC) Framing

- Goal: Establish a clear persona, task objective, and hard constraints to reduce ambiguity and improve determinism.
- Works best for: Code generation, refactoring, writing tests, migration scripts.
- Notes: Keep constraints testable and observable; avoid vague adjectives.

Examples

```text
Role: Senior TypeScript engineer in a monorepo using pnpm workspaces.
Objective: Implement an idempotent file-based cache utility with TTL and invalidation.
Constraints: Node 18+, ESM only, zero dependencies, 100% branch coverage via vitest.
Deliver: src/cache.ts, src/cache.test.ts with runnable examples and usage notes.
```

```text
Role: Python infra engineer.
Objective: Migrate a Flask app to FastAPI with minimal downtime.
Constraints: Preserve routes and JSON schemas; add OpenAPI docs; keep logging structure.
Deliver: A patch diff and a migration checklist with rollback steps.
```

```text
Role: Security-focused Go developer.
Objective: Build an HTTP client with retries, backoff, circuit breaker.
Constraints: gomod tidy; no global state; unit tests using httptest; race-free.
Deliver: go files and tests ready for `go test -race ./...`.
```

## 2) Stepwise Decomposition and Planning (Chain-of-Command Style)

- Goal: Ask the model to outline a plan before coding, then execute step-by-step.
- Works best for: Multistage tasks (design → scaffolding → implementation → tests).
- Notes: Enforce checkpoints; request a brief plan and then confirm before proceeding.

Examples

```text
Create a 6-step plan to add WebSocket support to an existing Express server (TypeScript). Include: schema, auth, connection lifecycle, heartbeat, broadcast, backpressure handling. Stop after the plan; wait for my OK.
```

```text
Given this repo description, propose a minimal migration plan from Jest to Vitest. Include command changes, config mapping, mocking updates, coverage, and CI tweaks. Stop at plan.
```

```text
Before writing any code, list the functions, their signatures, and test cases to implement a pluggable tokenizer interface in Rust. Stop and request approval.
```

## 3) Input–Output Pair Grounding (Specifications First)

- Goal: Provide concrete I/O examples, edge cases, and acceptance criteria to guide exact behavior.
- Works best for: Parsers, formatters, code mods, CLIs.
- Notes: Supply multiple representative examples, including failure cases.

Examples

```text
Task: Build a Markdown → HTML converter with code fence highlighting.
Inputs: (1) headings + lists; (2) nested code blocks; (3) malformed tables.
Outputs: Valid HTML5, escaping unsafe tags, no inline styles, class hooks.
Acceptance: Snapshots must match provided fixtures exactly.
```

```text
Write a codemod that converts CommonJS to ESM.
Input examples: require/exports default and named, dynamic requires guarded by conditions.
Output examples: import statements with live bindings, top-level await preserved.
Acceptance: idempotent transform; formatting preserved.
```

```text
Implement `camelCase <-> snake_case` converter.
I/O pairs:
- `"user_id" -> "userId"`
- `"HTTPRequest" -> "http_request"`
- `"__init__" -> "__init__"` (no-op for dunder)
Acceptance: Unicode-safe, ASCII-only option, stable round-trip.
```

## 4) Toolformer Style with Explicit Interfaces (Function Calling)

- Goal: Define strict function signatures/APIs the model must call or implement.
- Works best for: Agents, codegen for typed boundaries, plugin implementations.
- Notes: Provide precise parameter/return types, error contracts, and examples.

Examples

```text
Implement TypeScript function `resolveConfig(file: string): Promise<Result<Config,Err>>`.
Types: Config { extends?: string[]; rules: Record<string,string|number>; }
Rules: No sync fs; support JSON/JSONC; cyclic extends detection with path stack.
Return: Ok(Config) or Err(code,message,trace).
```

```text
You have tool `fetchSchema(url: string): Schema`. Call it to validate input JSON against AJV-compatible schema. On failure, return diagnostic with path and rule id. Provide 3 examples.
```

```text
Define interface `Storage` in Go with methods Get/Put/Delete(ctx, key) and List(prefix).
Implement S3-backed storage with context timeouts and retries. Provide unit tests using minio/mocks only (no network).
```

## 5) Guardrails via Contracts and Tests (Test-First Prompting)

- Goal: Ask for tests upfront, then implementation that passes them.
- Works best for: Libraries, utilities, refactors.
- Notes: Require runnable snippets and commands; enforce coverage or assertions count.

Examples

```text
Write Jest tests first for a pure function `topologicalSort<T>(edges: [T,T][])`.
Cover: cycles, multiple roots, disconnected graphs, stability. Then implement to pass.
```

```text
Create `pytest` tests for a Pydantic model with strict types, custom validators, and JSON export policy. Then implement the model to satisfy tests.
```

```text
Generate property-based tests (fast-check) for an `immutableSet` API. Include identities, associativity, idempotence, and law checks. Then author implementation.
```

## 6) Context Packing and Retrieval Curation

- Goal: Curate and compress repo context to avoid overload while preserving relevance.
- Works best for: Large repos, legacy systems.
- Notes: Summarize key modules, expose only necessary APIs, trim noise, include version pins.

Examples

```text
Summarize this monorepo: list packages, public APIs, config files, and compile targets. Produce a 200-line max brief that a new contributor needs to implement feature X.
```

```text
Given these 6 files, extract the database access layer interfaces and usage examples. Ignore UI. Provide a call graph.
```

```text
Compress this 1,500-line file into a 100-line technical brief retaining: exported symbols, side effects, env vars, and error handling paths.
```

## 7) Self-Verification and Critique Loops

- Goal: Have the model critique its own output with checklists and invariants.
- Works best for: Security-sensitive code, migrations, complex algorithms.
- Notes: Provide a scoring rubric or acceptance checklist; limit to concise review.

Examples

```text
Review the following PR diff for concurrency issues and data races. Use a checklist: locks held order, shared mutable state, goroutine lifetimes, context cancellation, error propagation.
```

```text
Critique this SQL migration for safety: idempotency, rollback path, lock impact, long-running query risks, and online index strategy. Provide severity and fixes.
```

```text
Given the code, run a static checklist: input validation, output encoding, secret handling, path traversal, SSRF, deserialization. Output only issues with actionable fixes.
```

## 8) Constrained Output Formatting (Schemas and Patches)

- Goal: Force outputs into machine-consumable formats to ease automation.
- Works best for: CI bots, codegen, config updates, codemods.
- Notes: Prefer JSON, unified diffs, or explicit file lists. Specify no extra prose.

Examples

```text
Output a unified diff (apply_patch format) that adds `src/logger.ts` and updates `src/index.ts` to wire it. No commentary; diff only.
```

```text
Emit JSON matching schema: { files: { path, contents, executable? }[] }. Include all created/updated files. No trailing commas.
```

```text
Produce a Kubernetes manifest YAML for a CronJob with image, env, resources, and a PodMonitor. No comments; validate with kubeconform.
```

## 9) Few-Shot + Contrastive Examples

- Goal: Show both good and bad examples to push the model toward the desired pattern.
- Works best for: API usage patterns, error handling, style consistency.
- Notes: Include 2–3 good and 1–2 anti-patterns with explanations.

Examples

```text
Target style: functional React with hooks, no classes.
Good: useReducer for complex state; memoized selectors; dependency arrays correct.
Bad: derived state in state; inline functions in render.
Generate a component following the good examples.
```

```text
Demonstrate correct vs incorrect SQL parameterization in Node pg. Then implement a repo method using the correct pattern only.
```

```text
Show good error handling in Rust with anyhow + thiserror vs panics. Then refactor this function accordingly.
```

## 10) Progressive Scoping and Budgeting

- Goal: Cap token use/latency by scoping tasks into bounded chunks with budgets.
- Works best for: Large features, long files, incremental refactors.
- Notes: Impose limits on output size, time, or files touched.

Examples

```text
Budget: 300 lines. Implement only the data layer for feature X: entities, repositories, and in-memory adapters with tests. Stop; summarize gaps.
```

```text
Touch at most 3 files to add an exponential backoff to fetch. List the files first; await approval.
```

```text
Produce a 200-token summary of the bug and a 150-line fix in a single file. No extra prose.
```

## 11) Clarifying Questions Before Action

- Goal: Force the model to ask targeted questions when requirements are ambiguous.
- Works best for: Greenfield features, integrations, migrating unknown systems.
- Notes: Cap to 3–5 questions to avoid stalls; require actionable defaults if unanswered.

Examples

```text
Before implementing OAuth, ask up to 4 questions to clarify provider, scopes, PKCE, and session storage. If unanswered, assume GitHub, repo:read scope, PKCE on, cookies.
```

```text
List missing assumptions for migrating from Mongo to Postgres. Limit to 5, prioritize data types, transactionality, and indexing. Provide defaults to proceed.
```

```text
Ask exactly 3 questions needed to implement a streaming CSV parser with backpressure. Then proceed with reasonable defaults if not answered.
```

## 12) Error-Driven Development (Reproduce → Fix → Verify)

- Goal: Start with failing cases, logs, or stack traces; then request minimal fix and verification plan.
- Works best for: Bugfixes, flaky tests, production incidents.
- Notes: Include reproduction commands; ask for delta-only patch.

Examples

```text
Given this stack trace and failing test, suggest the smallest diff to fix the race condition. Output only the patch. Include why it fixes the issue in 2 sentences.
```

```text
Reproduce this memory leak using a minimal script. Provide steps and then the fix in the lib, with a benchmark before/after.
```

```text
Convert this flaky Jest test to be deterministic by controlling timers and random seeds. Show only the test diff.
```

## 13) System Prompt + Policy Anchoring

- Goal: Anchor model behavior with persistent system rules (style, safety, scope).
- Works best for: Assistants embedded in IDEs/CLIs.
- Notes: Keep short, enforceable, and domain-specific; include do/don’t lists.

Examples

```text
System: You are a coding assistant. Be concise, output diffs or files only on request, avoid chatty prose, and never fabricate APIs. Prefer TypeScript strict mode.
Task: Implement feature X under these constraints.
```

```text
System: You must not add dependencies without approval. If needed, propose and wait.
Task: Add JWT auth to the API.
```

```text
System: Use RFC 8259 JSON only, no comments, no trailing commas. All timestamps ISO 8601.
Task: Emit deployment metadata.
```

## 14) Program Synthesis with Typed Stubs

- Goal: Provide type signatures, stubs, and failing tests for the model to complete.
- Works best for: Strongly-typed languages (TS, Rust, Go, Java).
- Notes: Freeze public interfaces; restrict edits to TODO blocks.

Examples

```text
Provide only TODO sections to complete in these files. Keep signatures constant. Make tests pass without modifying tests.
```

```text
Here are Rust traits and empty impls. Implement methods to satisfy trait bounds and property tests. No new crates.
```

```text
Given TS interfaces and Zod schemas, implement serialization/deserialization functions preserving branded types.
```

## 15) Planning-Execute-Reflect (PER) Cycles

- Goal: Prompt the model to plan, execute a slice, reflect, then continue.
- Works best for: Long-running coding tasks or multi-file changes.
- Notes: Keep reflection short and focused on deltas and next action.

Examples

```text
Phase 1 (Plan): list files to add/change to implement feature toggle infra. Stop.
Phase 2 (Execute): implement config loader + flag evaluator only.
Phase 3 (Reflect): verify tests, outline next steps.
```

```text
Plan → Implement → Reflect to build a streaming JSON parser with constant memory. Limit each phase output to 150 lines.
```

```text
Use PER to migrate callbacks to async/await across this package with staged PRs and test gates.
```

## 16) Safety and Security-First Prompting

- Goal: Embed security, privacy, and compliance constraints into prompts and outputs.
- Works best for: Auth, payments, user data, secrets.
- Notes: Include threat models, logging redaction, and secure defaults.

Examples

```text
Implement OAuth callback handler with CSRF, state validation, PKCE, short-lived codes, and refresh rotation. Add structured audit logs without PII.
```

```text
Sanitize and validate all user input for this upload endpoint. Enforce size limits, content-type allowlist, and malware scan hook. Provide tests.
```

```text
Refactor to use parameterized queries and least-privilege DB roles. Provide a migration plan and roll-forward/rollback instructions.
```

## 17) Style, Conventions, and Linters in Prompt

- Goal: Specify style guides and lint rules to align output with repo norms.
- Works best for: Teams with strict conventions or formatters.
- Notes: Include formatter/linter versions and must-pass commands.

Examples

```text
Follow Airbnb ESLint config, Prettier 3, TypeScript strict. The PR must pass `pnpm lint && pnpm typecheck && pnpm test`.
```

```text
Use Black 24.3 and Ruff rules. No unused imports. MyPy strict optional.
```

```text
Go: gofmt, go vet, golangci-lint with default presets. Fix all lints.
```

## 18) Data and Fixture-Driven Development

- Goal: Provide realistic sample data and fixtures to anchor behavior and edge cases.
- Works best for: ETL, adapters, API clients, migrations.
- Notes: Ask the model to generate fixtures that mirror production shape and volume.

Examples

```text
Create fixtures for Stripe webhook events (payment_intent.succeeded/failed) and write a validator that rejects malformed events. Include signature verification tests.
```

```text
Given these 3 CSV shapes, implement a resilient importer with schema inference, type coercion, and row-level error reporting. Provide fixtures and tests.
```

```text
Simulate a flaky third-party API with jitter, timeouts, and 500s. Build a client with retries, backoff, and hedging; include integration tests.
```

## 19) Agent-Oriented Delegation and Tool Use

- Goal: Structure prompts so the model delegates to tools or sub-tasks explicitly.
- Works best for: Complex tasks needing search, build systems, or scripts.
- Notes: Enumerate available tools, expected usage, and escalation rules.

Examples

```text
Tools: git, ripgrep, jq. Task: locate all usages of deprecated API X and produce a patch replacing it. Output only the diff. If uncertainty > 20%, stop and ask.
```

```text
You can run tests (`npm test`) but cannot install deps. Triage failing tests and produce minimal fix. If a dep is missing, propose alternatives.
```

```text
Use `rg` to find TODOs tagged `SECURITY`. Summarize risks and produce prioritized fixes with patches.
```

## 20) Chain-of-Thought (CoT) and Self-Consistency

- Goal: Improve reasoning by asking for intermediate reasoning steps; increase reliability by sampling multiple reasoning paths and selecting the most consistent answer.
- Works best for: Algorithmic reasoning, debugging steps, complex refactors, test derivation.
- Notes: For production, prefer brief, structured reasoning traces or hidden CoT; use self-consistency (n>1) and aggregate.

Examples

```text
Derive step-by-step the algorithm to detect cycles in a directed graph and then output only the final TypeScript function `hasCycle(edges: [string,string][])`. Keep the reasoning to a numbered list with at most 6 steps.
```

```text
You will think through 3 alternative fixes for this flaky test, then choose the best. Output: (1) brief reasoning for each option (<=3 sentences), (2) the chosen option, (3) the minimal diff.
```

```text
Self-consistency: Generate 5 independent solutions for computing rolling median in O(log n) per update in Python. Then vote to select one and emit only the final implementation + tests.
```

## 21) Least-to-Most (LtM) Decomposition

- Goal: Solve complex problems by decomposing into ordered subproblems from easiest to hardest, solving sequentially using prior results.
- Works best for: Multi-constraint coding tasks, parser design, stepwise migrations.
- Notes: Ask the model to explicitly list subproblems and reuse outputs.

Examples

```text
Use least-to-most: 1) parse tokens, 2) build AST, 3) evaluate with environment, 4) add error recovery. Implement step 1 completely and provide tests; stop thereafter.
```

```text
Decompose adding streaming support into: small file API, backpressure, chunked parsing, error boundaries. Complete the first two with benchmarks.
```

```text
For SQL migration safety, start with read-only dry-run validators, then lock analysis, then idempotent DDL generation. Show artifacts at each stage.
```

## 22) Chain-of-Verification (CoVe)

- Goal: Generate an initial solution, then run a verification chain that checks invariants, tests, and edge cases; revise if checks fail.
- Works best for: Critical code paths, math-heavy logic, schema migrations.
- Notes: Provide an explicit verification checklist and require pass/fail with fixes.

Examples

```text
Implement the function, then verify against: (1) unit tests (provided), (2) boundary values, (3) randomized fuzz cases, (4) performance threshold (<50ms for 10k items). If any fail, revise once and report deltas.
```

```text
Write SQL, then run a verification chain: explain plan check, lock time estimate, and rollback script synthesis. Emit a pass/fail summary and corrected SQL if needed.
```

```text
After producing the refactor, run a static verification pass for null safety, unchecked casts, and exception swallowing. If violations exist, produce a minimal diff to fix.
```

## 23) Chain-of-Draft/Sketch (CoD)

- Goal: Produce a coarse draft or skeleton first, then refine to a final implementation; useful for big files and architectures.
- Works best for: New modules, large components, API designs.
- Notes: Constrain draft length/shape; only then expand.

Examples

```text
Draft: Outline interfaces, data flow, and error model for an event bus (<=60 lines). Then expand into full TS implementation and tests.
```

```text
Create a sketch of React component structure and props for a dashboard. After approval, generate final code and stories.
```

```text
Produce a skeletal Rust crate layout (lib.rs, mod structure, traits) for a tokenizer. Then fill in two core algorithms with benches.
```

## 24) Deliberate Sampling and Temperature Control

- Goal: Use multiple samples with varied temperature/top-p to explore solution space; then select via constraints or tests.
- Works best for: Design choices, API styles, algorithm alternatives.
- Notes: Specify sample count, temperature, and selection criteria.

Examples

```text
Generate 4 alternative implementations of a rate limiter (token bucket vs leaky bucket vs sliding window vs fixed window). Select based on CPU usage and burst handling; provide microbenchmarks.
```

```text
Produce 3 Jest mocking strategies for fetch in Node: manual mocks, msw, and jest-fetch-mock. Choose based on readability and flake resistance.
```

```text
Sample 5 migration plans from Mongo to Postgres with different indexing strategies. Choose one given read-heavy workload; justify with query patterns.
```

## 25) Non-Programming General Prompting (Concise)

- Goal: A small set of high-value techniques for non-code tasks.
- Notes: Keep to 20% of scope; emphasize structure and sources.

Techniques
- Persona anchoring for domain expertise
- Fact-checking with claim/evidence tables
- Style transfer with exemplars
- Summarization with constraints (length, coverage)
- Decision matrices and trade-off analyses

Examples

```text
Act as a healthcare policy analyst. Summarize this 20-page report into 12 bullet points with citations placeholders, covering benefits, risks, costs, and uncertainties. Max 250 words.
```

```text
Create a claim → evidence table from this article. Separate facts from opinions. Provide confidence scores and note missing evidence.
```

```text
Rewrite this blog post in the style of Strunk & White: concise, active voice, no filler. Preserve technical accuracy.
```

---

# Appendix A: Prompt Checklist (Quick Use)

- Define role, objective, constraints, deliverables
- Ask for a brief plan first (when complex)
- Provide I/O pairs and acceptance criteria
- Constrain output format (diff/JSON/files)
- Require tests or verification steps
- Limit scope and files touched
- Request self-critique against a checklist
- Specify style/linter/version requirements
- Provide realistic fixtures and data
- Enumerate tools and allowed actions
