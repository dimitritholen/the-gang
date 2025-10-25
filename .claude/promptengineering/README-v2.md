# Prompt Engineering Optimizer v2

## Overview

Multi-pattern prompt optimizer that transforms vague user prompts into advanced, technique-driven instructions using semantic intent detection, pattern layering, and quality validation.

## Key Improvements Over v1

### v1 Limitations
- Single-pattern selection (primary technique only)
- Simple keyword matching
- Combination only when match <60%
- Template-driven output (fill blanks)
- No quality validation

### v2 Enhancements
- **Multi-pattern layering** (Foundation + Enhancements + Formatter)
- **Semantic intent detection** (Goals, Quality, Output types)
- **Pattern compatibility matrix** (explicit layering rules)
- **Quality validation** (Chain of Verification for enhanced prompts)
- **Pre-built combination templates** (common use cases)
- **Self-critique** (generate alternatives if confidence <80%)

## Architecture

```
User Prompt
    |
    v
Intent Detection (intent-taxonomy.json)
    |
    +-- Goal Classification (CREATE, DEBUG, OPTIMIZE, etc.)
    +-- Quality Requirements (CORRECTNESS, SECURITY, etc.)
    +-- Output Type (CODE, ARCHITECTURE, etc.)
    +-- Complexity Level (basic, intermediate, advanced, expert)
    |
    v
Pattern Selection
    |
    +-- Foundation Pattern (1 required)
    +-- Enhancement Patterns (0-2 optional)
    +-- Formatter Pattern (0-1 optional)
    |
    v
Pattern Layering (pattern-layering.json)
    |
    +-- Validate compatibility
    +-- Check layering rules
    +-- Apply integration points
    |
    v
Template Construction
    |
    +-- Use combination-templates.json if match
    +-- Otherwise, merge patterns using layering rules
    |
    v
Quality Validation (Chain of Verification)
    |
    +-- Remove vague terms
    +-- Add success criteria
    +-- Specify output format
    +-- Include validation steps
    |
    v
Self-Critique & Alternatives
    |
    +-- Identify weaknesses
    +-- Generate alternative if <80% confidence
    |
    v
Enhanced Prompt + Metadata
```

## File Structure

```
.claude/promptengineering/
├── patterns.json                 # 14 core techniques (unchanged from v1)
├── intent-taxonomy.json          # NEW: Intent detection rules
├── pattern-layering.json         # NEW: Compatibility & integration rules
├── combination-templates.json    # NEW: Pre-built multi-pattern templates
└── README-v2.md                  # This file
```

## Usage

### Command
```bash
/prompt-v2 "vague user prompt here"
```

### Examples

**Example 1: Debug Production Bug**
```
User: "fix the checkout bug"

v1 Output: Chain of Thought template with {problem_breakdown}

v2 Output:
- Intent: DEBUG goal + CORRECTNESS quality
- Patterns: CoT (1) + CoVe (2)
- Template: "debug_critical" from combination-templates.json
- Enhanced: Step-by-step analysis → Solution → Verification checklist → Validated fix
```

**Example 2: Design Scalable System**
```
User: "design a system for 1M users"

v1 Output: Role-Based template (generic expert)

v2 Output:
- Intent: DESIGN goal + PERFORMANCE quality + ARCHITECTURE output
- Patterns: Role (7) + Multi-Objective (5) + Self-Consistency (4)
- Template: "architecture_design"
- Enhanced: Staff Architect role → Multi-objective trade-offs → 3 approaches → Consensus → Optimal design
```

**Example 3: Implement New Feature**
```
User: "add user authentication"

v1 Output: Chain of Thought steps

v2 Output:
- Intent: CREATE goal + SECURITY quality + CODE output
- Patterns: Task Decomposition (12) + CoT (1) + CoVe (2)
- Template: "feature_implementation" with security enhancements
- Enhanced: Phase decomposition → Implementation details → Security verification → Deployment plan
```

## Intent Taxonomy

### Goals (8 categories)
- **CREATE**: Build new functionality
- **DEBUG**: Fix bugs, troubleshoot
- **OPTIMIZE**: Improve performance/quality
- **DESIGN**: Architecture, planning
- **ANALYZE**: Understand, investigate
- **MIGRATE**: Refactor, modernize
- **VALIDATE**: Test, verify, audit
- **DOCUMENT**: Write guides, docs

