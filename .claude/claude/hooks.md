# Hooks & Event-Driven Architecture

**Navigation**: [← Agents](./agents.md) | [Index](./index.md) | [Patterns →](./patterns.md)

**Related Documentation**: [commands.md](./commands.md) for command+hook integration | [agents.md](./agents.md) for agent+hook coordination | [patterns.md](./patterns.md) for workflow integration

---

## Overview

Hooks are event-driven scripts that execute automatically in response to specific Claude Code events. They enable validation, automation, and integration between components without modifying core behavior.

**When to create a hook**:

- You need to validate or modify tool usage
- Workflow requires automatic pre/post-processing
- Security validation is needed
- Integration between different components is required

---

## Hook Configuration

Hooks are configured in `.claude/settings.json` (project-level) or `~/.claude/settings.json` (user-level).

### Basic Structure

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "ToolName.*",
        "hooks": [
          {
            "type": "command",
            "command": "script_to_execute.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "ToolName.*",
        "hooks": [
          {
            "type": "command",
            "command": "script_to_execute.sh"
          }
        ]
      }
    ]
  }
}
```

### Configuration Fields

**matcher**: Regular expression matching tool calls

```json
// Match specific tool
"matcher": "Bash"

// Match tool with specific command
"matcher": "Bash.*git commit.*"

// Match multiple tools
"matcher": "(Write|Edit).*"

// Match all tools
"matcher": ".*"
```

**type**: Hook execution type

```json
// Execute shell command
"type": "command"

// Future: Other types may be added
```

**command**: Shell command to execute

```json
// Direct script execution
"command": "python validate.py"

// Script with arguments
"command": "./scripts/check.sh $CLAUDE_TOOL_NAME"

// Inline bash
"command": "bash -c 'echo Validating...'"
```

---

## Event Types

### PreToolUse

Executes **before** tool is invoked. Can block execution.

**Use cases**:

- Security validation
- Input sanitization
- Permission checks
- Environment validation
- Constraint enforcement

**Behavior**:

- Exit code 0: Allow tool execution
- Exit code 2: Block tool execution
- Blocking shows hook output to user

**Example**: Validate bash commands before execution

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash.*",
        "hooks": [
          {
            "type": "command",
            "command": "python scripts/validate_bash.py"
          }
        ]
      }
    ]
  }
}
```

### PostToolUse

Executes **after** successful tool execution.

**Use cases**:

- Code formatting
- Quality checks
- Automated testing
- Notification systems
- Logging and auditing

**Behavior**:

- Runs only if tool succeeded
- Cannot block (tool already executed)
- Output shown to user

**Example**: Auto-format code after file writes

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write.*\\.ts$",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_TOOL_ARGS"
          }
        ]
      }
    ]
  }
}
```

### UserPromptSubmit

Executes when user submits a prompt.

**Use cases**:

- Context validation
- Automatic project setup
- Workflow initiation
- Environment checks

**Behavior**:

- Runs before AI processes prompt
- Can provide context to AI
- Cannot block user input

**Example**: Validate project environment

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "scripts/check_env.sh"
          }
        ]
      }
    ]
  }
}
```

### Stop / SubagentStop

Executes when conversation or subagent completes.

**Use cases**:

- Resource cleanup
- Status reporting
- Result validation
- Archiving outputs

**Behavior**:

- Runs at completion
- Cannot affect execution
- Good for cleanup tasks

**Example**: Archive session logs

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "scripts/archive_session.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Environment Variables

Hooks have access to special environment variables with context about the event.

### CLAUDE_TOOL_NAME

The name of the tool being invoked.

```bash
# Example values:
# "Bash"
# "Write"
# "Edit"
# "Read"
```

**Usage**:

```bash
#!/bin/bash
echo "Tool: $CLAUDE_TOOL_NAME"

if [ "$CLAUDE_TOOL_NAME" = "Bash" ]; then
    # Bash-specific validation
fi
```

### CLAUDE_TOOL_ARGS

Arguments passed to the tool (as JSON string).

```bash
# For Bash tool: the command being executed
# For Write tool: the file path being written
# For Edit tool: JSON with file_path, old_string, new_string
```

**Usage**:

```python
#!/usr/bin/env python3
import os
import json

tool_args = os.environ.get('CLAUDE_TOOL_ARGS', '{}')
args = json.loads(tool_args)

# Access specific arguments
file_path = args.get('file_path')
command = args.get('command')
```

### CLAUDE_PROJECT_DIR

Absolute path to project root directory.

```bash
# Example: /home/user/projects/myapp
```

**Usage**:

```bash
#!/bin/bash
PROJECT_DIR="${CLAUDE_PROJECT_DIR}"

# Validate file is in project
if [[ ! "$FILE_PATH" =~ ^"$PROJECT_DIR" ]]; then
    echo "File outside project directory"
    exit 2
fi
```

---

## Security Patterns

### Input Validation Hook

Validate and sanitize inputs before execution.

**Python implementation**:

```python
#!/usr/bin/env python3
"""Validate bash commands for security"""
import sys
import json
import re
import os

def validate_bash_command(command):
    """Validate bash commands for dangerous patterns"""

    dangerous_patterns = [
        r'rm\s+-rf\s+/',           # Recursive delete root
        r'sudo\s+rm',               # Sudo with rm
        r'>\s*/dev/sd[a-z]',        # Write to disk device
        r'dd\s+if=',                # Disk duplication
        r'mkfs\.',                  # Format filesystem
        r'fdisk',                   # Partition manipulation
        r'eval\s+\$',               # Eval with variable
        r'curl.*\|\s*sh',           # Pipe curl to shell
        r'wget.*\|\s*sh',           # Pipe wget to shell
        r'chmod\s+777',             # Overly permissive
        r':\(\)\{.*\};:',           # Fork bomb
    ]

    issues = []
    for pattern in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            issues.append(f"Dangerous pattern detected: {pattern}")

    return issues

def main():
    # Get tool arguments from environment
    tool_args = os.environ.get('CLAUDE_TOOL_ARGS', '')

    # Validate command
    issues = validate_bash_command(tool_args)

    if issues:
        # Block execution
        result = {
            "block": True,
            "message": "Security validation failed",
            "issues": issues
        }
        print(json.dumps(result, indent=2))
        sys.exit(2)  # Exit code 2 blocks execution

    # Allow execution
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Configuration**:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash.*",
        "hooks": [
          {
            "type": "command",
            "command": "python scripts/validate_bash.py"
          }
        ]
      }
    ]
  }
}
```

### File Access Control

Restrict file operations to project boundaries.

**Bash implementation**:

```bash
#!/bin/bash
# Validate file operations stay within project boundaries

PROJECT_DIR="${CLAUDE_PROJECT_DIR}"
TOOL_ARGS="${CLAUDE_TOOL_ARGS}"

# Extract file path from tool arguments
# This varies by tool - Write, Edit, Read each have different formats
FILE_PATH=$(echo "$TOOL_ARGS" | jq -r '.file_path // .path // empty')

if [ -z "$FILE_PATH" ]; then
    # No file path found, allow operation
    exit 0
fi

# Resolve absolute path
RESOLVED_PATH=$(realpath "$FILE_PATH" 2>/dev/null)

# Check if path is within project directory
if [[ ! "$RESOLVED_PATH" =~ ^"$PROJECT_DIR" ]]; then
    echo '{"block": true, "message": "File access outside project directory denied"}'
    exit 2
fi

# Allow operation
exit 0
```

**Configuration**:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "(Write|Edit|Read).*",
        "hooks": [
          {
            "type": "command",
            "command": "bash scripts/validate_file_access.sh"
          }
        ]
      }
    ]
  }
}
```

### Credential Protection

Prevent accidental credential commits.

**Python implementation**:

```python
#!/usr/bin/env python3
"""Prevent credential commits"""
import os
import re
import sys
import json

