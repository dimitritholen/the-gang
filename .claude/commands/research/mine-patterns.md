---
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
argument-hint: --type [pattern-type]
description: Extract and analyze recurring code patterns from codebase to document conventions and identify deviations
---

# Pattern Mining Command

**System date assertion**: Retrieve current system date before proceeding (via Bash tool if needed)

Act as a code analysis specialist with expertise in pattern recognition, convention extraction, and codebase standardization.

## Objective

Automatically identify dominant code patterns in specific areas (error handling, state management, API design, testing, etc.), quantify their prevalence, document them as conventions, and highlight deviations that should be refactored for consistency.

## Usage

```bash
/mine-patterns --type "error-handling"
/mine-patterns --type "state-management"
/mine-patterns --type "api-design"
/mine-patterns --type "testing-patterns"
/mine-patterns --type "import-style"
/mine-patterns --type "export-style"
/mine-patterns --type "naming-conventions"
/mine-patterns --type "styling-patterns"
```

## Task Decomposition

### Task 0: Detect Language and Framework

**Objective**: Identify project language and framework before pattern detection.

**Sub-tasks**:

0.1. Detect primary language

- Use Glob to find language indicators:
  - JavaScript/TypeScript: `**/package.json`, `**/*.{js,ts,jsx,tsx}`
  - Python: `**/requirements.txt`, `**/setup.py`, `**/*.py`
  - Go: `**/go.mod`, `**/*.go`
  - Rust: `**/Cargo.toml`, `**/*.rs`
  - Java: `**/pom.xml`, `**/build.gradle`, `**/*.java`
  - C#: `**/*.csproj`, `**/*.cs`
- Count files by extension to determine dominant language
- Store in DETECTED_LANGUAGE variable

  0.2. Detect framework (if applicable)

- Read package.json/requirements.txt/etc. to identify frameworks
- Common frameworks to detect:
  - React, Vue, Svelte, Angular (JavaScript/TypeScript)
  - FastAPI, Flask, Django (Python)
  - Express, Fastify, Koa (Node.js)
  - Gin, Echo, Chi (Go)
  - Axum, Actix (Rust)
- Store in DETECTED_FRAMEWORK variable

  0.3. Determine source directories and exclusions

- Language-specific source paths:
  - JavaScript/TypeScript: src, lib, components, pages
  - Python: src, app, lib
  - Go: cmd, pkg, internal
  - Rust: src
  - Java: src/main/java
- Language-specific exclusions:
  - JavaScript/TypeScript: node_modules, dist, build
  - Python: venv, **pycache**, .eggs
  - Go: vendor, bin
  - Rust: target
  - Java: target, build

**Output**: DETECTED_LANGUAGE, DETECTED_FRAMEWORK, source paths, exclusions

---

### Task 1: Parse and Validate Arguments

**Objective**: Extract pattern type from command arguments and validate against supported types.

**Sub-tasks**:

1.1. Extract pattern type from arguments

- Strip `--type` prefix and any extra whitespace
- Store in PATTERN_TYPE variable

  1.2. Validate against supported pattern types

- Check against allowlist: error-handling, state-management, api-design, testing-patterns, import-style, export-style, naming-conventions, styling-patterns
- Exit with error message if invalid
- Display list of supported types on error

**Implementation**:

Extract and validate pattern type:

1. Parse arguments to extract pattern type (remove `--type` prefix if present)
2. Validate against supported types list
3. Exit with error message if invalid, showing list of supported types
4. Store validated pattern type

Supported types:

- error-handling
- state-management
- api-design
- testing-patterns
- import-style
- export-style
- naming-conventions
- styling-patterns

**Output**: PATTERN_TYPE variable validated and ready for use

---

### Task 2: Define Pattern Detection Strategy

**Objective**: Configure search patterns specific to the requested pattern type.

**Pre-requisite**: Detect project language/framework before defining patterns

**Language Detection Strategy**:

- Use Glob to find language indicators (package.json, requirements.txt, go.mod, Cargo.toml, etc.)
- Read project files to determine dominant language and framework
- Adapt pattern definitions based on detected ecosystem

