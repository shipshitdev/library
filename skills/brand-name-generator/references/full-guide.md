# Brand Name Generator - Full Guide

Complete guide to generating creative, memorable, and brandable names for companies, products, apps, and startups.

## AI-Assisted Name Generation

### Basic Generation Prompt

```
Generate 20 brand name ideas for a [INDUSTRY] company that [CORE_VALUE_PROPOSITION].

Requirements:
- Names should be 1-2 words, max 10 characters preferred
- Easy to spell and pronounce
- Memorable and unique
- Appropriate for [TARGET_AUDIENCE]

Keywords to incorporate or draw inspiration from: [KEYWORDS]

Brand personality: [PERSONALITY_TRAITS]

For each name, provide:
1. The name
2. Brief meaning/rationale
3. Suggested domain (.com, .io, etc.)
```

### Strategy-Specific Prompts

**Portmanteau Names (Pinterest, Instagram):**

```
Create 10 portmanteau brand names by creatively combining these concept pairs:
- [WORD1] + [WORD2]
- [WORD3] + [WORD4]

Rules:
- Blend should feel natural and pronounceable
- Result should be 6-10 characters
- Should hint at both source words
```

**Invented Words (Spotify, Kodak):**

```
Invent 10 completely new words that could work as brand names for a [INDUSTRY] company.

Guidelines:
- Use pleasing phonetics (soft consonants, open vowels)
- 5-8 characters ideal
- Should feel modern and tech-forward
- Easy to pronounce in English

For each, explain the phonetic appeal.
```

**Abstract/Metaphorical Names (Amazon, Apple, Uber):**

```
Generate 10 abstract or metaphorical brand names for a [INDUSTRY] company.

Draw from:
- Nature (animals, plants, elements)
- Mythology (gods, heroes, places)
- Science (concepts, phenomena)
- Geography (places, landmarks)

Each name should evoke: [DESIRED_EMOTIONS]
```

**Modern Tech Names (Stripe, Slack, Notion):**

```
Generate 10 single-word brand names with a modern tech feel for a [PRODUCT_TYPE].

Characteristics:
- Short (4-7 characters)
- Real English words with abstract meanings
- Evokes simplicity and efficiency
- Works well as a verb ("Let's Slack them")
```

## Brandability Scoring Implementation

### TypeScript

```typescript
interface BrandabilityScore {
  memorability: number;      // 1-10: How easily remembered
  pronounceability: number;  // 1-10: How easily spoken
  spellability: number;      // 1-10: How easily written
  uniqueness: number;        // 1-10: How distinctive
  meaningfulness: number;    // 1-10: How relevant to brand
  domainAvailable: boolean;  // .com availability
  totalScore: number;        // Weighted average
}

function scoreBrandability(name: string): BrandabilityScore {
  const scores = {
    // Memorability: shorter names score higher
    memorability: Math.max(1, 10 - Math.floor(name.length / 2)),

    // Pronounceability: check for difficult consonant clusters
    pronounceability: calculatePronounceability(name),

    // Spellability: common letter patterns score higher
    spellability: calculateSpellability(name),

    // Uniqueness: check against common words/brands
    uniqueness: calculateUniqueness(name),

    // Meaningfulness: context-dependent
    meaningfulness: 7, // Default, adjust based on context

    domainAvailable: false // Check via API
  };

  // Weighted average (adjust weights as needed)
  scores.totalScore = (
    scores.memorability * 0.25 +
    scores.pronounceability * 0.20 +
    scores.spellability * 0.20 +
    scores.uniqueness * 0.20 +
    scores.meaningfulness * 0.15
  );

  return scores;
}

function calculatePronounceability(name: string): number {
  const difficultPatterns = /[bcdfghjklmnpqrstvwxz]{4,}|^[^aeiou]+$/i;
  const vowelRatio = (name.match(/[aeiou]/gi) || []).length / name.length;

  let score = 10;
  if (difficultPatterns.test(name)) score -= 3;
  if (vowelRatio < 0.2) score -= 2;
  if (vowelRatio > 0.6) score -= 1;

  return Math.max(1, score);
}

function calculateSpellability(name: string): number {
  const confusingPatterns = [
    /ph/, /gh/, /ough/, /ie|ei/, /double[lsz]/,
    /[ck](?=[ei])/, /qu/, /x(?=[aou])/
  ];

  let score = 10;
  for (const pattern of confusingPatterns) {
    if (pattern.test(name.toLowerCase())) score -= 1;
  }

  return Math.max(1, score);
}
```

### Python

