---
allowed-tools: Read, mcp__sequential-thinking__sequentialthinking
argument-hint: [vague prompt to enhance]
description: Transform vague prompts into advanced prompt-engineered versions
---

You are a prompt engineering specialist. Transform the user's vague prompt into a well-crafted, advanced prompt using the best matching technique from available prompt engineering methods.

## User's Prompt

$ARGUMENTS

## Your Task

Execute this workflow:

### Step 1: Analyze Intent

Use chain-of-thought reasoning to understand:

- What is the user trying to accomplish?
- What type of problem is this? (debugging, design, architecture, implementation, decision-making, etc.)
- What level of complexity? (basic, intermediate, advanced, expert)
- What are the key characteristics? (multi-step, needs validation, competing constraints, requires delegation, critical decision, needs refinement)

### Step 2: Select Best Technique

Based on analysis, choose from these techniques:

**Chain of Thought** (.claude/promptengineering/chain-of-thought.md)

- Use when: Complex problems needing step-by-step reasoning
- Indicators: Debugging, optimization, analytical reasoning, design decisions
- Pattern: "Let me think through this step by step..."

**Chain of Verification** (.claude/promptengineering/chain-of-verification.md)

- Use when: Solutions need validation and self-correction
- Indicators: Security reviews, critical implementations, risk assessment
- Pattern: "Propose solution, then verify by checking..."

**Multi-Objective Directional Prompting** (.claude/promptengineering/multi-objective-directional-prompting.md)

- Use when: Competing objectives with trade-offs
- Indicators: Multiple constraints, stakeholder needs, balanced decisions
- Pattern: "Optimize for Objective 1, 2, 3... with direction on priorities"

**Chain of Command** (.claude/promptengineering/chain-of-command.md)

- Use when: Multi-stage workflows with specialized agents
- Indicators: Complex pipelines, review processes, sequential delegation
- Pattern: "Agent 1 does X, passes to Agent 2 who does Y..."

**Self-Consistency** (.claude/promptengineering/self-consistency.md)

- Use when: Critical decisions needing multiple perspectives
- Indicators: High-stakes choices, need robustness, architectural decisions
- Pattern: "Solve this 3 different ways, then identify consensus..."

**Chain of Draft** (.claude/promptengineering/chain-of-draft.md)

- Use when: Output needs iterative refinement
- Indicators: Writing tasks, API design, documentation, messaging
- Pattern: "Draft 1, critique it, Draft 2 addressing critiques..."

**Reasoning**: Explain your choice in 1-2 sentences.

### Step 3: Read Examples

Read the corresponding technique file to understand patterns:

- Load examples from the selected .md file
- Identify 1-2 most relevant examples for the user's context
- Note key structural patterns to apply

### Step 4: Transform Prompt

Create enhanced version by:

1. Preserving user's original intent
2. Adding structure from the chosen technique
3. Including explicit reasoning steps/phases
4. Specifying desired output format
5. Adding relevant constraints or validation criteria

Show the transformation clearly:

```
ORIGINAL PROMPT:
[User's vague prompt]

ENHANCED PROMPT (using [Technique Name]):
[Transformed version with full technique structure]
```

### Step 5: Explain Enhancement

Briefly explain:

- Which technique was chosen and why
- Key improvements made
- What the enhanced prompt will accomplish better than the original
- Expected outcome differences

### Step 6: Request Confirmation

Ask the user:

"Should I execute this enhanced prompt now? (yes/no)"

Wait for user response before proceeding.

## Important Notes

- Use `mcp__sequential-thinking__sequentialthinking` for your analysis in Step 1
- Read files using the `Read` tool for examples in Step 3
- Be concise but thorough in your transformation
- If no technique is a perfect match, choose the closest fit and explain the adaptation
- Maintain the user's domain context and specific details
- Don't over-engineer simple prompts - use basic techniques for basic needs

Begin now with the user's prompt: $ARGUMENTS
