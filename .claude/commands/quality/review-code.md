---
allowed-tools: Task, Read
argument-hint: [feature-slug]
description: Perform code review on a worktree branch before merge (project, gitignored)
---

<instructions>
You are orchestrating the **Code Review phase** for a feature implementation using Chain of Verification and Task Decomposition techniques. This phase sits between development completion and merging to main, providing systematic peer review with recursive validation to ensure code quality and correctness.

Date assertion: Before starting ANY task/action, get the current system date to ground time-sensitive reasoning.

## Prerequisites Validation

Before proceeding, verify these artifacts exist:

<prerequisites>
1. **Feature branch exists** - MUST exist
2. **implementation-plan-{feature}.md** - SHOULD exist
3. **requirements-{feature}.md** - SHOULD exist
4. **design-spec-{feature}.md** - MAY exist (if UI changes)
5. **CI/CD checks passed** - SHOULD be verified
</prerequisites>

Use code-tools (Read, Bash) to check:

- `.claude/memory/` for planning artifacts
- Git status for branch information
- CI/CD pipeline status

If feature branch doesn't exist:

- STOP and inform the user
- Suggest completing implementation first
- Explain: "Code review requires completed code on a feature branch."

If context artifacts are missing, proceed with available context but note limitations.
</instructions>

<review_orchestration>

## Task Decomposition: Review Process Structure

The code review is decomposed into independent, verifiable tasks executed sequentially with validation at each stage.

### Phase 1: Context Loading and Initial Assessment

**Task 1.1: Load all context artifacts**

```bash
# Get branch information
git branch --show-current
git log -5 --oneline

# Get diff information
git diff main...HEAD --stat
git diff main...HEAD --name-only
```

**Task 1.2: Read planning artifacts**

- Load `.claude/memory/requirements-$ARGUMENTS.md` (if exists)
- Load `.claude/memory/implementation-plan-$ARGUMENTS.md` (if exists)
- Load `.claude/memory/design-spec-$ARGUMENTS.md` (if exists)
- Extract key requirements, technical decisions, and acceptance criteria

**Task 1.3: Generate context summary**

Synthesize loaded information into structured summary:

```
Context for code review:
- Branch: [feature-branch-name]
- Commits: [list last 3-5 commit messages]
- Files Changed: [count] files, [count] insertions, [count] deletions
- Key Requirements: [3-5 bullet points from requirements]
- Technical Approach: [2-3 bullet points from implementation plan]
- Design Decisions: [if UI: key design choices]
- CI/CD Status: [Pass/Fail/Unknown with details]
```

**Verification Checkpoint 1:**

Before proceeding to review, verify:

1. Do I have sufficient context to conduct informed review?
2. Are there any blockers that would make review invalid? (e.g., failing CI/CD)
3. Is the diff size reasonable for thorough review? (<1000 lines ideal)

If verification fails: Document gaps and adjust review scope accordingly.

### Phase 2: Structural Review (Architecture Fit)

**Task 2.1: Analyze code organization**

Decompose changed files by type:

- New files vs modified files
- Frontend vs backend vs infrastructure
- Business logic vs utilities vs tests
- Configuration vs code

**Task 2.2: Evaluate architecture alignment**

For each significant change:

- Does this fit the existing architecture patterns?
- Are design patterns used correctly?
- Is the code in the right layer/module?
- Does it follow project conventions?

**Task 2.3: Assess dependencies and coupling**

- New dependencies: justified and necessary?
- Coupling between modules: appropriate level?
- Dependency directions: follow established rules?

**Verification Checkpoint 2:**

Validate structural review findings:

1. For each architectural concern, can I cite specific code or pattern violation?
2. Am I judging against project's actual conventions (not external ideals)?
3. Are structural issues genuine problems or stylistic preferences?

Revise findings: Remove subjective opinions, keep evidence-based concerns.

### Phase 3: Six-Dimension Systematic Review

Execute parallel analysis across six quality dimensions. Each dimension uses verification loops.

**Dimension A: Correctness (Logic & Behavior)**

Task A1: Initial correctness analysis

- Identify logic errors
- Check edge case handling
- Verify algorithm correctness
- Assess error handling completeness

