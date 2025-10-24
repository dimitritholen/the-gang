# Slash Commands Implementation

**Navigation**: [← Index](./index.md) | [Agents →](./agents.md)

**Related Documentation**: [hooks.md](./hooks.md) for command+hook integration | [patterns.md](./patterns.md) for command+agent workflows | [templates.md](./templates.md) for working examples

---

## Overview

Slash commands are user-invocable operations that provide repeatable, argument-based workflows. They are markdown files with YAML frontmatter configuration that control tool access, argument handling, and execution logic.

**When to create a slash command**:

- User needs repeatable action with specific arguments
- Task involves executing bash commands or file operations
- Workflow needs user confirmation or input validation
- You need standardized project-specific operations

---

## Basic Structure

Slash commands are markdown files stored in `.claude/commands/` with this structure:

```markdown
---
allowed-tools: Tool1, Tool2
argument-hint: [description of expected arguments]
description: Brief command explanation
---

Command instructions and prompt content here.
Use $ARGUMENTS for all arguments or $1, $2 for specific ones.
```

**File naming**: `command-name.md` → invoked as `/command-name [args]`

**Location**:

- Project: `.claude/commands/`
- User global: `~/.claude/commands/`

---

## Core Configuration Options

### allowed-tools

Controls which tools the command can access. Critical for security.

**Syntax patterns**:

```yaml
# Specific tool with specific commands
allowed-tools: Bash(git add:*)

# Multiple tools
allowed-tools: Read, Write, Edit

# Tool with multiple allowed commands
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git status:*)

# All tools (use cautiously!)
allowed-tools: *
```

**Security levels**:

- **Minimal**: `Read` - Read-only access
- **Standard**: `Read, Write, Edit` - File operations
- **Extended**: `Read, Write, Edit, Bash` - Full development
- **Unrestricted**: `*` - All tools (requires careful validation)

### argument-hint

Provides guidance to users on expected input format.

**Patterns**:

```yaml
# Single argument
argument-hint: [commit message]

# Multiple arguments
argument-hint: [component-name] [path]

# Optional arguments (use defaults in prompt)
argument-hint: [required-arg] [optional-flag]

# Mixed types
argument-hint: [name] [--option value]
```

**Best practices**:

- Use square brackets for all arguments
- Indicate optional vs required clearly
- Keep hints concise (< 50 chars)
- Match hint to actual argument parsing

### description

Brief explanation shown when listing commands.

```yaml
description: Create structured git commit with validation
```

**Guidelines**:

- One sentence, no period
- Focus on outcome, not implementation
- 40-80 characters optimal
- Use active verbs

---

## Argument Handling Patterns

### Single Argument Pattern

**Use case**: Command takes one piece of input

```markdown
---
argument-hint: [commit message]
---

Create a git commit with message: $ARGUMENTS
```

**Access**: `$ARGUMENTS` contains entire argument string

### Multiple Arguments Pattern

**Use case**: Command needs multiple distinct inputs

```markdown
---
argument-hint: [component-name] [optional-path]
---

Create React component named $1.
Path: ${2:-"src/components"}
```

**Access**:

- `$1` = first argument
- `$2` = second argument
- `${2:-"default"}` = second argument with default fallback

**Parsing**: Arguments split by spaces (quote multi-word arguments)

### Validation Pattern

**Use case**: Arguments need validation before use

```markdown
---
argument-hint: [branch-name]
---

<validation>
- Ensure branch name follows naming convention (kebab-case)
- Check if branch already exists using git branch --list
- Validate user has necessary permissions
- Reject if branch name contains invalid characters
</validation>

After validation passes, create and switch to branch: $ARGUMENTS
```

**Validation guidelines**:

- Always validate before destructive operations
- Check filesystem/git state as needed
- Provide clear error messages
- Ask user confirmation for ambiguous cases

---

## Security Best Practices

### Tool Restrictions

**Principle**: Grant minimum necessary permissions

