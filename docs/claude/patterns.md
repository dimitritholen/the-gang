# Advanced Patterns & Workflows

**Navigation**: [← Hooks](./hooks.md) | [Index](./index.md) | [Templates →](./templates.md)

**Related Documentation**: [commands.md](./commands.md) for command patterns | [agents.md](./agents.md) for agent coordination | [hooks.md](./hooks.md) for event integration

---

## Overview

This document covers advanced patterns for orchestrating complex workflows, coordinating multiple agents, and optimizing performance across Claude Code components.

---

## Decision Trees

### When to Create What

Use these decision trees to determine the right component type for your needs.

```
USER REQUIREMENT ANALYSIS:
│
├─ Need: Repeatable action with specific arguments
│  ├─ Involves: Bash commands or file operations
│  ├─ Requires: User confirmation or input validation
│  └─ Result: Standardized project-specific operations
│  → CREATE SLASH COMMAND
│     └─ Read: commands.md
│
├─ Need: Specialized expertise or domain knowledge
│  ├─ Involves: Complex multi-step reasoning
│  ├─ Requires: Different tool access patterns
│  └─ Result: Focused, context-specific assistance
│  → CREATE SUB-AGENT
│     └─ Read: agents.md
│
├─ Need: Validate or modify tool usage
│  ├─ Involves: Automatic pre/post-processing
│  ├─ Requires: Security validation
│  └─ Result: Integration between components
│  → CREATE HOOK
│     └─ Read: hooks.md
│
└─ Need: Complex multi-component workflow
   ├─ Involves: Multiple agents or commands
   ├─ Requires: Orchestration and coordination
   └─ Result: End-to-end automated workflow
   → CREATE WORKFLOW PATTERN
      └─ Read: This document
```

### Component Selection Guide

**Single Task Analysis**:

```
Task Type?
│
├─ Simple, repeatable, user-triggered
│  → Slash Command
│     Example: /commit, /deploy, /test
│
├─ Complex reasoning, specialized domain
│  → Sub-Agent
│     Example: Security auditor, architect, researcher
│
├─ Validation, automation, security
│  → Hook
│     Example: Validate inputs, format code, check security
│
└─ Multi-stage, coordinated, complex
   → Workflow Pattern
      Example: Feature development, code review pipeline
```

---

## File Locations

Understanding where components live and their scope.

```
Project Level (.claude/):
├── commands/          # Project-specific slash commands
│   ├── commit.md      # Custom commit workflow
│   ├── deploy.md      # Deployment automation
│   └── generate.md    # Code generation
│
├── agents/            # Project domain specialists
│   ├── architect.md   # System architecture expert
│   ├── reviewer.md    # Code review specialist
│   └── tester.md      # Testing expert
│
└── settings.json      # Project hooks configuration
    └── hooks:
        ├── PreToolUse   # Validation hooks
        └── PostToolUse  # Automation hooks

User Level (~/.claude/):
├── commands/          # Personal productivity commands
│   ├── note.md        # Personal note taking
│   └── search.md      # Custom search helpers
│
└── agents/            # Personal assistant agents
    ├── writer.md      # Writing assistance
    └── research.md    # Research helper
```

**Scope Decision**:

- **Project level**: Team-shared, project-specific, version-controlled
- **User level**: Personal productivity, cross-project tools, private workflows

---

## Multi-Agent Workflows

### Research Lead + Subagent Pattern

Coordinate complex research by breaking into focused sub-topics.

**Research Lead Agent**: `.claude/agents/research-lead.md`

```markdown
---
name: research-lead
description: Coordinate complex research projects with multiple sub-topics
tools: Task, WebSearch, Read
model: opus
---

<role_definition>
You are a research coordinator who breaks down complex research questions
into focused sub-topics and delegates to specialized research subagents.
</role_definition>

<coordination_strategy>
For complex research tasks:

1. **Decompose** - Break question into focused sub-topics
   - Identify distinct areas requiring investigation
   - Determine dependencies between topics
   - Prioritize by importance and dependency order

2. **Delegate** - Create specialized subagents for each area
   - Use Task tool to create research-specialist subagents
   - Provide focused instructions per sub-topic
   - Include context, constraints, and expected format
   - Specify reliable source recommendations

3. **Monitor** - Track progress and adjust as needed
   - Review subagent findings as they complete
   - Identify gaps or inconsistencies
   - Create additional subagents if needed

4. **Synthesize** - Combine findings into comprehensive report
   - Integrate findings across all sub-topics
   - Resolve conflicts or contradictions
   - Provide unified recommendations
   - Cite sources comprehensively
</coordination_strategy>

<subagent_creation>
When creating research subagents, provide:
- **Specific objective**: Narrow, focused research question
- **Expected output format**: Structure for findings
- **Context**: Why this matters, how it fits larger question
- **Constraints**: Time bounds, source preferences, depth level
- **Success criteria**: What makes answer complete
</subagent_creation>

<example_delegation>
For question: "Evaluate React state management solutions"

Create subagents for:
1. Context API patterns and limitations
2. Redux ecosystem and best practices
3. Zustand, Jotai, and lightweight alternatives
4. Performance comparison and benchmarks
5. Migration strategies and compatibility

Each subagent receives focused instructions and reports back
specific findings in defined format.
</example_delegation>
```

