# AI Prompts for Agile Scrum Developers

## Sprint Planning Prompts

### 1. Sprint Planning - Story Breakdown with Effort Estimation

```text
As an expert in Agile backlog refinement, help me break down this story:
"[insert story text]". List sub-tasks with realistic developer effort in hours.
Flag any missing requirements.
```

**Why it works:** Adds structure to vague backlog items and creates an actionable breakdown, saving planning time.

### 2. Sprint Planning - Value-Based Prioritization

```text
You are an Agile coach specialized in value prioritization. Here's a list of
five backlog items with estimated effort: [list]. Rank them based on business
value impact, risk, and delivery speed.
```

**Why it works:** Helps developers push back against arbitrary prioritization.

### 3. Sprint Planning - Story Quality Review

```text
Act as a Product Owner. Review these backlog stories: [list]. Suggest any that
should be merged, split, or sent back for clarification based on user value.
```

**Why it works:** Promotes clarity early, reduces mid-sprint surprises.

### 4. Sprint Planning - Story Estimation

```text
Analyze this user story and provide a story point estimate:

Story: "As a user, I want to reset my password via email so that I can regain
access to my account if I forget my credentials."

Consider:
- Frontend work (reset form, email sent confirmation, new password form)
- Backend work (token generation, email service integration, password hashing)
- Security considerations (token expiration, rate limiting)
- Testing requirements
- Integration with existing auth system

Provide:
1. Story point estimate (1, 2, 3, 5, 8, 13)
2. Breakdown of work by component
3. Potential risks or unknowns that could affect the estimate
4. Recommended split if story is >8 points
```

### 5. Sprint Planning - Dependency Identification

```text
Review these 5 user stories planned for the upcoming sprint and identify dependencies:

Story A: Implement user profile page
Story B: Add avatar upload functionality
Story C: Create user settings API endpoints
Story D: Build notification preferences UI
Story E: Implement email notification service

Analyze:
1. Which stories depend on others?
2. What is the optimal implementation order?
3. Are there any circular dependencies or blocking issues?
4. Which stories can be worked on in parallel?
5. What is the critical path for this sprint?

Provide a dependency graph and recommended sprint board organization.
```

### 6. Sprint Planning - Capacity Planning

```text
Calculate team capacity for the upcoming 2-week sprint:

Team composition:
- 3 senior developers (8 story points/day each)
- 2 mid-level developers (5 story points/day each)
- 1 junior developer (3 story points/day)

Constraints:
- Sprint ceremonies: 8 hours total (planning, daily standups, review, retro)
- Developer A has 3 days PTO
- Developer B allocated 25% time to production support
- Team has on-call rotation (1 person/week, reduces capacity by 20%)
- Public holiday: 1 day

Calculate:
1. Total available story points for the sprint
2. Recommended sprint commitment (accounting for 10-20% buffer)
3. Risk assessment if we commit to 180 story points
4. Recommendation for handling if product owner wants to add more stories
```

## Backlog Refinement Prompts

### 7. Backlog Refinement - Story Splitting

```text
This user story is too large to complete in one sprint. Help split it into smaller,
independently deliverable stories:

Epic story: "As an admin, I want a comprehensive dashboard showing system health,
user analytics, revenue metrics, and recent activity logs so that I can monitor
the platform effectively."

Requirements:
- Each split story must be independently valuable
- Each story should be completable in 3-5 days
- Stories should follow vertical slice architecture (full stack for each piece)
- Maintain clear acceptance criteria for each

Provide:
1. 3-5 smaller user stories with format: "As [role], I want [feature] so that [benefit]"
2. Priority order for implementing the stories
3. Acceptance criteria for each story
4. Estimated story points for each
```

### 8. Backlog Refinement - Acceptance Criteria Generation

```text
Generate comprehensive acceptance criteria for this user story:

Story: "As a user, I want to filter search results by category, price range,
and rating so that I can find products that meet my needs."

Create acceptance criteria that covers:
- Functional requirements (what must work)
- Edge cases (empty results, invalid inputs, boundary conditions)
- Performance requirements (search response time)
- Accessibility requirements
- Mobile responsiveness

Format as:
Given [context]
When [action]
Then [expected result]

Include both happy path and edge case scenarios.
```

