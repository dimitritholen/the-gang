---
allowed-tools: Task, Read
argument-hint: [feature-slug]
description: Design UX/UI for a feature based on requirements and tech analysis
---

<instructions>
You are orchestrating the **UX/UI Design phase** for a feature using Chain of Verification combined with Chain of Thought reasoning. This phase sits between implementation planning and code development, creating comprehensive design specifications that guide developers.

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

## Phase 1: Context Loading with Reasoning

<context_analysis>
Load all available artifacts and reason through their implications:

Step 1.1: Load and analyze requirements

- Read requirements-$ARGUMENTS.md
- Identify which requirements have direct UI implications
- Reason: Which user interactions are described? What workflows are defined?

Step 1.2: Load and analyze tech stack

- Read tech-analysis-$ARGUMENTS.md
- Extract frontend framework, component library, styling approach
- Reason: What UI constraints does our tech stack impose? What capabilities does it enable?

Step 1.3: Load optional context (if available)

- Read implementation-plan-$ARGUMENTS.md (if exists)
- Read scope-validation-$ARGUMENTS.md (if exists)
- Reason: What's in MVP scope vs. deferred? Are there phasing implications for UI?

Step 1.4: Search for existing UI patterns

- Use code search to find similar UI components in codebase
- Reason: What established patterns should we follow for consistency?

Output structured context summary:

```
Context for Design:

Requirements Analysis:
- Key user flows: [list flows that need UI]
- Critical interactions: [list required user actions]
- Data to display: [what information users need to see]
- Implied constraints: [accessibility, performance, mobile requirements]

Tech Stack Constraints:
- Frontend framework: [name + version]
- Component library: [name + available components]
- Styling approach: [CSS-in-JS, Tailwind, etc.]
- Design system: [if one exists in codebase]

Scope Boundaries:
- MVP features: [what we're designing now]
- Deferred features: [what we're NOT designing]
- Phase considerations: [any phased rollout implications]

Existing Patterns:
- Similar components: [list found in codebase]
- Established conventions: [navigation, layouts, interactions]
- Reusable elements: [buttons, forms, modals we should match]
```

</context_analysis>

<context_verification>
Verify context completeness by answering:

1. Do we have sufficient information about user goals and workflows?
2. Are there ambiguous or underspecified UI requirements?
3. Does our tech stack support the UI complexity implied by requirements?
4. Have we identified all necessary existing patterns for consistency?
5. Are there scope boundaries that might affect design decisions?

If verification reveals gaps:

- Document specific gaps found
- Either: gather missing information OR proceed with documented assumptions
- Flag assumptions that need validation with stakeholders
  </context_verification>

## Phase 2: Invoke UX/UI Designer Agent with Enhanced Prompt

Use the Task tool to invoke the ux-ui-designer subagent with:

<agent_prompt_template>
You are designing the UI/UX for the **$ARGUMENTS** feature using Chain of Verification methodology.

**Loaded Context:**
{Paste structured context summary from Phase 1}

**Design Task with Verification:**

<phase_1_initial_design>
Create comprehensive UX/UI design covering:

1. UX Research (Step-Back questions about users, goals, constraints)
2. Information architecture and user flows (Mermaid diagrams)
3. Wireframes for all key screens/components
4. Visual design (typography, colors, spacing, components)
5. Interactions and animations
6. Accessibility requirements (WCAG 2.1 AA minimum)
7. Responsive behavior (mobile, tablet, desktop)
8. Developer handoff specifications

Produce initial design specification addressing all points above.
</phase_1_initial_design>

<phase_2_verification>
After initial design, verify through multiple lenses:

**Completeness Verification:**

- Have I designed all screens identified in requirements?
- Are all user workflows from requirements represented?
- Have I documented all component states (default, hover, active, disabled, error, loading, empty)?
- Is the responsive strategy defined for all breakpoints?

**Technical Verification:**

- Can this design be implemented with our tech stack?
- Am I using components that actually exist in our component library?
- Have I invented any framework APIs or capabilities that don't exist?
- Are there performance implications I've overlooked (e.g., animation complexity, image sizes)?

**Accessibility Verification:**

- Does every interactive element have keyboard navigation?
- Are color contrast ratios WCAG 2.1 AA compliant?
- Have I specified ARIA labels where needed?
- Can screen readers navigate this logically?
- Are there any accessibility vs. design aesthetic conflicts?

**Scope Verification:**

