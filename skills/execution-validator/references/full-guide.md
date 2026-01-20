# Execution Validator - Full Guide

## Execution Workflow

### Step 1: Gather the Plan

Ask the user:

> **Tell me about your plan:**
>
> 1. What are you building/launching?
> 2. How long have you been working on this?
> 3. What's left before you can launch/sell?
> 4. What's your biggest concern or blocker?
> 5. What would the simplest possible version look like?
> 6. Have you talked to any potential customers yet?

### Step 2: Score Action Bias (0-10, Weight: 2x)

Evaluate if they're **taking action or just planning**:

- How much **time** spent planning vs. doing?
- Have they **shipped anything** yet?
- Are they **talking to customers** or theorizing?
- Have they **made money** or gotten signups?
- Are they **moving daily** or "waiting"?

**Scoring Criteria:**

| Score | Description |
|-------|-------------|
| 9-10 | Taking daily action, shipping weekly, talking to customers |
| 7-8 | Regular action, some shipping, customer conversations happening |
| 5-6 | Some action mixed with planning, occasional progress |
| 3-4 | Heavy planning, minimal action, "almost ready" |
| 0-2 | All planning, no action, months of "preparation" |

**Red Flags:**

- "I've been working on this for X months" (with nothing shipped)
- "I just need to finish [one more thing]"
- "I'm doing market research" (for months)
- No customer conversations yet
- Waiting for perfect conditions

### Step 3: Score Scope Minimalism (0-10, Weight: 2x)

Evaluate if the **scope is tight or bloated**:

- Can they describe the MVP in **one sentence**?
- Is there **one core feature** or a feature list?
- Have they **cut scope** or added to it?
- Could they launch in **one week** if forced?
- Are they building **nice-to-haves** before **must-haves**?

**Scoring Criteria:**

| Score | Description |
|-------|-------------|
| 9-10 | Ruthlessly minimal, one core feature, could launch this week |
| 7-8 | Tight scope, clear priorities, couple weeks to launch |
| 5-6 | Some bloat, but core is clear, month to launch |
| 3-4 | Significant bloat, unclear priorities, timeline unclear |
| 0-2 | Massive scope, feature creep, "someday" launch |

**Red Flags:**

- "I also want to add..."
- "It needs to have X, Y, Z before launch"
- Feature list longer than customer list
- "Industry standard" features
- Building admin panel before users exist

### Step 4: Score Decision Clarity (0-10, Weight: 1.5x)

Evaluate if **decisions are made or pending**:

- Are there **open questions** blocking progress?
- Do they have a **clear next action**?
- Are they **stuck on decisions** that don't matter?
- Do they need **permission** from anyone?
- Are they waiting for **more information**?

**Scoring Criteria:**

| Score | Description |
|-------|-------------|
| 9-10 | All key decisions made, clear roadmap, no blockers |
| 7-8 | Most decisions made, minor uncertainties only |
| 5-6 | Some open questions, but path forward exists |
| 3-4 | Several pending decisions, unclear on priorities |
| 0-2 | Paralyzed by decisions, waiting for certainty |

**Red Flags:**

- "I can't decide between..."
- "I need to figure out..."
- "I'm waiting to hear back from..."
- Decisions that could be made in 5 minutes taking weeks
- Seeking consensus on solo decisions

**Decision Framework:**

| Decision Type | Time to Decide |
|--------------|----------------|
| Reversible | Make it now |
| Irreversible, small | Make it today |
| Irreversible, big | 24-48 hours max |

### Step 5: Score Time to First Value (0-10, Weight: 2x)

Evaluate **how fast they can deliver value to first customer**:

- How long until **first customer/user**?
- Could they **pre-sell** before building?
- What's the **minimum to test the core assumption**?
- Are they building before **validating demand**?
- Could they **manually deliver** value first?

**Scoring Criteria:**

| Score | Description |
|-------|-------------|
| 9-10 | Can deliver value this week, maybe already has customers |
| 7-8 | 2-4 weeks to first customer, clear path |
| 5-6 | 1-2 months, some building required first |
| 3-4 | 3-6 months, significant building needed |
| 0-2 | 6+ months, or no clear path to first customer |

**Red Flags:**

- "After I finish building..."
- No customer conversations yet
- Building complex tech before validation
- No pre-sales or waitlist
- "I'll find customers after launch"

**First Value Framework:**

```
Manual First → Validate → Semi-Automate → Automate
```

Don't automate what you haven't validated.

### Step 6: Score Excuse Detection (0-10, Weight: 1.5x)

Evaluate if blockers are **real or excuses**:

- Are blockers **solvable in 24 hours**?
- Are they **external** (real) or **internal** (fear)?
- Do blockers **actually matter** for first customer?
- Is "perfect" killing "good enough"?
- Is fear disguised as logic?

**Scoring Criteria:**