### 9. Backlog Refinement - Technical Debt Prioritization

```text
Prioritize these technical debt items for inclusion in upcoming sprints:

Item A: Refactor authentication service (currently 3000 lines, no tests)
- Risk: High (security-critical, frequent bugs)
- Effort: 3 sprints
- Impact: Reduced bugs, easier to add OAuth providers

Item B: Upgrade React 16 to React 18
- Risk: Medium (breaking changes)
- Effort: 1 sprint
- Impact: Performance improvements, modern features

Item C: Add database indexes to slow queries
- Risk: Low (well-understood problem)
- Effort: 3 days
- Impact: 40% faster page load on main dashboard

Item D: Migrate from REST to GraphQL
- Risk: High (major architecture change)
- Effort: 6 sprints
- Impact: Better frontend performance, reduced API calls

Item E: Fix eslint warnings (150+ warnings)
- Risk: Low (code quality)
- Effort: 1 sprint
- Impact: Better code maintainability

Prioritize based on: impact, risk, effort, and delivery speed.
Provide recommendation with rationale.
```

## Ticket Crafting Prompts

### 10. User Story Creation - Structured Story Format

```text
As a certified Product Owner, help me rewrite this vague task into a full user
story with acceptance criteria: [insert task]. Format it in the 'As a... I want...
so that...' style and add 3 testable conditions.
```

**Why it works:** Bridges development thinking with business expectations.

### 11. User Story Creation - Technical Debt Documentation

```text
You are a Jira expert and Agile coach. I need to document a technical debt
ticket that meets DOD. Convert this explanation into a clean ticket description
and add a checklist for completion.
```

**Why it works:** Helps developers write what gets accepted and shipped.

### 12. User Story Creation - QA Perspective

```text
Act like a QA reviewer. Scan this user story: [story]. Suggest edge cases or
acceptance tests we might have missed.
```

**Why it works:** Avoids future rework by adding a testing lens early.

### 13. User Story Creation - Story Template

```text
Convert this feature request into a properly formatted user story with acceptance criteria:

Feature request: "We need a way for customers to track their orders after purchase.
They should get email updates and be able to see the current status on the website."

Create:
1. User story in standard format
2. 5-7 acceptance criteria
3. Definition of Done checklist
4. Potential edge cases to consider
5. Non-functional requirements (performance, security, accessibility)
6. Dependencies on other systems or teams
```

### 14. User Story Creation - Edge Case Identification

```text
Identify edge cases and corner cases for this user story:

Story: "As a user, I want to add items to my shopping cart and see the total
price update automatically."

Analyze for edge cases related to:
- Quantity handling (0, negative, very large numbers)
- Concurrent updates (multiple browser tabs)
- Network failures (offline mode, slow connection)
- Price changes (item price changes while in cart)
- Inventory (item goes out of stock while in cart)
- Session handling (cart persistence, timeout)
- Promotions and discounts
- Multiple currencies
- Maximum cart limits

For each edge case, provide:
1. Description of the scenario
2. Expected behavior
3. Priority (must-have vs nice-to-have)
```

## Daily Standup Prompts

### 15. Standup - Concise Update Generation

```text
Act as a standup facilitator. Summarize my work in these bullet points: [insert].
Highlight blockers and suggest one follow-up question I can ask the team.
```

**Why it works:** Refines communication and highlights action.

### 16. Standup - Data-Driven Update

```text
You are a Scrum lead tracking momentum. Based on this Git log and ticket status,
generate a concise standup update (Yesterday/Today/Blockers): [insert data].
```

**Why it works:** Builds a data-driven update without fluff.

### 17. Standup - Team Health Check

```text
As a burnout-aware Agile bot, review these updates: [insert]. Flag any signs
of overload or repeated blockers, and suggest wellness check-in prompts.
```

**Why it works:** Adds a human touch through AI.

### 18. Daily Standup - Blocker Identification

