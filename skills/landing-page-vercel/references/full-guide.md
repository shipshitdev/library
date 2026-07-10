# Landing Page (Vercel) — Full Guide

Full templates, config dumps, and integration snippets for the landing-page-vercel skill. See `SKILL.md` for the Contract, workflow phases, and quality checklists.

## PRD Brief Intake Template

```
I'll help you create a landing page. Based on your description:

**Product:** [Name]
**Tagline:** [One-line value proposition]

**Hero Section:**
- Headline: [Main headline]
- Subheadline: [Supporting text]
- CTA: [Button text]

**Features:** (3-5)
1. [Feature 1]: [Description]
2. [Feature 2]: [Description]
3. [Feature 3]: [Description]

**CTA Type:** [Waitlist / Sign Up / Demo Request / Contact]

**Social Proof:** [Testimonials / Logos / Stats / None]

Is this correct? Any adjustments?
```

## Generated Structure

```
my-landing-page/
├── index.html           # Main landing page
├── styles.css           # All styles (no framework)
├── script.js            # Form handling + interactions
├── data.json            # Content data (easy to edit)
├── vercel.json          # Vercel configuration
├── assets/
│   ├── favicon.ico
│   └── og-image.png     # Social sharing image
└── README.md            # Deployment instructions
```

## Form Handling (JavaScript)

```javascript
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('signup-form');
  const button = form.querySelector('button[type="submit"]');
  const messageEl = document.getElementById('form-message');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const originalText = button.textContent;

    try {
      button.textContent = 'Submitting...';
      button.disabled = true;

      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      });

      if (response.ok) {
        // Hide form and show success message
        form.style.display = 'none';
        messageEl.textContent = 'Thanks! We will be in touch.';
        messageEl.classList.add('success');
      } else {
        throw new Error('Form submission failed');
      }
    } catch (error) {
      button.textContent = originalText;
      button.disabled = false;
      messageEl.textContent = 'Something went wrong. Please try again.';
      messageEl.classList.add('error');
    }
  });
});
```

## Data Structure (data.json)

```json
{
  "name": "ProductName",
  "tagline": "Your compelling value proposition",
  "hero": {
    "headline": "Build something amazing",
    "subheadline": "The easiest way to create, launch, and grow your product.",
    "cta": "Join the Waitlist"
  },
  "features": [
    {
      "icon": "zap",
      "title": "Lightning Fast",
      "description": "Built for speed from the ground up."
    },
    {
      "icon": "shield",
      "title": "Secure by Default",
      "description": "Enterprise-grade security included."
    },
    {
      "icon": "sparkles",
      "title": "AI-Powered",
      "description": "Smart features that learn from you."
    }
  ],
  "faq": [
    {
      "question": "When will you launch?",
      "answer": "We're aiming for Q1 2026. Join the waitlist to be first to know."
    }
  ]
}
```

## Form Integration Guide

### Option 1: Formspree (Recommended)

1. Go to [formspree.io](https://formspree.io)
2. Create a free account
3. Create a new form
4. Copy your form ID
5. Replace `YOUR_FORM_ID` in the HTML

### Option 2: Custom Endpoint

```javascript
// In script.js, update the form action
const API_URL = 'https://your-api.com/api/waitlist';

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = form.querySelector('input[name="email"]').value;

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email })
  });
  // Handle response...
});
```

## Analytics Setup

### Plausible (Privacy-friendly)

```html
<!-- Add to head section -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

### Fathom

```html
<!-- Add to head section -->
<script src="https://cdn.usefathom.com/script.js" data-site="YOUR_SITE_ID" defer></script>
```

## Deployment

### Vercel (One-click)

```bash
cd my-landing-page
bunx vercel          # Deploy (no global install needed)
bunx vercel --prod   # Production deploy
```

### Vercel Configuration (vercel.json)

```json
{
  "version": 2,
  "builds": [
    { "src": "*.html", "use": "@vercel/static" },
    { "src": "*.css", "use": "@vercel/static" },
    { "src": "*.js", "use": "@vercel/static" },
    { "src": "assets/**", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/index.html" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" }
      ]
    }
  ]
}
```

## CSS Variables

```css
:root {
  --color-primary: #3b82f6;
  --color-primary-dark: #2563eb;
  --color-bg: #0f172a;
  --color-bg-secondary: #1e293b;
  --color-text: #f8fafc;
  --color-text-muted: #94a3b8;
  --font-sans: system-ui, -apple-system, sans-serif;
  --max-width: 1200px;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 2rem;
  --spacing-xl: 4rem;
}
```