| Score | Description |
|-------|-------------|
| 9-10 | No excuses, action-focused, solves problems as they arise |
| 7-8 | Minimal excuses, acknowledges fear but moves anyway |
| 5-6 | Some excuses mixed with real blockers |
| 3-4 | Multiple excuses, fear-based delays |
| 0-2 | Excuse machine, fear running the show |

### Step 7: Calculate Final Score

**Formula:**

```
Action Bias × 2 = ___
Scope Minimalism × 2 = ___
Decision Clarity × 1.5 = ___
Time to First Value × 2 = ___
Excuse Detection × 1.5 = ___
─────────────────────────
TOTAL = ___ / 100
```

## Output Format

```markdown
# Execution Validation: [Project Name]

## Quick Rating

| Rating | Score | Verdict |
|--------|-------|---------|
| [Ready / Almost / Needs Work / Stuck / Paralysis] | XX/100 | [One-line summary] |

## Speed Assessment

**Time in Planning:** [X weeks/months]
**Time to First Customer (Current Plan):** [X weeks/months]
**Time to First Customer (Compressed):** [X days/weeks]

**The One Thing That Matters:**
> [Single most important next action]

## Score Breakdown

| Dimension | Raw Score | Weight | Weighted Score | Status |
|-----------|-----------|--------|----------------|--------|
| Action Bias | X/10 | ×2 | XX/20 | [Act/Improve/Strong] |
| Scope Minimalism | X/10 | ×2 | XX/20 | [Cut/Trim/Strong] |
| Decision Clarity | X/10 | ×1.5 | XX/15 | [Decide/Clarify/Strong] |
| Time to First Value | X/10 | ×2 | XX/20 | [Compress/Improve/Strong] |
| Excuse Detection | X/10 | ×1.5 | XX/15 | [Confront/Acknowledge/Strong] |
| **TOTAL** | | | **XX/100** | |

## One Week Sprint Plan

If you had to launch in one week, here's exactly what to do:

### Day 1-2: Core Only
- [ ] [Minimum viable action]
- [ ] [Core feature only]

### Day 3-4: Test
- [ ] [Get it in front of people]
- [ ] [Gather feedback]

### Day 5-6: Iterate
- [ ] [Fix critical issues]
- [ ] [Ignore everything else]

### Day 7: Launch
- [ ] [Ship it]
- [ ] [Get first customer/user]

## Scope Surgery

### Cut These (Not Needed for V1):
- [Feature/task to cut]
- [Feature/task to cut]

### Keep These (Essential Only):
- [Essential feature]
- [Essential feature]

### The Minimum Viable Test:
> [One sentence describing the simplest possible test of the core assumption]

## Next Steps

### If Score 85+:
- [ ] Stop reading this
- [ ] Execute now
- [ ] Ship something today

### If Score 70-84:
- [ ] Make the pending decisions above
- [ ] Cut the scope items listed
- [ ] Set a launch date (this week)

### If Score 55-69:
- [ ] Do the one week sprint above
- [ ] No more planning allowed
- [ ] Talk to 5 customers this week

### If Score Below 55:
- [ ] Stop all building
- [ ] Manual delivery first
- [ ] Pre-sell before building anything
```

## Example Validations

### Example: Analysis Paralysis

**User's Situation:**

- Working on SaaS idea for 4 months
- Has "almost finished" the product
- Hasn't talked to customers yet
- Wants to "add a few more features"

**Validation:**

| Dimension | Score | Issue |
|-----------|-------|-------|
| Action Bias | 3/10 | 4 months, no customers |
| Scope Minimalism | 2/10 | Feature list keeps growing |
| Decision Clarity | 4/10 | "Deciding" on features for weeks |
| Time to First Value | 2/10 | "Maybe next month" |
| Excuse Detection | 3/10 | "Need to finish X first" |

**Total: 27/100 - Analysis Paralysis**

**Prescription:**

1. STOP building immediately
2. List 10 potential customers
3. Call 5 of them THIS WEEK
4. Pre-sell the concept before building more
5. Launch what you have in 7 days

### Example: Almost Ready

**User's Situation:**

- MVP built in 2 weeks
- Has talked to 10 potential customers
- 3 people interested in paying
- Waiting on "one more feature"

**Validation:**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Action Bias | 8/10 | Good speed, customer contact |
| Scope Minimalism | 7/10 | Mostly minimal, one extra feature |
| Decision Clarity | 8/10 | Clear next steps |
| Time to First Value | 7/10 | Close to launch |
| Excuse Detection | 6/10 | That "one more feature" is an excuse |

**Total: 73/100 - Almost Ready**

**Prescription:**

1. Cut "one more feature" - launch without it
2. Convert 3 interested people to paid THIS WEEK
3. Add feature after first revenue

## Common Validation Mistakes

1. **Being Too Gentle:** Call out excuses directly
2. **Accepting Scope:** Always push for smaller
3. **Validating Planning:** Plans don't matter, action does
4. **Accepting Timelines:** Compress aggressively
5. **Missing Fear:** Most blockers are fear in disguise
