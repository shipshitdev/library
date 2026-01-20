# Market Sizer - Full Guide

## Execution Workflow

### Step 1: Define What You're Sizing

Ask the user:

> **What market are you sizing?**
>
> 1. What product/service are you offering?
> 2. Who is the target customer? (Company type, size, role)
> 3. What problem does it solve?
> 4. What geography are you targeting?
> 5. What's the price point or annual contract value?

**Sizing Parameters:**

| Parameter | Your Answer |
|-----------|-------------|
| Product/Service | [What you sell] |
| Target Customer | [Company type + buyer role] |
| Problem Solved | [Core pain point] |
| Geography | [Initial market] |
| Price Point | $[X]/month or $[X]/year |

### Step 2: Bottom-Up Analysis (Build from Units)

**Bottom-up starts with your specific customer and multiplies out.**

Ask the user:

> **Let's build from the ground up:**
>
> 1. How many potential customers exist in your target segment?
> 2. What's your expected annual revenue per customer?
> 3. What percentage can you realistically reach?
> 4. What conversion rate do you expect?

**Bottom-Up Formula:**

```
TAM = Total Potential Customers × Annual Revenue Per Customer

SAM = TAM × Percentage You Can Reach (geographic, segment fit)

SOM = SAM × Realistic Market Share (usually 1-5% in years 1-3)
```

**Bottom-Up Worksheet:**

| Component | Calculation | Value |
|-----------|-------------|-------|
| **TAM** | | |
| Total companies in target segment | [Count] | |
| × Companies with the problem | [%] | |
| × Average revenue per customer | [$X/year] | |
| = **TAM** | | **$X** |
| **SAM** | | |
| TAM | $X | |
| × In target geography | [%] | |
| × In target company size | [%] | |
| × Can afford your price | [%] | |
| = **SAM** | | **$X** |
| **SOM (3-Year)** | | |
| SAM | $X | |
| × Realistic market share | [1-5%] | |
| = **SOM** | | **$X** |

### Step 3: Top-Down Analysis (Start from Industry)

**Top-down starts with industry reports and narrows to your slice.**

Ask the user:

> **Let's validate from the top:**
>
> 1. What industry category does this fall into?
> 2. What's the total industry market size? (Look up reports)
> 3. What percentage is your specific segment?
> 4. What percentage is your geography?

**Common Data Sources:**

- Gartner, Forrester, IDC (enterprise software)
- Statista (general statistics)
- IBISWorld (industry reports)
- CB Insights, PitchBook (startup data)
- Government census data (business counts)
- Trade association reports

**Top-Down Worksheet:**

| Component | Calculation | Value |
|-----------|-------------|-------|
| **TAM** | | |
| Total industry market | [From report] | $X |
| = **TAM** | | **$X** |
| **SAM** | | |
| TAM | $X | |
| × Your segment's share | [%] | |
| × Your geography's share | [%] | |
| = **SAM** | | **$X** |
| **SOM (3-Year)** | | |
| SAM | $X | |
| × Realistic capture rate | [1-5%] | |
| = **SOM** | | **$X** |

### Step 4: Sanity Check (Compare Methods)

**The two methods should be within 2-3x of each other.**

| Metric | Bottom-Up | Top-Down | Variance |
|--------|-----------|----------|----------|
| TAM | $X | $X | [X%] |
| SAM | $X | $X | [X%] |
| SOM | $X | $X | [X%] |

**Interpretation:**

| Variance | Meaning | Action |
|----------|---------|--------|
| < 50% | Good alignment | Proceed with confidence |
| 50-200% | Reasonable variance | Investigate discrepancy |
| > 200% | Major misalignment | One method is wrong—investigate |

**Common Reasons for Variance:**

- Bottom-up overcounts potential customers
- Top-down industry definition too broad
- Pricing assumptions differ
- Geography assumptions differ

### Step 5: Market Dynamics Assessment

Ask the user:

