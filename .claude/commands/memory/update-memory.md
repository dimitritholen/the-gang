---
allowed-tools: Task, Bash(code-tools:*), Read, Write, Edit, Glob, Grep
argument-hint: [aspect]
description: Incrementally update memory artifacts after codebase changes without full regeneration
---

# Memory Update Command

**System date assertion**: Retrieve current system date before proceeding

Act as a memory management specialist with expertise in incremental analysis, change detection, and artifact preservation.

## Objective

Re-analyze specific aspects of the codebase after changes (new dependencies, refactoring, new features) and update corresponding memory artifacts with minimal disruption to unchanged sections. This is faster and more surgical than full memory regeneration.

## Usage

```
/update-memory "tech-stack"      # After adding/removing dependencies
/update-memory "conventions"     # After establishing new patterns or refactoring
/update-memory "architecture"    # After architectural changes or ADR additions
/update-memory "features"        # After adding/removing features
/update-memory "project-context" # After major project changes
/update-memory "all"             # Full refresh (rare, only when necessary)
```

## Task Decomposition

Break the update workflow into independent, parallelizable sub-tasks:

### Task 1: Argument Validation and Routing

**Sub-task 1.1: Parse and validate aspect argument**

Validate aspect argument against supported values:

- tech-stack
- conventions
- architecture
- features
- project-context
- all

If invalid, report error with supported options.

**Sub-task 1.2: Map aspect to artifact filename**

Mapping:

- tech-stack → tech-stack-baseline.md
- conventions → coding-conventions.md
- architecture → architecture-decisions.md
- features → feature-inventory.md
- project-context → project-context.md
- all → (process all aspects sequentially)

**Sub-task 1.3: Handle "all" aspect with sequential delegation**

If aspect is "all", sequentially invoke update for each individual aspect:
tech-stack, conventions, architecture, features, project-context

### Task 2: Load Existing Artifact and Validate Preconditions

**Sub-task 2.1: Check artifact existence**

Check if artifact file exists at `.claude/memory/{ARTIFACT_FILE}`.
If not found, report error and recommend running `/generate-memory` first.

**Sub-task 2.2: Load artifact for baseline comparison**

Use Read tool to load current artifact state from `.claude/memory/{ARTIFACT_FILE}` for diff generation.
Store content as baseline for comparison.

**Sub-task 2.3: Parse artifact structure**

Extract sections using markdown headers for granular comparison:

- Parse `##` and `###` headers as section identifiers
- Map to key-value structure: `{section_id: content_hash}`
- Store metadata: confidence levels, timestamps, evidence citations

### Task 3: Re-Analyze Specified Aspect

Delegate to codebase-archeologist agent with focused scope based on aspect type.

**Sub-task 3.1: Determine analysis scope**

For each aspect, define:

- **Analysis focus**: What to re-analyze (files, patterns, structure)
- **Preservation target**: What to keep unchanged (high-confidence items)
- **Expected changes**: What evidence to look for (dependency additions, refactorings)

**Sub-task 3.2: Invoke aspect-specific analysis**

#### For tech-stack

Use Task tool to invoke codebase-archeologist:

```
Perform incremental tech stack analysis for memory update.

**Scope**: Technology dependencies and stack baseline only

**Focus**:
- Package dependencies (detect dependency files: package.json, requirements.txt, go.mod, Cargo.toml, composer.json, etc.)
- Framework versions and configurations
- Database systems and versions
- External service integrations
- Build tools and CI/CD

**Comparison Context**:
Load existing tech-stack-baseline.md using Read tool:
{Paste old artifact content from baseline}

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
Load existing coding-conventions.md using Read tool:
{Paste old artifact content from baseline}

**Pattern Mining Integration**:
If pattern mining reports exist, use them:
- Use Glob tool to find pattern analysis files: pattern="pattern-analysis-*.md" in .claude/memory/
- Load pattern-analysis-*.md files using Read tool for quantitative data

**Output Requirements**:
1. Re-analyze patterns using Grep and Glob tools
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
Load existing architecture-decisions.md using Read tool:
{Paste old artifact content from baseline}

**Output Requirements**:
1. Re-analyze system architecture with fresh analysis
2. Identify new ADRs using Glob tool (check docs/, ADR directory, common ADR locations)
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
Load existing feature-inventory.md using Read tool:
{Paste old artifact content from baseline}

**Cross-Reference**:
Check for feature-specific artifacts using Glob tool:
- Search pattern: "requirements-*.md" in .claude/memory/
- Search pattern: "implementation-plan-*.md" in .claude/memory/
- Search pattern: "implementation-summary-*.md" in .claude/memory/

**Output Requirements**:
1. Re-scan codebase for feature modules using Glob tool
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
Load existing project-context.md using Read tool:
{Paste old artifact content from baseline}

**Output Requirements**:
1. Re-analyze project README, docs, and dependency file metadata using Read tool
2. Update technology stack summary if major changes
3. Refresh project structure if directory layout changed
4. Preserve project purpose unless pivoted
5. Note significant milestones (check for version tags or release notes)

**Change Detection**:
- Project description updates (README changes)
- Technology stack shifts (major framework change)
- Structure reorganization (directory refactoring)
- Maturity progression (alpha → beta → production)
```