**Sub-tasks**:

2.1. Load pattern-specific detection patterns

- Map pattern type to search patterns for detected language/framework
- Define regex patterns for each category
- Specify file paths and extensions to scan (adapt to detected language)

  2.2. Configure category definitions

- Define mutually exclusive pattern categories
- Set category descriptions and metadata
- Specify detection regex for each category

  2.3. Set scope and exclusions

- Include directories: src, lib, api, components, services (or language-specific equivalents)
- Exclude directories: language-specific build/dependency dirs (node_modules, venv, target, dist, build, coverage, .git)
- Filter by file types relevant to detected language and pattern

**Pattern Definitions by Type**:

#### Error Handling (error-handling)

**Detection Patterns** (adapt based on detected language):

**Language-Agnostic Approach**:

1. Detect language first via Glob (_.js, _.py, _.go, _.rs, etc.)
2. Adapt search patterns to language syntax

**Example Patterns by Language**:

JavaScript/TypeScript:

- Grep pattern: `catch\s*\(` for catch blocks
- Grep pattern: `throw\s+` for throw statements
- Grep pattern: `console\.error` for console logging
- Grep pattern: `toast\.|showNotification\(|alert\(` for notifications
- Grep pattern: `logger\.|log\.error|logError` for structured logging

Python:

- Grep pattern: `except\s+` for exception handling
- Grep pattern: `raise\s+` for raising exceptions
- Grep pattern: `logging\.(error|exception)` for logging
- Grep pattern: `print.*error` for console output

Go:

- Grep pattern: `if err != nil` for error checking
- Grep pattern: `return.*err` for error propagation
- Grep pattern: `log\.(Error|Fatal|Panic)` for logging

Rust:

- Grep pattern: `Result<` for Result types
- Grep pattern: `\?` for error propagation operator
- Grep pattern: `unwrap\(\)|expect\(` for panic patterns
- Grep pattern: `match.*Err` for error matching

**Categories** (adapt labels to detected language):

- user-notification: User-facing error notifications
- logging: Error logging to console/file/service
- exception-propagation: Throw/raise/return error to caller
- structured-logging: Structured logging to external service
- error-value: Return error value/object (varies by language)
- silent-error: Empty error handling (anti-pattern)

#### State Management (state-management)

**Detection Patterns** (adapt based on detected framework):

**Framework Detection Strategy**:

1. Use Glob to find framework indicators (package.json dependencies, imports)
2. Detect if React, Vue, Svelte, Angular, or other framework
3. Adapt patterns to framework-specific state management

**Example Patterns by Framework**:

React:

- Grep pattern: `useState\(` for local state
- Grep pattern: `useContext\(` for context API
- Grep pattern: `useSelector\(|useDispatch\(|createSlice` for Redux
- Grep pattern: `create\(.*set.*get|useStore` for Zustand
- Grep pattern: `useRecoilState\(|atom\(` for Recoil

Vue:

- Grep pattern: `ref\(|reactive\(` for Vue 3 composition API
- Grep pattern: `data\(\)` for Vue options API
- Grep pattern: `pinia|defineStore` for Pinia
- Grep pattern: `Vuex|createStore` for Vuex

Svelte:

- Grep pattern: `writable\(|readable\(` for stores
- Grep pattern: `\$:` for reactive statements
- Grep pattern: `let\s+\w+\s*=` for component state

Angular:

- Grep pattern: `@Input\(|@Output\(` for component props
- Grep pattern: `BehaviorSubject|Subject` for RxJS state
- Grep pattern: `@ngrx` for NgRx state management

**Categories** (adapt to detected framework):

- local-state: Component-local state (scope: local)
- context-state: Shared state via context/provide-inject (scope: scoped)
- global-store: Global state management library (scope: global)
- reactive-primitives: Framework reactive primitives (scope: local)
- observable-state: Observable-based state (RxJS, etc.) (scope: varies)

#### API Design (api-design)

