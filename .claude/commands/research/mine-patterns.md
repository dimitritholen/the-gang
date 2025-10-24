---
allowed-tools: Bash(code-tools:*), Read, Grep, Glob, Write, Edit, WebFetch
argument-hint: --type [pattern-type]
description: Extract and analyze recurring code patterns from codebase to document conventions and identify deviations
---

# Pattern Mining Command

**System date assertion**: Retrieve current system date via `date +%Y-%m-%d` before proceeding

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

```bash
# Extract pattern type from arguments
PATTERN_TYPE="$ARGUMENTS"
# Remove --type prefix if present
PATTERN_TYPE="${PATTERN_TYPE#--type }"
PATTERN_TYPE="${PATTERN_TYPE#--type=}"

# Validate pattern type
case "$PATTERN_TYPE" in
  error-handling|state-management|api-design|testing-patterns|import-style|export-style|naming-conventions|styling-patterns)
    # Valid pattern type
    ;;
  *)
    echo "Error: Unknown pattern type '$PATTERN_TYPE'"
    echo "Supported types: error-handling, state-management, api-design, testing-patterns, import-style, export-style, naming-conventions, styling-patterns"
    exit 1
    ;;
esac
```

**Output**: PATTERN_TYPE variable validated and ready for use

---

### Task 2: Define Pattern Detection Strategy

**Objective**: Configure grep/glob patterns specific to the requested pattern type.

**Sub-tasks**:

2.1. Load pattern-specific detection patterns
- Map pattern type to search patterns
- Define regex patterns for each category
- Specify file paths and extensions to scan

2.2. Configure category definitions
- Define mutually exclusive pattern categories
- Set category descriptions and metadata
- Specify detection regex for each category

2.3. Set scope and exclusions
- Include directories: src, lib, api, components, services
- Exclude directories: node_modules, dist, build, coverage, .git
- Filter by file types relevant to pattern

**Pattern Definitions by Type**:

#### Error Handling (error-handling)

**Detection Patterns**:
```bash
# Find catch blocks
code-tools grep_code --pattern "catch\s*\(" --output-mode content -n --paths "src,lib"

# Find throw statements
code-tools grep_code --pattern "throw\s+" --output-mode content -n --paths "src,lib"

# Find console.error
code-tools grep_code --pattern "console\.error" --output-mode content -n --paths "src,lib"

# Find toast/notification calls
code-tools grep_code --pattern "toast\.|showNotification\(|alert\(" --output-mode content -n --paths "src,lib"

# Find error logging
code-tools grep_code --pattern "logger\.|log\.error|logError" --output-mode content -n --paths "src,lib"
```

**Categories**:
- toast-notification: User-facing error notifications (toast, modal, alert)
- console-error: Browser console logging
- throw-to-caller: Throw exception to calling function
- structured-logging: Structured logging to external service
- return-error-object: Return error object instead of throwing
- silent-catch: Empty catch block (anti-pattern)

#### State Management (state-management)

**Detection Patterns**:
```bash
# Find useState hooks
code-tools grep_code --pattern "useState\(" --output-mode content -n --paths "src"

# Find useContext
code-tools grep_code --pattern "useContext\(" --output-mode content -n --paths "src"

# Find Redux patterns
code-tools grep_code --pattern "useSelector\(|useDispatch\(|createSlice" --output-mode content -n --paths "src"

# Find Zustand patterns
code-tools grep_code --pattern "create\(.*set.*get|useStore" --output-mode content -n --paths "src"

# Find Recoil patterns
code-tools grep_code --pattern "useRecoilState\(|atom\(" --output-mode content -n --paths "src"
```

**Categories**:
- local-useState: Component-local state via useState (scope: local)
- context-api: Global state via React Context (scope: global)
- redux: Redux/Redux Toolkit (scope: global)
- zustand: Zustand state management (scope: global)
- recoil: Recoil atoms (scope: global)

#### API Design (api-design)

**Detection Patterns**:
```bash
# Find API endpoints/routes
code-tools grep_code --pattern "app\.(get|post|put|patch|delete|use)\(|router\.(get|post|put|patch|delete)" --output-mode content -n --paths "src,api"

# Find API response patterns
code-tools grep_code --pattern "res\.(json|send|status)" --output-mode content -n --paths "src,api"

# Find request validation
code-tools grep_code --pattern "validate\(|schema\.|z\." --output-mode content -n --paths "src,api"
```

**Categories**:
- rest-versioned: Versioned REST endpoints (/api/v1/resource)
- rest-unversioned: Unversioned REST endpoints (/api/resource)
- graphql: GraphQL API
- json-response: JSON response format
- status-first: Status-first response pattern (res.status().json())

#### Testing Patterns (testing-patterns)

**Detection Patterns**:
```bash
# Find test files
code-tools search_file --glob "**/*.test.{ts,tsx,js,jsx}" --limit 100
code-tools search_file --glob "**/*.spec.{ts,tsx,js,jsx}" --limit 100

# Find test framework usage
code-tools grep_code --pattern "describe\(|it\(|test\(|expect\(" --output-mode content -n --type ts --type js

# Find mocking patterns
code-tools grep_code --pattern "jest\.mock\(|vi\.mock\(|mock\(|spy\(" --output-mode content -n --type ts --type js
```

