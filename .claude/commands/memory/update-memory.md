---
allowed-tools: Task, Bash(code-tools:*), Read, Write, Edit, Glob, Grep
argument-hint: [aspect]
description: Incrementally update memory artifacts after codebase changes without full regeneration
---

# Memory Update Command

**System date assertion**: Retrieve current system date via `date +%Y-%m-%d` before proceeding

Act as a memory management specialist with expertise in incremental analysis, change detection, and artifact preservation.

## Objective

Re-analyze specific aspects of the codebase after changes (new dependencies, refactoring, new features) and update corresponding memory artifacts with minimal disruption to unchanged sections. This is faster and more surgical than full memory regeneration.

## Usage

```bash
/update-memory "tech-stack"      # After adding/removing dependencies
/update-memory "conventions"     # After establishing new patterns or refactoring
/update-memory "architecture"    # After architectural changes or ADR additions
/update-memory "features"        # After adding/removing features
/update-memory "project-context" # After major project changes
/update-memory "all"             # Full refresh (rare, only when necessary)
```

## Argument Parsing and Validation

```bash
# Extract aspect from arguments
ASPECT="$ARGUMENTS"

# Validate aspect
case "$ASPECT" in
  tech-stack|conventions|architecture|features|project-context|all)
    # Valid aspect
    ;;
  *)
    echo "Error: Unknown aspect '$ASPECT'"
    echo "Supported aspects: tech-stack, conventions, architecture, features, project-context, all"
    exit 1
    ;;
esac

# Map aspect to artifact filename
case "$ASPECT" in
  tech-stack)
    ARTIFACT_FILE="tech-stack-baseline.md"
    ;;
  conventions)
    ARTIFACT_FILE="coding-conventions.md"
    ;;
  architecture)
    ARTIFACT_FILE="architecture-decisions.md"
    ;;
  features)
    ARTIFACT_FILE="feature-inventory.md"
    ;;
  project-context)
    ARTIFACT_FILE="project-context.md"
    ;;
  all)
    # Update all artifacts sequentially
    ARTIFACT_FILE=""
    ;;
esac
```

## Methodology

### Phase 1: Load Existing Artifact

Retrieve current artifact for baseline comparison:

```bash
# Load existing artifact
if [ "$ASPECT" != "all" ]; then
  if [ -f ".claude/memory/$ARTIFACT_FILE" ]; then
    code-tools read_file --path .claude/memory/$ARTIFACT_FILE > /tmp/old-artifact.md
  else
    echo "Warning: $ARTIFACT_FILE does not exist. Creating new artifact instead of updating."
    echo "Recommendation: Run /generate-memory instead for initial creation."
    exit 1
  fi
fi
```

### Phase 2: Chain-of-Thought Update Strategy

Reason through the update approach before re-analyzing:

```xml
<update_reasoning>
<aspect_scope>
**Aspect Being Updated**: {tech-stack | conventions | architecture | features | project-context}

**Artifact File**: {filename.md}

**Update Triggers** (Why this update is needed):
- {Change 1}: {New dependency added, refactoring completed, feature shipped, etc.}
- {Change 2}: {Reason}

**Analysis Scope**:
- {What to re-analyze}: {Specific directories, file types, patterns}
- {What to preserve}: {Sections unlikely to have changed}
- {Expected changes}: {What we expect to find different}
</aspect_scope>

<preservation_strategy>
**Sections to Preserve**:
- {Section}: {Reason - unlikely to change frequently}

**Sections to Re-Analyze**:
- {Section}: {Reason - likely changed based on trigger}

**Merge Strategy**:
- If section unchanged: Keep old version (preserve timestamps, confidence levels)
- If section changed: Replace with new analysis, note change in changelog
- If section partially changed: Merge updates, preserve unchanged subsections
</preservation_strategy>

<change_detection_approach>
**Comparison Method**:
1. Generate new analysis for specified aspect
2. Parse both old and new into structured sections
3. Compare section-by-section (content hash or semantic diff)
4. Identify added, removed, modified sections
5. Calculate change percentage for confidence

**Confidence Handling**:
- Preserve HIGH confidence items unless contradicted
- Update LOW/MEDIUM confidence items with new evidence
- Flag conflicts (old HIGH confidence vs new contradictory finding)
</change_detection_approach>
</update_reasoning>
```