**Detection Patterns** (adapt based on detected language/framework):

**Language/Framework Detection**:

1. Use Glob to identify API framework (Express, FastAPI, Axum, Gin, etc.)
2. Adapt patterns to framework-specific routing and response patterns

**Example Patterns by Framework**:

Node.js (Express/Fastify/Koa):

- Grep pattern: `app\.(get|post|put|patch|delete|use)\(|router\.(get|post|put|patch|delete)` for routes
- Grep pattern: `res\.(json|send|status)` for responses
- Grep pattern: `validate\(|schema\.|z\.` for validation

Python (FastAPI/Flask/Django):

- Grep pattern: `@app\.(get|post|put|patch|delete)|@router\.(get|post|put|patch|delete)` for routes
- Grep pattern: `return.*JSONResponse|jsonify` for responses
- Grep pattern: `pydantic|BaseModel|Schema` for validation

Go (Gin/Echo/Chi):

- Grep pattern: `router\.(GET|POST|PUT|PATCH|DELETE)|Handle\(` for routes
- Grep pattern: `c\.JSON\(|ctx\.JSON\(` for responses
- Grep pattern: `Bind\(|ShouldBind\(|validator` for validation

Rust (Axum/Actix):

- Grep pattern: `get\(|post\(|put\(|patch\(|delete\(` for routes
- Grep pattern: `Json\(|HttpResponse` for responses
- Grep pattern: `validate\(|Validate` for validation

**Categories** (language-agnostic):

- rest-versioned: Versioned REST endpoints (/api/v1/resource)
- rest-unversioned: Unversioned REST endpoints (/api/resource)
- graphql: GraphQL API
- grpc: gRPC API
- json-response: JSON response format
- status-first: Status-first response pattern

#### Testing Patterns (testing-patterns)

**Detection Patterns** (adapt based on detected language/framework):

**Test Framework Detection**:

1. Use Glob to find test files by extension/naming pattern
2. Read test files to identify test framework (Jest, pytest, Go testing, etc.)
3. Adapt patterns to framework-specific syntax

**Example Patterns by Language**:

JavaScript/TypeScript:

- Glob pattern: `**/*.test.{ts,tsx,js,jsx}` or `**/*.spec.{ts,tsx,js,jsx}` for test files
- Grep pattern: `describe\(|it\(|test\(|expect\(` for test structure
- Grep pattern: `jest\.mock\(|vi\.mock\(|mock\(|spy\(` for mocking

Python:

- Glob pattern: `**/test_*.py` or `**/*_test.py` for test files
- Grep pattern: `def test_|class Test` for test structure
- Grep pattern: `@pytest\.|@mock\.|patch\(` for pytest/mocking

Go:

- Glob pattern: `**/*_test.go` for test files
- Grep pattern: `func Test|t\.Run\(` for test structure
- Grep pattern: `gomock|testify|assert` for test helpers

Rust:

- Grep pattern: `#\[test\]|#\[cfg\(test\)\]` for test modules
- Grep pattern: `assert!|assert_eq!` for assertions
- Grep pattern: `mock|MockTrait` for mocking

**Categories** (adapt to detected language):

- framework-primary: Dominant test framework detected
- framework-secondary: Secondary test framework (if mixed)
- describe-nested: Nested describe/context blocks
- flat-tests: Flat test structure (no nesting)
- file-colocated: Tests colocated with source files
- file-separate: Tests in separate test directory

**Output**: Detection strategy configured, ready for execution

---

### Task 3: Execute Pattern Detection

**Objective**: Run grep/glob commands and collect raw pattern instances from codebase.

**Sub-tasks**:

3.1. Execute search commands

- Run all grep patterns for the selected pattern type
- Capture output to temporary files for processing
- Handle command failures gracefully

  3.2. Collect file and line references

- Parse grep output for file:line:content tuples
- Store in structured format for analysis
- Track context (surrounding lines) for each instance

  3.3. Initial instance count

- Count total instances found across all searches
- Verify non-zero results (handle edge case of no instances)
- Log detection summary for verification