**Sub-task 3.3: Store re-analysis output**

Store new analysis output for diff generation and comparison.

### Task 4: Generate Diff and Detect Changes

**Sub-task 4.1: Parse both artifacts into section structure**

For old and new artifacts:

1. Extract sections using regex: `^##\s+(.+)$` for level-2 headers, `^###\s+(.+)$` for level-3
2. Create hierarchical map: `{section_id: {content, confidence, citations}}`
3. Compute content hash for fast comparison

**Sub-task 4.2: Section-by-section comparison**

```
For each section in (old_sections ∪ new_sections):
  If old_hash == new_hash:
    Status: UNCHANGED
    Action: Preserve old version

  Elif section in new but not in old:
    Status: ADDED
    Action: Insert new section

  Elif section in old but not in new:
    Status: REMOVED
    Action: Remove section, note in changelog

  Elif old_hash != new_hash:
    Status: MODIFIED
    Action: Replace with new version

    If old_confidence == HIGH and new contradicts:
      Status: CONFLICT
      Action: Flag for manual review
```

**Sub-task 4.3: Calculate change metrics**

```xml
<change_metrics>
  <total_sections>{count}</total_sections>
  <unchanged>{count} ({percentage}%)</unchanged>
  <modified>{count} ({percentage}%)</modified>
  <added>{count} ({percentage}%)</added>
  <removed>{count} ({percentage}%)</removed>
  <conflicts>{count}</conflicts>

  <magnitude>
    <!-- MINOR: <10%, MODERATE: 10-30%, MAJOR: >30% -->
    {MINOR|MODERATE|MAJOR}
  </magnitude>
</change_metrics>
```

**Sub-task 4.4: Generate structured diff report**

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
      <old>{Old content or summary}</old>
      <new>{New content or summary}</new>
      <reason>{Inferred reason - e.g., "New dependency added: package X"}</reason>
      <confidence>HIGH|MEDIUM|LOW</confidence>
    </modified_section>

    <added_section id="{section_name}">
      <content>{New content}</content>
      <reason>{Why added}</reason>
      <confidence>HIGH|MEDIUM|LOW</confidence>
    </added_section>

    <removed_section id="{section_name}">
      <old_content>{Content removed}</old_content>
      <reason>{Why removed - e.g., "Dependency removed from dependency file"}</reason>
    </removed_section>
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
    <note>{X}% of artifact preserved from previous version</note>
  </preservation>
</diff_report>
```

### Task 5: Merge Updates with Preservation

**Sub-task 5.1: Apply merge algorithm**

```
For each section:
  If UNCHANGED:
    → Keep old version (preserve timestamps, metadata)

  If MODIFIED:
    → Replace with new version
    → Add changelog entry
    → Preserve sub-sections that are UNCHANGED

  If ADDED:
    → Insert new section in appropriate location
    → Mark as "New as of {date}"

  If REMOVED:
    → Remove from artifact
    → Note in changelog

  If CONFLICT:
    → Keep old version
    → Add warning comment: "<!-- CONFLICT: Manual review required -->"
    → Flag for manual review
```

**Sub-task 5.2: Construct updated artifact**

```markdown
# {Artifact Title}

**Last Generated**: {original_date}
**Last Updated**: 2025-10-24 (incremental update: {aspect})
**Update Trigger**: {Reason for update}
**Change Magnitude**: {MINOR|MODERATE|MAJOR}

---

## Changelog

### Update 2025-10-24 ({aspect})

**Changes**:

- **Modified**: {Section} - {Reason}
- **Added**: {Section} - {Reason}
- **Removed**: {Section} - {Reason}

**Preserved**: {X}% of artifact unchanged

---

{Artifact content with merged updates}

---

## Update History