### Phase 3: Re-Analyze Specific Aspect

Delegate to codebase-archeologist agent with focused scope:

#### For tech-stack

```bash
# Invoke codebase-archeologist with tech-stack focus
```

**Agent Invocation**:

Use Task tool to invoke codebase-archeologist agent:

```
Perform incremental tech stack analysis for memory update.

**Scope**: Technology dependencies and stack baseline only

**Focus**:
- Package dependencies (package.json, requirements.txt, go.mod, etc.)
- Framework versions and configurations
- Database systems and versions
- External service integrations
- Build tools and CI/CD

**Comparison Context**:
Load existing tech-stack-baseline.md:
{Paste old artifact content}

**Output Requirements**:
1. Generate fresh tech stack analysis using same structure as existing artifact
2. Note all changes with HIGH/MEDIUM/LOW confidence levels
3. Cite evidence (file:line) for all findings
4. Do NOT analyze project context, conventions, or architecture (out of scope)

**Change Detection**:
Explicitly note:
- New dependencies added (with version and purpose)
- Dependencies removed (with reason if inferable)
- Version upgrades/downgrades (with old → new)
- Configuration changes (with impact)
- Unchanged dependencies (keep existing analysis)
```

#### For conventions

```bash
# Invoke codebase-archeologist with conventions focus
```

**Agent Invocation**:

```
Perform incremental coding conventions analysis for memory update.

**Scope**: Coding standards and patterns only

**Focus**:
- File naming and organization
- Code style and formatting
- Error handling patterns
- Testing conventions
- Documentation standards
- Import/export styles

**Comparison Context**:
Load existing coding-conventions.md:
{Paste old artifact content}

**Pattern Mining Integration**:
If pattern mining reports exist, use them:
- code-tools list_dir --path .claude/memory --depth 1 | grep "pattern-analysis"
- Load pattern-analysis-*.md files for quantitative data

**Output Requirements**:
1. Re-analyze patterns with fresh grep/glob searches
2. Update percentages if conformance changed
3. Note new patterns detected
4. Preserve convention text unless dominant pattern shifted
5. Cite evidence for all pattern claims

**Change Detection**:
- New conventions established (after refactoring)
- Pattern dominance shifts (e.g., 60% → 75% conformance)
- Deprecated patterns (usage dropped)
- Unchanged conventions (preserve)
```

#### For architecture

```bash
# Invoke codebase-archeologist with architecture focus
```

**Agent Invocation**:

```
Perform incremental architecture analysis for memory update.

**Scope**: Architectural decisions and system design only

**Focus**:
- ADRs (Architecture Decision Records)
- System architecture (layers, modules, services)
- Data flow and integration points
- Design patterns in use
- Architectural constraints

**Comparison Context**:
Load existing architecture-decisions.md:
{Paste old artifact content}

**Output Requirements**:
1. Re-analyze system architecture with fresh analysis
2. Identify new ADRs (check docs/ or ADR directory)
3. Detect refactoring that changes architecture
4. Preserve existing ADRs unless superseded
5. Note architectural evolution (old → new)

**Change Detection**:
- New ADRs documented
- Architecture refactored (e.g., monolith → microservices)
- Integration points added/removed
- Design patterns adopted/deprecated
```

#### For features

```bash
# Invoke codebase-archeologist with features focus
```

**Agent Invocation**:

```
Perform incremental feature inventory analysis for memory update.

**Scope**: Feature catalog and capabilities only

**Focus**:
- Feature modules and components
- User-facing capabilities
- API endpoints and functionality
- Feature flags and toggles
- Completed vs in-progress features

**Comparison Context**:
Load existing feature-inventory.md:
{Paste old artifact content}

**Cross-Reference**:
Check for feature-specific artifacts:
- code-tools list_dir --path .claude/memory --depth 1 | grep -E "requirements-|implementation-plan-|implementation-summary-"

**Output Requirements**:
1. Re-scan codebase for feature modules
2. Add new features completed since last update
3. Mark deprecated/removed features
4. Update feature status (in-progress → complete)
5. Preserve feature descriptions unless changed

**Change Detection**:
- New features added (with evidence)
- Features removed (with evidence)
- Feature status changes
- Feature metadata updates (owner, priority)
```

#### For project-context

```bash
# Invoke codebase-archeologist with project-context focus
```

**Agent Invocation**:

```
Perform incremental project context analysis for memory update.

**Scope**: Project overview and metadata only

**Focus**:
- Project purpose and description
- Technology stack summary (high-level)
- Project structure and organization
- Team and ownership info (if inferable)
- Project maturity and status

**Comparison Context**:
Load existing project-context.md:
{Paste old artifact content}

**Output Requirements**:
1. Re-analyze project README, docs, package.json metadata
2. Update technology stack summary if major changes
3. Refresh project structure if directory layout changed
4. Preserve project purpose unless pivoted
5. Note significant milestones (if git tags or releases)

**Change Detection**:
- Project description updates (README changes)
- Technology stack shifts (major framework change)
- Structure reorganization (directory refactoring)
- Maturity progression (alpha → beta → production)
```

#### For all

```bash
# Update all artifacts sequentially
for CURRENT_ASPECT in tech-stack conventions architecture features project-context; do
  /update-memory "$CURRENT_ASPECT"
done
```

### Phase 4: Diff Generation and Change Detection

After re-analysis, compare old vs new:

```xml
<diff_analysis>
<parsing>
**Parse Old Artifact**:
- Extract sections (e.g., ## Headers, ### Subheaders)
- Map to key-value structure: {section_id: content}

**Parse New Artifact**:
- Extract same section structure
- Map to key-value structure

**Section-by-Section Comparison**:
For each section:
  - If old_content == new_content → UNCHANGED
  - If old_content != new_content → MODIFIED
  - If section exists in new but not old → ADDED
  - If section exists in old but not new → REMOVED
</parsing>

<change_classification>
**Calculate Change Metrics**:
- Total sections: {count}
- Unchanged: {count} ({percentage}%)
- Modified: {count} ({percentage}%)
- Added: {count} ({percentage}%)
- Removed: {count} ({percentage}%)

**Overall Change Magnitude**: {MINOR|MODERATE|MAJOR}
- MINOR: <10% sections changed
- MODERATE: 10-30% sections changed
- MAJOR: >30% sections changed
</change_classification>

<conflict_detection>
**High-Confidence Conflicts**:
If old section had HIGH confidence and new section contradicts:
  - Flag as potential conflict
  - Require manual review before overwriting
  - Present both versions with evidence

**Example**:
Old (HIGH confidence): "Primary database: PostgreSQL 14 (package.json:45)"
New (MEDIUM confidence): "Primary database: MySQL 8"
→ CONFLICT: Verify before updating
</conflict_detection>
</diff_analysis>
```

**Generate Diff Report**:

```xml
<diff_report>
<summary>
  <artifact>{filename.md}</artifact>
  <change_magnitude>MINOR|MODERATE|MAJOR</change_magnitude>
  <sections_total>{count}</sections_total>
  <sections_unchanged>{count}</sections_unchanged>
  <sections_modified>{count}</sections_modified>
  <sections_added>{count}</sections_added>
  <sections_removed>{count}</sections_removed>
</summary>

<changes>
  <modified_section id="{section_name}">
    <old>
{Old content or summary}
    </old>
    <new>
{New content or summary}
    </new>
    <reason>
{Inferred reason for change - e.g., "New dependency added: package X"}
    </reason>
    <confidence>HIGH|MEDIUM|LOW</confidence>
  </modified_section>

  <added_section id="{section_name}">
    <content>{New content}</content>
    <reason>{Why added}</reason>
    <confidence>HIGH|MEDIUM|LOW</confidence>
  </added_section>

  <removed_section id="{section_name}">
    <old_content>{Content removed}</old_content>
    <reason>{Why removed - e.g., "Dependency removed from package.json"}</reason>
  </removed_section>

  <!-- List all changes -->
</changes>

<conflicts>
  <conflict id="CONF-001">
    <section>{section_name}</section>
    <old_value>{Value with HIGH confidence}</old_value>
    <new_value>{Contradictory value}</new_value>
    <recommendation>MANUAL_REVIEW</recommendation>
  </conflict>
</conflicts>

<preservation>
  <unchanged_count>{count}</unchanged_count>
  <note>
{X}% of artifact preserved from previous version. Only changed sections updated.
  </note>
</preservation>
</diff_report>
```

### Phase 5: Merge Updates with Preservation

Create updated artifact merging old + new:

**Merge Algorithm**:

```
For each section in (old_sections ∪ new_sections):
  If section UNCHANGED:
    → Keep old version (preserve timestamps, metadata)

  If section MODIFIED:
    → Replace with new version
    → Add changelog entry

  If section ADDED:
    → Insert new section in appropriate location
    → Mark as "New as of {date}"

  If section REMOVED:
    → Remove from artifact
    → Note in changelog

  If section CONFLICT:
    → Keep old version
    → Add warning comment
    → Flag for manual review
```

**Updated Artifact Structure**:

```markdown
# {Artifact Title}

**Last Generated**: {original_date}
**Last Updated**: 2025-10-23 (incremental update: {aspect})
**Update Trigger**: {Reason for update}
**Change Magnitude**: {MINOR|MODERATE|MAJOR}

---

## Changelog

### Update 2025-10-23 ({aspect})

**Changes**:

- **Modified**: {Section} - {Reason}
- **Added**: {Section} - {Reason}
- **Removed**: {Section} - {Reason}

**Preserved**: {X}% of artifact unchanged

---

{Artifact content with merged updates}

---

## Update History

| Date            | Aspect   | Magnitude              | Changes                                                   |
| --------------- | -------- | ---------------------- | --------------------------------------------------------- |
| 2025-10-23      | {aspect} | {MINOR/MODERATE/MAJOR} | {Modified}: {count}, {Added}: {count}, {Removed}: {count} |
| {previous_date} | {aspect} | ...                    | ...                                                       |
```

**Write Updated Artifact**:

```bash
code-tools edit_file \
  --file .claude/memory/$ARTIFACT_FILE \
  --patch @- <<EOF
{Generate patch that:
1. Updates Last Updated timestamp
2. Adds changelog entry
3. Merges changed sections
4. Preserves unchanged sections
5. Adds update history row}
EOF
```

### Phase 6: Chain-of-Verification

Validate update before finalizing:

```xml
<verification_checklist>
<question>Did I preserve unchanged sections correctly?</question>
<check>Verify no unintended modifications to UNCHANGED sections</check>
<check>Spot-check preserved content matches old artifact exactly</check>

<question>Are all changes properly cited with evidence?</question>
<check>Each MODIFIED section has file:line references for new claims</check>
<check>No hallucinated changes - all derived from re-analysis</check>

<question>Are confidence levels accurately assigned?</question>
<check>HIGH confidence only for direct evidence (file contents, package.json)</check>
<check>MEDIUM confidence for inferred patterns</check>
<check>LOW confidence for speculative analysis</check>

<question>Are conflicts identified and flagged?</question>
<check>All high-confidence contradictions flagged as conflicts</check>
<check>Conflicts not auto-resolved - left for manual review</check>

<question>Is changelog accurate and complete?</question>
<check>All MODIFIED/ADDED/REMOVED sections listed</check>
<check>Reasons provided for each change</check>

<question>Is change magnitude correctly classified?</question>
<check>MINOR: <10% changed</check>
<check>MODERATE: 10-30% changed</check>
<check>MAJOR: >30% changed</check>

<question>Is update history appended correctly?</question>
<check>New row added to Update History table</check>
<check>Row contains: date, aspect, magnitude, change counts</check>

<question>Did I avoid scope creep (only update specified aspect)?</question>
<check>If updating tech-stack, did NOT modify conventions section</check>
<check>Analysis stayed within aspect scope</check>
</verification_checklist>
```