```python
import re
from dataclasses import dataclass

@dataclass
class BrandabilityScore:
    memorability: int
    pronounceability: int
    spellability: int
    uniqueness: int
    meaningfulness: int
    domain_available: bool
    total_score: float

def score_brandability(name: str) -> BrandabilityScore:
    """Calculate brandability score for a name."""

    # Memorability: shorter = better
    memorability = max(1, 10 - len(name) // 2)

    # Pronounceability
    pronounceability = calculate_pronounceability(name)

    # Spellability
    spellability = calculate_spellability(name)

    # Uniqueness (simplified - would need database check)
    uniqueness = 7

    # Meaningfulness (context-dependent)
    meaningfulness = 7

    # Weighted total
    total = (
        memorability * 0.25 +
        pronounceability * 0.20 +
        spellability * 0.20 +
        uniqueness * 0.20 +
        meaningfulness * 0.15
    )

    return BrandabilityScore(
        memorability=memorability,
        pronounceability=pronounceability,
        spellability=spellability,
        uniqueness=uniqueness,
        meaningfulness=meaningfulness,
        domain_available=False,
        total_score=round(total, 2)
    )

def calculate_pronounceability(name: str) -> int:
    """Score how easy a name is to pronounce."""
    score = 10

    # Check for consonant clusters
    if re.search(r'[bcdfghjklmnpqrstvwxz]{4,}', name, re.I):
        score -= 3

    # Check vowel ratio
    vowels = len(re.findall(r'[aeiou]', name, re.I))
    ratio = vowels / len(name) if name else 0

    if ratio < 0.2:
        score -= 2
    elif ratio > 0.6:
        score -= 1

    return max(1, score)

def calculate_spellability(name: str) -> int:
    """Score how easy a name is to spell."""
    confusing = ['ph', 'gh', 'ough', 'ie', 'ei', 'qu']
    score = 10

    name_lower = name.lower()
    for pattern in confusing:
        if pattern in name_lower:
            score -= 1

    return max(1, score)
```

## Domain Integration

```typescript
import { isValidDomain } from './domain-validator';
import { checkDomainAvailability } from './domain-checker';

interface NameSuggestion {
  name: string;
  score: BrandabilityScore;
  domains: DomainOption[];
}

interface DomainOption {
  domain: string;
  available: boolean;
  tld: string;
}

async function generateWithDomainCheck(
  names: string[],
  tlds: string[] = ['com', 'io', 'co', 'ai', 'app']
): Promise<NameSuggestion[]> {
  const suggestions: NameSuggestion[] = [];

  for (const name of names) {
    const cleanName = name.toLowerCase().replace(/[^a-z0-9]/g, '');
    const score = scoreBrandability(name);
    const domains: DomainOption[] = [];

    for (const tld of tlds) {
      const domain = `${cleanName}.${tld}`;

      if (isValidDomain(domain)) {
        const available = await checkDomainAvailability(domain);
        domains.push({ domain, available, tld });

        if (available && tld === 'com') {
          score.domainAvailable = true;
          score.totalScore += 0.5; // Bonus for .com availability
        }
      }
    }

    suggestions.push({ name, score, domains });
  }

  // Sort by total score descending
  return suggestions.sort((a, b) => b.score.totalScore - a.score.totalScore);
}
```

## Complete Workflow Example

**User Request:** "Generate brand names for a productivity app for remote teams"

**Step 1: Gather Context**

```
Industry: SaaS / Productivity
Target: Remote workers, distributed teams
Values: Efficiency, collaboration, simplicity
Keywords: team, work, remote, flow, sync, together
Style: Modern, professional, approachable
```

**Step 2: Generate Names (AI Prompt)**

```
Generate 15 brand names for a productivity app targeting remote teams.

Requirements:
- 4-8 characters preferred
- Modern tech feel
- Easy to spell internationally
- Works as a verb ("Let's [name] this")

Keywords: team, flow, sync, collaborate, remote, together

Styles to explore:
- Abstract single words (like Slack, Notion)
- Invented words (like Asana, Trello)
- Compound/portmanteau (like Teamwork, Basecamp)
```

**Step 3: Evaluate Results**

| Name | Memorability | Pronounce | Spell | Unique | Score | .com |
|------|--------------|-----------|-------|--------|-------|------|
| Flowly | 9 | 9 | 9 | 7 | 8.4 | No |
| Syntra | 8 | 8 | 7 | 9 | 8.0 | Yes |
| Teamo | 9 | 10 | 9 | 6 | 8.3 | No |
| Collab | 8 | 9 | 9 | 5 | 7.6 | No |
| Remoto | 8 | 9 | 8 | 7 | 7.9 | Yes |

**Step 4: Final Recommendations**

1. **Syntra** - Invented word, .com available, strong tech feel
2. **Flowly** - Descriptive suffix pattern, memorable
3. **Teamo** - Playful portmanteau (Team + amigo/o)

## Best Practices

### Name Generation

- Generate 20-30 candidates before filtering
- Use multiple naming strategies for variety
- Check trademark databases before finalizing
- Test pronunciation with native speakers of target markets
- Verify no negative meanings in other languages

### Domain Strategy

- Prioritize .com for maximum credibility
- Consider .io for developer tools, .ai for AI products
- Check social media handle availability simultaneously
- Avoid hyphens and numbers in domains

## Example User Requests

**Example 1: "Generate names for a fintech startup"**

- Gather: target audience, specific fintech area (payments, lending, investing)
- Generate using: abstract names, invented words, -fy/-ly suffixes
- Check: .com, .io, .co availability

**Example 2: "I need a name for my AI writing tool"**

- Gather: target users (writers, marketers, students), key differentiator
- Generate using: compound words, invented words, -ai suffix
- Check: .ai, .com availability

**Example 3: "Find available domains for brand name 'Nexify'"**

- Validate format using search-domain-validator
- Check availability across TLDs
- Suggest alternatives if unavailable: Nexifyr, Nexifly, GetNexify
