# Prompt Engineering Reference for AI Agents

**Purpose:** Comprehensive reference for AI agents to understand and apply effective prompt engineering techniques across software development workflows.

**Last Updated:** 2025-10-23

---

## Core Principles

### Clarity and Specificity

- Provide explicit context, instructions, and constraints
- Avoid vague or ambiguous requests
- State desired output format explicitly
- Include relevant requirements and constraints

**Example:**

```
Generate 5 test cases for a REST API handling user authentication, including:
- Edge cases for invalid credentials
- Token expiration scenarios
- Rate limiting behavior
- Format: preconditions, steps, expected response codes, validation checks
```

### Structure and Formatting

#### Markdown Formatting

- Use headings to separate sections
- Employ bullet points for lists
- Apply code blocks for examples
- Leverage emphasis for key terms

#### XML-Like Tags (Claude-optimized)

```xml
<context>
  Project requirements and constraints
</context>

<task>
  Specific action to perform
</task>

<constraints>
  Limitations and guidelines
</constraints>

<output_format>
  Expected response structure
</output_format>
```

**Best Practice:** Structured prompts (Markdown or XML) significantly outperform unstructured text.

### Context Management

- Provide sufficient but focused background information
- Include relevant code, specifications, or prior decisions
- Balance completeness with conciseness
- Reference specific sources when applicable

**Prompt Length Guidelines:**

- Short prompts: Risk insufficient context
- Long prompts: Risk diluted focus and recency bias
- Optimal: Rich but focused (quality > quantity)
- Use RAG for extensive documentation needs

### Role Assignment

Set AI perspective through role prompting:

- "Act as a senior software engineer specialized in security testing"
- "You are a business analyst helping define software requirements"
- "As an Agile coach specialized in value prioritization"

**Effect:** Focuses responses on relevant expertise domain.

---

## Advanced Techniques

### Chain-of-Thought (CoT)

Request step-by-step reasoning before conclusions:

```
Think through this problem step by step:
1. Identify the core issue
2. List possible approaches
3. Evaluate trade-offs
4. Provide final recommendation with justification
```

**Benefits:**

- Reduces reasoning errors
- Enables error detection in logic
- Produces more complete answers

### Chain-of-Verification (CoVe)

Self-verification loop:

```
1. Provide initial answer
2. Generate verification questions
3. Answer verification questions
4. Revise initial answer based on checks
5. Provide final validated response
```

**Improvement:** Up to 23% better accuracy vs. standard prompting.

### Step-Back Prompting

Abstract before specific:

```
1. What are the key factors in this problem domain?
2. What general principles apply?
3. Now solve the specific problem using these insights
```

**Improvement:** Up to 36% better accuracy on complex problems.

### Few-Shot Prompting

Provide 1-3 examples of desired input/output:

```
Example 1:
Input: [sample]
Output: [desired format]

Example 2:
Input: [sample]
Output: [desired format]

Now process:
Input: [actual task]
```

**Use Cases:**

- Establishing output format consistency
- Demonstrating desired level of detail
- Training on domain-specific patterns

---

## Hallucination Prevention

### Primary Strategies

1. **Crystal-Clear Instructions**
   - Remove ambiguity
   - Provide complete context
   - Specify known sources explicitly
   - Use "According to [source]..." phrasing

2. **Task Decomposition**
   - Break complex questions into sub-questions
   - Process sequentially
   - Validate each step before proceeding

3. **Retrieval-Augmented Generation (RAG)**
   - Provide relevant documentation in prompt
   - Reference specific authoritative sources
   - Use "Based on the following document..." patterns

4. **Output Constraints**
   - Limit response length to force focus
   - Request source citations
   - Ask for uncertainty acknowledgment

5. **Reasoning Chains**
   - Use CoT to expose logic
   - Request verification of assumptions
   - Check consistency with established facts

6. **Validation Prompts**

   ```
   Review the above response:
   - Identify any assumptions not grounded in provided context
   - Flag statements lacking source evidence
   - Note areas of uncertainty
   ```

### Model-Specific Considerations

**GPT-5:**

- Improved instruction-following vs. predecessors
- Still requires clear prompts for best results
- Enhanced tool use and steerability

**Claude 4.5:**

