---
allowed-tools: Task, Read
argument-hint: [feature-slug]
description: Perform code review on a worktree branch before merge (project, gitignored)
---

<instructions>
You are orchestrating the **Code Review phase** for a feature implementation. This phase sits between development completion and merging to main, providing systematic peer review to ensure code quality and correctness.

Date assertion: Before starting ANY task/action, retrieve or affirm current system date (e.g., "System date: YYYY-MM-DD") to ground time-sensitive reasoning.

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

## Step 1: Context Loading

Load all available artifacts and git information:

```bash
# Get branch information
git branch --show-current
git log -5 --oneline

# Get diff information
git diff main...HEAD --stat
```

Provide this context summary:

```
Context for code review:
- Branch: [feature-branch-name]
- Commits: [list last 3-5 commit messages]
- Files Changed: [count] files, [count] insertions, [count] deletions
- Requirements: [Summarize from requirements-{feature}.md if exists]
- Implementation Plan: [Summarize from implementation-plan-{feature}.md if exists]
- Design Spec: [Summarize from design-spec-{feature}.md if exists]
- CI/CD Status: [Pass/Fail/Unknown]
```

## Step 2: Invoke Code Review Specialist Agent

Use the Task tool to invoke the code-review-specialist subagent with:

<agent_prompt_template>
You are conducting a code review for the **$ARGUMENTS** feature before merging to main.

**Context Artifacts:**
{Paste loaded context here}

**Git Information:**
{Paste branch, commits, diff stats here}

**Your Task:**

1. Gather full context (requirements, plan, design spec, tests)
2. Conduct structural review (architecture fit, design patterns)
3. Conduct dimension-based review:
   - Correctness (logic, edge cases, concurrency)
   - Code Quality (clarity, simplicity, idioms)
   - Security (vulnerabilities, secrets, injection)
   - Performance (algorithmic complexity, N+1 queries)
   - Testability (coverage, test quality)
   - Maintainability (documentation, API design)
4. Conduct line-by-line review for specific issues
5. Run Chain-of-Verification validation
6. Generate comprehensive review report

**Output:**
Create `code-review-$ARGUMENTS.md` in `.claude/memory/` with:
- Executive summary
- Merge recommendation (APPROVED / APPROVED WITH CONCERNS / CHANGES REQUIRED)
- Findings classified by severity (BLOCKER / MAJOR / MINOR / SUGGESTION)
- Dimension scores (1-5 stars)
- Detailed findings with file references
- Action items

**Quality Gates:**

- All 6 dimensions reviewed
- Every blocker/major has file reference
- Findings are evidence-based, not subjective
- Suggested fixes are specific and implementable
- Merge decision is clear and justified

**Anti-Hallucination:**

- Ground in project conventions (check style guides, linting rules)
- Use "According to..." prompting for best practices
- Verify findings against actual tech stack
- Only review changed code (not pre-existing issues)
- Run CoVe validation before finalizing

Proceed with systematic code review following your 6-dimension methodology.
</agent_prompt_template>

## Step 3: Monitor Review Progress

The code-review-specialist agent will:

1. Load context and git diff
2. Conduct structural review (architecture fit)
3. Review each dimension systematically
4. Perform line-by-line analysis
5. Run CoVe validation
6. Generate code-review-$ARGUMENTS.md

This may take several minutes for large diffs.

## Step 4: Validate Output

After the agent completes, verify the review report:

<validation_checklist>
✅ File created: `.claude/memory/code-review-$ARGUMENTS.md`
✅ Contains executive summary
✅ Contains merge recommendation (clear decision)
✅ Contains findings with severity classification
✅ Contains file references for all major issues
✅ Contains dimension scores (1-5 stars)
✅ Contains specific action items
✅ Contains test coverage analysis
✅ Findings are evidence-based (not subjective opinions)
✅ Suggested fixes are implementable
</validation_checklist>

If validation fails, ask the agent to revise incomplete sections.

## Step 5: Summary Report

Present to the user:

```markdown
## Code Review Complete: $ARGUMENTS

**Review Report**: `.claude/memory/code-review-$ARGUMENTS.md`

**Merge Recommendation**: ✅ APPROVED | ⚠️ APPROVED WITH CONCERNS | ❌ CHANGES REQUIRED

**Overall Score**: X.X / 5.0

**Summary**:
- 🔴 Blockers: X
- 🟠 Major Issues: X
- 🟡 Minor Issues: X
- 🟢 Suggestions: X

**Key Findings**:
- [Top 2-3 findings summarized]

**Dimension Scores**:
- Correctness: ⭐⭐⭐⭐⭐
- Code Quality: ⭐⭐⭐⭐☆
- Security: ⭐⭐⭐⭐⭐
- Performance: ⭐⭐⭐☆☆
- Testability: ⭐⭐⭐⭐☆
- Maintainability: ⭐⭐⭐⭐☆

**Next Steps**:
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
- Suggest: "Consider breaking into smaller PRs for thorough review"
- Focus review on high-risk areas (security, correctness)

**Issue: CI/CD checks failing**

- Note in review: "CI/CD checks failing - blockers present"
- List failing checks
- Recommendation: ❌ CHANGES REQUIRED (fix CI/CD first)

**Issue: No tests found**

- Flag as 🔴 BLOCKER: "No tests found for implementation"
- Require tests before merge
- Suggest test scenarios based on requirements

**Issue: Missing context artifacts**

- Proceed with available context
- Note limitations: "Review conducted without {missing artifact}"
- May affect review thoroughness

</error_handling>

<best_practices>

## Code Review Command Best Practices

1. **Always load context first** - Understand what code is supposed to do
2. **Verify branch exists** - Can't review non-existent code
3. **Check CI/CD status** - Failing tests are automatic blockers
4. **Be evidence-based** - Ground findings in best practices, not opinions
5. **Classify severity accurately** - Not everything is a blocker
6. **Provide specific fixes** - "Fix this" is not actionable feedback
7. **Stay in scope** - Review changed code, not entire codebase
8. **Be constructive** - Review is for improvement, not gatekeeping
9. **Acknowledge trade-offs** - Sometimes "good enough" is correct choice
10. **Teach, don't police** - Explain why something matters

</best_practices>

<integration_notes>

## Workflow Integration

**Before this command:**

- `/implement-feature` → Code written on feature branch ✅
- `/write-tests` → Tests written (optional but recommended) ✅
- CI/CD pipeline → Checks run and pass ✅

**This command:**

- `/review-code` → code-review-{feature}.md ✅

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

**Integration with Git Workflow**:

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

Review code for feature: **$ARGUMENTS**

Begin by loading context and git information.
