# Template Library & Troubleshooting

**Navigation**: [← Patterns](./patterns.md) | [Index](./index.md)

**Related Documentation**: All other files provide conceptual information; this file provides working examples and troubleshooting guidance.

---

## Overview

This document provides ready-to-use templates for commands, agents, and hooks, plus comprehensive troubleshooting guidance. Templates can be copied and adapted for your needs.

---

## Essential Command Templates

### Git Workflow Commands

#### Commit Command

**File**: `.claude/commands/commit.md`

```markdown
---
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git status:*)
argument-hint: [commit message]
description: Create structured git commit
---

<instructions>
1. Run git status to show current changes
2. Validate commit message follows project conventions
3. ALWAYS ask for user confirmation before committing
4. Only commit staged changes, never auto-stage files
</instructions>

<commit_rules>

- Use format: [scope] lowercase description
- Be concise but descriptive
- No trailing periods
- Max 72 characters for first line
- Examples:
  - [fix] resolve authentication timeout
  - [feat] add user profile page
  - [refactor] simplify data processing logic
    </commit_rules>

<validation>
Before committing:
- Check if there are staged changes (git diff --cached)
- Validate message format matches convention
- Ensure message is not empty
- Verify message accurately describes changes
- Ask user to confirm commit
</validation>

Create git commit with message: $ARGUMENTS

After committing:

- Display commit hash and summary
- Show current branch status
- Mention any next steps (push, PR, etc.)
```

#### Branch Command

**File**: `.claude/commands/branch.md`

```markdown
---
allowed-tools: Bash(git checkout:*), Bash(git branch:*), Bash(git status:*)
argument-hint: [branch-name]
description: Create and switch to new branch
---

<branch_rules>
Branch naming conventions:

- Use kebab-case: feature-name, bug-fix-name
- Include ticket number if applicable: ABC-123-feature-name
- Descriptive but concise
- Avoid special characters except hyphen
  </branch_rules>

<validation>
Before creating branch:
1. Check if branch name is valid (kebab-case, no spaces)
2. Verify branch doesn't already exist (git branch --list)
3. Ensure working directory is clean (git status)
4. Confirm current branch is appropriate base
5. Get user confirmation for branch name
</validation>

Create and switch to branch: $ARGUMENTS

After creation:

- Confirm branch created successfully
- Show current branch (git branch)- Display git log --oneline -5 for recent commits
```

#### Deploy Command

**File**: `.claude/commands/deploy.md`

```markdown
---
allowed-tools: Bash
argument-hint: [environment]
description: Deploy to specified environment
---

<deployment_safety>
Critical safety checks before deployment:

1. **Environment Validation**
   - Verify environment exists (staging, production, etc.)
   - Check environment configuration is loaded
   - Validate credentials/access for target environment

2. **Code State**
   - Check for uncommitted changes (git status)
   - Verify on correct branch for environment
   - Ensure all tests pass (run test suite)
   - Check build succeeds (run build command)

3. **Deployment Confirmation**
   - Show what will be deployed (branch, commit hash)
   - Display target environment clearly
   - Get explicit user confirmation
   - Warn if deploying to production

4. **Post-Deployment**
   - Verify deployment succeeded
   - Run smoke tests if available
   - Display deployment URL
   - Log deployment in project records
     </deployment_safety>

<environment_mapping>
Valid environments:

- dev: Development environment (auto-deploy)- staging: Staging environment (requires approval)
- production: Production environment (requires explicit confirmation)
  </environment_mapping>

Deploy to environment: $ARGUMENTS
```

### Code Generation Commands

#### React Component Generator

**File**: `.claude/commands/component.md`

```markdown
---
allowed-tools: Write, Read, Glob
argument-hint: [ComponentName] [props-type]
description: Generate TypeScript React component
---

<generation_rules>
Component structure:

- PascalCase component names (e.g., UserProfile, DataTable)
- TypeScript interfaces for props
- Functional components with hooks
- Export component as default
- Co-locate types with component
- Follow project structure conventions
  </generation_rules>

<props_types>
Props configuration options:

- "none": No props interface
- "ChildrenProps": {children: React.ReactNode}
- "ClassNameProps": {className?: string}
- "custom": Use $2 as custom type name
- Default: "none"
  </props_types>

<file_structure>
Generated structure:
ComponentName/
├── ComponentName.tsx # Component implementation
├── ComponentName.test.tsx # Unit tests (if project has tests)
└── index.ts # Re-export
</file_structure>

<implementation>
Before generating:
1. Validate ComponentName is PascalCase
2. Check if component already exists
3. Determine project conventions (check similar components)
4. Verify target path exists or create it
5. Show user proposed structure
6. Get confirmation

Generate:

- Component file with TypeScript
- Props interface if needed
- Basic JSDoc comment
- Index file for clean imports
- Test file skeleton if project uses tests
  </implementation>

Generate React component: $1
Props configuration: ${2:-"none"}
```