**Implementation Pattern**:

Use Grep tool with appropriate parameters:

- pattern: Detection regex for category
- output_mode: "content" to capture matching lines
- -n: Include line numbers
- path: Detected source directories (varies by language)

Store results for analysis, count instances, verify non-zero results.

**Verification Questions**:

- Did all Grep tool calls execute successfully?
- Is the instance count non-zero for at least one category?
- Are results properly categorized?

**Output**: Raw pattern data collected, instance counts recorded

---

### Task 4: Categorize and Count Patterns

**Objective**: Classify each instance into pattern categories and calculate frequency distribution.

**Sub-tasks**:

4.1. Classify instances by category

- For each detected instance, determine which category it belongs to
- Handle hybrid patterns (instances matching multiple categories)
- Resolve ambiguous cases by primary intent

  4.2. Count instances per category

- Aggregate counts for each pattern category
- Calculate percentages relative to total instances
- Identify top patterns by frequency

  4.3. Rank patterns by prevalence

- Sort categories by instance count (descending)
- Assign ranks: 1 = most common, N = least common
- Flag categories with zero instances

  4.4. Determine dominance status

- Calculate dominant pattern (highest count)
- Determine dominance strength:
  - STRONG: >80% conformance
  - MODERATE: 50-80% conformance
  - WEAK: 30-50% conformance
  - NONE: <30% conformance

**Frequency Calculation**:

Process collected data to:

1. Count instances per category from Grep results
2. Calculate total instances across all categories
3. Find dominant pattern (highest count)
4. Calculate dominance percentage: (dominant_count / total) \* 100
5. Rank patterns by frequency

**Verification Questions**:

- Are all instances classified (no orphans)?
- Do category percentages sum to ~100%?
- Is the dominant pattern calculation correct?

**Output**: Pattern frequency distribution with counts, percentages, and dominance metrics

---

### Task 5: Identify Deviations

**Objective**: Find instances that don't conform to dominant pattern(s).

**Sub-tasks**:

5.1. Define deviation criteria

- Deviation = instance NOT matching dominant pattern
- If multiple acceptable patterns exist, only flag true outliers
- Consider module-specific conventions (may be acceptable deviations)

  5.2. Extract deviation instances

- List all file:line references for non-dominant patterns
- Group by pattern variant for bulk refactoring
- Include code context for each deviation

  5.3. Calculate deviation metrics

- Total deviation count = total - dominant_count
- Deviation percentage = (deviations / total) \* 100
- Refactoring effort estimate based on count

  5.4. Prioritize deviations

- High priority: Critical paths, frequently-called code
- Medium priority: Core business logic
- Low priority: Test code, utilities, legacy modules

**Implementation**:

Calculate deviation metrics:

1. deviations = total - dominant_count
2. deviation_percentage = (deviations / total) \* 100
3. Extract file:line references for non-dominant patterns from Grep results
4. Group deviations by pattern variant for bulk refactoring

**Verification Questions**:

- Are deviations accurately counted?
- Have I excluded intentional local conventions?
- Is prioritization justified by code criticality?

**Output**: Deviation list with file:line references, grouped by pattern variant

---

### Task 6: Geographic Distribution Analysis

**Objective**: Analyze pattern distribution across different modules/directories.

**Sub-tasks**:

6.1. Group instances by module

- Extract directory path from file:line references
- Group by top-level module (src/services, src/components, etc.)
- Count instances per module per pattern

  6.2. Calculate per-module dominance

- For each module, determine local dominant pattern
- Calculate module-specific conformance percentage
- Compare to global dominant pattern

  6.3. Identify module-specific conventions

- Flag modules where local pattern differs from global
- Assess if local variation is justified (legacy code, different team, etc.)
- Note in report as acceptable exception or deviation

**Output**: Geographic distribution showing pattern usage by module, highlighting local conventions

---

### Task 7: Verification Phase (Chain of Verification)

**Objective**: Validate analysis accuracy before generating final report.

**Sub-tasks**:

7.1. Coverage verification

