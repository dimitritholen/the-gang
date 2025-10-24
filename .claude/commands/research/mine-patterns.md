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

## Argument Parsing

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

## Methodology

### Phase 1: Pattern Detection Strategy

Define grep/glob patterns for each pattern type:

#### Error Handling Patterns

**Detection Strategy**:

```bash
# Find all error handling blocks
code-tools grep_code --pattern "catch\s*\(" --output-mode content -n --paths "src,lib" > /tmp/error-handling-raw.txt

# Find throw statements
code-tools grep_code --pattern "throw\s+" --output-mode content -n --paths "src,lib" > /tmp/throw-statements.txt

# Find console.error
code-tools grep_code --pattern "console\.error" --output-mode content -n --paths "src,lib" > /tmp/console-error.txt

# Find toast/notification calls
code-tools grep_code --pattern "toast\.|showNotification\(|alert\(" --output-mode content -n --paths "src,lib" > /tmp/toast-notifications.txt

# Find error logging
code-tools grep_code --pattern "logger\.|log\.error|logError" --output-mode content -n --paths "src,lib" > /tmp/error-logging.txt
```

**Pattern Categorization Logic**:

```xml
<pattern_categories>
<category id="toast-notification">
  <regex>toast\.|showNotification\(|displayError\(</regex>
  <description>User-facing error notifications (toast, modal, alert)</description>
</category>

<category id="console-error">
  <regex>console\.(error|warn)</regex>
  <description>Browser console logging</description>
</category>

<category id="throw-to-caller">
  <regex>throw\s+new\s+\w+Error</regex>
  <description>Throw exception to calling function</description>
</category>

<category id="structured-logging">
  <regex>logger\.|log\.error|logError</regex>
  <description>Structured logging to external service</description>
</category>

<category id="return-error-object">
  <regex>return\s+\{\s*error:|return\s+\{.*error:\s*true</regex>
  <description>Return error object instead of throwing</description>
</category>

<category id="silent-catch">
  <regex>catch\s*\([^)]+\)\s*\{\s*\}</regex>
  <description>Empty catch block (anti-pattern)</description>
</category>
</pattern_categories>
```

#### State Management Patterns

**Detection Strategy**:

```bash
# Find useState hooks
code-tools grep_code --pattern "useState\(" --output-mode content -n --paths "src" > /tmp/use-state.txt

# Find useContext
code-tools grep_code --pattern "useContext\(" --output-mode content -n --paths "src" > /tmp/use-context.txt

# Find Redux patterns
code-tools grep_code --pattern "useSelector\(|useDispatch\(|createSlice" --output-mode content -n --paths "src" > /tmp/redux-patterns.txt

# Find Zustand patterns
code-tools grep_code --pattern "create\(.*set.*get|useStore" --output-mode content -n --paths "src" > /tmp/zustand-patterns.txt

# Find Recoil patterns
code-tools grep_code --pattern "useRecoilState\(|atom\(" --output-mode content -n --paths "src" > /tmp/recoil-patterns.txt
```

**Pattern Categories**:

```xml
<pattern_categories>
<category id="local-useState">
  <regex>useState\(</regex>
  <description>Component-local state via useState</description>
  <scope>local</scope>
</category>

<category id="context-api">
  <regex>useContext\(|createContext</regex>
  <description>Global state via React Context</description>
  <scope>global</scope>
</category>

<category id="redux">
  <regex>useSelector|useDispatch|createSlice</regex>
  <description>Redux/Redux Toolkit</description>
  <scope>global</scope>
</category>

<category id="zustand">
  <regex>create\(|useStore</regex>
  <description>Zustand state management</description>
  <scope>global</scope>
</category>

<category id="recoil">
  <regex>useRecoilState|atom\(</regex>
  <description>Recoil atoms</description>
  <scope>global</scope>
</category>
</pattern_categories>
```

#### API Design Patterns

**Detection Strategy**:

```bash
# Find API endpoints/routes
code-tools grep_code --pattern "app\.(get|post|put|patch|delete|use)\(|router\.(get|post|put|patch|delete)" --output-mode content -n --paths "src,api" > /tmp/api-routes.txt

# Find API response patterns
code-tools grep_code --pattern "res\.(json|send|status)" --output-mode content -n --paths "src,api" > /tmp/api-responses.txt

# Find request validation
code-tools grep_code --pattern "validate\(|schema\.|z\." --output-mode content -n --paths "src,api" > /tmp/validation-patterns.txt
```