#### API Endpoint Generator

**File**: `.claude/commands/endpoint.md`

````markdown
---
allowed-tools: Write, Read, Glob, Edit
argument-hint: [endpoint-name] [method]
description: Generate API endpoint with validation
---

<endpoint_generation>
REST API conventions:

- Endpoint names: kebab-case (e.g., user-profile, data-export)
- Methods: GET, POST, PUT, DELETE, PATCH
- Path: /api/[endpoint-name]
- File location: src/api/endpoints/[endpoint-name].ts

Method semantics:

- GET: Fetch resources (query params for filters, no body)
- POST: Create new resource (body required)
- PUT: Full resource update (body required)
- PATCH: Partial update (body required)
- DELETE: Remove resource (params/URL, no body)
  </endpoint_generation>

<template_structure>
Each endpoint includes:

1. Validation schema (Zod or similar)
2. TypeScript types (request/response)
3. Route handler with error handling
4. Input validation middleware
5. Basic JSDoc documentation
6. Rate limiting consideration
7. Authentication check if needed
   </template_structure>

<implementation>
Generate endpoint file:
```typescript
import { Router, Request, Response } from 'express';
import { z } from 'zod';

// Validation schema
const [EndpointName]Schema = z.object({
// Define based on HTTP method
});

// Types
type [EndpointName]Request = z.infer<typeof [EndpointName]Schema>;
type [EndpointName]Response = {
// Define response structure
};

// Handler
router.[method]('/api/[endpoint-name]', async (req: Request, res: Response) => {
try {
// Validate input
const data = [EndpointName]Schema.parse(req.body || req.query);

    // Process request
    // ...

    // Return response
    res.json({ success: true, data: result });

} catch (error) {
// Error handling
if (error instanceof z.ZodError) {
return res.status(400).json({ error: 'Validation failed', details: error.errors });
}
res.status(500).json({ error: 'Internal server error' });
}
});
````

</implementation>

Generate API endpoint: $1 using method: ${2:-"GET"}

````

#### Database Migration Generator

**File**: `.claude/commands/migration.md`

```markdown
---
allowed-tools: Write, Bash, Read
argument-hint: [migration-name]
description: Create database migration
---

<migration_safety>
Migration requirements:
- Reversible: Every up() must have corresponding down()
- Data preservation: Never drop columns with data without backup plan
- Index considerations: Add indexes in separate migrations if table is large
- Performance: Consider impact on production database
- Testing: Test migration on copy of production data
</migration_safety>

<naming_convention>
Migration file naming:
- Format: YYYYMMDDHHMMSS_migration_name.ts
- Timestamp ensures order
- Name describes change: add_user_email, create_posts_table
- Use snake_case for migration names
</naming_convention>

<template_structure>
Migration template:
```typescript
import { Knex } from 'knex';

export async function up(knex: Knex): Promise<void> {
  // Forward migration
  await knex.schema.createTable('table_name', (table) => {
    table.increments('id').primary();
    table.string('name').notNullable();
    table.timestamps(true, true);
  });
}

export async function down(knex: Knex): Promise<void> {
  // Rollback migration
  await knex.schema.dropTable('table_name');
}
````

</template_structure>

Create migration: $ARGUMENTS

After creation:

- Remind user to review migration
- Suggest testing on dev database first
- Note any special deployment considerations

````

---

## Essential Agent Templates

### Development Agents

#### Full-Stack Developer

**File**: `.claude/agents/fullstack-developer.md`

```markdown
---
name: fullstack-developer
description: Complete application development with frontend, backend, and testing
tools: Read, Write, Edit, Bash
model: sonnet
---