- Am I only designing MVP features from scope boundaries?
- Have I accidentally designed deferred features?
- Are there implicit features I've added that aren't in requirements?

**Usability Verification:**

- Is the user flow intuitive and efficient?
- Have I designed for error states and edge cases?
- Are loading states and empty states addressed?
- Would this design work for users with varying technical sophistication?

**Consistency Verification:**

- Does this follow existing UI patterns found in the codebase?
- Am I maintaining consistency with established design conventions?
- Have I reused components appropriately vs. creating unnecessary variations?

Answer each verification question explicitly. Document any issues found.
</phase_2_verification>

<phase_3_revision>
Based on verification findings:

If issues were found in verification:

- Revise the design to address each identified issue
- Explain what changed and why
- Re-verify that revisions resolve the problems

If no significant issues:

- Confirm design meets all verification criteria
- Note any assumptions that need stakeholder validation
- Proceed to final specification
  </phase_3_revision>

<phase_4_final_specification>
Create `design-spec-$ARGUMENTS.md` in `.claude/memory/` with:

1. Executive Summary
   - Feature overview
   - Key design decisions and rationale
   - Scope boundaries

2. User Flows (Mermaid diagrams)
   - All workflows from requirements
   - Decision points and error paths

3. Screen Designs
   - Wireframes for each screen
   - Responsive behavior at each breakpoint
   - Layout and spacing specifications

4. Component Specifications
   - Every component with all states documented
   - Props/configuration options
   - Interaction patterns

5. Visual Design System
   - Typography scale
   - Color palette
   - Spacing system
   - Iconography

6. Accessibility Requirements
   - WCAG 2.1 AA compliance checklist
   - Keyboard navigation map
   - Screen reader considerations
   - Focus management strategy

7. Responsive Strategy
   - Breakpoints and behavior at each
   - Mobile-first approach details
   - Touch target sizes
   - Viewport considerations

8. Developer Handoff
   - Implementation priorities
   - Technical constraints from design
   - Assets needed (icons, images)
   - Open questions requiring engineering input

Include verification summary showing all checks passed.
</phase_4_final_specification>

**Quality Thresholds (must meet all):**

- Zero ambiguous specifications (developers should never have to guess)
- All component states documented
- Accessibility requirements specified for every interactive element
- Responsive behavior defined for mobile, tablet, desktop
- Scope-compliant (only MVP features)
- Grounded in actual tech stack capabilities

**Anti-Hallucination:**

