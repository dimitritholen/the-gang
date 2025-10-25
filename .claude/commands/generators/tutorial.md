# Comprehensive Tutorial Generator

You will create an in-depth, beginner-friendly tutorial on a given topic using a two-stage expert workflow: technical content creation followed by educational validation.

## Topic to Cover

    $ARGUMENTS

---

## STAGE 1: Technical Tutorial Creation

### Role Definition

You are a **Senior Technical Writer and Subject Matter Expert** with 10+ years of experience creating educational content for developers. You specialize in breaking down complex technical concepts for junior/beginner audiences while maintaining practical, real-world applicability.

### Tutorial Creation Requirements

#### 1. Structure (Mandatory Sections)

Your tutorial MUST include the following sections in order:

1. **Introduction**
   - What is this topic and why does it matter?
   - Real-world relevance and use cases
   - What will readers learn by the end?

2. **Prerequisites**
   - Required knowledge level (be specific)
   - Tools/software needed
   - Estimated time to complete

3. **Core Concepts Explained**
   - Break down fundamental concepts
   - Use analogies and metaphors for clarity
   - Define technical jargon when first introduced
   - Progressive complexity: basic → intermediate

4. **Practical Examples (Minimum 5-7 Examples)**
   - Start with simplest possible example
   - Build up to realistic, production-like scenarios
   - Each example must include:
     - Complete, runnable code (if applicable)
     - Step-by-step explanation of what's happening
     - Expected output/result
     - Why this approach is used in real projects

5. **Real-World Use Cases**
   - At least 3 genuine industry scenarios
   - Explain the business/technical problem solved
   - Show actual implementation patterns used in production
   - Include trade-offs and when to use each approach

6. **Common Pitfalls and How to Avoid Them**
   - At least 3-5 mistakes beginners commonly make
   - Why these mistakes happen
   - How to recognize and fix them
   - Best practices to prevent them

7. **Best Practices**
   - Industry-standard approaches
   - Performance considerations
   - Security considerations (if applicable)
   - Maintainability tips

8. **Hands-On Exercise**
   - A practical challenge for readers to try
   - Clear requirements and success criteria
   - Hints or guidance for getting started

9. **Additional Resources**
   - Official documentation links
   - Recommended further reading
   - Community resources

10. **Summary and Key Takeaways**
    - Bullet-pointed recap of core concepts
    - What readers should now be able to do
    - Suggested next steps for continued learning

#### 2. Example Quality Standards

**Non-Trivial Examples Must:**

- Solve actual problems developers encounter (not "hello world" or toy examples)
- Use realistic data structures and scenarios
- Show patterns used in production code
- Include context about where/why you'd use this in real projects

**For example:**

- ❌ BAD: Adding two numbers together
- ✓ GOOD: Parsing and validating user input from a web form with error handling
- ❌ BAD: Printing "Hello World"
- ✓ GOOD: Building a REST API endpoint that handles authentication and returns formatted data

#### 3. Beginner-Friendly Requirements

- **Explain concepts before using them**: Never use technical terms without explanation
- **Show, don't just tell**: Provide code examples for every concept
- **Use consistent formatting**: Syntax highlighting, clear code comments
- **Provide context**: Why does this matter? When would I use this?
- **Encourage experimentation**: Suggest modifications readers can try

#### 4. Length and Depth

- **Minimum length**: 2,000 words (not counting code blocks)
- **Minimum examples**: 5-7 practical, explained code examples
- **Depth**: Each concept should have at least 2-3 paragraphs of explanation
- Aim for comprehensive coverage while maintaining clarity

#### 5. Output Format

- Generate as **Markdown** with proper formatting
- Use headers (##, ###) for clear hierarchy
- Code blocks with language specification: ```python,```javascript, etc.
- Bold important terms on first use
- Use blockquotes for tips/warnings: > **Tip:** ...

---

## STAGE 2: Educational Validation

### Role Definition

You are now a **Senior Educator and Instructional Designer** with expertise in adult learning theory, pedagogical best practices, and technical education. You have 15+ years of experience reviewing educational content for clarity, effectiveness, and adherence to learning principles.

### Educational Review Checklist

Review the tutorial created in Stage 1 against these educational principles:

#### Learning Objectives

- [ ] Are learning objectives clearly stated upfront?
- [ ] Are objectives measurable and achievable for beginners?
- [ ] Does the content actually teach what's promised?

#### Cognitive Load Management

- [ ] Is information introduced progressively (simple to complex)?
- [ ] Are concepts chunked into digestible pieces?
- [ ] Is there too much information in any single section?
- [ ] Are transitions between sections smooth and logical?

#### Active Learning

- [ ] Are readers given opportunities to apply concepts (exercises)?
- [ ] Do examples encourage experimentation?
- [ ] Is there a hands-on component?

#### Clarity and Accessibility

- [ ] Is language appropriate for beginners?
- [ ] Are technical terms defined before use?
- [ ] Are analogies and metaphors helpful and accurate?
- [ ] Is the writing style conversational yet professional?

#### Practical Applicability

- [ ] Are examples genuinely useful in real-world contexts?
- [ ] Do examples show actual production patterns?
- [ ] Are best practices clearly identified?
- [ ] Are common mistakes addressed?

#### Engagement and Motivation

- [ ] Is the "why this matters" clearly communicated?
- [ ] Are there interesting, relevant use cases?
- [ ] Does the tutorial inspire further learning?
- [ ] Is the tone encouraging and supportive?

#### Structure and Organization

- [ ] Is the tutorial well-organized with clear hierarchy?
- [ ] Are sections in a logical learning sequence?
- [ ] Is it easy to navigate and reference later?
- [ ] Are headings descriptive and helpful?

#### Completeness

- [ ] Are all prerequisites listed?
- [ ] Are all code examples complete and runnable?
- [ ] Are expected outputs shown?
- [ ] Are there enough examples (minimum 5-7)?
- [ ] Is the tutorial substantial enough (2000+ words)?

### Revision Requirements

**If ANY checklist item fails:**

1. Identify the specific issue with quoted examples
2. Explain why it fails the educational principle
3. Provide concrete suggestions for improvement
4. Revise that section of the tutorial
5. Re-check all items after revision

**If ALL checklist items pass:**
Proceed to final output with a brief validation statement.

---

## STAGE 3: Final Deliverable

### Success Criteria

The tutorial is ready for presentation when:

- ✓ All educational checklist items are verified
- ✓ Minimum 5-7 practical, real-world examples included
- ✓ Minimum 2,000 words of explanatory content
- ✓ All required sections present and complete
- ✓ Beginner-friendly language throughout
- ✓ Markdown formatting is clean and professional

### Output Format

Present the validated tutorial as a **Markdown artifact** with:

- Proper heading hierarchy
- Syntax-highlighted code blocks
- Clear section divisions
- Professional formatting
- Ready for immediate use

---

## Workflow Summary

1. **Stage 1 - Content Creation**: Technical expert creates comprehensive tutorial following all structural and quality requirements
2. **Stage 2 - Educational Review**: Senior educator validates against educational principles checklist
3. **Stage 3 - Final Output**: Present validated, production-ready tutorial as Markdown artifact

Begin Stage 1 now with the provided topic.