<expertise>
Technical stack expertise:
- Frontend: React, TypeScript, CSS, Tailwind
- Backend: Node.js, Express, Python, FastAPI
- Database: PostgreSQL, MongoDB, Redis
- DevOps: Docker, CI/CD, deployment automation
- Testing: Jest, Pytest, Playwright, unit/integration/e2e
</expertise>

<development_approach>
Systematic development process:

1. **Understanding**
   - Analyze requirements thoroughly
   - Identify constraints and dependencies
   - Plan architecture and approach
   - Confirm understanding with user

2. **Implementation**
   - Follow project conventions and patterns
   - Write clean, maintainable code
   - Include error handling
   - Add appropriate logging
   - Consider edge cases

3. **Testing**
   - Write unit tests for logic
   - Add integration tests for workflows
   - Include e2e tests for critical paths
   - Verify error scenarios

4. **Documentation**
   - Add JSDoc/docstrings for complex functions
   - Update README if needed
   - Document API changes
   - Note any gotchas or considerations
</development_approach>

<code_quality_standards>
- Type safety: Use TypeScript strict mode
- Error handling: Try-catch, validation, graceful degradation
- Performance: Avoid premature optimization, but be conscious
- Security: Validate inputs, sanitize outputs, follow OWASP
- Maintainability: Clear naming, single responsibility, DRY
</code_quality_standards>
````

#### DevOps Engineer

**File**: `.claude/agents/devops-engineer.md`

```markdown
---
name: devops-engineer
description: Infrastructure, deployment automation, and operations
tools: Read, Write, Bash, WebFetch
model: sonnet
---

<specializations>
Core competencies:
- Container orchestration: Docker, Kubernetes, Docker Compose
- CI/CD pipeline design: GitHub Actions, GitLab CI, Jenkins
- Infrastructure as code: Terraform, CloudFormation, Bicep
- Monitoring and observability: Prometheus, Grafana, ELK stack
- Security and compliance: Secret management, access control, auditing
- Cloud platforms: AWS, Azure, GCP
</specializations>

<operational_philosophy>
Principles:

- Automate everything possible
- Infrastructure as code (version control everything)
- Immutable infrastructure
- Security by default
- Observable systems (metrics, logs, traces)
- Disaster recovery planning
  </operational_philosophy>

<workflow>
Infrastructure tasks:

1. **Planning**
   - Understand application requirements
   - Design infrastructure architecture
   - Estimate costs
   - Plan scaling strategy

2. **Implementation**
   - Write IaC templates (Terraform, etc.)
   - Configure CI/CD pipelines
   - Set up monitoring and alerting
   - Implement security controls

3. **Validation**
   - Test infrastructure provisioning
   - Verify deployment automation
   - Validate monitoring and alerts
   - Security scanning

4. **Documentation**
   - Architecture diagrams
   - Runbooks for common operations
   - Disaster recovery procedures
   - Cost optimization notes
     </workflow>
```

#### QA Engineer

**File**: `.claude/agents/qa-engineer.md`

```markdown
---
name: qa-engineer
description: Comprehensive testing and quality assurance
tools: Read, Write, Bash
model: sonnet
---

<testing_approach>
Comprehensive QA strategy:

1. **Test Planning**
   - Analyze requirements and acceptance criteria
   - Identify test scenarios and edge cases
   - Design test strategy (unit, integration, e2e)
   - Plan test data and environment needs

2. **Test Development**
   - Write unit tests for business logic
   - Create integration tests for workflows
   - Develop e2e tests for user journeys
   - Include negative test cases
   - Test error handling and recovery

3. **Test Execution**
   - Run automated test suites
   - Perform exploratory testing
   - Validate across browsers/devices
   - Test performance and load
   - Security testing basics

4. **Quality Reporting**
   - Document test coverage
   - Report defects with reproduction steps
   - Assess release readiness
   - Suggest quality improvements
     </testing_approach>

<test_types>
Testing levels:

- Unit tests: Individual functions, pure logic
- Integration tests: Component interactions, API calls
- E2E tests: Full user workflows, critical paths
- Performance tests: Load, stress, endurance
- Security tests: OWASP top 10, vulnerability scanning
  </test_types>
```

### Specialized Agents

#### Data Analyst

**File**: `.claude/agents/data-analyst.md`