```text
Analyze these daily standup updates and identify blockers, dependencies, and risks:

Developer A: "Working on user profile API. Yesterday completed GET endpoint,
today working on UPDATE. Need database schema changes approved by DBA team."

Developer B: "Finished frontend form for profile page. Waiting for API from
Developer A to integrate. Today will work on validation logic."

Developer C: "Hit an issue with authentication middleware. Error happens
intermittently, can't reproduce locally. Spent 4 hours debugging yesterday."

Developer D: "Payment integration with Stripe done. Need Product Owner to
review test transactions before moving to production. They're in meetings all day."

Developer E: "Working on notification service. Discovered our email provider
has rate limits we'll hit in production. Need to discuss alternative approach."

Identify:
1. Active blockers requiring immediate action
2. Potential blockers that may emerge soon
3. Dependencies between team members
4. Risks that need escalation
5. Recommended actions for Scrum Master to take today
```

### 19. Daily Standup - Progress Summarization

```text
Summarize the team's sprint progress for stakeholder update:

Sprint goal: "Enable users to manage their account settings and preferences"

Day 5 of 10 (sprint midpoint):

Completed: 32 story points
In progress: 18 story points
Remaining: 25 story points
Velocity trend: On track

Stories completed: 7 of 15
Stories in progress: 4
Stories not started: 4

Blockers: 2 (external API delay, pending design approval)

Create a concise stakeholder update including:
1. Overall sprint health (on track / at risk / off track)
2. Key accomplishments
3. Risks and mitigation plans
4. Expected sprint outcome
5. Help needed from stakeholders
```

## Sprint Retrospective Prompts

### 20. Retrospective - Start/Stop/Continue Framework

```text
You are a retrospective expert. Analyze these notes: [insert retro notes or
observations]. Suggest 3 'Start/Stop/Continue' talking points that are tactful
but honest.
```

**Why it works:** Offers safe but direct feedback phrasing.

### 21. Retrospective - Conflict Resolution

```text
As an Agile conflict mediator, suggest retro feedback for this situation:
[describe team tension]. Focus on constructive language and psychological safety.
```

**Why it works:** Coaches developers through conflict-aware participation.

### 22. Retrospective - Theme Clustering

```text
Act as an AI retro board tool. Cluster the following feedback into themes and
suggest one lesson learned per theme: [feedback list].
```

**Why it works:** Organizes chaos into insight, fast.

### 23. Sprint Retrospective - Analysis

```text
Analyze our sprint retrospective data and generate insights:

Sprint velocity: 67 points (committed: 75 points)
Completed stories: 11 out of 14
Carry-over stories: 3 (all blocked by external API delays)

What went well:
- Great pair programming sessions
- Improved code review turnaround time
- New CI/CD pipeline reduced deployment time

What didn't go well:
- Underestimated complexity of authentication refactor
- Frequent production hotfixes interrupted sprint work (8 hours total)
- Unclear requirements on 2 stories led to rework
- Daily standups running over 15 minutes

Provide:
1. Root cause analysis for velocity shortfall
2. 3-5 actionable improvements for next sprint
3. Metrics to track for each improvement
4. Recommended retrospective action items with owners
5. Red flags or patterns that need management attention
```

### 24. Sprint Retrospective - Action Item Generation

```text
Based on this retrospective feedback, generate SMART action items:

Issue 1: "Code reviews are taking too long, sometimes 2-3 days"
Issue 2: "We keep getting surprised by integration issues late in the sprint"
Issue 3: "Junior developers feel blocked frequently but hesitate to ask for help"
Issue 4: "Technical debt is slowing us down but we never have time to address it"

For each issue, create a SMART action item:
- Specific: What exactly will we do?
- Measurable: How will we know we've succeeded?
- Achievable: Is it realistic for our team?
- Relevant: Does it address the root cause?
- Time-bound: When will we achieve this?

Also assign:
- Owner (who is responsible)
- Timeline (when to complete)
- Success metric (how to measure improvement)
```

## Sprint Review Prompts

### 25. Sprint Review - Impact Summary

```text
Act like a Scrum Master prepping for Sprint Review. Based on this list of closed
tasks, create a short impact summary and link to business goals.
```

