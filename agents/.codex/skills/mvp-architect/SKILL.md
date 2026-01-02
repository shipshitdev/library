---
name: mvp-architect
description: Use when users need to scope an MVP, define minimum viable features, plan early product development, or determine what to build first. Activates for "what should my MVP include," "scope my MVP," "what to build first," or product scoping questions.
---

# MVP Architect - Minimum Viable Product Scoping

## Overview

Act as an MVP architect applying Hexa's proven methodology for building early-stage products. Help indie founders scope the smallest possible product that validates their core hypothesis, avoiding over-building and getting to market in 3 months or less. Execute ruthless scoping—not just advise—by guiding users through problem discovery, feature prioritization, and architecture planning.

**Hexa's Core Principle:** "The objective is to put on the market an MVP with key high-value features within 3 months. It's actually better to launch a product with clear, easily understood features, even if they aren't at full power yet."

## When This Activates

Use when:
- User asks "what should my MVP include"
- User says "help me scope my MVP"
- User asks "what features do I need"
- User mentions being unsure what to build first
- User is planning their product roadmap
- User asks about "minimum viable" anything
- User wants to ship faster but doesn't know what to cut
- User says "I've been building for months and haven't launched"

## The Framework: Hexa's 7 Principles for Early-Stage Products

1. **Dig Beyond User Requests** — Understand root needs, not surface wants
2. **Combat Confirmation Bias** — Challenge your assumptions ruthlessly
3. **Partner with Design Partners Early** — Build with real users, not in a vacuum
4. **Prioritize Adaptable Milestones** — 6-month goals, 2-week sprints
5. **Sketch Before Designing** — Keep it ugly until validated
6. **Build Around "Dry Elements"** — Only include features unchanged through testing
7. **Stress-Test Your Architecture** — Database design affects everything

## Execution Workflow

### Step 1: Problem Clarity Check

Before scoping features, validate the problem is clear.

Ask the user:

> **Is the problem validated?**
> 1. Have you talked to 10+ potential customers?
> 2. Can you articulate the problem in one sentence?
> 3. Do you have 3-5 design partners committed?
> 4. Do you know how they currently solve this problem?
> 5. What PCV score did your idea get? (See `idea-validator`)

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

Ask the user:

> **What are you trying to prove with this MVP?**
> 1. What's the single most important assumption to validate?
> 2. What would prove the idea works?
> 3. What would prove the idea doesn't work?
> 4. What's the minimum you could build to get this answer?

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

Ask the user:

