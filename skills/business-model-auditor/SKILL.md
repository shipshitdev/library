---
name: business-model-auditor
description: >-
  Stress-tests business models to identify scale limitations, bottlenecks, and
  unit economics gaps using Hormozi frameworks. Triggers when a user asks "can
  this scale," "what breaks at 10x," mentions being the bottleneck, wants unit
  economics reviewed, or asks about business model viability.
metadata:
  version: "1.0.0"
  tags: "business, hormozi, scale, leverage, unit-economics, bottlenecks, business-model"
---

# Business Model Auditor - Scale Stress Test

## Overview

Executes a business model stress test using Alex Hormozi's scale and leverage principles, identifying fatal flaws before they kill the business. Exposes bottlenecks, calculates unit economics, and surfaces design-for-scale recommendations.

**Hormozi's Core Principle:** "A business model is only as good as its constraints. Can this scale without me?"

## The Framework: The Scale Test

**Key Questions:**

1. **Time Independence:** Does revenue require YOUR time linearly?
2. **Unit Economics:** Does each customer generate more than they cost?
3. **Bottleneck Clarity:** What breaks first at 10x scale?
4. **Leverage Type:** Are you building assets or just working?
5. **Margin Integrity:** Do margins hold or erode at scale?

## Execution Workflow

### Step 1: Current Model Mapping

Ask the user:

> **Describe your business model:**
>
> 1. How do you make money? (What do customers pay for?)
> 2. What's your average revenue per customer?
> 3. How much does it cost to acquire a customer?
> 4. How much does it cost to deliver what they bought?
> 5. How many hours do YOU spend per customer?

**Model Summary Template:**

| Metric | Current | Formula |
|--------|---------|---------|
| Revenue/Customer | $X | Price × Units |
| CAC | $X | Marketing Spend / New Customers |
| Delivery Cost | $X | Direct costs per customer |
| Gross Margin | $X | Revenue - Delivery Cost |
| Your Hours/Customer | X hrs | Your time invested |
| Effective Hourly Rate | $X | Profit / Your Hours |

### Step 2: Unit Economics Deep Dive

Calculate the fundamental health:

**Core Unit Economics:**

```
Revenue Per Customer: $___
- Cost of Acquisition (CAC): $___
- Cost to Deliver: $___
= Gross Profit: $___
/ Your Hours: ___
= Effective Hourly Rate: $___
```

**Health Check:**

| Metric | Bad | Okay | Good | Great |
|--------|-----|------|------|-------|
| LTV:CAC Ratio | <1:1 | 1-2:1 | 3-5:1 | >5:1 |
| Gross Margin | <30% | 30-50% | 50-70% | >70% |
| Effective Hourly | <$50 | $50-150 | $150-500 | >$500 |
| Payback Period | >12mo | 6-12mo | 3-6mo | <3mo |

### Step 3: Time Dependency Analysis

Ask the user:

> **How does your time relate to revenue?**
>
> 1. If you took a month off, what would happen to revenue?
> 2. What % of delivery requires YOUR specific involvement?
> 3. What tasks ONLY you can do?
> 4. What tasks could be delegated?
> 5. What tasks could be eliminated?

**Time Dependency Score:**

| Scenario | Score | Meaning |
|----------|-------|---------|
| Business stops if you stop | 1/10 | Totally dependent |
| Revenue drops 50%+ | 3/10 | Highly dependent |
| Revenue drops 20-50% | 5/10 | Moderately dependent |
| Revenue drops <20% | 7/10 | Low dependency |
| Revenue unaffected | 9/10 | Time independent |
| Revenue grows without you | 10/10 | True leverage |

### Step 4: The 10x Stress Test

> **What happens if you 10x customers tomorrow?**
>
> 1. What breaks first? (Delivery, support, quality, YOU)
> 2. What would you need to handle 10x? (People, systems, tools)
> 3. What would your margins look like at 10x?
> 4. How would customer experience change?
> 5. What's the actual capacity limit right now?

**Bottleneck Categories:**

| Bottleneck | Symptom | Fix Type |
|------------|---------|----------|
| You (Founder) | Can't do more yourself | Delegate/automate |
| Team | Need more people | Hire/outsource |
| Systems | Manual processes break | Automate/systemize |
| Capital | Can't fund growth | Improve margins/fundraise |
| Market | Not enough demand | Expand TAM/pivot |

### Step 5: Leverage Audit

**Four Types of Leverage:**