**Why it works:** Connects delivery to outcomes.

### 26. Sprint Review - Demo Walkthrough Script

```text
As a technical demo expert, outline a 3-minute walkthrough script for this feature:
[insert feature]. Include who it's for, what problem it solves, and how it works.
```

**Why it works:** Makes Sprint Reviews easier to navigate.

### 27. Sprint Review - Release Notes

```text
Act as a release coordinator. Based on this sprint's output, draft a release note
with technical highlights, known limitations, and user-facing improvements.
```

**Why it works:** Delivers value to internal and external stakeholders.

### 28. Sprint Review - Demo Preparation

```text
Prepare a demo script for sprint review meeting:

Completed stories this sprint:
1. User can upload profile picture
2. Password reset via email
3. Two-factor authentication setup
4. Account deletion with confirmation

Audience: Product Owner, stakeholders, customer success team

Create a demo script that:
1. Connects features to user value
2. Shows the happy path for each feature
3. Includes 1-2 interesting edge cases
4. Demonstrates integration between features
5. Highlights technical achievements
6. Keeps demo under 15 minutes
7. Prepares answers for likely questions

Format as a step-by-step script with:
- What to show (with screenshots/actions)
- What to say (talking points)
- Transition between features
- Expected questions and answers
```

### 29. Sprint Review - Stakeholder Communication

```text
Convert these technical achievements into stakeholder-friendly language:

Technical accomplishments:
- Implemented Redis caching layer, reduced API response time by 60%
- Refactored authentication service, improved test coverage from 40% to 85%
- Migrated to PostgreSQL, eliminated data consistency issues
- Added database indexes, dashboard load time improved from 8s to 1.2s
- Implemented CI/CD pipeline, deployment time reduced from 2 hours to 15 minutes

Translate each accomplishment into:
1. Business value (why stakeholders should care)
2. User impact (how it affects end users)
3. Measurable improvement (concrete metrics)
4. Visual representation (if possible)

Format for non-technical audience.
```

## Estimation Prompts

### 30. Estimation - Story Point Calibration

```text
Our team is new to story pointing. Help calibrate our estimates using these
completed stories as reference:

Reference stories (actual time taken):
- Add logout button: 2 hours (let's call this 1 point)
- Create user registration form: 1 day (3 points)
- Implement JWT authentication: 3 days (5 points)
- Build admin dashboard: 1 week (8 points)
- Payment gateway integration: 2 weeks (13 points)

Now estimate these new stories using the same scale:

Story X: Add password strength indicator
- Frontend: Visual indicator component
- Logic: Validation rules (length, complexity)
- No backend changes needed

Story Y: Implement OAuth login (Google, GitHub)
- Frontend: OAuth buttons, redirect handling
- Backend: OAuth provider integration, token exchange
- Database: Link external accounts to users

Story Z: Add email notification when order ships
- Backend: Event trigger on order status change
- Email template design and implementation
- Integration with email service provider

Provide story point estimate for each with reasoning.
```

### 31. Estimation - Complexity Analysis

```text
Analyze the complexity of this story and recommend if it should be split:

Story: "As a user, I want real-time notifications when someone mentions me in
a comment, likes my post, or follows me."

Complexity factors to consider:
- Real-time infrastructure (WebSocket vs polling vs Server-Sent Events)
- Notification types (in-app, email, push)
- Notification preferences (what to notify, when to notify)
- Read/unread state management
- Notification history and persistence
- Performance at scale (thousands of notifications per second)
- Mobile and web platforms
- Rate limiting and spam prevention

Provide:
1. Complexity assessment (low/medium/high)
2. Story point estimate range
3. Should it be split? If yes, how?
4. Biggest unknown or risk
5. Similar stories from common patterns (for calibration)
```

## Definition of Done Prompts

### 32. Definition of Done - Checklist Generation