- Did I scan ALL relevant files or miss some?
- Re-run with broader glob to verify coverage
- Check if any file extensions were excluded

  7.2. Categorization verification

- Are pattern categories mutually exclusive?
- Verify no instance counted in multiple categories
- Resolve hybrid patterns by primary intent

  7.3. Calculation verification

- Verify: dominant_percentage = (dominant_count / total) \* 100
- Ensure percentages sum to ~100% (accounting for rounding)
- Check arithmetic in all frequency calculations

  7.4. Deviation accuracy verification

- Deviation = total - dominant_count (if single acceptable pattern)
- If multiple acceptable patterns, only flag true outliers
- Verify deviation list matches calculated count

  7.5. Scope verification

- Excluded test files for production pattern analysis (unless testing-patterns)
- Excluded node_modules, build directories
- Included all relevant source directories

  7.6. Example representativeness verification

- Include both typical and edge-case instances
- Provide context (surrounding code) for clarity
- File:line references are accurate and resolvable

  7.7. Recommendation justification verification

- > 80% conformance → ENFORCE recommendation
- 50-80% conformance → STANDARDIZE recommendation
- <50% conformance → DOCUMENT_MULTIPLE recommendation
- Verify recommendation aligns with data

**Verification Checklist**:

```xml
<verification_results>
<coverage>
  <total_files_scanned>{count}</total_files_scanned>
  <verification_passed>true|false</verification_passed>
  <notes>{Any coverage gaps identified}</notes>
</coverage>

<categorization>
  <mutually_exclusive>true|false</mutually_exclusive>
  <overlaps_resolved>{count}</overlaps_resolved>
  <notes>{Any ambiguous instances}</notes>
</categorization>

<calculations>
  <percentages_sum>{X}%</percentages_sum>
  <arithmetic_verified>true|false</arithmetic_verified>
  <notes>{Any calculation corrections}</notes>
</calculations>

<deviations>
  <count_verified>true|false</count_verified>
  <list_matches_count>true|false</list_matches_count>
  <notes>{Any discrepancies found}</notes>
</deviations>

<scope>
  <exclusions_correct>true|false</exclusions_correct>
  <inclusions_complete>true|false</inclusions_complete>
  <notes>{Any scope adjustments needed}</notes>
</scope>

<examples>
  <representative>true|false</representative>
  <context_provided>true|false</context_provided>
  <references_accurate>true|false</references_accurate>
</examples>

<recommendation>
  <data_aligned>true|false</data_aligned>
  <justification>{Reasoning for recommendation}</justification>
</recommendation>
</verification_results>
```

**Self-Correction Protocol**:

- If any verification fails, revise analysis before proceeding
- Document corrections made during verification
- Re-run calculations if arithmetic errors found

**Output**: Verified analysis ready for report generation

---

### Task 8: Generate Pattern Mining Report

**Objective**: Create comprehensive markdown report documenting pattern analysis.

**Sub-tasks**:

8.1. Generate report metadata

- Pattern type analyzed
- Analysis date
- Codebase scope (directories, file types)
- Exclusions applied

  8.2. Create analysis summary section

- Total instances found
- Total files analyzed
- Patterns detected (count)
- Dominant pattern and dominance strength
- Overall conformance rate

  8.3. Document pattern distribution

- For each pattern (ranked by frequency):
  - Name and description
  - Instance count and percentage
  - Status (DOMINANT, ACCEPTABLE_SECONDARY, OUTLIER)
  - 2-3 representative code examples with file:line
  - Usage by module/directory

    8.4. Generate dominance analysis

- Assessment of dominance strength
- Recommendation (ENFORCE, STANDARDIZE, DOCUMENT_MULTIPLE, NO_ACTION)
- Rationale for recommendation
- Proposed convention text for coding-conventions.md

  8.5. Document deviations

- Summary: total count, percentage of codebase
- Deviations by pattern variant
- File:line references for all deviations
- Refactor-to suggestions for each
- Bulk refactoring opportunities

  8.6. Add geographic insights