```markdown
---
name: data-analyst
description: Data analysis, visualization, and reporting
tools: Read, Write, ExecuteCode
model: sonnet
---

<analytical_skills>
Data analysis capabilities:

- Statistical analysis: descriptive, inferential, correlation
- Data visualization: charts, graphs, dashboards
- Pattern recognition: trends, anomalies, outliers
- Predictive modeling: regression, classification basics
- Report generation: insights, recommendations, presentations
  </analytical_skills>

<analysis_workflow>
Data analysis process:

1. **Data Understanding**
   - Load and explore dataset
   - Check data types and structure
   - Identify missing values
   - Understand domain context

2. **Data Cleaning**
   - Handle missing values
   - Remove duplicates
   - Fix data types
   - Validate data quality

3. **Analysis**
   - Descriptive statistics
   - Distribution analysis
   - Correlation analysis
   - Segment/group analysis
   - Trend identification

4. **Visualization**
   - Choose appropriate chart types
   - Create clear, informative visualizations
   - Highlight key insights
   - Design for audience

5. **Reporting**
   - Summarize key findings
   - Provide actionable recommendations
   - Include supporting visualizations
   - Note data limitations
     </analysis_workflow>

<tools>
Python libraries:
- pandas: Data manipulation
- numpy: Numerical computation
- matplotlib/seaborn: Visualization
- scipy: Statistical analysis
- scikit-learn: Machine learning basics
</tools>
```

#### Technical Writer

**File**: `.claude/agents/technical-writer.md`

```markdown
---
name: technical-writer
description: Documentation and technical communication
tools: Read, Write, WebFetch
model: haiku
---

<documentation_types>
Documentation expertise:

- API documentation: Endpoints, parameters, examples
- User guides: Step-by-step instructions, screenshots
- Architecture decisions: ADRs, design rationale
- Process documentation: Workflows, procedures, runbooks
- Training materials: Tutorials, onboarding guides
  </documentation_types>

<writing_principles>
Documentation standards:

- Clarity: Simple language, avoid jargon
- Completeness: All necessary information included
- Accuracy: Technically correct, up-to-date
- Structure: Logical organization, easy navigation
- Examples: Code samples, use cases, scenarios
- Maintainability: Version control, easy updates
  </writing_principles>

<documentation_structure>
Standard documentation format:

# Title

Brief description of what this documents

## Overview

High-level explanation

## Prerequisites

What user needs before starting

## Step-by-Step Guide

1. First step with explanation
2. Second step with code examples
3. Continue...

## Common Issues

Troubleshooting guidance

## Examples

Real-world usage examples

## Related Resources

Links to related documentation
</documentation_structure>
```

#### Security Analyst

**File**: `.claude/agents/security-analyst.md`

```markdown
---
name: security-analyst
description: Security assessment, hardening, and compliance
tools: Read, Grep, Bash
model: opus
---

<security_domains>
Security expertise:

- Vulnerability assessment: OWASP Top 10, CVEs
- Penetration testing: Security validation, exploit identification
- Security architecture review: Design analysis, threat modeling
- Compliance validation: SOC2, ISO 27001, GDPR, HIPAA
- Incident response: Detection, containment, recovery
  </security_domains>

<assessment_methodology>
Security assessment process:

1. **Reconnaissance**
   - Understand application architecture
   - Identify attack surface
   - Map data flows and trust boundaries
   - Document external dependencies

2. **Threat Modeling**
   - Identify assets and threats
   - Analyze potential attack vectors
   - Assess risk likelihood and impact
   - Prioritize security concerns

3. **Vulnerability Analysis**
   - Static code analysis
   - Dependency scanning
   - Configuration review
   - Authentication/authorization checks
   - Input validation review

4. **Risk Assessment**
   - Severity scoring (CVSS)
   - Exploitability analysis
   - Business impact evaluation
   - Remediation priority

5. **Remediation Planning**
   - Specific fix recommendations
   - Secure coding examples
   - Architectural improvements
   - Security control implementations
     </assessment_methodology>

<focus_areas>
Priority vulnerabilities:

- Injection attacks (SQL, NoSQL, command, LDAP)
- Broken authentication and session management
- Sensitive data exposure
- XML external entities (XXE)
- Broken access control
- Security misconfiguration
- Cross-site scripting (XSS)
- Insecure deserialization
- Using components with known vulnerabilities
- Insufficient logging and monitoring
  </focus_areas>
```

---

## Troubleshooting & Validation

### Common Issues and Solutions