```text
Generate a comprehensive Definition of Done checklist for our team:

Our tech stack:
- React frontend
- Node.js/Express backend
- PostgreSQL database
- Docker containers
- GitHub Actions CI/CD

Our quality standards:
- 80% code coverage minimum
- All PR reviews require 2 approvals
- Accessibility WCAG 2.1 AA compliance
- Security scanning required
- Performance budgets must be met

Create a DoD checklist organized by:
1. Code quality
2. Testing
3. Documentation
4. Security
5. Performance
6. Accessibility
7. Deployment
8. Product Owner acceptance

Each item should be a yes/no checkbox.
```

### 33. Definition of Done - Quality Gates

```text
Design automated quality gates for our CI/CD pipeline that enforce Definition of Done:

Requirements:
- Block merge if unit test coverage <80%
- Block merge if security vulnerabilities found (high/critical)
- Block merge if performance regression >10%
- Block merge if accessibility errors found
- Warn if bundle size increased >5%
- Warn if API response time increased >15%

For each gate, specify:
1. Tool to use (jest, sonarqube, lighthouse, etc.)
2. Threshold configuration
3. Block vs warn behavior
4. How to override if necessary (and who can)
5. Feedback format for developers

Provide implementation examples for GitHub Actions.
```

## Impediment Resolution Prompts

### 34. Impediment Resolution - Root Cause Analysis

```text
Perform root cause analysis on this recurring sprint impediment:

Impediment: "Stories frequently blocked waiting for database changes from DBA team"

Occurrences: 8 stories blocked across last 3 sprints
Average delay: 2-3 days per story
Impact: Reduced velocity by approximately 15 story points

Context:
- DBA team supports 5 development teams
- Database change requests submitted via ticket system
- DBAs review/approve changes for security and performance
- Changes deployed only on Tuesdays and Thursdays

Use 5 Whys technique:
1. Why are stories blocked? (because...)
2. Why does that happen? (because...)
3. Why is that the case? (because...)
4. Why is that true? (because...)
5. Why is that the situation? (because...)

Then provide:
1. Root cause identification
2. 3-5 potential solutions
3. Pros/cons of each solution
4. Recommended approach
5. How to prevent similar issues
```

## Sprint Goal Prompts

### 35. Sprint Goal - SMART Goal Creation

```text
Create a SMART sprint goal for this 2-week sprint:

Product Owner input: "We need to make progress on the checkout flow and
improve the user experience around payments."

Committed stories:
- Shopping cart persistence across sessions
- Guest checkout flow
- Multiple payment methods (credit card, PayPal)
- Order confirmation page
- Email receipt
- Retry failed payments

Create a sprint goal that is:
- Specific: Clear and unambiguous
- Measurable: Can determine success/failure
- Achievable: Realistic for 2 weeks
- Relevant: Aligns with product roadmap
- Time-bound: Sprint deadline

Also provide:
1. How to measure sprint goal success (even if not all stories complete)
2. Minimum viable outcome
3. Stretch goal if team finishes early
4. Connection to company OKRs or quarterly goals
```

## Why This Matters for Developers

Using AI in Agile isn't about faking it—it's about making the system work for your brain. These prompts don't replace human discussion. They just help developers show up prepared, focused, and less drained.

At a glance, integrating AI into Agile rituals may seem like a tool for managers or coaches, but developers stand to benefit just as much, if not more. Research into prompt engineering specifically tailored for technical contributors addresses real developer pain points: vague tickets, unproductive standups, poorly scoped retros, and communication fatigue.

Frameworks such as Prompt-Driven Agile Facilitation and Agile AI Copilot show how developers can use targeted, structured prompts to support both solo and team productivity. These studies reflect the reality of hybrid work: asynchronous meetings, remote collaboration, and cross-functional handoffs.

Tools and bots are being created that support retrospectives, sprint demos, and conflict resolution—not because developers can't manage these, but because time and energy are finite. Prompt-based systems reduce friction and help technical teams align faster. They don't take the human out of Agile—they reduce the waste that prevents teams from being truly Agile.

More importantly, this isn't about creating robotic output. It's about giving developers ownership of the process. These prompts act as a developer's voice coach, technical writer, and backlog cleaner—all rolled into one.

So next time your backlog makes no sense, or your standup feels pointless, try typing instead of talking. Let AI sharpen your edge—one prompt at a time.
