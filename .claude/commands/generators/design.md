---
allowed-tools: Task, Read, Write
argument-hint: [project idea or path to prd]
description: Transform project plans into designs via multi-agent pipeline with strict verification
---

# Design Pipeline Orchestrator

Execute 6-stage design pipeline with STRICT VERIFICATION GATES using specialized sub-agents.

Each stage operates in its own context window, reading handoff documents from previous stages.
This prevents context exhaustion while maintaining knowledge continuity.

## Input

User's project plan/PRD: $ARGUMENTS

## Architecture

```
Stage 1: Sector Research (business-analyst)
  Input: User's PRD
  Output: sector_analysis.json

Stage 2: Design Research (design-researcher)
  Input: sector_analysis.json
  Output: design_research.json

Stage 3: Quality Checklist (qa-specialist)
  Input: design_research.json
  Output: quality_checklist.json

Stage 4: Design Variants (VERIFICATION LOOP)
  4A: Initial Design (design-strategist)
    Input: design_research.json, quality_checklist.json
    Output: design_specs_draft.json

  4B: Design Audit (quality-auditor)
    Input: design_specs_draft.json, quality_checklist.json
    Output: audit_report_v1.json

  4C: Revision Loop (design-strategist, max 3 iterations)
    IF audit FAIL: Fix violations, re-audit
    IF audit PASS: Proceed to Stage 5

  Output: design_specs_final.json

Stage 5: HTML Implementation (VERIFICATION LOOP)
  5A: Initial HTML (implementation-engineer)
    Input: design_specs_final.json
    Output: 6 HTML files, implementation_manifest.json

  5B: Code Audit (code-auditor)
    Input: HTML files, quality_checklist.json, design_specs_final.json
    Output: code_audit_report_v1.json

  5C: Fix Loop (implementation-engineer, max 3 iterations)
    IF audit FAIL: Fix violations, re-audit
    IF audit PASS: Proceed to Stage 6

  Output: Approved HTML files

Stage 6: Documentation (documentation-specialist)
  Input: design_specs_final.json, HTML files
  Output: design_system_1.md, design_system_2.md, design_system_3.md
```

## Execution Protocol

**CRITICAL RULES**:

1. Each stage waits for previous stage completion
2. Verification loops (4B-4C, 5B-5C) are MANDATORY
3. Auditor agents have VETO power - cannot skip verification
4. Max 3 revision iterations per verification loop
5. If verification fails after 3 iterations, ESCALATE with details
6. All pain point checks are BINARY (pass/fail)

---

## Stage 1: Sector Research

Invoke business-analyst to analyze project and identify competitors.

<stage_1>
Use Task tool to invoke business-analyst:

subagent_type: business-analyst
description: Analyze project and identify sector competitors
prompt: |
Analyze the following project plan/PRD and identify the sector, target audience, and 8-12 competitor websites for design research.

Project Plan/PRD:
$ARGUMENTS

Your tasks:

1. Read and analyze the project documentation
2. Identify sector/niche classification
3. Define target audience clearly
4. Research and list 8-12 competitor websites with strong design
5. Provide comprehensive business context

Write your findings to: sector_analysis.json

Use this structure:
{
"sector": "Primary industry sector",
"niche": "Specific niche within sector",
"target_audience": "Detailed audience description",
"competitor_urls": ["https://competitor1.com", ...8-12 URLs],
"business_context": "Comprehensive market context"
}

Wait for business-analyst to complete and write sector_analysis.json.
</stage_1>

After Stage 1 completion, proceed to Stage 2.

---

## Stage 2: Design Research

Invoke design-researcher to analyze competitor designs.

<stage_2>
Use Task tool to invoke design-researcher:

subagent_type: design-researcher
description: Research competitor designs and extract patterns
prompt: |
Analyze competitor websites from sector research to extract design patterns and sector conventions.

Read from: sector_analysis.json (in current working directory)

Your tasks:

1. Visit each competitor URL from sector_analysis.json
2. Document layout patterns, visual mood, typography, colors
3. Extract sector-specific design conventions
4. Synthesize dominant design style for this niche

Write your findings to: design_research.json

Include: dominant_style, layout_patterns, mood_assessment (1-10 scale),
typography_patterns, color_patterns, whitespace_strategy, sector_conventions

