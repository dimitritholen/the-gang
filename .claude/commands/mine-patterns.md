---
allowed-tools: Task, Grep, Glob
argument-hint: --type [pattern-type]
description: Extract recurring patterns from codebase
---

## Purpose

Automatically identify and document dominant patterns in specific areas (error handling, state management, API design, etc.).

## Usage

```bash
/mine-patterns --type "error-handling"
/mine-patterns --type "state-management"
/mine-patterns --type "api-design"
/mine-patterns --type "testing"
```

## Process

1. **Grep for pattern** (e.g., catch blocks for error handling)
2. **Analyze frequency** of each pattern variant
3. **Calculate dominance** (which pattern is most common?)
4. **Generate recommendation** (standardize on dominant pattern)
5. **Update coding-conventions.md** automatically

## Example Output

```markdown
## Pattern Mining: Error Handling

**Analyzed**: 45 error handling blocks

**Patterns Detected**:
1. Toast notifications: 27 instances (60%) ← DOMINANT
2. Console.error: 13 instances (29%)
3. Throw to caller: 5 instances (11%)

**Recommendation**: Standardize on toast notifications

**Updated**: coding-conventions.md section "Error Handling"

**Deviations to Fix**: 18 instances (40%)
- src/services/backgroundJob.ts:45 (console.error)
- src/utils/parser.ts:78 (throw)
- [... 16 more]
```

## Supported Pattern Types

- `error-handling`: How errors are handled
- `state-management`: Local vs global state patterns
- `api-design`: REST conventions, response formats
- `testing`: Test structure, mocking strategies
- `imports`: Import order and style
- `exports`: Named vs default exports
- `naming`: Variable/function naming patterns