#### Command Issues

**Problem**: Command not found or not executing

```markdown
Troubleshooting Steps:

1. Check file location
   - Must be in .claude/commands/
   - Filename must match invocation: command.md → /command

2. Verify YAML frontmatter syntax
   - Check for proper indentation
   - Ensure all required fields present
   - Validate YAML with: yq eval .claude/commands/command.md

3. Validate markdown format
   - Frontmatter between --- markers
   - Valid markdown after frontmatter

4. Check tool permissions
   - allowed-tools field present
   - Tool names spelled correctly
   - Syntax: Tool(command:\*) for restrictions

5. Test argument parsing
   - Try with different argument patterns
   - Verify $ARGUMENTS, $1, $2 work as expected
```

**Problem**: Tool permission errors

```markdown
Solutions:

- Verify allowed-tools configuration
  Example: allowed-tools: Bash(git:\*), Read, Write

- Check specific tool syntax
  Correct: Bash(git add:\*)
  Wrong: Bash git add

- Validate argument patterns
  Command patterns: tool:command:_
  All commands: tool:_

- Review security restrictions
  Some tools may be restricted by policy

Test permission:

1. Add \* to allowed-tools temporarily
2. If works, narrow down specific tool needed
3. Remove \* and use specific tool list
```

**Problem**: Arguments not parsing correctly

```markdown
Debug argument handling:

- $ARGUMENTS = all arguments as single string
- $1, $2, $3 = individual space-separated arguments
- ${2:-"default"} = second argument with fallback

Common issues:

- Multi-word arguments need quotes: /cmd "multi word"
- Missing default values cause empty strings
- Argument order matters for $1, $2, etc.

Test patterns:
/command single → $ARGUMENTS="single", $1="single"
/command one two → $ARGUMENTS="one two", $1="one", $2="two"
/command "one two" → $ARGUMENTS="one two", $1="one two"
```

#### Agent Issues

**Problem**: Agent not being invoked

```markdown
Troubleshooting Steps:

1. Check agent description clarity
   - Description should clearly state when to use agent
   - Use specific keywords that match user requests
   - Example: "security analysis" not just "analysis"

2. Verify file naming conventions
   - Must be in .claude/agents/
   - Filename: agent-name.md
   - No spaces in filename (use hyphens)

3. Test manual invocation
   - User can explicitly request: "Use security-auditor agent"
   - Verify agent loads and executes

4. Review tool access configuration
   - Ensure agent has necessary tools
   - Check tools: field in frontmatter
   - Empty/omitted = inherits all tools

5. Validate YAML syntax
   - Check frontmatter structure
   - Verify all fields properly formatted
```

**Problem**: Poor agent performance

```markdown
Optimization Steps:

1. Refine role definition
   - Be more specific about expertise
   - Clarify responsibilities
   - Add domain knowledge
   - Include examples of good outputs

2. Improve prompt specificity
   - Add structured thinking patterns
   - Define clear methodology
   - Include quality standards
   - Provide output templates

3. Adjust model selection
   - Haiku: Simple, fast tasks
   - Sonnet: Standard development (default)
   - Opus: Complex reasoning, architecture

4. Optimize tool access
   - Restrict to necessary tools only
   - Too many tools = slower, less focused
   - Minimal access = better performance

5. Add structured thinking patterns
   - OODA loop for decision making
   - Step-by-step methodology
   - Verification checkpoints
   - Quality validation steps
```

**Problem**: Agent context overflow

```markdown
Causes and solutions:

1. Too much context provided
   Solution: Only include relevant information
   - Don't pass entire codebase
   - Use specific file references
   - Provide focused examples

2. Agent reads too many files
   Solution: Direct agent to specific files
   - Use Grep instead of reading all files
   - Specify exact file paths
   - Limit scope in instructions

3. Agent output too verbose
   Solution: Request specific format
   - Define output structure
   - Set length limits
   - Ask for summaries over full details

4. Recursive agent creation
   Solution: Limit delegation depth
   - Don't create agents that create agents infinitely
   - Set maximum delegation depth
   - Use iteration over recursion
```

#### Hook Issues

**Problem**: Hooks not triggering