- Prefers XML-like structure
- Strong coding capabilities
- Better prompt injection resistance
- Reduced sycophantic behavior

---

## SDLC Application

### Requirements Gathering

**Role Setup:**

```
You are a requirements analyst. Ask comprehensive questions to gather:
- Project goals and target users
- Key features and constraints
- Performance, security, timeline requirements
- Success criteria

Ask iteratively until complete understanding achieved.
```

**Output:** Structured requirements specification list.

### Technology Stack Research

**Research Prompt:**

```
Given requirements: {summary}

Provide 2-3 technology stack options with:
- Recommended languages, frameworks, tools
- Justification for each choice
- Pros/cons analysis
- Alignment with requirements (scalability, security, team expertise)
- Known industry examples
```

**Validation:** Always verify AI recommendations against official documentation.

### Memory and Context Artifacts

**Summarization:**

```
Summarize project context:
- Agreed requirements (bullet list)
- Chosen tech stack
- Key constraints
- Success criteria
- Coding standards

Format for injection into future prompts.
```

**Usage:** Prepend summary to all subsequent phase prompts to maintain consistency.

### Task Breakdown and Dependencies

**Decomposition Prompt:**

```
Break project into:
1. Major components/phases
2. Specific tasks per component
3. Task dependencies (prerequisite identification)
4. Logical sequencing
5. Time estimates (if applicable)

Output as structured markdown list with dependency tags.
```

**Output Structure:**

```markdown
## Phase 1: Database Design
- Task 1.1: Define schema [No dependencies]
- Task 1.2: Create migrations [Depends: 1.1]

## Phase 2: API Development
- Task 2.1: Implement auth endpoint [Depends: 1.2]
```

### Development Prompts

**Task-Specific Coding:**

```
Context: {previous decisions, schema, standards}

Implement: [specific feature/function]

Requirements:
- Tech stack: {chosen technologies}
- Follow coding standards: {standards}
- Include error handling
- Add tests
- Output format: code only in markdown blocks
```

**Iterative Approach:**

```
1. Request implementation plan
2. Review and approve plan
3. Request code implementation
4. Review code
5. Request refinements if needed
```

### UX/UI Design

**Research Phase:**

```
As a UX designer, provide:
- Best practices for {application type}
- Relevant design principles (e.g., Nielsen's heuristics)
- Common design patterns for {features}
- Accessibility considerations (WCAG)
- Responsive design guidelines
```

**Design Phase:**

```
Create UI specification for {screens}:
- Layout descriptions
- Key elements and interactions
- Alignment with UX best practices
- Accessibility compliance
- Responsive behavior

Optional: Generate code for {framework} following {design system}
```

### Testing and QA

**Test Generation:**

```
Generate test cases for {feature}:
- Typical/happy path scenarios
- Edge cases
- Error conditions
- Input validation tests
- Performance scenarios

Format as {test framework} code with:
- Clear test names
- Setup/teardown
- Assertions
- Test data
```

**Code Review:**

```
Act as senior code reviewer. Analyze for:
- Security vulnerabilities (SQL injection, XSS, etc.)
- Performance bottlenecks
- Style guide adherence
- Best practice violations
- Maintainability issues

Provide specific findings and fixes.
```

---

## Role-Specific Guidance

### Developers

**Context Requirements:**

- Function declarations, class interfaces
- Module architecture
- Language, framework, version
- Existing codebase patterns

**Validation Prompts:**

```
Generate unit tests for above function
Check edge case handling (null, empty, boundary values)
Verify compliance with {coding standard}
```

### Testers/QA

**Test Case Generation:**

```
For {feature}, provide test cases covering:
- Functional requirements (positive/negative)
- Boundary conditions
- Error handling
- Integration points
- Performance criteria

Format: ID, Title, Preconditions, Steps, Expected Result
```

**Bug Analysis:**

```
Analyze error: {stack trace / description}

Provide:
- Possible root causes
- Steps to reproduce
- Expected vs actual behavior
- Suggested fixes
- Impact assessment
```

**Risk Assessment:**

```
Analyze {feature} for risks:
- Technical risks (scalability, security, performance)
- UX risks
- Integration risks

Provide: Impact, Probability, Mitigation suggestions
```

### Scrum Masters/Agile Teams

**User Story Refinement:**

