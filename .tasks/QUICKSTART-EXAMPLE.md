# Task Management System - Quick Start Example

**Date**: 2025-10-23
**Purpose**: Demonstrate complete workflow with minimal test feature

---

## Complete Workflow Example

### Step 1: Gather Requirements

```bash
/gather-requirements "Add a simple welcome page with navigation menu"
```

**Result**:

- Creates: `.tasks/01-welcome-page/feature-brief.md`
- Creates: `.tasks/01-welcome-page/requirements-welcome-page.md`
- Updates: `.tasks/manifest.json` (adds feature with status NOT_STARTED)

### Step 2: Research Technology Stack

```bash
/research-tech 01-welcome-page
```

**Result**:

- Creates: `.tasks/01-welcome-page/tech-analysis-welcome-page.md`
- Recommends: React components, routing library, styling approach

### Step 3: Create Implementation Plan

```bash
/plan-implementation 01-welcome-page
```

**Result**:

- Creates: `.tasks/01-welcome-page/manifest.json`
- Creates: `.tasks/01-welcome-page/T01-page-layout.xml`
- Creates: `.tasks/01-welcome-page/T02-navigation-component.xml`
- Creates: `.tasks/01-welcome-page/T03-styling.xml`
- Updates: `.tasks/manifest.json` (status → IN_PROGRESS, taskCount: 3)

**Directory structure now**:

```
.tasks/
├── manifest.json                                   # Root tracking
└── 01-welcome-page/
    ├── feature-brief.md                           # Context
    ├── requirements-welcome-page.md               # Detailed requirements
    ├── tech-analysis-welcome-page.md              # Stack recommendations
    ├── manifest.json                              # Task navigation
    ├── T01-page-layout.xml                        # Task definition
    ├── T02-navigation-component.xml               # Task definition
    └── T03-styling.xml                            # Task definition
```

### Step 4: Check Progress

```bash
/task-status 01-welcome-page
```

**Output**:

```
Feature: 01-welcome-page - Welcome Page
Status: IN_PROGRESS

Progress: 0/3 tasks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0%

Next Task: T01 - Page Layout
  Priority: HIGH
  Complexity: LOW
  Estimate: 2 hours

Dependencies: None (ready to start)

Tasks:
  ⏸️  T01 - Page Layout (NOT_STARTED)
  ⏸️  T02 - Navigation Component (NOT_STARTED, depends on T01)
  ⏸️  T03 - Styling (NOT_STARTED, depends on T02)
```

### Step 5: Get Next Task Details

```bash
/task-next 01-welcome-page
```

**Output**:

```
Next Task: T01 - Page Layout

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Description:
  Create the basic page layout structure with header,
  main content area, and footer sections.

Acceptance Criteria:
  ✓ Page component exists in src/pages/Welcome.jsx
  ✓ Header section includes logo placeholder
  ✓ Main content area is responsive
  ✓ Footer section includes copyright text
  ✓ Component renders without errors

Completion Checklist:
  ☐ Create Welcome.jsx component
  ☐ Add basic HTML structure
  ☐ Add semantic HTML tags
  ☐ Test component rendering
  ☐ Add basic accessibility attributes

Effort Estimate: 2 hours (HIGH confidence)

Technical Notes:
  - Use functional component with hooks
  - Prepare props for navigation data
  - Use semantic HTML5 elements
  - Consider mobile-first responsive approach

Ready to start: /task-start T01 01-welcome-page
```

### Step 6: Start Task

```bash
/task-start T01 01-welcome-page
```

**Result**:

- Updates: T01-page-layout.xml (status="IN_PROGRESS")
- Updates: `.tasks/01-welcome-page/manifest.json` (task status)
- **Hook trigger**: `validate-task-transition` checks dependencies (✓ passed)

**Output**:

```
✓ Task Started: T01 - Page Layout

Feature: 01-welcome-page
Started: 2025-10-23 16:30:00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task Details:
  Component: Pages
  Priority: HIGH
  Complexity: LOW
  Estimate: 2 hours

Dependencies: None ✓

Next Steps:
  1. Create src/pages/Welcome.jsx
  2. Implement basic layout structure
  3. Test rendering
  4. Complete acceptance criteria

When done: /task-complete T01 01-welcome-page
```

### Step 7: Do The Work

**Developer actions** (not shown in commands):

1. Create `src/pages/Welcome.jsx`
2. Implement layout with header, main, footer
3. Test component
4. Verify all acceptance criteria met

**Optional**: Create output document

```bash
cat > .tasks/01-welcome-page/T01-output.md <<'EOF'
# T01 - Page Layout - Completion Summary

## Task Summary
Created Welcome page component with responsive layout structure.

## Acceptance Criteria Status
✓ Page component exists in src/pages/Welcome.jsx
✓ Header section includes logo placeholder
✓ Main content area is responsive
✓ Footer section includes copyright text
✓ Component renders without errors

## Work Performed
- Created Welcome.jsx functional component
- Implemented three-section layout (header, main, footer)
- Added semantic HTML5 elements
- Included basic ARIA labels
- Tested component rendering successfully

## Files Created
- src/pages/Welcome.jsx (45 lines)

## Testing
- Unit test: Component renders ✓
- Visual test: Layout displays correctly ✓
- Responsive test: Mobile/desktop views ✓

## Effort Tracking
Estimated: 2 hours
Actual: 1.5 hours
EOF
```

### Step 8: Complete Task

```bash
/task-complete T01 01-welcome-page
```

**Result**:

