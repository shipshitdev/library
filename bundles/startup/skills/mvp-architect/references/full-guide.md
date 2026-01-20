# MVP Architect - Full Guide

## Execution Workflow

### Step 1: Problem Clarity Check

Before scoping features, validate the problem is clear.

**Problem Clarity Assessment:**

| Criteria | Status | If No |
|----------|--------|-------|
| 10+ customer interviews | [Yes/No] | Stop—go validate first |
| One-sentence problem | [Yes/No] | Clarify before building |
| 3-5 design partners | [Yes/No] | Find them before building |
| Current solution known | [Yes/No] | Research alternatives |
| PCV score 7+ | [Yes/No] | Re-validate idea |

**If any "No" above:** Use `idea-validator` before continuing.

### Step 2: Core Hypothesis Definition

**Hypothesis Framework:**

```
We believe that [target customer]
has a problem with [specific pain point].

We believe that [our solution]
will solve this because [mechanism].

We will know we're right when [success metric]
within [timeframe].

We will know we're wrong when [failure indicator].
```

**Example:**

```
We believe that B2B sales teams
have a problem with tracking follow-ups across channels.

We believe that a unified inbox with automated reminders
will solve this because it reduces context-switching.

We will know we're right when 50% of trial users
become paying customers within 2 weeks.

We will know we're wrong when users don't log in
more than twice in the first week.
```

### Step 3: Feature Brainstorm (Then Cut)

**Feature Capture Template:**

| # | Feature | Why You Think It's Needed |
|---|---------|---------------------------|
| 1 | | |
| 2 | | |
| 3 | | |

### Step 4: Feature Prioritization (The Ruthless Cut)

**For each feature, ask:**

| Question | If No | Action |
|----------|-------|--------|
| Does this directly test the core hypothesis? | → | Cut it |
| Have design partners explicitly asked for this? | → | Defer it |
| Is this needed for the first use case to work? | → | Defer it |
| Would users cancel if this was missing? | → | Maybe keep |
| Can this be done manually instead of built? | → | Do it manually |

**Feature Prioritization Matrix:**

| Feature | Tests Hypothesis? | Users Asked? | Critical Path? | Keep/Cut/Defer |
|---------|-------------------|--------------|----------------|----------------|
| [Feature 1] | [Y/N] | [Y/N] | [Y/N] | [Keep/Cut/Defer] |
| [Feature 2] | [Y/N] | [Y/N] | [Y/N] | [Keep/Cut/Defer] |

**Target: 3-5 features maximum for MVP.**

### Step 5: The "Dry Elements" Test

**Dry Elements** = Features that remained stable through all design partner feedback.

**Dry Elements Identification:**

| Feature | Changed During Feedback? | Dry Element? |
|---------|-------------------------|--------------|
| [Feature 1] | [Y/N] | [Yes/No] |
| [Feature 2] | [Y/N] | [Yes/No] |

**Your MVP = Only Dry Elements.**

Wet elements (features that keep changing) need more validation before building.

### Step 6: MVP Scope Definition

**MVP Scope Template:**

```
┌─────────────────────────────────────────────────┐
│ MVP SCOPE: [Product Name]                       │
├─────────────────────────────────────────────────┤
│ Core Value Prop: [One sentence]                 │
│ Target User: [Specific persona]                 │
│ Primary Use Case: [Main job-to-be-done]         │
├─────────────────────────────────────────────────┤
│ IN SCOPE (3-5 Features):                        │
│ 1. [Feature] — [Why critical]                   │
│ 2. [Feature] — [Why critical]                   │
│ 3. [Feature] — [Why critical]                   │
├─────────────────────────────────────────────────┤
│ EXPLICITLY OUT (For Now):                       │
│ • [Feature] — [When we'll add it]               │
│ • [Feature] — [Why it can wait]                 │
│ • [Feature] — [Manual workaround instead]       │
├─────────────────────────────────────────────────┤
│ SUCCESS METRIC: [What proves MVP works]         │
│ TIMELINE: [X weeks to launch]                   │
└─────────────────────────────────────────────────┘
```

### Step 7: User Journey Mapping (3-4 Screens)

**Hexa targets 3-4 simple screens for an MVP.**

**Screen Map:**

```
Screen 1: [Name]
Purpose: [What user does here]
Key Action: [Primary button/action]
     │
     ▼
Screen 2: [Name]
Purpose: [What user does here]
Key Action: [Primary button/action]
     │
     ▼
Screen 3: [Name]
Purpose: [What user does here]
Key Action: [Primary button/action]
     │
     ▼
Screen 4: [Name] (if needed)
Purpose: [What user does here]
Success State: [What success looks like]
```

### Step 8: Technical Architecture Check

**Architecture Review Checklist:**

| Question | Answer | Risk Level |
|----------|--------|------------|
| Core entities clearly defined? | [Y/N] | [High if No] |
| Relationships make sense? | [Y/N] | [High if No] |
| Scale considerations addressed? | [Y/N] | [Med if No] |
| Third-party dependencies identified? | [Y/N] | [Med if No] |
| Security/auth approach decided? | [Y/N] | [High if No] |
| Tech lead has reviewed? | [Y/N] | [High if No] |