> **What's happening in this market?**
>
> 1. Is the market growing, stable, or shrinking?
> 2. What's the annual growth rate?
> 3. What's driving growth or decline?
> 4. Are there consolidation or disruption trends?

**Market Dynamics:**

| Factor | Assessment |
|--------|------------|
| Growth Rate | [X% annually] |
| Growth Drivers | [What's causing growth] |
| Decline Risks | [What could shrink it] |
| Maturity | [Emerging/Growing/Mature/Declining] |
| Fragmentation | [Fragmented/Consolidating/Oligopoly] |

### Step 6: Timing Analysis (Why Now?)

Ask the user:

> **Why is NOW the right time?**
>
> 1. What barriers existed before that are now gone?
> 2. What technology enables this now?
> 3. What behavior has changed?
> 4. What regulatory/economic shifts support this?
> 5. Why hasn't this been built before?

**Timing Factors:**

| Factor | Evidence | Strength |
|--------|----------|----------|
| Technology enabler | [What's now possible] | [Strong/Moderate/Weak] |
| Behavior shift | [What's changed] | [Strong/Moderate/Weak] |
| Economic driver | [Budget/spending change] | [Strong/Moderate/Weak] |
| Regulatory change | [What's now allowed/required] | [Strong/Moderate/Weak] |
| Competitive vacuum | [Why gap exists] | [Strong/Moderate/Weak] |

**Timing Score:** Count "Strong" factors. 3+ = Great timing. 1-2 = Okay timing. 0 = Timing may be off.

### Step 7: Market Size Adequacy Test

**Is this market big enough for your ambitions?**

| Your Goal | Required SOM | Required SAM |
|-----------|--------------|--------------|
| Lifestyle business ($500K-2M/year) | $500K-2M | $10M+ |
| Venture-scale ($10M+ ARR) | $10M+ | $100M+ |
| Unicorn potential ($100M+ ARR) | $100M+ | $1B+ |

**The 10% Rule:**
If you captured 10% of your SAM, would that be an interesting business?

- **If yes:** Market is big enough
- **If no:** Market too small or SAM definition too narrow

## Output Format

```markdown
# Market Sizing Report: [Product/Market]

## Executive Summary

**Target Market:** [Description]
**Geography:** [Initial focus]
**Price Point:** $[X]/year per customer

### Market Size Summary

| Metric | Bottom-Up | Top-Down | Final Estimate |
|--------|-----------|----------|----------------|
| TAM | $[X]M | $[X]M | $[X]M |
| SAM | $[X]M | $[X]M | $[X]M |
| SOM (3-Year) | $[X]M | $[X]M | $[X]M |

**Confidence Level:** [High/Medium/Low]
**Variance Between Methods:** [X%]

## Bottom-Up Analysis

### Assumptions

| Parameter | Value | Source |
|-----------|-------|--------|
| Total potential customers | [X] | [How calculated] |
| % with the problem | [X%] | [Source/estimate] |
| Average revenue/customer | $[X] | [Pricing model] |
| % in target geography | [X%] | [Source] |
| % can afford price | [X%] | [Estimate] |
| Realistic market share (3yr) | [X%] | [Conservative/moderate/aggressive] |

### Calculations

**TAM:** [X] customers × $[X]/year = **$[X]M**

**SAM:** $[X]M × [X]% geography × [X]% segment fit = **$[X]M**

**SOM:** $[X]M × [X]% market share = **$[X]M**

## Top-Down Analysis

### Data Sources

| Source | Data Point | Value |
|--------|------------|-------|
| [Report/Source] | [What it says] | $[X] |
| [Report/Source] | [What it says] | [X%] |

### Calculations

**TAM:** [Industry total from reports] = **$[X]B**

**SAM:** $[X]B × [X]% your segment × [X]% geography = **$[X]M**

**SOM:** $[X]M × [X]% capture = **$[X]M**

## Variance Analysis

| Metric | Bottom-Up | Top-Down | Variance | Explanation |
|--------|-----------|----------|----------|-------------|
| TAM | $[X]M | $[X]M | [X%] | [Why different] |
| SAM | $[X]M | $[X]M | [X%] | [Why different] |
| SOM | $[X]M | $[X]M | [X%] | [Why different] |

## Market Dynamics

### Growth Trajectory

| Metric | Value | Source |
|--------|-------|--------|
| Current market size | $[X]M | [Source] |
| Annual growth rate | [X%] | [Source] |
| Projected size (5 years) | $[X]M | [Calculation] |

### Market Stage

**Current Stage:** [Emerging/Growing/Mature/Declining]

### Competitive Landscape

| Player Type | Count | Market Share |
|-------------|-------|--------------|
| Market leaders | [X] | [X%] |
| Mid-tier players | [X] | [X%] |
| Small/emerging | [X] | [X%] |
| Your opportunity | - | [X% available] |

## Timing Assessment

| Factor | Evidence | Strength |
|--------|----------|----------|
| Technology | [What enables this] | [Strong/Moderate/Weak] |
| Behavior | [What's changed] | [Strong/Moderate/Weak] |
| Economic | [Spending shifts] | [Strong/Moderate/Weak] |
| Regulatory | [Policy changes] | [Strong/Moderate/Weak] |
| Competitive | [Gap in market] | [Strong/Moderate/Weak] |

**Timing Score:** [X/5 strong factors]

## Adequacy Assessment

### Your Ambition vs. Market Size

| Goal | Required SOM | Your SOM | Adequate? |
|------|--------------|----------|-----------|
| Lifestyle ($1M ARR) | $1M | $[X]M | [Yes/No] |
| Venture ($10M ARR) | $10M | $[X]M | [Yes/No] |
| Unicorn ($100M ARR) | $100M | $[X]M | [Yes/No] |

### The 10% Test

**If you captured 10% of SAM:** $[X]M × 10% = **$[X]M**

**Is this interesting?** [Yes/No]

## Recommendations

### If Market Is Big Enough (SOM > Your Goal)

- [ ] Proceed with validation using `idea-validator`
- [ ] Define go-to-market using `startup-icp-definer`
- [ ] Scope MVP using `mvp-architect`

### If Market Is Too Small

**Options:**
1. **Expand geography** — Add more markets to SAM
2. **Expand use cases** — Solve adjacent problems
3. **Move upmarket** — Target larger customers (higher ACV)
4. **Create category** — If market doesn't exist, you're creating it

### If Market Is Declining

**Warning:** Entering a declining market requires:
- Clear disruption thesis
- Technology that transforms the category
- First-mover on a new platform
- Otherwise, avoid
```

## Market Size Benchmarks

### By Business Type

| Business Type | Typical SAM Needed | Typical SOM Target |
|--------------|-------------------|-------------------|
| Solo SaaS | $10M+ | $500K-2M |
| Bootstrapped startup | $50M+ | $2-10M |
| VC-backed seed | $100M+ | $10M+ |
| VC-backed Series A | $500M+ | $30M+ |
| Unicorn path | $1B+ | $100M+ |

### By ACV (Annual Contract Value)

| ACV | Customers Needed for $1M ARR | Customers for $10M ARR |
|-----|------------------------------|------------------------|
| $100/year | 10,000 | 100,000 |
| $1,000/year | 1,000 | 10,000 |
| $10,000/year | 100 | 1,000 |
| $100,000/year | 10 | 100 |

## Common Mistakes to Avoid

1. **Using only top-down:** "The market is $10B, we just need 1%" — Lazy and unconvincing
2. **Overcounting TAM:** Including everyone even tangentially related
3. **Ignoring competition:** TAM means nothing if competitors own it all
4. **Confusing TAM with SAM:** Your serviceable market is usually much smaller
5. **Static thinking:** Markets change—size today ≠ size in 5 years
6. **Ignoring timing:** Right market, wrong time = failure
7. **No bottom-up validation:** Top-down without unit economics is guessing
