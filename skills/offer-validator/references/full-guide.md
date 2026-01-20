# Offer Validator - Full Guide

Complete guide to validating offers against Hormozi's Value Equation.

## Scoring Criteria

### Dream Outcome (0-10, Weight: 2x)

| Score | Description |
|-------|-------------|
| 9-10 | Crystal clear, deeply desirable transformation that speaks to their core pain |
| 7-8 | Clear outcome, addresses real desire, but could be more emotionally compelling |
| 5-6 | Decent outcome, somewhat vague, or only addresses surface-level wants |
| 3-4 | Unclear outcome, feature-focused instead of outcome-focused |
| 0-2 | No clear outcome, just a list of deliverables |

**Red Flags:**

- "Get access to..." (feature, not outcome)
- "Learn how to..." (process, not result)
- Vague superlatives ("the best", "amazing results")
- No specific numbers or timeframes

### Perceived Likelihood (0-10, Weight: 2x)

| Score | Description |
|-------|-------------|
| 9-10 | Overwhelming proof: specific results, multiple testimonials, clear track record |
| 7-8 | Good proof: some testimonials, credentials established, believable claims |
| 5-6 | Moderate proof: generic testimonials, some credibility, but gaps |
| 3-4 | Weak proof: claims without evidence, vague testimonials |
| 0-2 | No proof: just promises with nothing to back them up |

**Red Flags:**

- "Results may vary" (without context)
- Stock photo testimonials
- No specific numbers in case studies
- "Trust me" without evidence

### Time to Results (0-10, Weight: 1.5x, Inverted)

| Score | Description |
|-------|-------------|
| 9-10 | Immediate quick wins (24-48 hours) with clear milestones to big outcome |
| 7-8 | Results within first week, clear timeline, some quick wins |
| 5-6 | Results in 2-4 weeks, some milestones, but waiting period |
| 3-4 | Results in 1-3 months, vague timeline, long wait before any wins |
| 0-2 | No timeline given, or results take 6+ months with no quick wins |

**Red Flags:**

- No timeline mentioned
- "Results take time" without specifics
- No quick wins or early milestones

### Effort Required (0-10, Weight: 1.5x, Inverted)

| Score | Description |
|-------|-------------|
| 9-10 | Done-for-you, plug-and-play, zero learning curve |
| 7-8 | Done-with-you, templates provided, minimal learning, hand-held |
| 5-6 | Some effort required, decent templates, moderate learning curve |
| 3-4 | Significant effort, must learn and implement, limited support |
| 0-2 | High effort, steep learning curve, they do everything themselves |

**Red Flags:**

- "You'll learn how to..." (implies effort)
- No templates or done-for-you elements
- "Self-paced" without support

### Bonus Stack (0-10, Weight: 1x)

| Score | Description |
|-------|-------------|
| 9-10 | Overwhelming stack: 4+ bonuses that each stand alone in value |
| 7-8 | Strong stack: 2-3 valuable bonuses that address different needs |
| 5-6 | Decent stack: 1-2 bonuses, somewhat useful |
| 3-4 | Weak stack: bonuses feel like filler or don't add real value |
| 0-2 | No bonuses, or bonuses that are obviously padding |

**Red Flags:**

- Bonuses that feel like padding
- Inflated bonus values ("$997 value" for a PDF)
- Bonuses that duplicate the core offer

### Guarantee Strength (0-10, Weight: 1x)

| Score | Description |
|-------|-------------|
| 9-10 | Performance guarantee with specific outcome, plus bonus if they fail |
| 7-8 | Conditional guarantee with clear criteria, or strong unconditional |
| 5-6 | Standard money-back guarantee (30-60 days) |
| 3-4 | Vague guarantee, restrictive conditions, or hard to claim |
| 0-2 | No guarantee, or "all sales final" |

**Red Flags:**

- "Satisfaction guaranteed" (meaningless)
- Hidden conditions to claim guarantee
- 7-day or very short guarantee window

## Score Calculation

```
Dream Outcome Score × 2 = ___
Perceived Likelihood × 2 = ___
Time to Results × 1.5 = ___
Effort Required × 1.5 = ___
Bonus Stack × 1 = ___
Guarantee × 1 = ___
─────────────────────────
TOTAL = ___ / 100
```