- Module-specific pattern preferences
- Local conventions vs global dominant
- Notes on acceptable local variations

  8.7. Include evolution analysis (if git available)

- Pattern trends (increasing/decreasing usage)
- Newer files vs older files comparison
- Suggestions for evolving conventions

**Report Template**:

````markdown
# Pattern Mining Report: {pattern_type}

**Analysis Date**: {date}
**Pattern Type**: {error-handling | state-management | etc.}
**Detected Language/Framework**: {language/framework detected via Glob/Read}

## Codebase Scope

**Directories Scanned**: {detected source directories}
**File Types**: {detected file extensions}
**Excluded**: {language-specific exclusions: node_modules, venv, target, dist, build, coverage}

## Analysis Summary

- **Total Instances**: {count}
- **Total Files**: {count}
- **Patterns Detected**: {count}
- **Dominant Pattern**: {pattern_id} ({X}% conformance)
- **Dominance Strength**: STRONG | MODERATE | WEAK | NONE

## Pattern Distribution

### 1. {Pattern Name} (DOMINANT - {X}%)

**Description**: {What this pattern does}

**Count**: {instances} ({X}%)

**Status**: DOMINANT

**Examples**:

```{detected_language}
// File: {file_path}:{line_number}
{3-5 lines of code showing pattern usage}

// File: {file_path}:{line_number}
{3-5 lines of code showing pattern usage}
```
````

**Usage by Module**:

- {detected_module_1}: {X} instances ({Y}%)
- {detected_module_2}: {X} instances ({Y}%)
- {detected_module_3}: {X} instances ({Y}%)

---

{Repeat for all patterns, ranked by frequency}

## Dominance Analysis

**Assessment**: {Interpretation of dominance strength and conformance rate}

**Recommendation**: ENFORCE | STANDARDIZE | DOCUMENT_MULTIPLE | NO_ACTION

**Rationale**: {Why this recommendation based on data}

**Proposed Convention**:

```
{Convention text for coding-conventions.md}
```

**Migration Strategy**:

- Refactor {deviation_count} instances ({deviation_percentage}%) to use {dominant_pattern}
- Effort Estimate: {Low | Medium | High} - {reasoning}

## Deviations

**Summary**:

- Total Deviations: {count} ({X}% of codebase)
- Refactoring Priority: HIGH | MEDIUM | LOW

**Deviations by Pattern**:

### {Non-dominant Pattern Name}

**Count**: {instances}

**Instances**:

```
{file_path}:{line_number}
  {code snippet}
  Refactor to: {Dominant pattern suggestion}

{file_path}:{line_number}
  {code snippet}
  Refactor to: {Dominant pattern suggestion}
```

{List all deviations, up to 100, then summarize remaining}

**Bulk Refactoring Opportunity**:

- Pattern From: {Current pattern}
- Pattern To: {Dominant pattern}
- Files Affected: {count}
- Automation Feasibility: HIGH | MEDIUM | LOW

## Geographic Insights

### {detected_module_1}

- Dominant Pattern: {pattern_id}
- Conformance: {X}%
- Note: {If different from global, explain why}

### {detected_module_2}

- Dominant Pattern: {pattern_id}
- Conformance: {X}%
- Note: {If different from global, explain why}

{Repeat for other significant modules}

## Evolution Analysis

**Trend**: {Pattern usage increasing/decreasing based on git history analysis}

**Suggestions**: {Recommendations for evolving conventions}

---

**Report Generated**: {timestamp}

````

**Output**: Comprehensive markdown report saved to `.claude/memory/pattern-analysis-{type}.md`

---

### Task 9: Auto-Update Coding Conventions (Conditional)

**Objective**: If dominance is strong (>80%), automatically update coding-conventions.md.

**Condition**: Execute only if dominant_percentage > 80

**Sub-tasks**:

9.1. Load existing conventions
- Read `.claude/memory/coding-conventions.md`
- Parse existing sections
- Identify if section for this pattern type exists

