# MVP Plan - Minimum Viable Product Planning

**Purpose:** Define MVP scope, prioritize features, and create launch roadmap

## Usage

```bash
/mvp-plan              # Interactive MVP planning workflow
/mvp-plan --review     # Review existing MVP plan
```

## When to Use

Use this command when:

- Starting a new product/startup
- Defining scope for initial launch
- Prioritizing features for MVP vs future releases
- Creating a structured roadmap
- Need to scope down from a larger vision

## What This Command Does

Helps structure MVP planning:

1. **Feature Brainstorming** - Capture all feature ideas
2. **Priority Matrix** - Categorize features (must-have, should-have, could-have, won't-have)
3. **User Stories** - Define user-facing features as stories
4. **Technical Scope** - Assess technical complexity and dependencies
5. **Timeline Estimation** - Create realistic timeline for MVP launch
6. **MVP Definition Document** - Generate comprehensive MVP plan

---

## Workflow

### Phase 1: Feature Brainstorming

**1.1 Capture All Ideas**

Gather all feature ideas from:

- User research
- Competitive analysis
- Team brainstorming
- User feedback (if existing product)

**Format:**

```markdown
## Feature Ideas

### Core Features
- [Feature 1]
- [Feature 2]

### Nice-to-Have Features
- [Feature 3]
- [Feature 4]

### Future Considerations
- [Feature 5]
- [Feature 6]
```

**1.2 Group Related Features**

Organize features into logical groups:

- Authentication & User Management
- Core Product Features
- Analytics & Reporting
- Integrations
- Admin/Management

### Phase 2: Priority Matrix (MoSCoW Method)

**Categorize each feature:**

- **Must Have (M)** - MVP cannot launch without this
- **Should Have (S)** - Important but not critical for launch
- **Could Have (C)** - Nice to have, can wait for v2
- **Won't Have (W)** - Not in scope for MVP

**Priority Matrix Template:**

```markdown
## MVP Priority Matrix

### Must Have (M)
- [ ] Feature A - Core user value
- [ ] Feature B - Essential functionality

### Should Have (S)
- [ ] Feature C - Important for user experience
- [ ] Feature D - Competitive advantage

### Could Have (C)
- [ ] Feature E - Enhancement
- [ ] Feature F - Nice-to-have

### Won't Have (W)
- [ ] Feature G - Out of scope
- [ ] Feature H - Future consideration
```

**Criteria for Must-Have:**

- Solves core user problem
- Required for product to work
- Users expect it (minimum expectations)
- Blocks core user flow if missing

**Criteria for Should-Have:**

- Improves user experience significantly
- Expected by most users
- Competitive parity

**Criteria for Could-Have:**

- Nice enhancement
- Differentiating feature (but not essential)
- Can validate product without it

### Phase 3: User Stories

**3.1 Define User Personas**

Identify target users:

- Primary persona (main target)
- Secondary personas (if applicable)

**3.2 Create User Stories**

Format: "As a [user type], I want [goal] so that [benefit]"

```markdown
## User Stories

### Authentication
- As a new user, I want to sign up so that I can access the product
- As a user, I want to sign in so that I can access my account

### Core Feature
- As a user, I want to [core action] so that [core value]
- As a user, I want to [secondary action] so that [benefit]

### Admin/Management
- As an admin, I want to manage users so that I can maintain the platform
```

**3.3 Acceptance Criteria**

For each user story, define acceptance criteria:

```markdown
### User Story: [Title]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

### Phase 4: Technical Scope Assessment

**4.1 Technical Requirements**

For each Must-Have feature, assess:

- Backend complexity
- Frontend complexity
- Database requirements
- Third-party integrations
- Infrastructure needs

**Technical Complexity Scale:**

- **Simple (1)** - Straightforward, well-understood patterns
- **Moderate (2)** - Some complexity, may need research
- **Complex (3)** - Significant complexity, custom implementation
- **Very Complex (4)** - Major technical challenge

**4.2 Dependencies**

Map feature dependencies:

- Feature A depends on Feature B
- Feature C blocks Feature D
- Feature E can be done in parallel

**Dependency Graph:**

```markdown
## Technical Dependencies

### Foundation Layer
- Authentication (required for all)
- User Management (depends on: Authentication)

### Core Features
- Feature A (depends on: Authentication, User Management)
- Feature B (depends on: Feature A)
- Feature C (independent)
```

**4.3 Technology Stack Validation**

Verify tech stack supports MVP:

- Backend: NestJS, MongoDB (EC2/Docker)
- Frontend: Next.js, Tailwind
- Infrastructure: AWS (EC2, VPC, ALB)
- Monitoring: Sentry, Google Analytics

### Phase 5: Timeline Estimation

**5.1 Break Down Features**

Break Must-Have features into tasks:

- Authentication → 3-5 days
- Core Feature A → 5-7 days
- Core Feature B → 3-5 days
- Admin Dashboard → 2-3 days

**5.2 Estimate Timeline**

Consider:

- Development time
- Testing time
- Deployment/infrastructure setup
- Buffer for unexpected issues (20-30%)

**MVP Timeline Template:**

```markdown
## MVP Timeline

### Week 1-2: Foundation
- Authentication & User Management
- Project setup & infrastructure
- Database schema design

### Week 3-4: Core Features
- Core Feature A
- Core Feature B

### Week 5: Polish & Launch Prep
- Testing
- Bug fixes
- Deployment setup
- Launch preparation

**Target Launch:** [Date]
**Estimated Duration:** [X weeks]
```

**5.3 Risk Assessment**

Identify risks:

- Technical risks (unproven tech, complexity)
- Timeline risks (scope creep, delays)
- Resource risks (team capacity, dependencies)

### Phase 6: MVP Definition Document

**Generate comprehensive MVP plan:**

```markdown
# MVP Plan - [Product Name]

**Date:** [Date]
**Target Launch:** [Date]

## Executive Summary
[Brief overview of MVP scope and goals]

## User Personas
[Primary and secondary personas]

## Must-Have Features
[List of must-have features with descriptions]

## User Stories
[All user stories for must-have features]

## Technical Scope
- Backend: [Technologies]
- Frontend: [Technologies]
- Infrastructure: [Setup]
- Integrations: [Third-party services]

## Timeline
[Detailed timeline breakdown]

## Success Metrics
- User signups
- Core feature usage
- User retention
- [Product-specific metrics]

## Out of Scope (Post-MVP)
- [Should-have features moved to v2]
- [Could-have features]
- [Nice-to-haves]

## Risks & Mitigation
[Identified risks and mitigation strategies]
```

Save to: `.agent/PRDS/mvp-plan-[product-name].md` or `.agent/MVP/[product-name]-mvp.md`

---

## Manual Checklist for AI Agent

When user runs `/mvp-plan`:

### Phase 1: Feature Brainstorming

- [ ] Gather all feature ideas
- [ ] Group features by category
- [ ] Document in structured format
- [ ] Review with user for completeness

### Phase 2: Priority Matrix

- [ ] Categorize each feature (M/S/C/W)
- [ ] Justify Must-Have selections
- [ ] Review priorities with user
- [ ] Finalize MVP feature list

### Phase 3: User Stories

- [ ] Define user personas
- [ ] Create user stories for Must-Have features
- [ ] Write acceptance criteria
- [ ] Review stories with user

### Phase 4: Technical Assessment

- [ ] Assess technical complexity for each feature
- [ ] Map feature dependencies
- [ ] Validate tech stack supports MVP
- [ ] Identify technical risks

### Phase 5: Timeline Estimation

- [ ] Break features into tasks
- [ ] Estimate development time
- [ ] Create timeline with milestones
- [ ] Add buffer for risks
- [ ] Review timeline with user

### Phase 6: Documentation

- [ ] Generate MVP definition document
- [ ] Include all phases above
- [ ] Save to appropriate location
- [ ] Review with user for final approval

---

## Examples

### Example 1: New Product MVP

**User:** `/mvp-plan`

**AI Actions:**

1. Ask: "What problem does your product solve?"
2. Gather feature ideas through conversation
3. Guide through priority matrix
4. Create user stories
5. Assess technical scope
6. Generate timeline
7. Create MVP definition document

### Example 2: Review Existing MVP

**User:** `/mvp-plan --review`

**AI Actions:**

1. Find existing MVP plan
2. Review against current progress
3. Identify scope creep
4. Suggest adjustments if needed

---

## Best Practices

**Keep MVP Focused:**

- Only include features that solve core problem
- Defer nice-to-haves to post-MVP
- Validate with minimal features first

**Set Clear Boundaries:**

- Explicitly list what's out of scope
- Resist scope creep
- Stick to timeline

**Validate Assumptions:**

- Test core value proposition
- Get user feedback early
- Iterate based on learning

**Technical Considerations:**

- Build on proven tech stack
- Minimize technical debt
- Plan for scale (but don't over-engineer)

---

## Integration with Other Commands

This command integrates with:

- **`/task`** - Creates tasks from MVP features
- **`/launch`** - Uses MVP plan for launch preparation
- **`/scaffold`** - Uses MVP scope for project setup

---

**Created:** 2025-01-27
**Purpose:** Structured MVP planning workflow for startup launches