## Output Template

```markdown
# Offer Validation: [Offer Name]

## Quick Rating

| Rating | Score | Verdict |
|--------|-------|---------|
| [Grand Slam / Strong / Decent / Weak / Broken] | XX/100 | [One-line summary] |

## Score Breakdown

| Dimension | Raw Score | Weight | Weighted Score | Status |
|-----------|-----------|--------|----------------|--------|
| Dream Outcome | X/10 | ×2 | XX/20 | [Fix/Optimize/Strong] |
| Perceived Likelihood | X/10 | ×2 | XX/20 | [Fix/Optimize/Strong] |
| Time to Results | X/10 | ×1.5 | XX/15 | [Fix/Optimize/Strong] |
| Effort Required | X/10 | ×1.5 | XX/15 | [Fix/Optimize/Strong] |
| Bonus Stack | X/10 | ×1 | XX/10 | [Fix/Optimize/Strong] |
| Guarantee | X/10 | ×1 | XX/10 | [Fix/Optimize/Strong] |
| **TOTAL** | | | **XX/100** | |

## Detailed Assessment

### Dream Outcome: X/10
**What's Working:** [Positive aspects]
**What's Missing:** [Gaps identified]
**Fix:** [Specific action to improve]

[Repeat for each dimension...]

## Priority Fixes (Do These First)

1. **[Dimension]:** [Specific fix with expected impact]
2. **[Dimension]:** [Specific fix with expected impact]
3. **[Dimension]:** [Specific fix with expected impact]

## Next Steps

### If Score 85+:
- [ ] Launch and scale
- [ ] A/B test minor optimizations

### If Score 70-84:
- [ ] Fix priority items above
- [ ] Re-validate after changes

### If Score 55-69:
- [ ] Major rework needed before launch
- [ ] Use `offer-architect` to rebuild weak components

### If Score Below 55:
- [ ] Do not launch this offer
- [ ] Use `offer-architect` to create from scratch
```

## Example Validations

### Example: Weak Offer (28/100)

**User's Offer:**
"Social Media Management - $500/month

- 3 posts per week
- Monthly report
- Email support"

| Dimension | Score | Issue |
|-----------|-------|-------|
| Dream Outcome | 3/10 | No outcome, just deliverables |
| Perceived Likelihood | 2/10 | No proof, no credentials |
| Time to Results | 4/10 | No timeline or quick wins |
| Effort Required | 6/10 | Done-for-you (good) |
| Bonus Stack | 1/10 | No bonuses |
| Guarantee | 1/10 | No guarantee mentioned |

**Priority Fixes:**

1. **Add Dream Outcome:** "Book 5+ sales calls from social media in 90 days"
2. **Add Proof:** Show case studies with specific numbers
3. **Add Guarantee:** "5 calls in 90 days or we work free until you get them"

### Example: Strong Offer (81/100)

**User's Offer:**
"Revenue Machine: Done-For-You Social That Sells - $1,997/mo

- For service businesses stuck under $50K/mo
- 90 days of done-for-you content
- Weekly lead intelligence report
- Direct-to-DM sales system
- Guarantee: 5 sales calls in 90 days or we work free
- Bonuses: DM templates, strategy call, content vault"

| Dimension | Score | Notes |
|-----------|-------|-------|
| Dream Outcome | 8/10 | Clear outcome (sales calls), specific timeline |
| Perceived Likelihood | 7/10 | Needs more case studies |
| Time to Results | 8/10 | 90 days with weekly milestones |
| Effort Required | 9/10 | Done-for-you, minimal customer effort |
| Bonus Stack | 7/10 | Solid stack, could be stronger |
| Guarantee | 9/10 | Performance guarantee, clear and strong |

**Minor Optimizations:**

1. Add 2-3 case studies with specific numbers
2. Add one more "certainty" bonus (community access?)

## Common Validation Mistakes

1. **Being Too Nice:** Don't sugarcoat. Tell them what's broken.
2. **Missing Context:** Always understand WHO the offer is for
3. **Ignoring Competition:** What are competitors offering?
4. **Surface-Level Assessment:** Dig into WHY each score is what it is
5. **No Actionable Fixes:** Every weakness needs a specific fix
6. **Skipping Dimensions:** Score all 6 dimensions, even if they overlap