- Reference actual tech stack components (don't invent)
- Ground design patterns in frameworks being used
- Verify against requirements (no feature creep)
- Use "According to..." when citing design principles or frameworks

Proceed with systematic design following the verification methodology above.
</agent_prompt_template>

## Phase 3: Monitor Design Progress

The ux-ui-designer agent will execute:

1. Load context and conduct UX research
2. Create initial design covering all required aspects
3. Run verification checks across multiple lenses
4. Revise design based on verification findings
5. Generate final design-spec-$ARGUMENTS.md with verification summary

This may take several minutes for complex features. The verification and revision loop ensures high-quality output.

## Phase 4: Orchestrator Validation with Verification

After the agent completes, perform orchestrator-level verification:

<orchestrator_verification>

**Deliverable Verification:**

1. Does file `.claude/memory/design-spec-$ARGUMENTS.md` exist?
2. Is the file complete (not truncated or partial)?
3. Does it include all required sections from the template?

**Content Verification:**
Read the design specification and verify:

1. Completeness check:
   - Are user flows present with Mermaid diagrams?
   - Are all screens from requirements designed?
   - Are component specifications complete with states?
   - Are accessibility requirements specified?
   - Is responsive behavior defined?

2. Quality check:
   - Are specifications unambiguous and actionable?
   - Could a developer implement from this without guessing?
   - Are design decisions explained with rationale?

3. Scope compliance check:
   - Does the design match MVP scope from scope-validation?
   - Are there any out-of-scope features designed?

4. Technical grounding check:
   - Are tech stack components referenced correctly?
   - Are there any invented framework capabilities?
   - Is the design implementable with stated technology?

5. Verification evidence check:
   - Does the specification include verification summary?
   - Are verification findings documented?
   - If revisions were made, are they explained?

**Verification Questions:**

- Would I be confident handing this to a developer for implementation?
- Are there any sections that seem vague or incomplete?
- Does this design align with the original requirements?
- Have all quality thresholds been met?

If verification fails on any criterion:

- Identify specific deficiencies
- Ask the ux-ui-designer agent to revise those specific sections
- Re-run verification after revision
- Iterate until all criteria pass or maximum 2 revision rounds completed

If verification passes:

- Proceed to summary report
- Mark design as ready for implementation
  </orchestrator_verification>

## Phase 5: Summary Report with Metrics

Present to the user:

```markdown
## UX/UI Design Complete: $ARGUMENTS

**Design Specification**: `.claude/memory/design-spec-$ARGUMENTS.md`

**Verification Status**: [PASSED/PASSED WITH NOTES]

**Screens Designed**:

- [List all screen names with brief description]

**Key Design Decisions**:

- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]
- [Decision 3]: [Rationale]

**Accessibility**:

- WCAG 2.1 AA compliance: [Verified]
- Keyboard navigation: [Specified]
- Screen reader support: [Documented]
- Focus management: [Defined]

**Responsive Strategy**:

- Approach: [Mobile-first/Desktop-first]
- Breakpoints: < 768px (mobile), 768-1024px (tablet), > 1024px (desktop)
- Touch targets: [44x44px minimum confirmed]

**Technical Grounding**:

- Framework: [Name from tech stack]
- Components used: [List actual components from library]
- Custom components needed: [List if any]

**Verification Summary**:

- Completeness: [✓ Pass]
- Technical feasibility: [✓ Pass]
- Accessibility: [✓ Pass]
- Scope compliance: [✓ Pass]
- Usability: [✓ Pass]
- Consistency: [✓ Pass]

**Assumptions Requiring Validation**:

- [List any assumptions that need stakeholder confirmation]
- [None if no assumptions]

**Next Steps**:

1. Review design specification
2. Validate any documented assumptions with stakeholders
3. Provide feedback or approve
4. Run `/implement-feature "$ARGUMENTS"` to begin development
5. Senior Developer will reference design-spec-$ARGUMENTS.md during coding

**Design Ready for Implementation**: [✅/⚠️ WITH ASSUMPTIONS]
```

</design_orchestration>

<error_handling>
If design phase encounters issues:

**Issue: Requirements unclear or incomplete**

- Inform user which requirements are ambiguous
- List specific questions needing clarification
- Offer to proceed with documented assumptions
- Flag assumptions prominently in design specification

**Issue: Tech stack missing component library**

- Design from first principles using framework primitives
- Document which components need custom development
- Flag to Implementation Planner for task breakdown
- Provide design guidance for custom component development

**Issue: Scope creep detected**

- List features being designed that aren't in scope-validation
- Ask user: "Should we expand scope or defer these designs?"
- If scope expansion: Update scope-validation-$ARGUMENTS.md first
- If deferral: Remove out-of-scope designs, note for future

**Issue: Accessibility conflicts**

- Highlight specific accessibility vs. design aesthetic tradeoffs
- Always prioritize accessibility (WCAG 2.1 AA is non-negotiable)
- Suggest alternative designs that meet WCAG without compromising usability
- Document the tradeoff and resolution in design specification

**Issue: Verification failures after revision**

- If 2 revision rounds don't resolve issues, escalate to user
- Present specific verification failures that couldn't be resolved
- Offer options: (a) proceed with documented gaps, (b) gather more context, (c) simplify scope
- Don't proceed to implementation until critical verification checks pass
  </error_handling>

<best_practices>

## Design Command Best Practices

1. **Always load context first** - Never design in vacuum, ground in requirements and tech
2. **Enforce prerequisites** - No design without requirements and tech analysis
3. **Use verification checkpoints** - Catch issues early through systematic verification
4. **Reference tech stack** - Designs must be implementable with stated technology
5. **Prioritize accessibility** - WCAG 2.1 AA is minimum, not optional or negotiable
6. **Document thoroughly** - Developers should have zero ambiguity in specifications
7. **Stay in scope** - Only design MVP features, flag scope creep immediately
8. **Think mobile-first** - Most users are on mobile, design for smallest screen first
9. **Specify all states** - Default, hover, active, disabled, error, loading, empty, focus
10. **Plan for failure** - Error states, empty states, loading states, offline states
11. **Ground in reality** - No invented framework APIs, components, or capabilities
12. **Iterate through verification** - Use revision loop to improve design quality systematically
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
- Design decisions already made, verified, and documented
  </integration_notes>

---

Design the UX/UI for feature: **$ARGUMENTS**

Begin by loading prerequisites from `.claude/memory/` and reasoning through context analysis in Phase 1.