**Categories**:
- jest: Jest testing framework
- vitest: Vitest testing framework
- describe-it: Describe/it test structure
- test-only: Test() only (no describe)
- file-colocated: Tests colocated with source files
- file-separate: Tests in separate __tests__ directory

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

```bash
# Execute grep and store results
code-tools grep_code --pattern "{pattern}" --output-mode content -n --paths "src,lib" > /tmp/pattern-results-$CATEGORY.txt

# Count instances
INSTANCE_COUNT=$(wc -l < /tmp/pattern-results-$CATEGORY.txt)

# Verify results
if [ $INSTANCE_COUNT -eq 0 ]; then
  echo "Warning: No instances found for category: $CATEGORY"
fi
```

**Verification Questions**:
- Did all grep commands execute successfully?
- Are temporary files created and readable?
- Is the instance count non-zero for at least one category?

**Output**: Raw pattern data collected in temporary files, instance counts recorded

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

```bash
declare -A pattern_counts

# Count instances for each category
for category in "${!categories[@]}"; do
  count=$(grep -c "${category_regex[$category]}" /tmp/pattern-results.txt)
  pattern_counts[$category]=$count
done

# Calculate total
total=0
for count in "${pattern_counts[@]}"; do
  total=$((total + count))
done

# Find dominant pattern
dominant_pattern=""
dominant_count=0
for pattern in "${!pattern_counts[@]}"; do
  count=${pattern_counts[$pattern]}
  if [ $count -gt $dominant_count ]; then
    dominant_count=$count
    dominant_pattern=$pattern
  fi
done

# Calculate dominance percentage
if [ $total -gt 0 ]; then
  dominant_percentage=$((dominant_count * 100 / total))
else
  dominant_percentage=0
fi
```

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
- Deviation percentage = (deviations / total) * 100
- Refactoring effort estimate based on count

5.4. Prioritize deviations
- High priority: Critical paths, frequently-called code
- Medium priority: Core business logic
- Low priority: Test code, utilities, legacy modules

**Implementation**:

```bash
# Calculate deviations
deviations=$((total - dominant_count))
deviation_percentage=$((deviations * 100 / total))

# Extract deviation file references
for pattern in "${!pattern_counts[@]}"; do
  if [ "$pattern" != "$dominant_pattern" ]; then
    echo "Deviation pattern: $pattern (${pattern_counts[$pattern]} instances)"
    grep -n "${category_regex[$pattern]}" /tmp/pattern-results.txt
  fi
done
```

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
- Verify: dominant_percentage = (dominant_count / total) * 100
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
- >80% conformance → ENFORCE recommendation
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

```markdown
# Pattern Mining Report: {pattern_type}

**Analysis Date**: {date}
**Pattern Type**: {error-handling | state-management | etc.}

## Codebase Scope

**Directories Scanned**: {src, lib, api}
**File Types**: {.ts, .tsx, .js, .jsx}
**Excluded**: {node_modules, dist, build, coverage}

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

```{language}
// File: src/services/auth.ts:45
{3-5 lines of code showing pattern usage}

// File: src/components/form.tsx:128
{3-5 lines of code showing pattern usage}
```

**Usage by Module**:
- src/services: {X} instances ({Y}%)
- src/components: {X} instances ({Y}%)
- src/utils: {X} instances ({Y}%)

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
src/utils/parser.ts:78
  {code snippet}
  Refactor to: {Dominant pattern suggestion}

src/components/modal.tsx:203
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

### src/services
- Dominant Pattern: {pattern_id}
- Conformance: {X}%
- Note: {If different from global, explain why}

### src/components
- Dominant Pattern: {pattern_id}
- Conformance: {X}%
- Note: {If different from global, explain why}

{Repeat for other significant modules}

## Evolution Analysis

**Trend**: {Pattern usage increasing/decreasing based on git history analysis}

**Suggestions**: {Recommendations for evolving conventions}

---

**Report Generated**: {timestamp}
```

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

**Dominant Pattern**: {pattern_name} ({X}% conformance)

**Convention**: {Description of required pattern}

**Examples**:

```{language}
// CORRECT (dominant pattern)
{code example}

// INCORRECT (deviation)
{code example of outlier pattern}
```

**Rationale**: {Why this pattern is preferred - based on analysis}

**Exceptions**: {Any acceptable deviations and when justified}

**Migration Status**: {X} deviations remain (see pattern-analysis-{type}.md)
```

**Output**: Updated coding-conventions.md (if >80% dominance), otherwise skip this task

---

## Anti-Hallucination Safeguards

**Evidence-Based Only**:
- Every pattern claim backed by grep results with file:line references
- No invented patterns without code evidence
- All code examples from actual codebase files

**Quantitative Precision**:
- Use exact counts and percentages
- Do NOT claim "most code uses X" without numerical evidence
- Always show calculation: (count / total) * 100

**Source Citation**:
- Every code example includes file:line reference
- Do NOT create synthetic examples
- Context from actual file content only

**No Assumption of Uniformity**:
- Explicitly note module-specific conventions
- Do NOT assume global patterns apply everywhere
- Report local variations as findings

**Verification of Coverage**:
- Verify grep covered all relevant files before finalizing
- Note excluded directories explicitly
- Document any scope limitations

## Error Handling

### No Instances Found

If grep returns 0 results:
- Report: "No instances of {pattern_type} found in codebase"
- Recommendation: Either pattern not used OR detection regex needs refinement
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