def check_for_credentials(content):
    """Scan content for credential patterns"""

    credential_patterns = [
        (r'aws_access_key_id\s*=\s*[A-Z0-9]{20}', 'AWS Access Key'),
        (r'aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}', 'AWS Secret Key'),
        (r'["\']?api[_-]?key["\']?\s*[:=]\s*["\'][^"\']+["\']', 'API Key'),
        (r'["\']?password["\']?\s*[:=]\s*["\'][^"\']+["\']', 'Password'),
        (r'Bearer\s+[A-Za-z0-9\-._~+/]+=*', 'Bearer Token'),
        (r'ghp_[A-Za-z0-9]{36}', 'GitHub Personal Access Token'),
        (r'sk-[A-Za-z0-9]{48}', 'OpenAI API Key'),
    ]

    findings = []
    for pattern, name in credential_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            findings.append({
                'type': name,
                'pattern': pattern,
                'sample': match.group(0)[:20] + '...'
            })

    return findings

def main():
    tool_args = os.environ.get('CLAUDE_TOOL_ARGS', '')
    tool_name = os.environ.get('CLAUDE_TOOL_NAME', '')

    # Only check Write and Edit operations
    if tool_name not in ['Write', 'Edit']:
        sys.exit(0)

    # Parse arguments to get content
    try:
        args = json.loads(tool_args)
        content = args.get('content', '') or args.get('new_string', '')
    except:
        sys.exit(0)

    # Check for credentials
    findings = check_for_credentials(content)

    if findings:
        result = {
            "block": True,
            "message": "Potential credentials detected in file",
            "findings": findings
        }
        print(json.dumps(result, indent=2))
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Integration Patterns

### Command + Hook Integration

Hooks can validate command execution automatically.

**Command**: `/commit [message]`

```markdown
---
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(git status:*)
argument-hint: [commit message]
---

Create git commit with message: $ARGUMENTS
```

**Hook**: Validate commit message format

```python
#!/usr/bin/env python3
"""Validate commit message format"""
import os
import re
import sys
import json

def validate_commit_message(command):
    """Check commit message follows conventions"""

    # Extract message from git commit command
    match = re.search(r'git\s+commit.*-m\s+["\']([^"\']+)["\']', command)
    if not match:
        return []

    message = match.group(1)
    issues = []

    # Check format: [scope] description
    if not re.match(r'^\[[\w-]+\]\s+[a-z]', message):
        issues.append("Format must be: [scope] lowercase description")

    # Check length
    if len(message) > 72:
        issues.append("Commit message too long (max 72 chars)")

    # Check for trailing period
    if message.endswith('.'):
        issues.append("No trailing period allowed")

    return issues

def main():
    tool_args = os.environ.get('CLAUDE_TOOL_ARGS', '')

    issues = validate_commit_message(tool_args)

    if issues:
        result = {
            "block": True,
            "message": "Commit message validation failed",
            "issues": issues,
            "hint": "Format: [scope] lowercase description (max 72 chars, no period)"
        }
        print(json.dumps(result, indent=2))
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Configuration**:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash.*git commit.*",
        "hooks": [
          {
            "type": "command",
            "command": "python scripts/validate_commit.py"
          }
        ]
      }
    ]
  }
}
```

### Agent + Hook Coordination

Hooks work automatically with agent-invoked tools.

**Agent**: `secure-developer.md`

```markdown
---
name: secure-developer
description: Development with automatic security validation
tools: Write, Edit, Bash
---

<security_integration>
This agent works with security hooks to:

- Validate all file operations against project boundaries
- Check code for security patterns
- Ensure compliance with project policies
- Prevent credential leaks
  </security_integration>

<workflow>
All code changes will be automatically validated by security hooks.
You can focus on implementation - security checks run automatically.
If validation fails, you'll receive specific feedback to address.
</workflow>

Proceed with development tasks. Security validation is automatic.
```

**Hooks**: Automatic validation

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash.*",
        "hooks": [
          { "type": "command", "command": "python scripts/validate_bash.py" }
        ]
      },
      {
        "matcher": "(Write|Edit).*",
        "hooks": [
          {
            "type": "command",
            "command": "bash scripts/validate_file_access.sh"
          },
          {
            "type": "command",
            "command": "python scripts/check_credentials.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write.*\\.(ts|js|tsx|jsx)$",
        "hooks": [
          { "type": "command", "command": "prettier --write $CLAUDE_TOOL_ARGS" }
        ]
      }
    ]
  }
}
```

**Result**: Agent operates normally, hooks enforce security automatically.

---

## Hook Response Format

Hooks communicate results via JSON output and exit codes.

### Success (Allow Operation)

**Exit code**: 0

**Output**: Optional (not shown to user)

```bash
#!/bin/bash
# Validation passed
exit 0
```

### Block Operation

**Exit code**: 2

**Output**: JSON with block information (shown to user)

```python
import json
import sys