```markdown
---
# GOOD: Specific git operations only
allowed-tools: Bash(git add:*), Bash(git commit:*), Read

# ACCEPTABLE: Broad but justified
allowed-tools: Read, Write, Edit, Bash

# DANGEROUS: Requires strong validation
allowed-tools: *
---
```

### Input Validation

**Always validate**:

1. File paths are within project directory
2. User input doesn't contain injection attempts
3. Destructive operations have user confirmation
4. External data is sanitized

**Example validation block**:

```markdown
Before proceeding:

1. Validate all file paths are within project directory
   - Use realpath to resolve
   - Check prefix matches project root
2. Sanitize user input to prevent injection
   - Escape shell metacharacters
   - Validate against whitelist patterns
3. Confirm destructive operations with user
   - Ask explicit yes/no
   - Show what will be affected
4. Verify required tools/dependencies exist
   - Check command availability
   - Validate version compatibility
```

### Dangerous Patterns to Avoid

```markdown
# NEVER do these without strong validation:

- rm -rf with user input
- eval or similar dynamic execution
- Unvalidated file path operations
- System-level modifications
- Credential handling without encryption
```

---

## Real-World Command Examples

### Git Commit Command

```markdown
---
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git status:*)
argument-hint: [commit message]
description: Create structured git commit with validation
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
  </commit_rules>

<validation>
- Check if there are staged changes
- Validate message format matches convention
- Ensure message is not empty
- Confirm message accurately describes changes
</validation>

Create git commit with message: $ARGUMENTS

After committing:

- Display commit hash and summary
- Show current branch status
```

**Usage**: `/commit "[fix] resolve authentication timeout"`

### React Component Generator

```markdown
---
allowed-tools: Write, Read, Glob
argument-hint: [ComponentName] [optional-props-type]
description: Generate TypeScript React component
---

<component_generation>

1. Validate ComponentName is PascalCase
   - Reject if not matching /^[A-Z][a-zA-Z0-9]\*$/
2. Default path: "src/components"
   - Override with second argument if provided
3. Props types: none, ChildrenProps, ClassNameProps, custom
   - "none" = no props interface
   - "ChildrenProps" = {children: React.ReactNode}
   - "ClassNameProps" = {className?: string}
   - custom = use $2 as type name
4. Follow project TypeScript conventions
   - Use interface for props
   - Export component as default
   - Include basic JSDoc comment
5. No aria-\* attributes per project rules
   </component_generation>

<file_structure>
ComponentName/
├── ComponentName.tsx
└── index.ts (re-export)
</file_structure>

Generate React component: $1
Props configuration: ${2:-"none"}

Before writing files:

- Check if component already exists
- Verify path exists or create it
- Show user the proposed file structure
- Ask for confirmation
```

**Usage**:

- `/component Button` - No props
- `/component Modal ChildrenProps` - With children
- `/component Card CustomCardProps` - Custom props

### API Endpoint Generator

````markdown
---
allowed-tools: Write, Read, Glob, Edit
argument-hint: [endpoint-name] [method]
description: Generate API endpoint with validation and types
---

<api_generation>

1. Validate endpoint name is kebab-case
2. Method must be: GET, POST, PUT, DELETE, PATCH
3. Generate endpoint file in src/api/endpoints/
4. Include: route handler, validation schema, types, tests stub
   </api_generation>

<api_patterns>
RESTful conventions:

- GET: Fetch resources (query params for filters)
- POST: Create new resource (body required)
- PUT: Full resource update (body required)
- PATCH: Partial update (body required)
- DELETE: Remove resource (no body)

Always include:

- Input validation using Zod or similar
- Error handling with appropriate status codes
- Type safety for request/response
- Basic JSDoc documentation
- Rate limiting consideration
  </api_patterns>

<template_structure>

```typescript
import { Router } from "express";
import { z } from "zod";

// Validation schema
const $1Schema = z.object({
  // Define based on $2 method
});

// Types
type $1Request = z.infer<typeof $1Schema>;
type $1Response = {
  // Define response structure
};

// Handler
router.$2("/api/$1", async (req, res) => {
  // Validate input
  // Process request
  // Return response
});
```
````