Wait for design-researcher to complete and write design_research.json.
</stage_2>

After Stage 2 completion, proceed to Stage 3.

---

## Stage 3: Quality Checklist Creation

Invoke qa-specialist to create testable validation criteria.

<stage_3>
Use Task tool to invoke qa-specialist:

subagent_type: qa-specialist
description: Create quality checklist with binary validation criteria
prompt: |
Create a comprehensive quality checklist with CONCRETE, testable rejection criteria to prevent AI-generated design failures.

Read from: design_research.json (in current working directory)

Your tasks:

1. Research AI-generated UI common failures
2. Create CONCRETE, testable rejection criteria (not subjective)
3. Map pain points to this specific sector
4. Define FORBIDDEN_PATTERNS with binary tests
5. Define REQUIRED_ELEMENTS with validation criteria

Write your checklist to: quality_checklist.json

Include TWO sections:

- FORBIDDEN_PATTERNS: Minimum 10 patterns with objective tests
- REQUIRED_ELEMENTS: Minimum 5 requirements with validation criteria

  Each forbidden pattern must include:

- pattern: Name
- test: Exact, objective test to perform
- why_forbidden: Reason

  Each required element must include:

- requirement: Description
- test: How to validate
- sector_justification: Why it matters

Wait for qa-specialist to complete and write quality_checklist.json.
</stage_3>

After Stage 3 completion, proceed to Stage 4.

---

## Stage 4: Design Variant Generation with Verification Loop

### Stage 4A: Initial Design Generation

Invoke design-strategist to create 3 design variants.

<stage_4a>
Use Task tool to invoke design-strategist:

subagent_type: design-strategist
description: Generate 3 design variants from research
prompt: |
Create 3 design variants based on sector research while avoiding AI design cliches.

MODE: INITIAL GENERATION

Read from (current working directory):

- design_research.json
- quality_checklist.json

  Your tasks:
  1. Create 3 variants of SAME base style (from dominant_style in design_research.json)
  2. Variants differ by: layout, typography, color palette, spacing
  3. All variants stay within researched design language
  4. ALL variants must avoid EVERY forbidden pattern from quality_checklist.json
  5. ALL variants must include EVERY required element from quality_checklist.json

  Write to: design_specs_draft.json

  Structure: Array of 3 variant objects, each with:

