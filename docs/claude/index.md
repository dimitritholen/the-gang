# Claude Code Documentation Index

## Purpose

This directory contains comprehensive documentation for implementing Claude Code extensions including slash commands, sub-agents, hooks, and advanced workflow patterns. All documentation is written for AI model consumption with detailed, structured content optimized for reasoning and code generation.

---

## Quick Navigation

### What Do You Need?

**Creating a repeatable command or workflow?**
→ Read [commands.md](./commands.md) - Slash commands with argument handling and security

**Building a specialized AI assistant?**
→ Read [agents.md](./agents.md) - Sub-agent design, prompt engineering, and model selection

**Validating or automating tool usage?**
→ Read [hooks.md](./hooks.md) - Event-driven architecture and security validation

**Designing multi-step or complex workflows?**
→ Read [patterns.md](./patterns.md) - Advanced patterns, orchestration, and optimization

**Need ready-to-use templates or troubleshooting help?**
→ Read [templates.md](./templates.md) - Complete examples and validation checklists

---

## File Structure Overview

```
docs/claude/
├── index.md         # This file - navigation and quick reference
├── commands.md      # Slash commands implementation (~140 lines)
├── agents.md        # Sub-agents design & prompting (~260 lines)
├── hooks.md         # Event-driven architecture (~175 lines)
├── patterns.md      # Advanced workflows (~175 lines)
└── templates.md     # Examples & troubleshooting (~350 lines)
```

---

## Documentation Summaries

### [commands.md](./commands.md) - Slash Commands Implementation

**When to read**: Creating user-invocable commands, automating repetitive tasks, building project-specific operations

**Key topics**:
- YAML frontmatter structure and configuration
- `allowed-tools` security restrictions
- `argument-hint` and argument handling patterns ($ARGUMENTS, $1, $2)
- Input validation and security best practices
- Real-world examples: Git workflows, React components, API endpoints

**Typical use cases**:
- `/commit [message]` - Structured git commits
- `/component [name]` - Code generation
- `/deploy [env]` - Deployment automation

---

### [agents.md](./agents.md) - Sub-Agents Design & Prompt Engineering

**When to read**: Building specialized AI assistants, implementing domain expertise, coordinating complex tasks

**Key topics**:
- Architecture principles (separate context, tool access control)
- Role definition techniques (expertise-based, process-based)
- Model selection (Haiku vs Sonnet vs Opus)
- Tool access patterns (minimal to full)
- Advanced prompt engineering (structured thinking, OODA loops)
- Multi-agent coordination rules

**Typical use cases**:
- Security auditor agents with OWASP expertise
- Backend architect for system design
- Research specialists for information gathering
- Code reviewers with focused expertise

---

### [hooks.md](./hooks.md) - Hooks & Event-Driven Architecture

**When to read**: Validating tool usage, automating pre/post-processing, enforcing security policies, integrating components

**Key topics**:
- Hook configuration in `.claude/settings.json`
- Event types: PreToolUse, PostToolUse, UserPromptSubmit, Stop
- Security patterns (input validation, file access control)
- Integration with commands and agents
- Environment variables (CLAUDE_TOOL_ARGS, CLAUDE_PROJECT_DIR)

**Typical use cases**:
- Validate bash commands before execution
- Auto-format code after file writes
- Enforce project-specific conventions
- Security validation and access control

---

### [patterns.md](./patterns.md) - Advanced Patterns & Workflows

**When to read**: Orchestrating multi-agent workflows, optimizing performance, building complex systems

**Key topics**:
- Decision trees: When to create command vs agent vs hook
- Multi-agent workflows (research lead, code review pipeline)
- Workflow orchestration (command+agent patterns)
- Performance optimization (parallel execution, context management)
- Progressive enhancement strategies

**Typical use cases**:
- Research coordination with specialized subagents
- Multi-stage code review pipelines
- Feature development workflows
- Incremental codebase improvements

---

### [templates.md](./templates.md) - Template Library & Troubleshooting

**When to read**: Need working examples, debugging issues, validating implementations, following best practices

**Key topics**:
- Essential command templates (Git, code generation, migrations)
- Essential agent templates (developers, specialists, analysts)
- Troubleshooting common issues
- Validation checklists (command, agent, hook)
- Testing strategies and validation scripts
- Best practices summary

**Typical use cases**:
- Copy-paste starting points for new commands/agents
- Debug why commands aren't executing
- Validate configuration syntax
- Optimize existing implementations

---

## Decision Trees

### What Should I Create?

```
USER NEEDS:
│
├─ Repeatable action with specific arguments?
│  └─> CREATE SLASH COMMAND → Read commands.md
│
├─ Specialized expertise or domain knowledge?
│  └─> CREATE SUB-AGENT → Read agents.md
│
├─ Validate or modify tool usage automatically?
│  └─> CREATE HOOK → Read hooks.md
│
└─ Complex multi-step coordination?
   └─> CREATE WORKFLOW PATTERN → Read patterns.md + agents.md
```

### Where Do Files Go?

```
Project Level:
├── .claude/
│   ├── commands/          # Slash commands (.md files)
│   ├── agents/            # Sub-agents (.md files)
│   └── settings.json      # Hooks configuration

User Level:
├── ~/.claude/
│   ├── commands/          # Personal commands
│   └── agents/            # Personal agents
```

---

## Reading Strategies for AI Models

### Quick Lookup (Single Question)
1. Use this index to identify relevant file
2. Read only that file (~140-350 lines)
3. Extract specific section needed

### Implementation Task (Create Something New)
1. Read relevant file completely (commands.md OR agents.md OR hooks.md)
2. Optionally read templates.md for starting point
3. Reference patterns.md if coordination needed

### Complex Integration (Multi-Component)
1. Read patterns.md first for architecture guidance
2. Read specific implementation files (commands.md, agents.md, hooks.md)
3. Reference templates.md for validation checklist

### Troubleshooting (Something Not Working)
1. Read templates.md troubleshooting section first
2. Deep-dive into relevant implementation file
3. Check patterns.md for integration issues

---

## Cross-Reference Map

**Commands ↔ Agents**: See patterns.md for command+agent workflows
**Commands ↔ Hooks**: See hooks.md for command+hook integration
**Agents ↔ Hooks**: See hooks.md for agent+hook coordination
**All Components**: See patterns.md for orchestration examples

---

## Version & Maintenance

**Source**: Derived from `command-and-agents.md` (1157 lines)
**Split Date**: 2025-10-23
**Target Audience**: AI models (Claude, GPT, etc.)
**Verbosity Level**: Preserved from original - detailed for model reasoning

---

## Getting Started

**New to Claude Code extensions?**
1. Read this index completely
2. Read [patterns.md](./patterns.md) sections 1-2 for overview
3. Pick your task type and read relevant file
4. Use [templates.md](./templates.md) for working examples

**Need to create something specific?**
- Jump directly to relevant file using Quick Navigation above
- Use Decision Trees to confirm file choice
- Reference templates.md for starting code

**Troubleshooting existing code?**
- Start with [templates.md](./templates.md) troubleshooting section
- Use validation checklists to identify issues
- Deep-dive into implementation file for specifics