**Usage**:
```
User: Research best practices for implementing microservices authentication

Research Lead Agent:
1. Creates subagents for:
   - OAuth2/OIDC implementation patterns
   - JWT vs session tokens analysis
   - API gateway authentication strategies
   - Service-to-service auth (mTLS, service mesh)
   - Security best practices and compliance

2. Each subagent researches focused area

3. Lead synthesizes into comprehensive guide
```

### Code Review Pipeline

Multi-stage review with specialized agents.

**Review Orchestrator**: `.claude/commands/review.md`

```markdown
---
allowed-tools: Task, Read, Grep
argument-hint: [branch-or-pr]
description: Comprehensive multi-stage code review
---

<review_pipeline>
Execute comprehensive code review in stages:

1. **Security Review** (security-reviewer agent)
   - Vulnerability scanning
   - Authentication/authorization checks
   - Data protection validation
   - Dependency security audit

2. **Performance Review** (performance-reviewer agent)
   - Algorithmic complexity analysis
   - Memory usage patterns
   - Database query optimization
   - Bundle size impact

3. **Style Review** (style-reviewer agent)
   - Code style consistency
   - Documentation quality
   - Naming conventions
   - Maintainability patterns

4. **Architecture Review** (architecture-reviewer agent)
   - Design pattern compliance
   - Component coupling
   - Abstraction appropriateness
   - Technical debt assessment
</review_pipeline>

<execution>
For each stage:
1. Create specialized reviewer subagent
2. Provide code diff and context
3. Collect findings in structured format
4. Aggregate results with severity levels
5. Provide unified review summary
</execution>

Review target: $ARGUMENTS
```

**Security Reviewer**: `.claude/agents/security-reviewer.md`

```markdown
---
name: security-reviewer
description: Security-focused code review for vulnerabilities
tools: Read, Grep, Bash
model: opus
---

Focus exclusively on security vulnerabilities, authentication flaws,
and data protection issues.

<review_checklist>
- SQL injection risks
- XSS vulnerabilities
- CSRF protection
- Authentication bypasses
- Authorization flaws
- Credential exposure
- Dependency vulnerabilities
- Cryptographic weaknesses
- Input validation gaps
- Output encoding issues
</review_checklist>

Provide findings with:
- Severity (Critical/High/Medium/Low)
- Location (file:line)
- Description of vulnerability
- Exploitation scenario
- Remediation steps
```

**Performance Reviewer**: `.claude/agents/performance-reviewer.md`

```markdown
---
name: performance-reviewer
description: Performance and optimization review
tools: Read, Grep, Bash
model: sonnet
---

Analyze performance bottlenecks, memory usage, and optimization opportunities.

<review_focus>
- Algorithmic complexity (O(n), O(n²), etc.)
- Unnecessary re-renders (React)
- Memory leaks
- Database N+1 queries
- Inefficient data structures
- Missing caching opportunities
- Bundle size impact
- Network request optimization
</review_focus>

Provide findings with:
- Impact level (High/Medium/Low)
- Location (file:line)
- Performance issue description
- Expected impact on user experience
- Optimization suggestions with code examples
```

**Style Reviewer**: `.claude/agents/style-reviewer.md`

```markdown
---
name: style-reviewer
description: Code style and maintainability review
tools: Read, Grep
model: haiku
---

Check coding standards, documentation quality, and maintainability patterns.

<review_checklist>
- Naming conventions (camelCase, PascalCase, kebab-case)
- Code organization and structure
- Comment quality and JSDoc completeness
- Magic numbers and hard-coded values
- Function length and complexity
- Import organization
- Consistent error handling
- Test coverage patterns
</review_checklist>

Provide findings as suggestions, not requirements.
Focus on maintainability improvements.
```

---

## Workflow Orchestration

### Command + Agent Workflow

Orchestrate complete feature development.

**Feature Command**: `.claude/commands/feature.md`