9.2. Generate convention section
- Use proposed convention text from report
- Include code examples (correct vs incorrect)
- Add rationale and exceptions
- Note migration status (deviations remaining)

9.3. Update or append section
- If section exists: Replace with updated content
- If section doesn't exist: Append new section
- Preserve existing sections unchanged
- Add "Last Updated" timestamp

9.4. Verify update
- Re-read file to confirm changes applied
- Validate markdown formatting
- Ensure no data loss in existing content

**Convention Section Template**:

```markdown
## {Pattern Type} Convention

**Last Updated**: {date} (auto-generated from pattern mining)

**Detected Language/Framework**: {detected_language_framework}

**Dominant Pattern**: {pattern_name} ({X}% conformance)

**Convention**: {Description of required pattern}

**Examples**:

```{detected_language}
// CORRECT (dominant pattern)
{code example}

// INCORRECT (deviation)
{code example of outlier pattern}
````

**Rationale**: {Why this pattern is preferred - based on analysis}

**Exceptions**: {Any acceptable deviations and when justified}

**Migration Status**: {X} deviations remain (see pattern-analysis-{type}.md)

```

**Output**: Updated coding-conventions.md (if >80% dominance), otherwise skip this task

---

## Anti-Hallucination Safeguards

**Evidence-Based Only**:
- Every pattern claim backed by Grep tool results with file:line references
- No invented patterns without code evidence
- All code examples from actual codebase files (via Read tool)

**Quantitative Precision**:
- Use exact counts and percentages
- Do NOT claim "most code uses X" without numerical evidence
- Always show calculation: (count / total) * 100

**Source Citation**:
- Every code example includes file:line reference
- Do NOT create synthetic examples
- Context from actual file content only (verified via Read)

**No Assumption of Uniformity**:
- Explicitly note module-specific conventions
- Do NOT assume global patterns apply everywhere
- Report local variations as findings

**No Language/Framework Hardcoding**:
- Always detect language/framework first via Glob/Read
- Adapt patterns dynamically to detected ecosystem
- Never assume JavaScript/React or any specific stack

**Verification of Coverage**:
- Verify Grep/Glob covered all relevant files before finalizing
- Note excluded directories explicitly (language-specific)
- Document any scope limitations

## Error Handling

### No Instances Found

If Grep returns 0 results:
- Report: "No instances of {pattern_type} found in codebase for detected language {language}"
- Recommendation: Either pattern not used OR detection regex needs refinement for this language
- Suggest checking if language detection was correct
- Do NOT fabricate patterns
- Exit gracefully with informative message

### Insufficient Data

If total_instances < 10:
- Report: "Insufficient data for reliable pattern analysis"
- Recommendation: Manual review required
- Do NOT claim dominance with small sample
- List all instances found for manual review

### Equal Distribution (No Dominant)

If all patterns < 40% conformance:
- Report: "No clear dominant pattern"
- Recommendation: DOCUMENT_MULTIPLE acceptable patterns
- Note: Team should discuss and choose standard
- Provide usage statistics for each pattern

### Coding Conventions File Missing

If `.claude/memory/coding-conventions.md` not found:
- Create new file with pattern section
- Note: "Initial conventions generated from pattern mining"
- Include standard header and structure

## Success Criteria

**Task Completion Indicators**:
- All phases executed without errors
- Verification phase passed all checks
- Report generated with complete data
- File written successfully to `.claude/memory/`
- (Optional) Coding conventions updated if applicable

**Output Validation**:
- Report contains all required sections
- All file:line references are resolvable
- Calculations are mathematically sound
- Recommendations justified by data

**Final Output Message**:

```

SUCCESS: Pattern mining complete

Pattern Type: {pattern_type}
Total Instances: {count}
Dominant Pattern: {pattern_name} ({X}% conformance)
Deviations: {count} ({Y}%)

Report: .claude/memory/pattern-analysis-{type}.md
{If updated: Conventions: .claude/memory/coding-conventions.md (updated)}

Recommendation: {ENFORCE | STANDARDIZE | DOCUMENT_MULTIPLE | NO_ACTION}

```

```