- Updates: T01-page-layout.xml (status="COMPLETED", completed timestamp)
- Updates: `.tasks/01-welcome-page/manifest.json` (completedCount: 1, nextTask: "T02")
- Updates: `.tasks/manifest.json` (feature completedCount: 1)
- **Hook trigger**: `validate-manifest-consistency` checks synchronization (✓ passed)

**Output**:

```
✓ Task Completed: T01 - Page Layout

Feature: 01-welcome-page
Completed: 2025-10-23 18:00:00
Duration: 1.5 hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Acceptance Criteria: All met ✓

Feature Progress: 1/3 tasks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 33%

Next Task Available: T02 - Navigation Component
  All dependencies met ✓
  Ready to start: /task-start T02 01-welcome-page
```

### Step 9: Continue with Remaining Tasks

```bash
# Start T02
/task-start T02 01-welcome-page

# [Do the work...]

# Complete T02
/task-complete T02 01-welcome-page

# Start T03
/task-start T03 01-welcome-page

# [Do the work...]

# Complete T03
/task-complete T03 01-welcome-page
```

### Step 10: Feature Completion

After completing T03, automatic detection triggers:

**Output**:

```
✓ Task Completed: T03 - Styling

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 FEATURE COMPLETED: 01-welcome-page

All tasks completed: 3/3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

Feature deliverables:
  ✓ Welcome page with layout
  ✓ Navigation component
  ✓ Styling implementation

Feature artifacts:
  - Feature brief: .tasks/01-welcome-page/feature-brief.md
  - Requirements: .tasks/01-welcome-page/requirements-welcome-page.md
  - Tech analysis: .tasks/01-welcome-page/tech-analysis-welcome-page.md
  - Task outputs: T01-output.md, T02-output.md, T03-output.md

Feature Status: COMPLETED ✓
```

---

## Example: Handling Blocked Task

### Scenario: T02 blocked by missing design assets

```bash
# Start T02
/task-start T02 01-welcome-page

# Discover blocker during work
/task-block T02 01-welcome-page "Missing navigation icon assets from design team"
```

**Output**:

```
Task Blocked: T02 - Navigation Component 🚫

Feature: 01-welcome-page
Blocked: 2025-10-23 18:30:00
Reason: Missing navigation icon assets from design team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommended Actions:
  1. Contact design team for icon assets
  2. Request specific SVG icons needed
  3. Establish expected delivery timeline

Alternative Work:
  No independent tasks available (T03 depends on T02)
  Focus on resolving blocker

Once resolved:
  /task-unblock T02 01-welcome-page
```

**Later, after getting assets**:

```bash
/task-unblock T02 01-welcome-page "Received icon assets via email"
```

**Output**:

```
Task Unblocked: T02 - Navigation Component ✓

Feature: 01-welcome-page
Unblocked: 2025-10-23 20:00:00
Block Duration: 1.5 hours
Resolution: Received icon assets via email

Task Status: IN_PROGRESS (resumed)

Resume work on this task
When complete: /task-complete T02 01-welcome-page
```

---

## Validation Example

### Check Manifest Consistency

```bash
/validate-manifests 01-welcome-page
```

**Output** (all valid):

```
✓ Manifest Validation Complete

Feature: 01-welcome-page
  ✓ Task count: 3 ✓
  ✓ Completed count: 1 ✓
  ✓ Feature status: IN_PROGRESS ✓
  ✓ Next task: T02 ✓
  ✓ Blockers: 0 ✓

All manifests are synchronized and consistent.
```

---

## Multi-Feature Example

### User Request with Multiple Features

```bash
/gather-requirements "Build authentication system and product catalog"
```

**Auto-detection** (requirements-analyst Step 1.5):

```
Chain-of-Thought: Multi-Feature Detection

Analyzing user input...

Feature 1 Detected: Authentication System
  Indicators: login, signup, password, user accounts
  User Persona: All users
  Distinct Goal: Secure user access

Feature 2 Detected: Product Catalog
  Indicators: products, listing, search, categories
  User Persona: Shoppers/buyers
  Distinct Goal: Browse and discover products

Decision: SEPARATE FEATURES (2 distinct capabilities)

Proceeding with separate feature analysis...
```

**Result**:

- Creates: `.tasks/01-authentication-system/`
- Creates: `.tasks/02-product-catalog/`
- Updates: `.tasks/manifest.json` (2 features added)

**Then proceed independently**:

```bash
/research-tech 01-authentication-system
/research-tech 02-product-catalog

/plan-implementation 01-authentication-system
/plan-implementation 02-product-catalog

# Work on features in parallel or sequentially
/task-next 01-authentication-system
/task-next 02-product-catalog
```

---

## Token Efficiency Demonstration

### Before (Monolithic)

```
Reading implementation-plan-user-auth.md: 2500 lines
Token usage: ~8,000 tokens per task context load
```

### After (Modular)

```
Reading T01-database-schema.xml: 85 lines
Token usage: ~300 tokens per task context load

Reduction: ~96% for individual task operations
```

### Manifest Navigation

```
Reading task manifest: 45 lines (nextTask: "T06")
Reading T06-api-endpoints.xml: 120 lines
Total: ~500 tokens

vs. reading entire 2500-line file: ~8,000 tokens
Savings: ~94% per task lookup
```

---

## Summary

**Complete workflow demonstrated**:

1. ✓ Requirements → feature brief + requirements doc
2. ✓ Tech research → stack recommendations
3. ✓ Planning → task manifest + XML task files
4. ✓ Execution → start, complete, block, unblock
5. ✓ Validation → manifest consistency checks
6. ✓ Completion → automatic feature completion detection

**Token efficiency**: ~80-95% reduction in context usage per task operation

**Workflow integrity**: Validated by hooks at every status transition

**Ready for production use** ✓
