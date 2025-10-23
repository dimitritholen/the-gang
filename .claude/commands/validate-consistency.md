---
allowed-tools: Task, Read
argument-hint: [feature-slug]
description: Validate new feature plan against existing conventions
---

## Purpose

Check if a new feature's implementation plan aligns with existing codebase conventions before implementation.

## Usage

```bash
/validate-consistency "user-authentication"
```

## Process

1. **Load memory artifacts** (coding-conventions.md, architecture-decisions.md)
2. **Load feature plan** (implementation-plan-{feature}.md)
3. **Compare against conventions**:
   - File naming matches pattern?
   - Directory structure follows convention?
   - Error handling uses dominant pattern?
   - API design follows REST conventions?
   - Testing strategy matches pyramid?

4. **Generate consistency report** with severity:
   - 🔴 **Critical**: Violates core architectural decision
   - 🟠 **Warning**: Deviates from convention (80%+ conformance)
   - 🟡 **Info**: Minor deviation (acceptable)
   - 🟢 **Compliant**: Fully matches conventions

## Output

```markdown
## Consistency Validation: {feature}

**Overall Score**: 85/100

### Critical Issues (Must Fix)
- None

### Warnings (Should Fix)
- Error handling uses `throw` instead of `toast` (convention: 60% use toast)
- File naming: `user-auth.ts` should be `userAuth.ts` (convention: camelCase 95%)

### Info (Consider)
- Testing: Only unit tests planned, no integration tests (convention: test pyramid)

### Compliant
- ✅ API endpoints follow /api/v1/{resource} pattern
- ✅ Directory structure matches feature-based organization
- ✅ TypeScript strict mode enabled

**Recommendation**: Fix 2 warnings before implementation
```