## Update Policies

### When to Preserve vs Overwrite

**PRESERVE (keep old version)**:

- Section content is identical between old and new analysis
- Old section has HIGH confidence and new contradicts with MEDIUM/LOW (flag conflict)
- Section is out of scope for current update aspect

**OVERWRITE (replace with new)**:

- Section content changed (verified by re-analysis)
- New analysis has equal or higher confidence level
- Evidence shows clear change (e.g., dependency added to package.json)

**MERGE (combine old + new)**:

- Section has subsections where some changed, some didn't
- List-type sections (e.g., dependency list) where items were added/removed

**FLAG (manual review)**:

- HIGH confidence old vs HIGH confidence new with different conclusions
- Significant change (>50% of section modified)
- Suspicious change (contradicts recent updates)

### Confidence Level Guidelines

**HIGH Confidence** (evidence-based, verifiable):

- Extracted from file contents (package.json, README.md, source code)
- Direct observation (file exists, function defined, import present)
- Quantitative data (X% conformance from pattern mining)

**MEDIUM Confidence** (inferred, likely):

- Pattern dominance from code samples (not exhaustive)
- Inferred architecture from structure (not documented)
- Naming conventions from file analysis (not style guide)

**LOW Confidence** (speculative, uncertain):

- Inferred purpose from context
- Guessed rationale for decisions
- Uncertain pattern classification

## Anti-Hallucination Safeguards

**Evidence Required for Changes**: Every MODIFIED section must cite evidence (file:line or pattern analysis data). Do NOT claim changes without proof.

**Preserve When Uncertain**: If re-analysis is inconclusive, preserve old section. Do NOT guess or invent changes.

**No Scope Drift**: Only analyze and update specified aspect. Do NOT update unrelated sections "while we're at it".

**Cite Re-Analysis Method**: For each change, note how it was detected (e.g., "grep found new dependency", "package.json line 45 added").

**Conflict Transparency**: If old and new contradict, do NOT silently overwrite. Flag conflict with both versions.

## Error Handling

**Artifact Not Found**:

```
If .claude/memory/{artifact_file} does not exist:
  - Error: "Cannot update non-existent artifact"
  - Recommendation: "/generate-memory first to create initial artifacts"
  - Exit 1
```

**Re-Analysis Fails**:

```
If codebase-archeologist returns error or empty analysis:
  - Preserve old artifact
  - Report: "Update failed - re-analysis error"
  - Do NOT create empty artifact
```

**100% Unchanged**:

```
If diff shows 0 changes:
  - Report: "No changes detected for {aspect}"
  - Update "Last Verified" timestamp but not "Last Updated"
  - Append to changelog: "Verified unchanged as of {date}"
  - Exit 0 (success, no-op)
```

**Major Conflicts**:

```
If >3 HIGH-confidence conflicts detected:
  - Block automatic update
  - Generate conflict report
  - Recommendation: "Manual review required before update"
  - List all conflicts with evidence
```

## Output

Generate updated memory artifact in `.claude/memory/{artifact_file}` with:

- Preserved unchanged sections (minimize disruption)
- Updated changed sections (with evidence)
- Changelog entry (what changed and why)
- Conflict flags (if high-confidence contradictions)
- Update history row (tracking evolution)
- Change magnitude classification (MINOR/MODERATE/MAJOR)

**Success**: Memory artifact incrementally updated with surgical precision, preserving institutional knowledge while incorporating fresh analysis.