</template_structure>

Generate API endpoint: $1 using method: ${2:-"GET"}

Before creating:

- Check for existing endpoint
- Validate method is appropriate for endpoint name
- Show proposed file location
- Confirm with user

````

**Usage**:
- `/endpoint users GET` - List users
- `/endpoint user POST` - Create user

---

## Advanced Argument Handling

### Default Values

```markdown
Path: ${1:-"default/path"}
Method: ${2:-"GET"}
Config: ${3:-"standard"}
````

### Conditional Logic

```markdown
<argument_processing>
If $1 is empty:

- Prompt user for required input
- Exit with error if still empty

If $2 equals "test":

- Use test configuration
- Skip production validation

If $3 is provided:

- Override default settings
- Validate custom configuration
  </argument_processing>
```

### Complex Parsing

```markdown
<parse_arguments>
Parse $ARGUMENTS as:

- First word = command type
- Remaining = command-specific args
- Flags start with --
- Options are --key=value

Example: "create user --admin --email=test@example.com"
→ command_type = "create"
→ resource = "user"
→ flags = ["admin"]
→ options = {email: "test@example.com"}
</parse_arguments>
```

---

## Integration Patterns

### Command + Hook

See [hooks.md](./hooks.md) for detailed hook integration.

```markdown
# Command: /deploy

---

allowed-tools: Bash
argument-hint: [environment]

---

Deploy to environment: $ARGUMENTS

# Hook validates deployment safety
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash.*deploy.*",
        "hooks": [{ "type": "command", "command": "python validate_deploy.py" }]
      }
    ]
  }
}
```

### Command + Agent

See [patterns.md](./patterns.md) for workflow orchestration.

```markdown
---
allowed-tools: Task
argument-hint: [feature-description]
---

<workflow>
1. Use architect-agent to design: $ARGUMENTS
2. Use developer-agent to implement
3. Use reviewer-agent to validate
</workflow>
```

---

## Testing & Validation

### Manual Testing

```bash
# Test command execution
claude /test-command "test arguments"

# Test with various argument patterns
claude /test-command single
claude /test-command "multiple words"
claude /test-command arg1 arg2 arg3
```

### Validation Checklist

Before deploying command:

```markdown
✓ YAML frontmatter is valid
✓ All required fields present (description, allowed-tools, argument-hint)
✓ Tool permissions are minimal but sufficient
✓ Argument handling covers all cases
✓ Default values are appropriate
✓ Validation logic is comprehensive
✓ Error cases are handled
✓ Security considerations addressed
✓ User confirmation for destructive operations
✓ Clear description and hints provided
✓ Documentation/comments explain complex logic
```

### Common Issues

**Command not found**:

- Check file location (`.claude/commands/`)
- Verify filename matches invocation
- Ensure `.md` extension

**Tool permission errors**:

- Review `allowed-tools` configuration
- Check tool name spelling
- Validate argument patterns (e.g., `Bash(git:*)`)

**Argument parsing failures**:

- Test with quoted multi-word arguments
- Verify `$1`, `$2` indexing
- Check default value syntax `${2:-"default"}`

---

## Best Practices Summary

1. **Minimal permissions**: Grant only necessary tool access
2. **Explicit validation**: Validate all inputs before use
3. **User confirmation**: Ask before destructive operations
4. **Clear communication**: Provide helpful hints and descriptions
5. **Error handling**: Gracefully handle edge cases
6. **Security first**: Treat all user input as untrusted
7. **Documentation**: Comment complex logic and decisions
8. **Testing**: Manually test all argument patterns

---

**See Also**:

- [agents.md](./agents.md) - Creating specialized AI assistants
- [hooks.md](./hooks.md) - Validating and automating command execution
- [patterns.md](./patterns.md) - Orchestrating commands with agents
- [templates.md](./templates.md) - More command examples and troubleshooting
