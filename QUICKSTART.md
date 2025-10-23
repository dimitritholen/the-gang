# Feature Analysis Workflow - Quick Start

Get started in 60 seconds.

## Installation

```bash
# 1. Install code-tools CLI
cd tools && pip install -e .[web]

# 2. Verify installation
code-tools --help
```

## Usage

### Analyze Complete Feature (Recommended)

```bash
/analyze-feature "your feature description here"
```

This runs the entire workflow and produces all artifacts.

### Individual Commands

```bash
# Just requirements
/gather-requirements "feature description"

# Just tech research (requires requirements first)
/research-tech "feature-slug"

# Just implementation planning (requires requirements + tech)
/plan-implementation "feature-slug"

# Just scope validation (requires all above)
/validate-scope "feature-slug"
```

## What You Get

After `/analyze-feature` completes, find these files in `.claude/memory/`:

| File | Contains | Use For |
|------|----------|---------|
| `requirements-{feature}.md` | Complete requirements spec | Understanding what to build |
| `tech-analysis-{feature}.md` | Tech recommendations | Stack decisions |
| `implementation-plan-{feature}.md` | Task breakdown (WBS) | Sprint planning |
| `scope-validation-{feature}.md` | Scope verification | MVP definition |
| `feature-brief-{feature}.md` | Executive summary | Stakeholder communication |
| `checklist-{feature}.md` | Implementation checklist | Development tracking |

## Example

```bash
# Analyze a feature
/analyze-feature "Add real-time collaborative editing to documents"

# Review outputs
ls .claude/memory/

# Read the feature brief
cat .claude/memory/feature-brief-collaborative-editing.md

# Start implementation using checklist
cat .claude/memory/checklist-collaborative-editing.md
```

## Tips

**Provide specific feature descriptions**:
- ✅ "Add OAuth2 login with Google and GitHub providers, including account linking"
- ❌ "Add login"

**Answer questions thoroughly**:
- The requirements phase asks 15-20 questions
- Detailed answers = better downstream analysis

**Review scope validation**:
- Always check `.claude/memory/scope-validation-{feature}.md`
- It catches feature creep and over-engineering

## Need Help?

See [README.md](.claude/README.md) for complete documentation.

**Most common question**: "How do I use existing requirements?"

Answer: Just reference the feature slug:
```bash
# If requirements-api-caching.md already exists
/research-tech "api-caching"
```

The agent will automatically load existing requirements from memory.