Verification Loop A:

1. For each issue identified, ask: "Would this cause observable failure?"
2. Can I construct a test case that demonstrates the bug?
3. Am I certain this is incorrect, or just unusual?

Revise: Keep only verifiable correctness issues.

Task A2: Concurrency and race condition analysis

- Shared state access patterns
- Lock/synchronization usage
- Atomic operations
- Thread safety guarantees

Verification Loop A2:

1. Can I describe the race condition sequence?
2. Is this actually concurrent code, or am I over-analyzing?
3. Does the framework/runtime already handle this?

**Dimension B: Code Quality (Readability & Maintainability)**

Task B1: Readability assessment

- Variable/function naming clarity
- Code complexity (cyclomatic, cognitive)
- Comment quality and necessity
- Code organization and structure

Verification Loop B1:

1. Would a team member unfamiliar with this code understand it?
2. Are my readability concerns based on team standards or personal taste?
3. Is complexity inherent to the problem or avoidable?

Task B2: Maintainability evaluation

- Code duplication (DRY violations)
- Separation of concerns
- Single Responsibility Principle adherence
- Future extensibility

Verification Loop B2:

1. Would these maintainability issues actually cause problems in practice?
2. Am I suggesting over-engineering or genuine improvements?
3. Are my concerns relevant to this project's scale and lifecycle?

**Dimension C: Security (Vulnerabilities & Best Practices)**

Task C1: Security vulnerability scan

- Input validation and sanitization
- Authentication/authorization checks
- SQL injection, XSS, CSRF risks
- Secrets management
- Dependency vulnerabilities

Verification Loop C1:

1. Is this exploitable in the actual deployment context?
2. Can I describe an attack vector specifically?
3. Does existing security infrastructure already mitigate this?
4. Am I checking against OWASP Top 10 / CWE standards?

Task C2: Data protection review

- PII handling compliance
- Encryption at rest/in transit
- Data access logging
- Privacy policy alignment

Verification Loop C2:

1. Does this actually violate regulations or best practices?
2. Are there existing controls I'm not aware of?
3. Is the risk proportional to my concern level?

**Dimension D: Performance (Efficiency & Scalability)**

Task D1: Algorithmic complexity analysis

- Time complexity of key operations
- Space complexity and memory usage
- N+1 query patterns
- Unnecessary computations

Verification Loop D1:

1. Would this performance issue manifest at expected scale?
2. Can I calculate or estimate the actual impact?
3. Is premature optimization my concern, or genuine bottleneck?

Task D2: Resource utilization review

- Database query efficiency
- API call patterns
- Caching strategy
- Batch processing opportunities

Verification Loop D2:

1. Are there metrics or benchmarks supporting my concern?
2. Would proposed optimization provide measurable benefit?
3. Does the trade-off (complexity vs performance) favor optimization?

**Dimension E: Testability (Test Coverage & Quality)**

Task E1: Test coverage analysis

- Unit test coverage for new code
- Integration test coverage
- Edge cases tested
- Error scenarios covered

Verification Loop E1:

1. Are there genuinely untested code paths?
2. Would these tests catch real bugs?
3. Am I requiring tests for trivial code?

Task E2: Test quality assessment

- Test clarity and maintainability
- Brittle tests (over-mocking, implementation details)
- Test isolation
- Assertion quality

Verification Loop E2:

1. Are test quality issues affecting test value?
2. Would my suggestions improve or complicate tests?
3. Do tests verify behavior, not implementation?

**Dimension F: Maintainability (Documentation & API Design)**

Task F1: Documentation review

- Public API documentation
- Complex logic explanations
- Architecture decision records
- README/guide updates

Verification Loop F1:

1. Is missing documentation actually needed?
2. Is existing documentation accurate and helpful?
3. Am I over-documenting obvious code?

Task F2: API design evaluation

- Interface clarity and consistency
- Backward compatibility
- Error handling patterns
- Versioning strategy

Verification Loop F2:

1. Would API changes break existing consumers?
2. Is the API intuitive for intended use cases?
3. Are my design preferences or genuine usability concerns?