```markdown
Debugging Steps:

1. Verify settings.json syntax
   - Validate JSON: jq . .claude/settings.json
   - Check for trailing commas (invalid in JSON)
   - Verify bracket matching

2. Check matcher patterns
   - Test regex pattern with tool name
   - Use .\* carefully (matches everything)
   - Be specific: Bash._git._ not just Bash

3. Test hook commands manually
   - Run hook script directly
   - Set environment variables:
     export CLAUDE_TOOL_NAME="Bash"
     export CLAUDE_TOOL_ARGS="test command"
   - Verify exit code (0 or 2)

4. Review event types
   - PreToolUse: Before tool execution
   - PostToolUse: After successful execution
   - Correct event for use case?

5. Validate file permissions
   - Hook scripts must be executable: chmod +x script.sh
   - Check script interpreter exists: which python3
```

**Problem**: Hook blocking unexpectedly

````markdown
Causes and solutions:

1. Hook script error causes exit code 2
   Debug: Run hook manually, check for errors
   Solution: Add error handling, return 0 on error

2. Validation logic too strict
   Debug: Test with various inputs
   Solution: Relax validation, add exceptions

3. Environment variable not available
   Debug: Print environment in hook: env | grep CLAUDE
   Solution: Check for variable, provide default

4. Path resolution issues
   Debug: Print resolved paths in hook
   Solution: Use absolute paths, realpath

Fix example:

```python
#!/usr/bin/env python3
import sys

try:
    # Hook logic
    # ...
    sys.exit(0)  # Success
except Exception as e:
    # Log error but don't block
    print(f"Hook warning: {e}")
    sys.exit(0)  # Allow operation despite error
```
````

````

**Problem**: Performance impact from hooks

```markdown
Causes:
- Hook does expensive operations (API calls, large file processing)
- Multiple hooks on same event compound delay
- Hook doesn't exit quickly
- External dependencies slow down hook

Solutions:

1. Optimize hook logic
   - Cache results where possible
   - Avoid expensive operations
   - Process only what's necessary
   - Set timeouts for external calls

2. Run expensive operations async
   - Fork process for long-running tasks
   - Don't wait for completion
   - Log results separately

3. Use selective matchers
   - Don't match all tools: .*
   - Be specific: Write.*\.ts$ not Write.*
   - Reduces hook invocation frequency

4. Consider PostToolUse instead
   - PostToolUse doesn't block workflow
   - User continues while hook runs
   - Good for non-critical operations

Performance target: < 100ms per hook
````

---

## Validation Checklists

### Command Validation

```markdown
Pre-deployment checklist:

✓ YAML frontmatter is valid

- Test: yq eval .claude/commands/command.md

✓ All required fields present

- allowed-tools: specified or \*
- description: clear, concise
- argument-hint: helpful for users

✓ Tool permissions are minimal but sufficient

- Only tools actually used
- Specific command patterns when possible
- No \* unless necessary

✓ Argument handling is correct

- $ARGUMENTS for full string
- $1, $2 for specific args
- Defaults for optional args

✓ Validation logic is comprehensive

- Input validation
- State checks (git status, file exists)
- Error handling

✓ Error cases are handled

- Missing arguments
- Invalid inputs
- Tool failures

✓ Security considerations addressed

- Input sanitization
- Path validation
- Credential protection

✓ User confirmation for destructive operations

- Deleting files
- Force pushing
- Production deployments

✓ Clear description and hints provided

- Description explains what command does
- Argument hint shows expected format
- Examples in documentation

✓ Tested with various inputs

- Normal cases
- Edge cases
- Error cases
```

### Agent Validation

```markdown
Pre-deployment checklist:

✓ Role definition is specific and clear

- Domain expertise identified
- Responsibilities well-defined
- Scope is focused (not too broad)

✓ Capabilities are well-defined

- Lists specific skills
- Includes domain knowledge
- References methodologies

✓ Tool access is appropriate

- Minimal necessary tools
- Security considered
- Performance optimized

✓ Model selection is optimal

- Haiku for simple tasks
- Sonnet for standard work (default)
- Opus for complex reasoning

✓ Prompt engineering follows best practices

- Structured thinking patterns
- Clear methodology
- Quality standards defined
- Output format specified

✓ Structured thinking patterns included

- OODA loop or similar
- Step-by-step approach
- Verification steps

✓ Integration with other agents considered

- Coordination rules defined
- Input/output formats clear
- Handoff procedures specified

✓ Performance characteristics acceptable

- Response time reasonable
- Token usage optimized
- Context managed efficiently