result = {
    "block": True,
    "message": "Operation blocked: Security violation",
    "details": "Detailed explanation of why operation was blocked",
    "suggestion": "How to fix the issue"
}

print(json.dumps(result, indent=2))
sys.exit(2)
```

### Provide Information

**Exit code**: 0

**Output**: Text information (shown to user)

```bash
#!/bin/bash
echo "Validation passed with warnings:"
echo "- Consider using const instead of let"
echo "- Add error handling for async operations"
exit 0
```

---

## Testing & Debugging

### Manual Testing

```bash
# Set environment variables manually
export CLAUDE_TOOL_NAME="Bash"
export CLAUDE_TOOL_ARGS="rm -rf /"
export CLAUDE_PROJECT_DIR="/home/user/project"

# Run hook script
python scripts/validate_bash.py
echo "Exit code: $?"
```

### Debug Mode

Add debug logging to hooks:

```python
#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path

# Debug logging
DEBUG = os.environ.get('HOOK_DEBUG', 'false').lower() == 'true'

def debug_log(message):
    if DEBUG:
        debug_file = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')) / '.hook_debug.log'
        with open(debug_file, 'a') as f:
            f.write(f"{message}\n")

def main():
    debug_log(f"Tool: {os.environ.get('CLAUDE_TOOL_NAME')}")
    debug_log(f"Args: {os.environ.get('CLAUDE_TOOL_ARGS')}")

    # Hook logic here...

    sys.exit(0)

if __name__ == "__main__":
    main()
```

Enable debug mode:

```bash
export HOOK_DEBUG=true
```

### Validation Checklist

Before deploying hooks:

```markdown
✓ Matcher patterns are accurate and specific
✓ Hook scripts are executable (chmod +x)
✓ Hook commands are tested manually
✓ Security implications reviewed
✓ Error handling is robust
✓ Performance impact is minimal
✓ Exit codes are correct (0 or 2)
✓ JSON output is valid when blocking
✓ Environment variables are accessed correctly
✓ Integration points are validated
✓ Documentation is complete
✓ Rollback procedures exist
```

---

## Common Issues

### Hook Not Triggering

**Causes**:

- Matcher pattern doesn't match tool usage
- Settings.json syntax error
- Hook script not executable
- Wrong event type (PreToolUse vs PostToolUse)

**Debug**:

```bash
# Check settings.json syntax
jq . .claude/settings.json

# Verify matcher with tool name
echo "ToolName: Bash"
echo "Pattern: Bash.*"
# Should match

# Check script permissions
ls -l scripts/hook.sh
chmod +x scripts/hook.sh
```

### Hook Blocking Unexpectedly

**Causes**:

- Hook script error causes exit code 2
- Validation logic too strict
- Environment variable not available
- Path resolution issues

**Debug**:

```bash
# Test hook directly
bash -x scripts/hook.sh

# Check exit code
echo $?

# Add error logging to hook
```

### Performance Impact

**Causes**:

- Hook does expensive operations
- Multiple hooks on same event
- Hook doesn't exit quickly
- External API calls in hook

**Solutions**:

- Cache results when possible
- Run expensive operations async
- Optimize validation logic
- Use timeout mechanisms

---

## Best Practices

1. **Minimal Processing**: Hooks should be fast (<100ms)
2. **Clear Feedback**: Blocked operations should explain why
3. **Graceful Degradation**: Handle missing environment gracefully
4. **Idempotent**: Safe to run multiple times
5. **Tested**: Thoroughly test before deployment
6. **Documented**: Explain hook purpose and behavior
7. **Specific Matchers**: Target specific tools, not all
8. **Error Handling**: Catch and handle errors appropriately

---

**See Also**:

- [commands.md](./commands.md) - Command+hook integration
- [agents.md](./agents.md) - Agent+hook coordination
- [patterns.md](./patterns.md) - Hook in workflow patterns
- [templates.md](./templates.md) - Hook script examples