| Date       | Aspect   | Magnitude | Changes                   |
| ---------- | -------- | --------- | ------------------------- |
| 2025-10-24 | {aspect} | {M/M/M}   | Mod:{n}, Add:{n}, Rem:{n} |
| {prev}     | {aspect} | ...       | ...                       |
```

**Sub-task 5.3: Write updated artifact**

Use Edit or Write tool to update artifact file at `.claude/memory/{ARTIFACT_FILE}` with:

1. Updated Last Updated timestamp
2. New changelog entry
3. Merged changed sections
4. Preserved unchanged sections
5. New update history row

### Task 6: Chain of Verification

Before finalizing, systematically verify the update:

**Verification Question 1**: Did I preserve unchanged sections correctly?

- Check: Verify no unintended modifications to UNCHANGED sections
- Check: Spot-check preserved content matches old artifact exactly
- Method: Hash comparison of UNCHANGED sections

**Verification Question 2**: Are all changes properly cited with evidence?

- Check: Each MODIFIED section has file:line references for new claims
- Check: No hallucinated changes - all derived from re-analysis
- Method: Cross-reference citations against codebase

**Verification Question 3**: Are confidence levels accurately assigned?

- Check: HIGH confidence only for direct evidence (file contents, dependency files)
- Check: MEDIUM confidence for inferred patterns
- Check: LOW confidence for speculative analysis

**Verification Question 4**: Are conflicts identified and flagged?

- Check: All high-confidence contradictions flagged as conflicts
- Check: Conflicts not auto-resolved - left for manual review
- Method: Review conflict detection output

**Verification Question 5**: Is changelog accurate and complete?

- Check: All MODIFIED/ADDED/REMOVED sections listed
- Check: Reasons provided for each change
- Method: Compare changelog against diff report

**Verification Question 6**: Is change magnitude correctly classified?

- Check: MINOR: <10% changed, MODERATE: 10-30% changed, MAJOR: >30% changed
- Method: Recalculate percentages

**Verification Question 7**: Is update history appended correctly?

- Check: New row added to Update History table
- Check: Row contains: date, aspect, magnitude, change counts

**Verification Question 8**: Did I avoid scope creep (only update specified aspect)?

- Check: If updating tech-stack, did NOT modify conventions section
- Check: Analysis stayed within aspect scope

**Corrective Actions**:

If any verification fails:

1. Identify root cause (parsing error, hallucination, scope drift)
2. Revert problematic changes
3. Re-run affected sub-task with corrected approach
4. Re-verify before finalizing

### Task 7: Handle Special Cases

**Sub-task 7.1: Handle 100% unchanged scenario**

```
If diff shows 0 changes:
  - Report: "No changes detected for {aspect}"
  - Update "Last Verified" timestamp (not "Last Updated")
  - Append to changelog: "Verified unchanged as of {date}"
  - Exit 0 (success, no-op)
```

**Sub-task 7.2: Handle re-analysis failure**

```
If codebase-archeologist returns error or empty analysis:
  - Preserve old artifact
  - Report: "Update failed - re-analysis error: {error_details}"
  - Do NOT create empty artifact
  - Exit 1 (failure)
```

**Sub-task 7.3: Handle major conflicts**

```
If >3 HIGH-confidence conflicts detected:
  - Block automatic update
  - Generate conflict report with evidence
  - Recommendation: "Manual review required before update"
  - List all conflicts with both versions
  - Exit 2 (requires manual intervention)
```

## Update Policies

### Preservation vs Overwrite Decision Matrix

| Scenario                                                          | Action    | Rationale                    |
| ----------------------------------------------------------------- | --------- | ---------------------------- |
| Section content identical (hash match)                            | PRESERVE  | No change detected           |
| Old HIGH confidence, new MEDIUM/LOW contradicts                   | FLAG      | Requires manual review       |
| Section out of scope for current aspect                           | PRESERVE  | Prevent scope creep          |
| Section changed with equal/higher confidence                      | OVERWRITE | New evidence supersedes      |
| Evidence shows clear change (e.g., dependency in dependency file) | OVERWRITE | Verifiable change            |
| List section with items added/removed                             | MERGE     | Combine old + new            |
| HIGH confidence old vs HIGH confidence new (different conclusion) | FLAG      | Conflict requires resolution |
| Significant change (>50% of section modified)                     | FLAG      | Review before overwriting    |

### Confidence Level Guidelines

**HIGH Confidence** (evidence-based, verifiable):

- Extracted from file contents (dependency files, README.md, source code)
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

1. **Evidence Required for Changes**: Every MODIFIED section must cite evidence (file:line or pattern analysis data). Do NOT claim changes without proof.

2. **Preserve When Uncertain**: If re-analysis is inconclusive, preserve old section. Do NOT guess or invent changes.

3. **No Scope Drift**: Only analyze and update specified aspect. Do NOT update unrelated sections "while we're at it".

4. **Cite Re-Analysis Method**: For each change, note how it was detected (e.g., "Grep tool found new dependency", "dependency file line 45 added").

5. **Conflict Transparency**: If old and new contradict, do NOT silently overwrite. Flag conflict with both versions.

## Output

Generate updated memory artifact in `.claude/memory/{artifact_file}` with:

- Preserved unchanged sections (minimize disruption)
- Updated changed sections (with evidence)
- Changelog entry (what changed and why)
- Conflict flags (if high-confidence contradictions)
- Update history row (tracking evolution)
- Change magnitude classification (MINOR/MODERATE/MAJOR)

**Success**: Memory artifact incrementally updated with surgical precision, preserving institutional knowledge while incorporating fresh analysis.