**Pattern Categories**:

```xml
<pattern_categories>
<category id="rest-versioned">
  <regex>/api/v\d+/</regex>
  <description>Versioned REST endpoints (/api/v1/resource)</description>
</category>

<category id="rest-unversioned">
  <regex>/api/(?!v\d+)</regex>
  <description>Unversioned REST endpoints (/api/resource)</description>
</category>

<category id="graphql">
  <regex>graphql|gql\`</regex>
  <description>GraphQL API</description>
</category>

<category id="json-response">
  <regex>res\.json\(</regex>
  <description>JSON response format</description>
</category>

<category id="status-first">
  <regex>res\.status\(\d+\)\.json\(</regex>
  <description>Status-first response pattern</description>
</category>
</pattern_categories>
```

#### Testing Patterns

**Detection Strategy**:

```bash
# Find test files
code-tools search_file --glob "**/*.test.{ts,tsx,js,jsx}" --limit 100 > /tmp/test-files.txt
code-tools search_file --glob "**/*.spec.{ts,tsx,js,jsx}" --limit 100 >> /tmp/test-files.txt

# Find test framework usage
code-tools grep_code --pattern "describe\(|it\(|test\(|expect\(" --output-mode content -n --type ts --type js > /tmp/test-framework.txt

# Find mocking patterns
code-tools grep_code --pattern "jest\.mock\(|vi\.mock\(|mock\(|spy\(" --output-mode content -n --type ts --type js > /tmp/mocking-patterns.txt
```

**Pattern Categories**:

```xml
<pattern_categories>
<category id="jest">
  <regex>jest\.|expect\(.*\)\.to</regex>
  <description>Jest testing framework</description>
</category>

<category id="vitest">
  <regex>vi\.|import.*vitest</regex>
  <description>Vitest testing framework</description>
</category>

<category id="describe-it">
  <regex>describe\(.*it\(</regex>
  <description>Describe/it test structure</description>
</category>

<category id="test-only">
  <regex>test\(</regex>
  <description>Test() only (no describe)</description>
</category>

<category id="file-colocated">
  <pattern>*.test.tsx next to *.tsx</pattern>
  <description>Tests colocated with source files</description>
</category>

<category id="file-separate">
  <pattern>__tests__/ directory</pattern>
  <description>Tests in separate __tests__ directory</description>
</category>
</pattern_categories>
```

### Phase 2: Chain-of-Thought Pattern Analysis

Before quantifying patterns, reason through the analysis approach:

```xml
<pattern_analysis_reasoning>
<detection_summary>
**Raw Data Collected**:
- {Pattern Type}: {Number of files scanned}
- {Total instances found}: {Count}
- {Categories detected}: {List}

**Categorization Strategy**:
- Group similar patterns into categories
- Identify edge cases or hybrid patterns
- Note any ambiguous instances requiring manual review
</detection_summary>

<frequency_analysis_approach>
**Counting Method**:
1. For each category, count instances (file:line occurrences)
2. Calculate percentage of total instances
3. Identify dominant pattern (>50% = strong dominance, 40-50% = moderate, <40% = no clear dominant)
4. Track by directory/module to find local vs global patterns

**Dominance Threshold**:
- **Strong Dominance**: >80% conformance → recommend enforcing
- **Moderate Dominance**: 50-80% conformance → recommend standardizing
- **Weak Dominance**: <50% conformance → document multiple accepted patterns
</frequency_analysis_approach>

<deviation_identification>
**Deviation Definition**:
- Instance that doesn't match dominant pattern (top 1-2 patterns)
- Calculate: total_instances - (dominant_instances + acceptable_secondary_instances)

**Reporting Strategy**:
- List file:line for each deviation
- Prioritize by impact (critical paths, frequently-called code)
- Group by pattern variant for bulk refactoring
</deviation_identification>
</pattern_analysis_reasoning>
```

### Phase 3: Frequency Analysis

Implement pattern counting and dominance calculation:

```bash
# Pseudo-algorithm for error-handling example
declare -A pattern_counts

# Count instances for each category
pattern_counts["toast-notification"]=$(grep -c "toast\." /tmp/error-handling-raw.txt)
pattern_counts["console-error"]=$(grep -c "console\.error" /tmp/error-handling-raw.txt)
pattern_counts["throw-to-caller"]=$(grep -c "throw\s*new" /tmp/error-handling-raw.txt)
# ... repeat for all categories

# Calculate total
total=0
for count in "${pattern_counts[@]}"; do
  total=$((total + count))
done

# Calculate percentages and identify dominant
dominant_pattern=""
dominant_count=0
for pattern in "${!pattern_counts[@]}"; do
  count=${pattern_counts[$pattern]}
  percentage=$((count * 100 / total))

  if [ $count -gt $dominant_count ]; then
    dominant_count=$count
    dominant_pattern=$pattern
  fi

  echo "$pattern: $count instances ($percentage%)"
done

dominant_percentage=$((dominant_count * 100 / total))
```

**Frequency Calculation Template**:

```xml
<frequency_analysis>
<total_instances>{count}</total_instances>
<total_files_analyzed>{count}</total_files_analyzed>

<pattern_distribution>
  <pattern id="{id}" rank="1">
    <name>{Pattern name}</name>
    <count>{instances}</count>
    <percentage>{X}%</percentage>
    <status>DOMINANT | SECONDARY | MINORITY</status>
    <files>
      <file path="{path}" line="{number}" context="{code snippet}"/>
      <!-- List top 10-20 instances -->
    </files>
  </pattern>
</pattern_distribution>

<dominance_assessment>
  <dominant_pattern>{pattern_id}</dominant_pattern>
  <dominance_strength>STRONG|MODERATE|WEAK|NONE</dominance_strength>
  <conformance_percentage>{X}%</conformance_percentage>
  <recommendation>
    {ENFORCE | STANDARDIZE | DOCUMENT_MULTIPLE | NO_CLEAR_PATTERN}
  </recommendation>
</dominance_assessment>

<deviations>
  <deviation_count>{total - dominant_count}</deviation_count>
  <deviation_percentage>{Y}%</deviation_percentage>
  <deviations_by_pattern>
    <pattern id="{non-dominant-id}">
      <count>{instances}</count>
      <files>
        <file path="{path}" line="{number}"/>
      </files>
    </pattern>
  </deviations_by_pattern>
</deviations>

<geographic_distribution>
  <module path="src/services">
    <pattern id="{id}" percentage="{X}%"/>
  </module>
  <module path="src/components">
    <pattern id="{id}" percentage="{X}%"/>
  </module>
  <!-- Note if certain modules have different conventions -->
</geographic_distribution>
</frequency_analysis>
```

### Phase 4: Chain-of-Verification

Validate analysis before generating report:

```xml
<verification_checklist>
<question>Did I count ALL instances or miss some files?</question>
<check>Re-run grep with glob patterns to verify coverage</check>
<check>Check if any file extensions were excluded</check>

<question>Are pattern categories mutually exclusive?</question>
<check>Verify no instance counted in multiple categories</check>
<check>Resolve hybrid patterns (e.g., "toast + logger") by primary intent</check>

<question>Is dominance calculation correct?</question>
<check>Verify: dominant_percentage = (dominant_count / total) * 100</check>
<check>Ensure percentages sum to ~100% (accounting for rounding)</check>

<question>Are deviations accurately identified?</question>
<check>Deviation = instance NOT matching dominant pattern</check>
<check>If multiple acceptable patterns, only flag true outliers</check>

<question>Did I analyze the right file scope?</question>
<check>Exclude test files for production pattern analysis (unless testing-patterns)</check>
<check>Exclude node_modules, build directories</check>

<question>Are examples representative?</question>
<check>Include both typical and edge-case instances</check>
<check>Provide context (surrounding code) for clarity</check>

<question>Is recommendation justified by data?</question>
<check>>80% conformance → ENFORCE recommendation</check>
<check>50-80% conformance → STANDARDIZE recommendation</check>
<check><50% conformance → DOCUMENT_MULTIPLE recommendation</check>
</verification_checklist>
```

### Phase 5: Pattern Mining Report Generation

Create comprehensive pattern analysis report:

```xml
<pattern_mining_report>
<metadata>
  <pattern_type>{error-handling | state-management | etc.}</pattern_type>
  <analysis_date>2025-10-23</analysis_date>
  <codebase_scope>
    <directories_scanned>{src, lib, api}</directories_scanned>
    <file_types>{.ts, .tsx, .js, .jsx}</file_types>
    <excluded>{node_modules, dist, build, coverage}</excluded>
  </codebase_scope>
</metadata>

<analysis_summary>
  <total_instances>{count}</total_instances>
  <total_files>{count}</total_files>
  <patterns_detected>{count}</patterns_detected>
  <dominant_pattern>{pattern_id}</dominant_pattern>
  <dominance_strength>STRONG|MODERATE|WEAK|NONE</dominance_strength>
  <conformance_rate>{X}%</conformance_rate>
</analysis_summary>

<pattern_distribution>
  <pattern id="{id}" rank="1">
    <name>{Human-readable name}</name>
    <description>{What this pattern does}</description>
    <count>{instances}</count>
    <percentage>{X}%</percentage>
    <status>DOMINANT | ACCEPTABLE_SECONDARY | OUTLIER</status>

    <examples>
      <example>
        <file>src/services/auth.ts</file>
        <line>45</line>
        <context>
          <code>
{3-5 lines of code showing pattern usage}
          </code>
        </context>
      </example>
      <!-- 2-3 representative examples -->
    </examples>

    <usage_locations>
      <module path="src/services" count="{X}" percentage="{Y}%"/>
      <module path="src/components" count="{X}" percentage="{Y}%"/>
    </usage_locations>
  </pattern>

  <!-- Repeat for all patterns, ranked by frequency -->
</pattern_distribution>

<dominance_analysis>
  <assessment>
    {Interpretation of dominance strength and conformance rate}
  </assessment>

  <recommendation>
    <action>ENFORCE | STANDARDIZE | DOCUMENT_MULTIPLE | NO_ACTION</action>
    <rationale>
      {Why this recommendation based on data}
    </rationale>
    <convention_text>
      {Proposed convention text for coding-conventions.md}
    </convention_text>
  </recommendation>

  <migration_strategy>
    <if_enforce>
      Refactor {deviation_count} instances ({deviation_percentage}%) to use {dominant_pattern}
    </if_enforce>
    <effort_estimate>
      {Low|Medium|High} - {reasoning}
    </effort_estimate>
  </migration_strategy>
</dominance_analysis>

<deviations>
  <summary>
    <total>{count}</total>
    <percentage_of_codebase>{X}%</percentage_of_codebase>
    <refactoring_priority>HIGH|MEDIUM|LOW</refactoring_priority>
  </summary>

  <deviations_by_pattern>
    <pattern id="{non-dominant-pattern-id}">
      <name>{Pattern name}</name>
      <count>{instances}</count>
      <instances>
        <instance>
          <file>src/utils/parser.ts</file>
          <line>78</line>
          <code>{Code snippet}</code>
          <refactor_to>{Dominant pattern suggestion}</refactor_to>
        </instance>
        <!-- List ALL deviations up to 100, then summarize -->
      </instances>
    </pattern>
  </deviations_by_pattern>

  <bulk_refactoring_opportunities>
    <opportunity>
      <pattern_from>{Current pattern}</pattern_from>
      <pattern_to>{Dominant pattern}</pattern_to>
      <instance_count>{count}</instance_count>
      <files_affected>{list}</files_affected>
      <automation_feasibility>HIGH|MEDIUM|LOW</automation_feasibility>
    </opportunity>
  </bulk_refactoring_opportunities>
</deviations>

<geographic_insights>
  <module path="{directory}">
    <dominant_pattern>{pattern_id}</dominant_pattern>
    <conformance>{X}%</conformance>
    <note>{If different from global dominant, explain why this might be acceptable}</note>
  </module>
  <!-- Note any module-specific conventions -->
</geographic_insights>

<evolution_analysis>
  <trend>
    {If able to determine, note if pattern usage is increasing/decreasing}
    {Check git history for newer files vs older files}
  </trend>
  <suggestions>
    {Any recommendations for evolving conventions}
  </suggestions>
</evolution_analysis>
</pattern_mining_report>
```

**Write report to memory**:

```bash
code-tools create_file \
  --file .claude/memory/pattern-analysis-$PATTERN_TYPE.md \
  --content @- \
  --add-last-line-newline <<EOF
# Pattern Mining Report: {pattern_type}

{Render pattern_mining_report XML as markdown}
EOF
```

### Phase 6: Auto-Update Coding Conventions

