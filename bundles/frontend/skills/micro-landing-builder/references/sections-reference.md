# Sections Reference

Quick reference for available section types and their props.

---

## Section Order Recommendations

Typical landing page flow:

1. `hero` - First impression, main value prop
2. `stats` - Social proof numbers (optional)
3. `features` - What the product does
4. `pricing` - How much it costs
5. `testimonials` - Social proof quotes
6. `faq` - Address objections
7. `cta` - Final conversion

---

## Hero

The main hero section at the top of the page.

```json
{
  "type": "hero",
  "eyebrow": "Now in beta",
  "headline": "Your main headline",
  "subheadline": "Supporting text that explains the value",
  "badges": ["YC W24", "Product Hunt #1"],
  "primaryCta": { "label": "Get Started", "href": "#signup" },
  "secondaryCta": { "label": "Learn More", "href": "#features" },
  "image": "/hero.png",
  "note": "No credit card required"
}
```

**Tips:**

- Keep headline under 10 words
- Subheadline should explain the "how"
- Include social proof badges if available

---

## Stats

Key metrics that build credibility.

```json
{
  "type": "stats",
  "items": [
    { "value": "10K+", "label": "Users" },
    { "value": "99.9%", "label": "Uptime" },
    { "value": "4.9", "label": "Rating" },
    { "value": "50M+", "label": "Requests" }
  ]
}
```

**Tips:**

- Use 3-4 stats maximum
- Include units in value (K, M, %)
- Focus on impressive numbers

---

## Features

Showcase product capabilities.

```json
{
  "type": "features",
  "title": "Everything you need",
  "subtitle": "Powerful features for modern teams",
  "items": [
    {
      "icon": "zap",
      "title": "Lightning Fast",
      "description": "Sub-millisecond response times"
    },
    {
      "icon": "shield",
      "title": "Secure",
      "description": "Enterprise-grade security"
    },
    {
      "icon": "trending-up",
      "title": "Analytics",
      "description": "Real-time insights"
    }
  ]
}
```

**Available icons:**

- `zap` - Speed/performance
- `shield` - Security
- `trending-up` - Growth/analytics
- `users` - Team/collaboration
- `lock` - Privacy
- `globe` - Global/international
- `check` - Verification/success
- `star` - Quality/premium
- `heart` - Favorites/love
- `settings` - Customization

**Tips:**

- Use 3, 6, or 9 features for best grid layout
- Keep descriptions under 15 words

---

## Pricing

Display pricing plans.

```json
{
  "type": "pricing",
  "title": "Simple pricing",
  "subtitle": "No hidden fees",
  "plans": [
    {
      "name": "Free",
      "price": { "monthly": 0, "yearly": 0 },
      "description": "For individuals",
      "features": ["1,000 requests", "Basic support"],
      "cta": { "label": "Start Free", "href": "#" }
    },
    {
      "name": "Pro",
      "price": { "monthly": 29, "yearly": 290 },
      "description": "For teams",
      "features": ["Unlimited requests", "Priority support"],
      "cta": { "label": "Get Pro", "href": "#" },
      "highlighted": true
    }
  ]
}
```

**Tips:**

- Always include a free tier
- Highlight the recommended plan
- Keep feature lists scannable (5-7 items)

---

## Testimonials

Social proof from customers.

```json
{
  "type": "testimonials",
  "title": "Loved by teams",
  "items": [
    {
      "quote": "This product changed everything for us.",
      "author": "Jane Doe",
      "role": "CEO at TechCorp",
      "avatar": "/avatars/jane.jpg"
    }
  ]
}
```

**Tips:**

- Include real names and roles
- Keep quotes under 30 words
- Use avatars when available

---

## FAQ

Address common questions and objections.

```json
{
  "type": "faq",
  "title": "Frequently asked questions",
  "items": [
    {
      "q": "Is there a free trial?",
      "a": "Yes, our Free plan is free forever."
    },
    {
      "q": "Can I cancel anytime?",
      "a": "Yes, no long-term contracts."
    }
  ]
}
```

**Tips:**

- Address pricing objections
- Include technical questions
- Keep answers concise

---

## CTA

Final call to action.

```json
{
  "type": "cta",
  "headline": "Ready to get started?",
  "subheadline": "Join thousands of happy users",
  "emailCapture": {
    "enabled": true,
    "provider": "resend",
    "placeholder": "Enter your email",
    "buttonText": "Join Waitlist"
  }
}
```

**Or with button instead of email:**

```json
{
  "type": "cta",
  "headline": "Start your free trial",
  "cta": { "label": "Get Started", "href": "/signup" }
}
```

**Tips:**

- Create urgency in headline
- Email capture for waitlists
- Direct CTA for live products