- variant_id
- differentiation_strategy
- layout_approach
- typography (font_families, scale, weights)
- color_palette (primary, secondary, accent, backgrounds, text)
- spacing_system
- component_inventory
- pages (main_page and detail_page wireframes)

  CRITICAL: Primary colors must NOT be in blue (#0000FF-#0099FF) or purple (#6600FF-#9966FF) ranges.
  CRITICAL: Backgrounds must include colored/textured options (not all white).

Wait for design-strategist to complete and write design_specs_draft.json.
</stage_4a>

### Stage 4B: Design Specification Audit

Invoke quality-auditor to validate designs against checklist.

<stage_4b_iteration>
iteration = 1
current_spec_file = "design_specs_draft.json"

LOOP (max 3 iterations):
Use Task tool to invoke quality-auditor:

subagent_type: quality-auditor
description: Audit design specifications iteration {iteration}
prompt: |
Audit design specifications against quality checklist with binary pass/fail validation.

    Read from (current working directory):
    - {current_spec_file}
    - quality_checklist.json

    Your tasks:
    1. Check EACH variant against ALL forbidden patterns
    2. Check EACH variant against ALL required elements
    3. Record specific violations with exact locations
    4. Determine PASS or FAIL for each variant
    5. Determine overall decision: PROCEED or REVISE

    Write to: audit_report_v{iteration}.json

    For each variant, execute ALL tests from quality_checklist.json.
    Record violations with: type, pattern/missing, location, value, fix.

    Output structure:
    {
      "iteration": {iteration},
      "variants": [
        {"variant_id": 1, "status": "PASS/FAIL", "violations": [...]},
        {"variant_id": 2, "status": "PASS/FAIL", "violations": [...]},
        {"variant_id": 3, "status": "PASS/FAIL", "violations": [...]}
      ],
      "overall_decision": "PROCEED" or "REVISE",
      "summary": "X variants passed, Y variants failed, Z total violations"
    }

Wait for quality-auditor to complete and write audit_report_v{iteration}.json.

Read audit_report_v{iteration}.json to check overall_decision.

IF overall_decision == "PROCEED":
Rename {current_spec_file} to design_specs_final.json
BREAK loop
Proceed to Stage 5

ELSE IF iteration < 3: ### Stage 4C: Design Revision
Use Task tool to invoke design-strategist:

    subagent_type: design-strategist
    description: Revise design specifications based on audit feedback
    prompt: |
      Revise design specifications to address violations from audit report.

      MODE: REVISION

      Read from (current working directory):
      - {current_spec_file}
      - audit_report_v{iteration}.json
      - quality_checklist.json

      Your tasks:
      1. Address SPECIFIC violations listed in audit report
      2. Fix ONLY cited problems (no unrelated changes)
      3. Ensure fixes don't create new violations
      4. Maintain differentiation between variants
      5. Preserve successful elements

      Write to: design_specs_revised.json

      For each failing variant:
      - Review violations array
      - Fix each violation specifically
      - Ensure required elements now present
      - Remove/replace forbidden patterns

    Wait for design-strategist to complete and write design_specs_revised.json.

    current_spec_file = "design_specs_revised.json"
    iteration++
    Continue loop (re-audit)

ELSE:
ESCALATE TO USER with violations from audit_report_v3.json
EXIT pipeline
</stage_4b_iteration>

After Stage 4 completion (design_specs_final.json created), proceed to Stage 5.

---

## Stage 5: HTML Implementation with Verification Loop

### Stage 5A: Initial HTML Generation

Invoke implementation-engineer to generate HTML files.

<stage_5a>
Use Task tool to invoke implementation-engineer:

subagent_type: implementation-engineer
description: Generate production HTML/CSS for 3 variants
prompt: |
Generate production-quality HTML files implementing the approved design specifications.

MODE: INITIAL GENERATION

Read from: design_specs_final.json (in current working directory)

Your tasks:

1. For each of 3 variants, generate 2 HTML files (main page + detail page)
2. Implement responsive layouts matching specs exactly
3. Use semantic HTML5
4. Inline CSS in <style> tag with CSS custom properties
5. Apply typography, colors, spacing from design specs
6. NO placeholder Lorem Ipsum unless clearly demo context
7. Create implementation_manifest.json

Write to current working directory:

- main_1.html (Variant 1, main page)
- detail_1.html (Variant 1, detail page)
- main_2.html (Variant 2, main page)
- detail_2.html (Variant 2, detail page)
- main_3.html (Variant 3, main page)
- detail_3.html (Variant 3, detail page)
- implementation_manifest.json

  Quality requirements:

- Clean, readable code
- Responsive (mobile, tablet, desktop)
- Semantic markup
- Exact color hex values from design_specs_final.json
- Font families from specifications
- Spacing system applied consistently

Wait for implementation-engineer to complete and write all 7 files.
</stage_5a>

### Stage 5B: Code Audit

Invoke code-auditor to validate HTML/CSS implementation.

<stage_5b_iteration>
iteration = 1

LOOP (max 3 iterations):
Use Task tool to invoke code-auditor:

subagent_type: code-auditor
description: Audit HTML/CSS code iteration {iteration}
prompt: |
Audit actual HTML/CSS code against quality checklist with binary pass/fail validation.

    Read from (current working directory):
    - main_1.html, detail_1.html, main_2.html, detail_2.html, main_3.html, detail_3.html
    - quality_checklist.json
    - design_specs_final.json

    Your tasks:
    1. Inspect ACTUAL HTML/CSS code in each file
    2. Check for forbidden patterns in real code (parse CSS, extract colors, check layout)
    3. Verify implementation matches design_specs_final.json
    4. Record violations with file names and line numbers
    5. Determine PASS or FAIL for each file
    6. Determine overall decision: PROCEED or REVISE

    Write to: code_audit_report_v{iteration}.json

    Execute code inspection tests:
    - Parse CSS for gradients, extract hex colors, check forbidden ranges
    - Inspect hero section HTML structure
    - Extract font-family declarations
    - Analyze layout code for asymmetry
    - Check background-color values
    - Find border-radius patterns
    - Search button text for generic CTAs
    - Compare colors to design_specs_final.json

    For each violation provide:
    {
      "file": "filename.html",
      "line": line_number,
      "issue": "Specific code pattern found",
      "forbidden_pattern": "Pattern name",
      "fix": "Exact fix needed"
    }

    Output structure:
    {
      "iteration": {iteration},
      "files": [
        {"file": "main_1.html", "status": "PASS/FAIL", "violations": [...]},
        ...all 6 files
      ],
      "overall_decision": "PROCEED" or "REVISE",
      "summary": "X files passed, Y files failed, Z total violations"
    }

Wait for code-auditor to complete and write code_audit_report_v{iteration}.json.

Read code_audit_report_v{iteration}.json to check overall_decision.

IF overall_decision == "PROCEED":
BREAK loop
Proceed to Stage 6

ELSE IF iteration < 3: ### Stage 5C: Code Revision
Use Task tool to invoke implementation-engineer:

    subagent_type: implementation-engineer
    description: Fix HTML/CSS violations from audit
    prompt: |
      Fix HTML/CSS code violations based on audit report.

      MODE: FIX MODE

      Read from (current working directory):
      - main_1.html through detail_3.html (existing files)
      - code_audit_report_v{iteration}.json
      - design_specs_final.json (for reference)

      Your tasks:
      1. Read audit report violations for each file
      2. Fix violations at specified line numbers
      3. Do NOT make unrelated changes
      4. Ensure fixes match design_specs_final.json
      5. Preserve working code

      For each file with violations:
      - Navigate to line numbers cited
      - Fix ONLY the specific issues:
        * Remove gradients
        * Change colors to match design_specs_final.json
        * Fix generic CTAs to context-specific text
        * Add missing elements
        * Fix border-radius uniformity

      Write updated HTML files to current working directory (overwrite existing).

    Wait for implementation-engineer to complete and write updated HTML files.

    iteration++
    Continue loop (re-audit)

ELSE:
ESCALATE TO USER with violations from code_audit_report_v3.json
EXIT pipeline
</stage_5b_iteration>

After Stage 5 completion (all HTML files pass audit), proceed to Stage 6.

---

## Stage 6: Design System Documentation

Invoke documentation-specialist to create comprehensive docs.

<stage_6>
Use Task tool to invoke documentation-specialist:

subagent_type: documentation-specialist
description: Create design system documentation for all variants
prompt: |
Create comprehensive design system documentation for each of the 3 approved design variants.

Read from (current working directory):

- design_specs_final.json
- main_1.html through detail_3.html (approved implementation)

  Your tasks:
  1. For EACH variant, create comprehensive design system documentation
  2. Document all design tokens (colors, typography, spacing)
  3. Explain design rationale and differentiation
  4. Provide component patterns with examples
  5. Document layout guidelines and responsive strategy
  6. Include accessibility notes
  7. Explain how design avoids AI pain points

  Write to current working directory:

- design_system_1.md
- design_system_2.md
- design_system_3.md

  Each file must include sections:

- Overview (philosophy, differentiation, sector context)
- Design Tokens (colors with hex, typography with fonts, spacing)
- Component Patterns (extracted from HTML with usage guidelines)
- Layout Guidelines (grid, breakpoints, responsive strategy)
- Accessibility Notes (contrast ratios, semantic markup)
- Why This Avoids AI Pain Points (explicit explanation)

  Be comprehensive but readable. Provide concrete examples.
  Calculate contrast ratios. Reference sector research findings.

Wait for documentation-specialist to complete and write all 3 markdown files.
</stage_6>

---

## Completion

All deliverables ready:

**Handoff Documents**:

- sector_analysis.json
- design_research.json
- quality_checklist.json
- design_specs_final.json
- audit_report_v\*.json files
- code_audit_report_v\*.json files
- implementation_manifest.json

**Final Deliverables**:

- main_1.html, detail_1.html (Variant 1)
- main_2.html, detail_2.html (Variant 2)
- main_3.html, detail_3.html (Variant 3)
- design_system_1.md, design_system_2.md, design_system_3.md

Present summary to user with file locations and next steps (e.g., open HTML files in browser to review variants).