**Hexa's Rule:** Have 3-4 tech leaders review your architecture before building.

### Step 9: Timeline & Milestones

**Timeline Framework:**

| Milestone | Target Date | What's Included |
|-----------|-------------|-----------------|
| Week 1-2 | [Date] | Core data model + basic UI |
| Week 3-4 | [Date] | Primary feature working |
| Week 5-6 | [Date] | Design partner testing |
| Week 7-8 | [Date] | Iteration + polish |
| Week 9-10 | [Date] | Public launch |

**If you can't launch in 10 weeks, scope is too big.**

### Step 10: Manual vs. Automated Decision

**Many MVP features can be manual first.**

| Feature | Build It? | Manual Alternative |
|---------|-----------|-------------------|
| Onboarding emails | Build later | Send manually from Gmail |
| Analytics dashboard | Build later | Use Mixpanel/Amplitude |
| Payment processing | Build later | Send Stripe payment links |
| Admin panel | Build later | Edit database directly |
| Notifications | Build later | Send manually |
| User support | Build later | Use Intercom/email |

**The "Wizard of Oz" MVP:** Automate the frontend, do backend manually. Users don't know the difference.

## Output Format Template

```markdown
# MVP Scope: [Product Name]

## Executive Summary

**Product:** [One-line description]
**Target User:** [Specific persona]
**Core Hypothesis:** [What we're testing]
**Timeline:** [X weeks to launch]
**Success Metric:** [How we know it works]

## Problem Validation Status

| Check | Status | Notes |
|-------|--------|-------|
| 10+ customer interviews | [✓/✗] | [Details] |
| Problem clearly articulated | [✓/✗] | [Details] |
| 3-5 design partners committed | [✓/✗] | [Names] |
| PCV score | [X/24] | [Assessment] |

## Core Hypothesis

**We believe that:** [target customer]
**Has a problem with:** [specific pain point]
**Our solution:** [what we're building]
**Will work because:** [mechanism]
**We'll know we're right when:** [success metric]
**We'll know we're wrong when:** [failure indicator]

## Feature Scope

### IN SCOPE (MVP)

| # | Feature | Rationale | Dry Element? |
|---|---------|-----------|--------------|
| 1 | [Feature] | [Why it's essential] | [Yes/No] |
| 2 | [Feature] | [Why it's essential] | [Yes/No] |
| 3 | [Feature] | [Why it's essential] | [Yes/No] |

### EXPLICITLY OUT (V2+)

| Feature | Why Deferred | When to Add |
|---------|--------------|-------------|
| [Feature] | [Reason] | [Trigger for adding] |

### MANUAL FOR NOW

| Automated Feature | Manual Alternative | When to Automate |
|-------------------|-------------------|------------------|
| [Feature] | [How we'll do it manually] | [When to build] |

## User Journey (3-4 Screens)

### Screen 1: [Name]
**Purpose:** [What happens here]
**User Action:** [What they click/do]

### Screen 2: [Name]
**Purpose:** [What happens here]
**User Action:** [What they click/do]

### Screen 3: [Name]
**Purpose:** [What happens here]
**User Action:** [What they click/do]

## Technical Architecture

### Core Entities

| Entity | Key Fields | Relationships |
|--------|------------|---------------|
| [Entity] | [Fields] | [Relations] |

### Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Frontend | [Tech] | [Why] |
| Backend | [Tech] | [Why] |
| Database | [Tech] | [Why] |
| Auth | [Tech] | [Why] |
| Hosting | [Tech] | [Why] |

## Timeline

| Week | Milestone | Deliverables |
|------|-----------|--------------|
| 1-2 | Foundation | [What's done] |
| 3-4 | Core Feature | [What's done] |
| 5-6 | Design Partner Testing | [Who tests] |
| 7-8 | Iteration | [What we'll fix] |
| 9-10 | Launch | [Public release] |

**Hard Deadline:** [Date]

## Success Metrics

### Week 4 (Internal)
- [Metric 1]
- [Metric 2]

### Week 8 (Design Partner)
- [Metric 1]
- [Metric 2]

### Week 12 (Public)
- [Metric 1]
- [Metric 2]

## Next Steps

### This Week
- [Action 1]
- [Action 2]
- [Action 3]
```

## Common Mistakes to Avoid

1. **Building before validating:** No design partners = building in the dark
2. **Too many features:** If you have more than 5, you're over-scoped
3. **Premature polish:** Ugly but working > beautiful but unfinished
4. **Fixed roadmaps:** Plans change—stay adaptable
5. **Building what you'd use:** You're not the customer (usually)
6. **Ignoring feedback:** Design partners know better than your assumptions
7. **Perfect architecture first:** You'll rewrite it anyway—ship first
8. **Underestimating manual options:** Many features can be manual for months
