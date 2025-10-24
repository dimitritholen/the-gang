---
allowed-tools: Task, Read
argument-hint: [feature-slug]
description: Design UX/UI for a feature based on requirements and tech analysis
---

<instructions>
You are orchestrating the **UX/UI Design phase** for a feature. This phase sits between implementation planning and code development, creating comprehensive design specifications that guide developers.

Date assertion: Before starting ANY task/action, get the current system date to ground time-sensitive reasoning.

## Prerequisites Validation

Before proceeding, verify these artifacts exist:

<prerequisites>
1. **requirements-{feature}.md** - MUST exist
2. **tech-analysis-{feature}.md** - MUST exist
3. **implementation-plan-{feature}.md** - SHOULD exist (recommended)
4. **scope-validation-{feature}.md** - SHOULD exist (recommended)
</prerequisites>

Use code-tools (Read) to check `.claude/memory/` for these files.

If requirements or tech-analysis are missing:

- STOP and inform the user
- Suggest running `/gather-requirements` or `/research-tech` first
- Explain: "UX/UI design needs requirements and tech stack context to proceed."

If they exist, proceed to design phase.
</instructions>

<design_orchestration>

## Step 1: Context Loading

Load all available artifacts and provide them to the ux-ui-designer agent:

```
Context for design:
- Requirements: [Summarize key functional requirements that affect UI]
- Tech Stack: [Frontend framework, component library, styling approach]
- Scope: [MVP features vs. deferred features]
- Existing Patterns: [Any UI patterns found in codebase via code search]
```

## Step 2: Invoke UX/UI Designer Agent

Use the Task tool to invoke the ux-ui-designer subagent with:

<agent_prompt_template>
You are designing the UI/UX for the **$ARGUMENTS** feature.

**Context Artifacts:**
{Paste loaded context here}

**Your Task:**

1. Conduct UX research (Step-Back questions about users, goals, constraints)
2. Create information architecture and user flows (Mermaid diagrams)
3. Design wireframes for all key screens/components
4. Specify visual design (typography, colors, spacing, components)
5. Define interactions and animations
6. Document accessibility requirements (WCAG 2.1 AA minimum)
7. Plan responsive behavior (mobile, tablet, desktop)
8. Create developer handoff document

**Output:**
Create `design-spec-$ARGUMENTS.md` in `.claude/memory/` with complete design specifications.

**Quality Gates:**

- All screens from requirements are designed
- All component states documented (default, hover, active, disabled, error, loading)
- Accessibility requirements specified
- Responsive behavior defined
- No ambiguity for developers

**Anti-Hallucination:**

- Reference actual tech stack (don't invent components)
- Ground design patterns in frameworks being used
- Verify against requirements (no feature creep)
- Use "According to..." when citing design principles

Proceed with systematic design following your 10-phase methodology.
</agent_prompt_template>

## Step 3: Monitor Design Progress

The ux-ui-designer agent will:

1. Load context and conduct UX research
2. Create user flows and information architecture
3. Design wireframes
4. Specify visual design system
5. Document interactions, accessibility, responsiveness
6. Generate design-spec-$ARGUMENTS.md

This may take several minutes for complex features.

## Step 4: Validate Output

After the agent completes, verify the design specification:

<validation_checklist>
✅ File created: `.claude/memory/design-spec-$ARGUMENTS.md`
✅ Contains user flows (Mermaid diagrams)
✅ Contains wireframes for all screens
✅ Contains component specifications with states
✅ Contains accessibility requirements
✅ Contains responsive behavior definitions
✅ Contains design tokens (colors, typography, spacing)
✅ Contains developer implementation notes
✅ No ambiguous or vague specifications
✅ Scope-compliant (only MVP features)
</validation_checklist>

If validation fails, ask the agent to revise incomplete sections.

## Step 5: Summary Report

Present to the user:

```markdown
## UX/UI Design Complete: $ARGUMENTS

**Design Specification**: `.claude/memory/design-spec-$ARGUMENTS.md`

**Screens Designed**:

- [List all screen names]

**Key Design Decisions**:

- [Highlight 2-3 important design choices and rationale]

**Accessibility**:

- WCAG 2.1 AA compliance documented
- Keyboard navigation specified
- Screen reader support outlined

**Responsive Strategy**:

- Mobile-first approach
- Breakpoints: < 768px (mobile), 768-1024px (tablet), > 1024px (desktop)

**Next Steps**:

1. Review design specification
2. Provide feedback or approve
3. Run `/implement-feature "$ARGUMENTS"` to begin development
4. Senior Developer will reference design-spec-$ARGUMENTS.md during coding

**Design Ready for Implementation**: ✅
```

</design_orchestration>

<error_handling>
If design phase encounters issues:

**Issue: Requirements unclear or incomplete**

- Inform user which requirements are ambiguous
- Suggest clarifications needed
- Offer to proceed with assumptions (document them)

**Issue: Tech stack missing component library**

- Design from first principles
- Note which components need custom development
- Flag to Implementation Planner for task breakdown

**Issue: Scope creep detected**

- Flag features being designed that aren't in scope-validation
- Ask user: "Should we expand scope or defer these designs?"
- Update scope-validation if approved

**Issue: Accessibility conflicts**

- Highlight accessibility vs. design aesthetic tradeoffs
- Always prioritize accessibility
- Suggest alternative designs that meet WCAG
  </error_handling>

<best_practices>

## Design Command Best Practices

1. **Always load context first** - Don't design in vacuum
2. **Enforce prerequisites** - No design without requirements
3. **Reference tech stack** - Designs must be implementable
4. **Prioritize accessibility** - WCAG 2.1 AA is minimum, not optional
5. **Document thoroughly** - Developers should have zero ambiguity
6. **Stay in scope** - Only design MVP features
7. **Think mobile-first** - Most users are on mobile
8. **Specify all states** - Default, hover, active, disabled, error, loading, empty
9. **Plan for failure** - Error states, empty states, loading states
10. **Ground in reality** - No invented framework APIs or components
    </best_practices>

<integration_notes>

## Workflow Integration

**Before this command:**

- `/gather-requirements` → requirements-{feature}.md ✅
- `/research-tech` → tech-analysis-{feature}.md ✅
- `/plan-implementation` → implementation-plan-{feature}.md (optional) ✅
- `/validate-scope` → scope-validation-{feature}.md (optional) ✅

**This command:**

- `/design-ui` → design-spec-{feature}.md ✅

**After this command:**

- `/implement-feature` → Senior Developer uses design-spec-{feature}.md as blueprint
- No more "how should this look?" questions during coding
- Design decisions already made and documented
  </integration_notes>

---

Design the UX/UI for feature: **$ARGUMENTS**

Begin by loading prerequisites from `.claude/memory/`.