```
Refine user story using INVEST criteria:
"{story}"

Add:
- Clear acceptance criteria
- Missing details
- Testability requirements
- Dependencies
```

**Backlog Prioritization:**

```
As Agile coach, prioritize these stories by:
- Business value
- Risk
- Dependencies
- Delivery speed

Provide ranking with justification.
```

**Sprint Planning:**

```
Break down story: "{description}"

Provide:
- Subtasks with estimates
- Missing requirements
- Technical dependencies
- Team capacity considerations
```

---

## Best Practices Summary

### Prompt Construction Checklist

- [ ] Clear, specific instructions
- [ ] Sufficient context provided
- [ ] Output format specified
- [ ] Constraints explicitly stated
- [ ] Role assigned (if applicable)
- [ ] Examples included (for complex tasks)
- [ ] Validation criteria defined

### Quality Control

- [ ] Verify AI outputs against sources
- [ ] Check consistency across multiple queries
- [ ] Request reasoning/justification
- [ ] Validate against requirements
- [ ] Test edge cases
- [ ] Review for hallucinations

### Scope Management

- [ ] Reiterate core vision in prompts
- [ ] Explicit scope constraints
- [ ] Flag out-of-scope additions
- [ ] Compare outputs against requirements
- [ ] Defer "nice-to-haves" to Phase 2

### Coding Standards

- [ ] Provide style guide in prompt
- [ ] Reference best practices
- [ ] Request adherence checks
- [ ] Use role prompting for expertise
- [ ] Validate generated code

---

## Common Anti-Patterns

### Avoid

- ❌ Vague, open-ended questions
- ❌ Missing context
- ❌ Unstructured prompts
- ❌ Assuming AI knows your codebase
- ❌ Accepting first output without verification
- ❌ Mixing multiple concerns in one prompt
- ❌ Ignoring inconsistent responses
- ❌ Omitting output format requirements

### Prefer

- ✅ Specific, constrained requests
- ✅ Rich contextual information
- ✅ Structured (Markdown/XML) prompts
- ✅ Explicit context provision
- ✅ Iterative refinement
- ✅ Single-concern prompts
- ✅ Validation through re-asking
- ✅ Clear format specifications

---

## Prompt Templates

### Generic Code Generation

```markdown
## Context
{Project background, tech stack, relevant code}

## Task
Implement {specific functionality}

## Requirements
- Language/Framework: {specifics}
- Input: {parameters}
- Output: {return type/format}
- Constraints: {performance, security, style}

## Standards
{Coding guidelines, best practices}

## Output Format
Code only in ```language blocks, with inline comments for complex logic
```

### Code Review Template

```markdown
## Role
Act as {expertise level} {specialty} developer

## Code to Review
```{language}
{code block}
```

## Review Criteria

- Security: {specific concerns}
- Performance: {specific concerns}
- Style: {guide reference}
- Best Practices: {specific patterns}

## Output Format

- Issue: {description}
- Severity: {High/Medium/Low}
- Location: {line/function}
- Fix: {specific recommendation}

```

### Requirements Elicitation
```markdown
## Role
Software requirements analyst

## Context
{Brief project description}

## Task
Ask comprehensive questions to gather:
1. Functional requirements
2. Non-functional requirements
3. Constraints
4. Success criteria
5. Target users
6. Technical considerations

## Output
Structured requirements document with categorized lists
```

---

## References

### Key Sources

- SUSE AI Documentation (Hallucination Prevention)
- OpenAI GPT-5 Prompting Guide
- Anthropic Claude 4.5 Documentation
- PromptHub Research (CoVe, Step-Back techniques)
- Software Testing Prompt Engineering (aqua-cloud.io)
- Agile/Scrum AI Integration (DZone)
- Product Management (Feature Creep Prevention)
- Code Review AI Optimization (BytePlus)

### Further Reading

- Chain-of-Thought Prompting (academic research)
- XML vs Markdown Performance (Medium)
- Test-Driven Prompt Engineering (Promptimize)
- Long Prompt Disadvantages (PromptLayer)
- Memory Management in LLM Conversations (OpenAI Community)

---

## Version History

- **2025-10-23**: Initial consolidated version from effective-prompt-engineering.md and Prompt-Engineering-for-Complete-SDLC-Workflow.md