| Leverage Type | Description | Example | Scale Factor |
|--------------|-------------|---------|--------------|
| **Labor** | Other people's time | Employees, contractors | Linear |
| **Capital** | Other people's money | Invest to grow | Variable |
| **Code** | Software/automation | SaaS, tools | Infinite |
| **Media** | Content/audience | YouTube, podcasts | Infinite |

> **Assess your current leverage:**
>
> 1. Are you using labor leverage? (Team multiplies your output)
> 2. Are you using capital leverage? (Money working for you)
> 3. Are you using code leverage? (Software scales infinitely)
> 4. Are you using media leverage? (Content works while you sleep)

**Leverage Score:**

- 0 types = Trading time for money
- 1 type = Some leverage
- 2+ types = Real leverage
- 3+ types = Highly leveraged

### Step 6: Model Stress Points

Identify where the model will break:

**Stress Point Mapping:**

| Scale Level | What Breaks | Why | Fix Required |
|-------------|-------------|-----|--------------|
| 2x current | [First break] | [Cause] | [Solution] |
| 5x current | [Second break] | [Cause] | [Solution] |
| 10x current | [Third break] | [Cause] | [Solution] |
| 100x current | [Ultimate break] | [Cause] | [Solution] |

### Step 7: Fix Recommendations

For each bottleneck:

**Priority Framework:**

1. **First:** Fix the lowest-cost, highest-impact bottleneck
2. **Second:** Fix what directly impacts revenue
3. **Third:** Fix what impacts margin
4. **Fourth:** Fix what impacts customer experience

## Output Format

See `assets/output-template.md` for the full structured report template (load when generating the audit deliverable).

## Quick Scale Score (100-Point Assessment)

For fast validation without the full audit:

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Time Independence | 2x | Can it run without you? |
| Unit Economics | 2x | Do the numbers work at scale? |
| Bottleneck Clarity | 1.5x | Do you know what's constraining? |
| Leverage Active | 1x | How many leverage types? |
| Delivery Scalability | 1.5x | Can you deliver 10x without 10x cost? |
| Margin Integrity | 1x | Do margins hold at scale? |

| Score | Rating | Verdict |
|-------|--------|---------|
| 85-100 | Scale-Ready | Pour fuel on fire |
| 70-84 | Strong Foundation | Fix weak points first |
| 55-69 | Fixable | Address constraints first |
| 40-54 | Risky | Major issues to fix |
| 0-39 | Broken Model | Rebuild fundamentals |

## The "Would I Hire Me?" Test

Ask yourself:
> "If this business had to pay me a salary for the work I do, would the economics still work?"

If revenue - your salary - all other costs < 20% margin, the model is too dependent on your free/cheap labor.

## Model Evolution Paths

**From Service to Productized Service:**

- Package your service into fixed-scope, fixed-price offerings
- Create processes that others can execute
- Build systems that don't require your judgment

**From Productized Service to SaaS:**

- Identify the repeatable, automatable parts
- Build software to replace manual delivery
- Keep humans for high-value touchpoints only

**From 1:1 to 1:Many:**

- Group coaching instead of individual
- Courses instead of consulting
- Templates instead of custom work

## Integration with Other Skills

| Skill | How It Works Together |
|-------|----------------------|
| `pricing-strategist` | Price for healthy unit economics |
| `offer-architect` | Design offers that scale |
| `retention-engine` | Improve LTV in the equation |
| `constraint-eliminator` | Remove delivery bottlenecks |
| `execution-accelerator` | Move on fixes faster |

## Common Mistakes to Avoid

1. **Ignoring your time cost:** Counting "profit" without valuing your hours
2. **Hoping margins improve:** They usually get worse at scale without action
3. **Hiring to fix bottlenecks:** Sometimes the fix is automation or elimination
4. **Scaling before fixing:** 10x a broken model = 10x the problems
5. **Complexity creep:** Adding services that don't scale
6. **Vanity revenue:** Growing revenue while margins shrink

## The Founder Replacement Test

Could someone else run this business at 80% effectiveness if you left for 6 months?

- **If yes:** You have a business
- **If no:** You have a job you created for yourself

## When to Route Elsewhere

- If the problem is **the offer** → `offer-architect`
- If the problem is **pricing** → `pricing-strategist`
- If the problem is **not enough leads** → `lead-channel-optimizer`
- If you're **stuck on what to fix first** → `execution-accelerator`