✓ Tested with representative tasks

- Normal cases
- Edge cases
- Complex scenarios

✓ Documentation is complete

- When to use agent
- What to expect
- Example use cases
```

### Hook Validation

```markdown
Pre-deployment checklist:

✓ Matcher patterns are accurate

- Test with actual tool names
- Specific enough to avoid false matches
- Not too broad

✓ Hook commands are tested

- Run manually with test data
- Verify exit codes (0 or 2)
- Check JSON output when blocking

✓ Security implications reviewed

- Hook can't be exploited
- Validates inputs properly
- Fails safely

✓ Error handling is robust

- Handles missing environment variables
- Catches exceptions
- Provides clear error messages

✓ Performance impact is minimal

- Executes quickly (< 100ms target)
- No blocking operations
- Efficient algorithms

✓ Integration points are validated

- Works with commands
- Works with agents
- Correct event type used

✓ Documentation is complete

- What hook does
- When it triggers
- How to debug

✓ Rollback procedures exist

- Can disable hook easily
- No permanent state changes
- Graceful degradation

✓ Tested in realistic scenarios

- Various inputs
- Error conditions
- Edge cases

✓ Script is executable

- chmod +x script.sh
- Correct shebang (#!/bin/bash, #!/usr/bin/env python3)
- Dependencies available
```

---

## Testing Strategies

### Integration Testing

**Manual command testing**:

```bash
# Test command execution
claude /test-command "test arguments"

# Verify output
# Check files created/modified
# Confirm expected behavior

# Test with edge cases
claude /test-command ""                    # Empty argument
claude /test-command "very long argument with special characters !@#"
claude /test-command arg1 arg2 arg3 arg4   # Multiple arguments
```

**Agent testing**:

```bash
# Explicit agent invocation
claude "Use test-agent to analyze file.ts"

# Verify agent loaded
# Check output quality
# Confirm tool usage

# Test with various scenarios
claude "Use test-agent for complex multi-step task"
claude "Use test-agent with minimal input"
```

**Hook testing**:

```bash
# Enable debug mode
export HOOK_DEBUG=true

# Set test environment
export CLAUDE_TOOL_NAME="Bash"
export CLAUDE_TOOL_ARGS="test command"
export CLAUDE_PROJECT_DIR=$(pwd)

# Run hook manually
./scripts/test_hook.sh

# Check exit code
echo $?  # Should be 0 or 2

# Check output
cat .hook_debug.log
```

### Validation Scripts

**Comprehensive validation script**:

```python
#!/usr/bin/env python3
"""Validate Claude Code configuration"""

import yaml
import json
import os
import sys
from pathlib import Path

def validate_commands():
    """Validate all command files"""
    commands_dir = Path(".claude/commands")
    if not commands_dir.exists():
        print("✗ Commands directory not found")
        return False

    issues = []
    for cmd_file in commands_dir.glob("*.md"):
        print(f"Checking {cmd_file.name}...")

        with open(cmd_file) as f:
            content = f.read()

        # Check for frontmatter
        if not content.startswith('---'):
            issues.append(f"{cmd_file.name}: Missing frontmatter")
            continue

        # Extract and validate YAML
        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                issues.append(f"{cmd_file.name}: Invalid frontmatter structure")
                continue

            frontmatter = yaml.safe_load(parts[1])

            # Check required fields
            if 'description' not in frontmatter:
                issues.append(f"{cmd_file.name}: Missing description")

        except yaml.YAMLError as e:
            issues.append(f"{cmd_file.name}: Invalid YAML - {e}")

    if issues:
        print("\n✗ Command validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        return False

    print("✓ All commands valid")
    return True

def validate_agents():
    """Validate all agent files"""
    agents_dir = Path(".claude/agents")
    if not agents_dir.exists():
        print("✗ Agents directory not found")
        return False

    issues = []
    for agent_file in agents_dir.glob("*.md"):
        print(f"Checking {agent_file.name}...")

        with open(agent_file) as f:
            content = f.read()

        # Check for frontmatter
        if not content.startswith('---'):
            issues.append(f"{agent_file.name}: Missing frontmatter")
            continue

        # Extract and validate YAML
        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                issues.append(f"{agent_file.name}: Invalid frontmatter structure")
                continue

            frontmatter = yaml.safe_load(parts[1])

            # Check required fields
            if 'name' not in frontmatter:
                issues.append(f"{agent_file.name}: Missing name")
            if 'description' not in frontmatter:
                issues.append(f"{agent_file.name}: Missing description")

            # Check model if specified
            if 'model' in frontmatter:
                valid_models = ['haiku', 'sonnet', 'opus']
                if frontmatter['model'] not in valid_models:
                    issues.append(f"{agent_file.name}: Invalid model '{frontmatter['model']}'")

        except yaml.YAMLError as e:
            issues.append(f"{agent_file.name}: Invalid YAML - {e}")

    if issues:
        print("\n✗ Agent validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        return False

    print("✓ All agents valid")
    return True

def validate_hooks():
    """Validate hooks configuration"""
    settings_file = Path(".claude/settings.json")
    if not settings_file.exists():
        print("⚠ No settings.json found (hooks optional)")
        return True

    print("Checking settings.json...")

    try:
        with open(settings_file) as f:
            config = json.load(f)

        # Check hooks structure
        if 'hooks' not in config:
            print("⚠ No hooks configured")
            return True

        hooks = config['hooks']
        valid_events = ['PreToolUse', 'PostToolUse', 'UserPromptSubmit', 'Stop', 'SubagentStop']

        for event_type, matchers in hooks.items():
            if event_type not in valid_events:
                print(f"✗ Invalid hook event type: {event_type}")
                return False

            for matcher_config in matchers:
                if 'matcher' not in matcher_config:
                    print(f"✗ Missing matcher in {event_type}")
                    return False

                if 'hooks' not in matcher_config:
                    print(f"✗ Missing hooks array in {event_type}")
                    return False

                for hook in matcher_config['hooks']:
                    if 'type' not in hook or 'command' not in hook:
                        print(f"✗ Invalid hook configuration in {event_type}")
                        return False

        print("✓ Hooks configuration valid")
        return True

    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in settings.json: {e}")
        return False

def main():
    print("Claude Code Configuration Validator\n")

    results = [
        validate_commands(),
        validate_agents(),
        validate_hooks()
    ]

    if all(results):
        print("\n✓ All validations passed!")
        sys.exit(0)
    else:
        print("\n✗ Validation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Usage**:

```bash
# Make script executable
chmod +x scripts/validate_config.py

# Run validation
python scripts/validate_config.py

# Add to git pre-commit hook (optional)
```

---

## Best Practices Summary

### For AI Models Creating Claude Code Extensions

1. **Start Simple**: Begin with basic functionality, then enhance
   - Minimal viable command/agent first
   - Add features incrementally
   - Test thoroughly at each step

2. **Be Explicit**: Clear instructions prevent ambiguity
   - Detailed role definitions for agents
   - Specific validation rules for commands
   - Clear error messages in hooks

3. **Security First**: Always validate inputs and restrict tools appropriately
   - Minimal tool permissions
   - Input sanitization
   - Path validation
   - Credential protection

4. **User Experience**: Provide clear hints, descriptions, and confirmations
   - Helpful argument hints
   - Clear descriptions
   - Confirm destructive operations
   - Provide feedback at each step

5. **Maintainability**: Use consistent patterns and good documentation
   - Follow naming conventions
   - Document complex logic
   - Use templates as starting points
   - Version control everything

6. **Performance**: Optimize for efficiency and minimal context usage
   - Parallel tool execution when possible
   - Focused agent scopes
   - Efficient tool selection
   - Context management

7. **Integration**: Consider how components work together
   - Command + agent workflows
   - Hook integration points
   - Agent coordination
   - Event-driven automation

8. **Validation**: Always test and validate functionality
   - Manual testing with various inputs
   - Automated validation scripts
   - Edge case coverage
   - Error scenario testing

### Key Principles

- **Specificity over Generality**: Focused tools are more effective
- **Security by Design**: Build in protections from the start
- **User-Centric Design**: Optimize for developer experience
- **Composability**: Design components that work well together
- **Maintainability**: Write code that's easy to understand and modify

---

**Navigation**: Return to [Index](./index.md) for complete documentation map

---

## Quick Reference

**Need templates?** See sections above for copy-paste starting points.

**Having issues?** Check troubleshooting sections for common problems.

**Validating config?** Use validation checklists and scripts provided.

**Best practices?** Review summary section for key principles.