**Verification Checkpoint 3: Dimension Cross-Validation**

After completing all six dimensions:

1. Are findings classified correctly by dimension?
2. Is any issue counted multiple times across dimensions?
3. Are severity levels (BLOCKER/MAJOR/MINOR/SUGGESTION) justified?
4. For each BLOCKER: Is it truly blocking merge, or can it be addressed post-merge?
5. For each MAJOR: Is there concrete evidence of impact?

Revise: Adjust severity levels, merge duplicates, remove weak findings.

### Phase 4: Line-by-Line Focused Review

**Task 4.1: Identify high-risk areas**

Focus line-by-line review on:

- Security-critical code (auth, payments, data access)
- Complex algorithms
- External integrations
- Error handling paths

**Task 4.2: Detailed code inspection**

For each high-risk file:

- Read code line by line
- Check for subtle bugs
- Verify error handling
- Validate input/output handling

**Verification Loop 4:**

For each issue found:

1. Can I point to the exact line(s) with the problem?
2. Can I suggest a specific fix?
3. Is this a new issue or pre-existing?

Rule: Only review changed code, not pre-existing issues.

### Phase 5: Final Chain of Verification

Before generating the review report, perform comprehensive verification:

**Verification Round 1: Accuracy Check**

Questions to validate findings:

1. Evidence: Is every finding backed by specific code references?
2. Context: Did I consider the full context (framework, libraries, patterns)?
3. False Positives: Are any findings based on incomplete understanding?
4. Severity: Are severity levels proportional to actual impact?

Action: For any "no" answer, investigate and revise findings.

**Verification Round 2: Completeness Check**

Questions to validate coverage:

1. All changed files reviewed?
2. All six dimensions evaluated?
3. Tests reviewed for quality and coverage?
4. Documentation changes assessed?
5. CI/CD failures investigated?

Action: For any "no" answer, complete missing analysis.

**Verification Round 3: Actionability Check**

Questions to validate usefulness:

1. Specific: Does each finding have file:line reference?
2. Fixable: Is each finding actionable with suggested approach?
3. Clear: Would a developer understand the issue without asking?
4. Prioritized: Are findings ordered by severity?

Action: For any "no" answer, improve finding clarity.

**Verification Round 4: Objectivity Check**

Questions to prevent bias:

1. Standards: Am I applying project's standards (not personal preferences)?
2. Consistency: Would I flag this in all code, or just because I'm reviewing?
3. Balance: Am I acknowledging what's done well, not just problems?
4. Constructive: Is feedback teaching, not policing?

Action: For any "no" answer, reframe findings constructively.

**Final Decision Verification:**

Merge recommendation decision tree:

```
✅ APPROVED IF:
- Zero BLOCKER issues
- Zero HIGH-SEVERITY security issues
- CI/CD passing
- Adequate test coverage for changes

⚠️ APPROVED WITH CONCERNS IF:
- Zero BLOCKER issues
- Some MAJOR issues that can be addressed post-merge
- CI/CD passing
- Test coverage acceptable

❌ CHANGES REQUIRED IF:
- Any BLOCKER issues exist
- CI/CD failing
- Critical security vulnerabilities
- Missing tests for critical paths
- Multiple MAJOR issues in core logic
```

Verify: Does recommendation follow this decision tree consistently?

### Phase 6: Generate Review Report

**Task 6.1: Create code-review-$ARGUMENTS.md**

Structure:

```markdown
# Code Review: $ARGUMENTS

**Date:** [YYYY-MM-DD]
**Reviewer:** Claude Code Review Specialist
**Branch:** [branch-name]
**Commits:** [count] commits, [insertions](+) / [deletions](-)

## Executive Summary

[2-3 paragraph summary of review findings]

## Merge Recommendation

**Decision:** ✅ APPROVED | ⚠️ APPROVED WITH CONCERNS | ❌ CHANGES REQUIRED

**Justification:** [Clear reasoning based on findings]

## Review Metrics

**Dimension Scores:**

- Correctness: ⭐⭐⭐⭐⭐ (5/5)
- Code Quality: ⭐⭐⭐⭐☆ (4/5)
- Security: ⭐⭐⭐⭐⭐ (5/5)
- Performance: ⭐⭐⭐☆☆ (3/5)
- Testability: ⭐⭐⭐⭐☆ (4/5)
- Maintainability: ⭐⭐⭐⭐☆ (4/5)

**Overall Score:** X.X / 5.0

**Issue Counts:**

- 🔴 Blockers: X
- 🟠 Major Issues: X
- 🟡 Minor Issues: X
- 🟢 Suggestions: X

## Detailed Findings

### 🔴 Blocker Issues

[For each blocker:]

**BLOCKER-N: [Brief title]**

- **File:** `path/to/file.ext:line`
- **Severity:** BLOCKER
- **Dimension:** [Correctness/Security/etc]
- **Description:** [Detailed explanation with evidence]
- **Impact:** [What breaks, security risk, data loss, etc]
- **Suggested Fix:** [Specific code change or approach]

### 🟠 Major Issues

[Same structure as blockers]

### 🟡 Minor Issues

[Same structure, briefer descriptions acceptable]

### 🟢 Suggestions

[Same structure, focus on improvements not problems]

## Test Coverage Analysis

- **Unit Test Coverage:** X% (Target: 80%+)
- **Integration Test Coverage:** [assessment]
- **Missing Test Scenarios:** [list if any]
- **Test Quality:** [assessment]

## Performance Considerations

[Any performance observations, benchmarks, or concerns]

## Security Assessment

[Summary of security review, any compliance notes]

## Positive Highlights

[3-5 things done well - balance critical feedback]

## Action Items

**Before Merge (if CHANGES REQUIRED):**

1. [Specific action with file reference]
2. [...]

**Post-Merge (if APPROVED WITH CONCERNS):**

1. [Follow-up item with priority]
2. [...]

## Review Verification

This review was conducted using:

- ✅ Chain of Verification methodology (4 validation rounds)
- ✅ Task Decomposition across 6 quality dimensions
- ✅ Evidence-based findings (all issues have file:line references)
- ✅ Project-specific standards (not external ideals)
- ✅ Pre-mortem analysis for blockers

**Context Used:**

- Requirements: [✅/❌ available]
- Implementation Plan: [✅/❌ available]
- Design Spec: [✅/❌ available]
- CI/CD Results: [✅/❌/⚠️ status]
```

**Task 6.2: Validate report completeness**

Checklist:

- [ ] Executive summary present
- [ ] Clear merge recommendation with justification
- [ ] Dimension scores with evidence
- [ ] All findings have file:line references
- [ ] Severity classifications justified
- [ ] Suggested fixes are specific
- [ ] Positive highlights included (balance)
- [ ] Test coverage analyzed
- [ ] Action items clear and prioritized

If checklist incomplete, revise report.

### Phase 7: Present Summary to User

Generate user-facing summary:

```markdown
## Code Review Complete: $ARGUMENTS

**Review Report:** `.claude/memory/code-review-$ARGUMENTS.md`

**Merge Recommendation:** [✅ APPROVED | ⚠️ APPROVED WITH CONCERNS | ❌ CHANGES REQUIRED]

**Overall Score:** X.X / 5.0

**Summary:**

- 🔴 Blockers: X
- 🟠 Major Issues: X
- 🟡 Minor Issues: X
- 🟢 Suggestions: X

**Key Findings:**

1. [Top finding with severity]
2. [Second finding]
3. [Third finding]

**Dimension Scores:**

- Correctness: ⭐⭐⭐⭐⭐
- Code Quality: ⭐⭐⭐⭐☆
- Security: ⭐⭐⭐⭐⭐
- Performance: ⭐⭐⭐☆☆
- Testability: ⭐⭐⭐⭐☆
- Maintainability: ⭐⭐⭐⭐☆

**Next Steps:**

[If APPROVED]:

1. Merge feature branch to main
2. Deploy to staging for integration testing
3. Monitor production metrics post-deploy

[If APPROVED WITH CONCERNS]:

1. Create follow-up issues for major items
2. Merge to main
3. Address concerns in next sprint

[If CHANGES REQUIRED]:

1. Review blocker issues in report
2. Implement fixes on feature branch
3. Re-request code review with `/review-code "$ARGUMENTS"`

**Review Methodology:**

This review used Chain of Verification (4 validation rounds) and Task Decomposition (6-dimension analysis) to ensure evidence-based, objective findings grounded in project conventions.
```