> **List everything you think the product should do:**
> (Don't filter yet—get it all out)

**Feature Capture Template:**

| # | Feature | Why You Think It's Needed |
|---|---------|---------------------------|
| 1 | | |
| 2 | | |
| 3 | | |
| ... | | |

### Step 4: Feature Prioritization (The Ruthless Cut)

Now apply the filter:

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
| ... | | | | |

**Target: 3-5 features maximum for MVP.**

### Step 5: The "Dry Elements" Test

**Dry Elements** = Features that remained stable through all design partner feedback.

Ask the user:

> **Which features have NOT changed through customer conversations?**
> 1. What did everyone agree on?
> 2. What feedback was consistent across all interviews?
> 3. What's the undisputed core value?

**Dry Elements Identification:**

| Feature | Changed During Feedback? | Dry Element? |
|---------|-------------------------|--------------|
| [Feature 1] | [Y/N] | [Yes/No] |
| [Feature 2] | [Y/N] | [Yes/No] |
| ... | | |

**Your MVP = Only Dry Elements.**

Wet elements (features that keep changing) need more validation before building.

### Step 6: MVP Scope Definition

Based on the analysis:

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

Ask the user:

> **What's the critical user journey?**
> 1. How do users sign up?
> 2. What's the FIRST thing they do?
> 3. What's the core action that delivers value?
> 4. How do they know it worked?

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

**Your database design affects the entire product lifecycle and UX.**

Ask the user:

> **Technical sanity check:**
> 1. What are the core data entities?
> 2. How do they relate to each other?
> 3. What data must be stored vs. computed?
> 4. Have you validated this with a technical advisor?

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

**Adaptable milestones, not rigid roadmaps.**

Ask the user:

> **What's your launch timeline?**
> 1. When do you want to have the MVP live?
> 2. What's blocking you from launching in 4 weeks?
> 3. What would a "launch in 2 weeks" version look like?

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

For each feature, ask:

| Feature | Build It? | Manual Alternative |
|---------|-----------|-------------------|
| Onboarding emails | Build later | Send manually from Gmail |
| Analytics dashboard | Build later | Use Mixpanel/Amplitude |
| Payment processing | Build later | Send Stripe payment links |
| Admin panel | Build later | Edit database directly |
| Notifications | Build later | Send manually |
| User support | Build later | Use Intercom/email |

**The "Wizard of Oz" MVP:** Automate the frontend, do backend manually. Users don't know the difference.

## Output Format

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
| 4 | [Feature] | [Why it's essential] | [Yes/No] |
| 5 | [Feature] | [Why it's essential] | [Yes/No] |

### EXPLICITLY OUT (V2+)

| Feature | Why Deferred | When to Add |
|---------|--------------|-------------|
| [Feature] | [Reason] | [Trigger for adding] |
| [Feature] | [Reason] | [Trigger for adding] |
| [Feature] | [Reason] | [Trigger for adding] |

### MANUAL FOR NOW

| Automated Feature | Manual Alternative | When to Automate |
|-------------------|-------------------|------------------|
| [Feature] | [How we'll do it manually] | [When to build] |
| [Feature] | [How we'll do it manually] | [When to build] |

## User Journey (3-4 Screens)

### Screen 1: [Name]
**Purpose:** [What happens here]
**User Action:** [What they click/do]
**Key Elements:**
- [Element 1]
- [Element 2]

### Screen 2: [Name]
**Purpose:** [What happens here]
**User Action:** [What they click/do]
**Key Elements:**
- [Element 1]
- [Element 2]

### Screen 3: [Name]
**Purpose:** [What happens here]
**User Action:** [What they click/do]
**Key Elements:**
- [Element 1]
- [Element 2]

### Screen 4: [Name] (if needed)
**Purpose:** [What happens here]
**Success State:** [What completion looks like]

## Technical Architecture

### Core Entities

| Entity | Key Fields | Relationships |
|--------|------------|---------------|
| [Entity] | [Fields] | [Relations] |
| [Entity] | [Fields] | [Relations] |

### Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Frontend | [Tech] | [Why] |
| Backend | [Tech] | [Why] |
| Database | [Tech] | [Why] |
| Auth | [Tech] | [Why] |
| Hosting | [Tech] | [Why] |

### Architecture Review Status

- [ ] Core entities validated with tech lead
- [ ] Scale considerations reviewed
- [ ] Security approach approved
- [ ] Third-party integrations scoped

## Timeline

| Week | Milestone | Deliverables |
|------|-----------|--------------|
| 1-2 | Foundation | [What's done] |
| 3-4 | Core Feature | [What's done] |
| 5-6 | Design Partner Testing | [Who tests, feedback loop] |
| 7-8 | Iteration | [What we'll fix] |
| 9-10 | Launch | [Public release] |

**Hard Deadline:** [Date]
**If not launched by this date:** [What we'll cut]

## Design Partner Plan

| Name | Company | Commitment | Feedback Schedule |
|------|---------|------------|-------------------|
| [Name] | [Co] | [What they agreed to] | [Weekly/Bi-weekly] |
| [Name] | [Co] | [What they agreed to] | [Weekly/Bi-weekly] |
| [Name] | [Co] | [What they agreed to] | [Weekly/Bi-weekly] |

## Success Metrics

### Week 4 (Internal)
- [ ] [Metric 1]
- [ ] [Metric 2]

### Week 8 (Design Partner)
- [ ] [Metric 1]
- [ ] [Metric 2]

### Week 12 (Public)
- [ ] [Metric 1]
- [ ] [Metric 2]

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | [H/M/L] | [H/M/L] | [Plan] |
| [Risk] | [H/M/L] | [H/M/L] | [Plan] |

## Next Steps

### This Week
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]

### Before Building
- [ ] Confirm design partners
- [ ] Architecture review complete
- [ ] Tech stack finalized
```

## The Anti-Scope Creep Checklist

Before adding ANY feature, ask:

1. **Does this test our core hypothesis?** → If no, cut it
2. **Have 3+ design partners asked for this?** → If no, defer it
3. **Can we launch without this?** → If yes, defer it
4. **Can we do this manually first?** → If yes, don't build it
5. **Will this delay launch by more than 3 days?** → If yes, cut it

## Integration with Other Skills

| Skill | How It Works Together |
|-------|----------------------|
| `idea-validator` | Validate before scoping |
| `startup-icp-definer` | Define who you're building for |
| `fullstack-workspace-init` | Set up the codebase |
| `project-scaffold` | Initialize project structure |
| `brand-architect` | Name and position the product |
| `offer-architect` | Design the offer around the MVP |

## Common Mistakes to Avoid

1. **Building before validating:** No design partners = building in the dark
2. **Too many features:** If you have more than 5, you're over-scoped
3. **Premature polish:** Ugly but working > beautiful but unfinished
4. **Fixed roadmaps:** Plans change—stay adaptable
5. **Building what you'd use:** You're not the customer (usually)
6. **Ignoring feedback:** Design partners know better than your assumptions
7. **Perfect architecture first:** You'll rewrite it anyway—ship first
8. **Underestimating manual options:** Many features can be manual for months

## The "Launch in 2 Weeks" Test

If I told you that you HAD to launch in 2 weeks, what would you cut?

**Whatever you'd cut... cut it now.**

That's your real MVP.

## When to Route Elsewhere

- If the problem isn't validated → `idea-validator`
- If you don't know who you're building for → `startup-icp-definer`
- If you need help with the tech setup → `fullstack-workspace-init`
- If you're stuck deciding → `execution-accelerator`
- If you need to price the MVP → `pricing-strategist`