If dominance is strong (>80%), automatically update `coding-conventions.md`:

```bash
# Load existing conventions
code-tools read_file --path .claude/memory/coding-conventions.md > /tmp/current-conventions.md

# Check if section for this pattern type exists
if grep -q "## {Pattern Type}" /tmp/current-conventions.md; then
  # Section exists, update it
  # Use code-tools edit_file to replace section
else
  # Section doesn't exist, append it
  # Use code-tools edit_file to add new section
fi
```

**Convention Section Template**:

````markdown
## {Pattern Type} Convention

**Last Updated**: 2025-10-23 (auto-generated from pattern mining)

**Dominant Pattern**: {pattern_name} ({X}% conformance)

**Convention**: {Description of required pattern}

**Examples**:

```{language}
// ✅ Correct (dominant pattern)
{code example}

// ❌ Incorrect (deviation)
{code example of outlier pattern}
```
````

**Rationale**: {Why this pattern is preferred - based on analysis}

**Exceptions**: {Any acceptable deviations and when they're justified}

**Migration Status**: {X} deviations remain (see pattern-analysis-{type}.md)

```

## Anti-Hallucination Safeguards

**Evidence-Based Pattern Detection**: Every pattern claim MUST be backed by grep results with file:line references. No invented patterns.

**Quantitative Dominance**: Use exact counts and percentages. Do NOT claim "most code uses X" without numerical evidence.

**Source Citation**: Every code example MUST include file:line reference. Do NOT create synthetic examples.

**No Assumption of Uniformity**: Explicitly note if different modules have different conventions. Do NOT assume global patterns.

**Verify Grep Coverage**: Before finalizing, verify all relevant files were scanned. Note any excluded directories.

## Error Handling

**No Instances Found**:

```

If grep returns 0 results:

- Report: "No instances of {pattern_type} found in codebase"
- Recommendation: Either pattern not used OR detection regex needs refinement
- Do NOT fabricate patterns

```

**Insufficient Data**:

```

If total_instances < 10:

- Report: "Insufficient data for reliable pattern analysis"
- Recommendation: Manual review required
- Do NOT claim dominance with small sample

```

**Equal Distribution (No Dominant)**:

```

If all patterns <40% conformance:

- Report: "No clear dominant pattern"
- Recommendation: DOCUMENT_MULTIPLE acceptable patterns
- Note: Team should discuss and choose standard

```

**Coding Conventions Missing**:

```

If .claude/memory/coding-conventions.md not found:

- Create new file with pattern section
- Note: "Initial conventions generated from pattern mining"

```

## Supported Pattern Types

### 1. error-handling

**Detects**: catch blocks, throw statements, toast notifications, logging, error returns

**Categories**: toast-notification, console-error, throw-to-caller, structured-logging, return-error-object, silent-catch

### 2. state-management

**Detects**: useState, useContext, Redux, Zustand, Recoil patterns

**Categories**: local-useState, context-api, redux, zustand, recoil

### 3. api-design

**Detects**: REST endpoints, versioning, response formats, validation

**Categories**: rest-versioned, rest-unversioned, graphql, json-response, status-first

### 4. testing-patterns

**Detects**: Test files, frameworks, structure, mocking

**Categories**: jest, vitest, describe-it, test-only, file-colocated, file-separate

### 5. import-style

**Detects**: Import statement formats

**Categories**: named-imports, default-imports, namespace-imports, side-effect-imports

### 6. export-style

**Detects**: Export statement formats

**Categories**: named-exports, default-exports, re-exports

### 7. naming-conventions

**Detects**: Variable, function, class, file naming patterns

**Categories**: camelCase, PascalCase, snake_case, kebab-case, SCREAMING_SNAKE_CASE

### 8. styling-patterns

**Detects**: CSS-in-JS, CSS Modules, Tailwind, inline styles

**Categories**: styled-components, emotion, css-modules, tailwind, inline-styles

## Output

Generate comprehensive pattern analysis report in `.claude/memory/pattern-analysis-{type}.md` with:

- Frequency distribution (counts and percentages)
- Dominant pattern identification
- Deviation list (file:line references)
- Bulk refactoring opportunities
- Geographic insights (module-specific patterns)
- Auto-update coding-conventions.md if >80% dominance

**Success**: Pattern mining complete with quantitative analysis and convention recommendations generated.
```