</review_orchestration>

<error_handling>
If code review encounters issues:

**Issue: Feature branch doesn't exist**

- Inform user: "No feature branch found for {feature}"
- Suggest: "Complete implementation first with `/implement-feature`"
- Explain: Cannot review code that doesn't exist

**Issue: Diff too large (> 1000 lines changed)**

- Note in review: "Diff exceeds 1000 lines - review may be partial"
- Focus on high-risk areas: security, correctness, critical paths
- Suggest: "Consider breaking into smaller PRs for thorough review"
- Apply stricter verification on sampled code

**Issue: CI/CD checks failing**

- **Automatic BLOCKER**: "CI/CD checks failing"
- List failing checks with details
- Recommendation: ❌ CHANGES REQUIRED (fix CI/CD first)
- Do not proceed with detailed review until CI/CD passes

**Issue: No tests found**

- Flag as 🔴 BLOCKER: "No tests found for implementation"
- Require tests before merge
- Suggest test scenarios based on requirements
- Lower testability dimension score to 1/5

**Issue: Missing context artifacts**

- Proceed with available context
- Note in report: "Review conducted without {missing artifact} - may affect thoroughness"
- Adjust verification questions to account for missing context
- Cannot verify requirements alignment without requirements doc

**Issue: Verification conflicts (dimensions in tension)**

Example: Performance optimization reduced readability

- Acknowledge trade-off explicitly in review
- Assess if balance is appropriate for use case
- Provide guidance: "This trade-off is [acceptable/questionable] because..."
- Do not penalize both dimensions if trade-off is intentional and justified

</error_handling>

<best_practices>

## Code Review Command Best Practices

1. **Evidence-based findings only** - Every issue must have file:line reference
2. **Apply project standards** - Not external ideals or personal preferences
3. **Verify before finalizing** - Use 4-round verification to prevent false positives
4. **Be constructive** - Teach, don't police; explain the "why"
5. **Balance feedback** - Acknowledge what's done well, not just problems
6. **Appropriate severity** - Not everything is a blocker; save that for true blockers
7. **Specific fixes** - "Fix this" is not actionable; suggest concrete approaches
8. **Review changed code only** - Don't flag pre-existing issues
9. **Context-aware** - Consider framework, libraries, and established patterns
10. **Acknowledge trade-offs** - Sometimes "good enough" is the right choice
11. **Recursive verification** - Question your own findings before presenting
12. **Systematic coverage** - All six dimensions, all changed files

## Anti-Hallucination Safeguards

- Ground in project conventions (check style guides, linting rules)
- Use "According to [standard/doc]" prompting for best practices
- Verify findings against actual tech stack documentation
- When uncertain, say "Verify with team: [question]" instead of asserting
- Cross-check security issues against OWASP/CWE before flagging
- Validate performance concerns with actual scale estimates

</best_practices>

<integration_notes>

## Workflow Integration

**Before this command:**

- `/implement-feature` → Code written on feature branch ✅
- `/write-tests` → Tests written (optional but recommended) ✅
- CI/CD pipeline → Checks run and pass ✅

**This command:**

- `/review-code` → `.claude/memory/code-review-{feature}.md` ✅

**After this command:**

[If APPROVED or APPROVED WITH CONCERNS]:

- Merge feature branch to main
- Deploy to staging
- Run integration tests
- Monitor production

[If CHANGES REQUIRED]:

- Developer fixes blockers
- Re-run `/review-code` for another review iteration
- Repeat until approved

**Integration with Git Workflow:**

```
feature/user-auth (development)
    ↓
/review-code "user-auth" (peer review)
    ↓
[If approved] git merge feature/user-auth → main
    ↓
Deploy to production
```

</integration_notes>

---

**Begin code review for feature:** $ARGUMENTS

**Methodology:** Chain of Verification + Task Decomposition

Execute Phase 1: Context Loading and Initial Assessment