### Quality Requirements (6 categories)
- **CORRECTNESS** (priority 10): Must be correct, reliable
- **SECURITY** (priority 10): Must be secure, audited
- **PERFORMANCE** (priority 8): Must be fast, efficient
- **COMPLETENESS** (priority 7): Handle all edge cases
- **MAINTAINABILITY** (priority 6): Clean, readable
- **COLLABORATIVE** (priority 5): Team/stakeholder needs

### Output Types (6 categories)
- CODE: Implementation files
- ARCHITECTURE: Design docs, diagrams
- TESTS: Test suites
- DOCUMENTATION: Guides, explanations
- CONFIGURATION: Setup, deployment
- ANALYSIS: Reports, findings

## Pattern Layering

### Roles
- **FOUNDATION**: Primary structure (1 required)
  - Patterns: 1, 3, 4, 5, 7, 12, 13
- **ENHANCEMENT**: Quality layers (0-2 optional)
  - Patterns: 2, 6, 8, 9, 10, 11
- **FORMATTER**: Output structure (0-1 optional)
  - Patterns: 3, 10, 14

### Layering Rules
- Max 3 patterns total
- Must check canCombineWith compatibility
- Integration points define where patterns merge
- Priority: Foundation > Quality requirements > Formatter

### Common Combinations
- **CoT + CoVe**: Verified reasoning (patterns 1, 2)
- **Role + CoT + CoVe**: Expert verified reasoning (7, 1, 2)
- **Decomposition + CoC**: Specialized workflow (12, 3)
- **ReAct + CoVe**: Verified investigation (13, 2)
- **Multi-Objective + Self-Consistency**: Trade-off analysis (5, 4)

## Pre-built Templates

### debug_critical
- **Patterns**: CoT (1) + CoVe (2)
- **Use**: Production bugs needing systematic analysis
- **Output**: Analysis → Solution → Verification → Deployment checklist

### architecture_design
- **Patterns**: Role (7) + Multi-Objective (5) + Self-Consistency (4)
- **Use**: System design with competing objectives
- **Output**: Expert role → Trade-offs → Multiple approaches → Optimal design

### feature_implementation
- **Patterns**: Task Decomposition (12) + CoT (1) + CoVe (2)
- **Use**: New feature development
- **Output**: Phase breakdown → Details → Verification → Deployment

### security_audit
- **Patterns**: Role (7) + CoVe (2) + Recursive Self-Improvement (11)
- **Use**: Security review and remediation
- **Output**: Expert audit → Multi-perspective verification → Recursive fixes

### refactoring_legacy
- **Patterns**: Task Decomposition (12) + Reflexion (8) + Chain of Draft (6)
- **Use**: Legacy code modernization
- **Output**: Decomposed phases → Iterative drafts → Reflection → Migration plan

## Quality Validation

Enhanced prompts are verified against:
- [ ] Removed vague terms (good, better, optimize)
- [ ] Defined measurable success criteria
- [ ] Specified output format/structure
- [ ] Included validation/verification steps
- [ ] Added edge case considerations
- [ ] Used imperative verbs (analyze, generate, verify)
- [ ] Set clear constraints (scope, length, format)

If any validation fails, prompt is automatically revised.

## Self-Critique

If pattern match confidence <80%:
1. Generate alternative pattern combination
2. Compare primary vs alternative
3. Present both options to user
4. Recommend best based on clarity/actionability

## Migration from v1

### Keep Using v1 If
- Simple single-pattern optimization sufficient
- Basic keyword matching adequate
- Don't need multi-pattern combinations

### Use v2 If
- Complex prompts needing multiple techniques
- Critical tasks requiring validation
- Want semantic intent detection
- Need pre-built templates for common scenarios
- Require quality assurance on enhanced prompts

## Future Enhancements

Potential v3 improvements:
- Machine learning for pattern selection
- User feedback loop for template refinement
- Domain-specific pattern libraries (ML, DevOps, etc.)
- Integration with execution layer (auto-run enhanced prompts)
- Pattern effectiveness metrics (track which combinations work best)