```markdown
---
allowed-tools: Task
argument-hint: [feature-description]
description: Complete feature development workflow
---

<workflow>
Implement complete feature from design to deployment:

1. **Architecture Design** (architect-agent)
   - Analyze requirements from description
   - Design system architecture
   - Define component boundaries
   - Plan data models and APIs
   - Provide implementation roadmap

2. **Implementation** (developer-agent)
   - Follow architecture design
   - Implement feature components
   - Write unit tests
   - Handle error cases
   - Follow project conventions

3. **Testing** (test-agent)
   - Create integration tests
   - Add e2e test coverage
   - Verify error handling
   - Test edge cases
   - Performance validation

4. **Review** (review-agent)
   - Validate implementation against design
   - Check code quality
   - Security review
   - Suggest improvements

5. **Documentation** (docs-agent)
   - API documentation
   - Usage examples
   - Architecture decision records
   - Update README if needed
</workflow>

<execution>
Each stage:
- Creates appropriate subagent with Task tool
- Provides context from previous stages
- Validates output before proceeding
- Accumulates artifacts for next stage
- Provides progress updates to user
</execution>

Implement feature: $ARGUMENTS
```

### Progressive Enhancement

Incrementally improve codebase systematically.

**Progressive Enhancer**: `.claude/agents/progressive-enhancer.md`

```markdown
---
name: progressive-enhancer
description: Incrementally improve codebase quality
tools: Read, Write, Edit, Task, Grep, Glob
model: sonnet
---

<role_definition>
You systematically improve codebase quality through incremental,
validated enhancements. Each improvement is independent and testable.
</role_definition>

<enhancement_strategy>
Incremental Improvement Process:

1. **Analyze** - Current code quality and patterns
   - Scan codebase for improvement opportunities
   - Identify patterns and anti-patterns
   - Assess technical debt
   - Prioritize by impact/effort ratio

2. **Prioritize** - Improvements by impact and effort
   Scoring matrix:
   - High Impact, Low Effort → Do first
   - High Impact, High Effort → Plan carefully
   - Low Impact, Low Effort → Quick wins
   - Low Impact, High Effort → Skip

3. **Implement** - Changes incrementally
   - One improvement at a time
   - Complete implementation including tests
   - Validate functionality unchanged
   - Commit with clear description

4. **Validate** - Each improvement independently
   - Run test suite
   - Verify no regressions
   - Check performance impact
   - Review with user

5. **Document** - Changes and rationale
   - Why change was made
   - What was improved
   - Any trade-offs accepted
   - Future improvement opportunities
</enhancement_strategy>

<improvement_categories>
Focus areas:
- Type safety improvements (add TypeScript types)
- Error handling (add try-catch, validation)
- Code duplication (extract shared logic)
- Performance optimization (memoization, caching)
- Accessibility improvements (ARIA, semantic HTML)
- Test coverage (add missing tests)
- Documentation (JSDoc, comments)
</improvement_categories>

<safety_rules>
Never:
- Change multiple unrelated things at once
- Break existing functionality
- Skip validation steps
- Assume improvements without measuring
- Ignore user feedback
</safety_rules>
```

---

## Performance Optimization

### Parallel Tool Execution

Maximize efficiency by running independent operations concurrently.

**Pattern**: Multiple file reads

```markdown
<efficiency>
When gathering information from multiple sources:

INEFFICIENT (Sequential):
1. Read file1.ts
2. Wait for result
3. Read file2.ts
4. Wait for result
5. Read file3.ts
6. Wait for result

EFFICIENT (Parallel):
1. Issue Read(file1.ts), Read(file2.ts), Read(file3.ts) simultaneously
2. Receive all results together
3. Process combined information

Parallel execution reduces total time from 3x to 1x.
</efficiency>

<implementation>
Use Task tool to run multiple agents in parallel:
- Create all subagents in single response
- Each works independently
- Results collected when all complete
- No dependencies between agents
</implementation>

<when_to_parallelize>
Safe for parallel execution:
- Reading different files
- Independent web searches
- Multiple agent analysis of same code
- Non-conflicting file operations

Must be sequential:
- Operations with dependencies
- File write followed by read
- Command execution with state changes
- User confirmation in workflow
</when_to_parallelize>
```

### Context Management

Minimize token usage while maintaining effectiveness.

**Optimization Techniques**:

```markdown
<context_optimization>

1. **Limit Tool Output**
   - Use Grep instead of reading entire files
   - Specify line ranges for large files
   - Filter results at source

2. **Specific Queries**
   - Precise grep patterns vs broad searches
   - Targeted file paths vs recursive globs
   - Specific function/class searches

3. **Focused Instructions**
   - Provide only relevant context to subagents
   - Define clear scope boundaries
   - Specify expected output format
   - Limit to necessary information

4. **Efficient Tool Selection**
   - Grep for finding content location
   - Read for viewing specific content
   - Glob for finding files by pattern
   - Task for delegation, not simple operations

5. **Incremental Processing**
   - Process in chunks if needed
   - Stream results rather than bulk load
   - Cache frequently accessed data
   - Reuse analysis between operations
</context_optimization>

<anti_patterns>
Avoid:
- Reading entire codebase at once
- Unnecessary file reads for validation
- Redundant searches for same information
- Creating subagents for trivial tasks
- Including irrelevant context in agent prompts
</anti_patterns>
```

---

## Integration Patterns

### Command Invokes Agent

Command delegates complex work to specialized agent.

```markdown
# Command: /analyze [file-or-directory]
---
allowed-tools: Task, Read
argument-hint: [file-or-directory]
description: Comprehensive code analysis
---

<workflow>
1. Determine scope from $ARGUMENTS
2. Create analyzer-agent with Task tool
3. Provide file/directory path and context
4. Receive detailed analysis report
5. Format and present results to user
</workflow>

Analyze: $ARGUMENTS

Delegate to analyzer-agent for deep analysis.
```

### Agent Coordinates Multiple Agents

High-level agent orchestrates specialized agents.

```markdown
# Agent: feature-architect
---
name: feature-architect
description: Design and coordinate feature implementation
tools: Task
model: opus
---

<orchestration>
For complex features:
1. Break down into implementation domains
2. Create specialized agents per domain:
   - backend-architect for server components
   - frontend-architect for UI components
   - database-architect for data models
   - test-architect for testing strategy
3. Coordinate between agents
4. Synthesize complete feature design
</orchestration>
```

### Hook Enhances Command/Agent

Hook provides automatic enhancement without code changes.

```markdown
# Command: /write [file] [content]
---
allowed-tools: Write
---
Write file with content...

# Hook: Auto-format after write
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write.*\\.(ts|js)$",
      "hooks": [
        {"type": "command", "command": "prettier --write $CLAUDE_TOOL_ARGS"}
      ]
    }]
  }
}

# Result: File written AND formatted automatically
```

---

## Common Workflow Patterns

### Research → Design → Implement → Test → Document

```markdown
# Orchestrator agent coordinates full workflow

<workflow>
Stage 1: Research
- research-agent investigates requirements
- Gathers relevant examples and patterns
- Identifies constraints and dependencies

Stage 2: Design
- architect-agent creates design
- Reviews research findings
- Proposes architecture and approach

Stage 3: Implement
- developer-agent writes code
- Follows design specifications
- Handles edge cases

Stage 4: Test
- test-agent creates tests
- Validates implementation
- Checks edge cases

Stage 5: Document
- docs-agent writes documentation
- Explains architecture decisions
- Provides usage examples
</workflow>
```

### Analyze → Prioritize → Execute → Validate

```markdown
# Progressive improvement workflow

<workflow>
Stage 1: Analyze
- scanner-agent finds improvement opportunities
- Categorizes by type and impact
- Estimates effort for each

Stage 2: Prioritize
- Orchestrator ranks by impact/effort
- Gets user approval for priority list
- Plans implementation order

Stage 3: Execute
- enhancer-agent makes improvements
- One change at a time
- Tests after each change

Stage 4: Validate
- reviewer-agent validates changes
- Runs test suite
- Confirms no regressions
</workflow>
```

---

## Best Practices Summary

### Workflow Design

1. **Clear Stages**: Define distinct phases with clear outputs
2. **Validation Points**: Check results between stages
3. **Error Handling**: Plan for failures at each stage
4. **User Feedback**: Keep user informed of progress
5. **Idempotent**: Safe to restart from any stage

### Agent Coordination

1. **Focused Scope**: Each agent has single clear purpose
2. **Complete Context**: Provide all necessary information
3. **Expected Format**: Define output structure clearly
4. **Dependencies**: Specify execution order when needed
5. **Result Synthesis**: Combine outputs coherently

### Performance

1. **Parallelize**: Run independent operations concurrently
2. **Minimize Context**: Only include relevant information
3. **Cache Results**: Reuse expensive computations
4. **Right Tool**: Choose most efficient tool for task
5. **Batch Operations**: Group related operations

### Integration

1. **Composability**: Design components to work together
2. **Clear Interfaces**: Define input/output contracts
3. **Loose Coupling**: Components work independently
4. **Event-Driven**: Use hooks for cross-cutting concerns
5. **Maintainability**: Document integration points

---

**See Also**:
- [commands.md](./commands.md) - Building command components
- [agents.md](./agents.md) - Creating specialized agents
- [hooks.md](./hooks.md) - Event-driven integration
- [templates.md](./templates.md) - Complete working examples
