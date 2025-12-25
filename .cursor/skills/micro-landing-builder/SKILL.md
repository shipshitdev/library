---
name: micro-landing-builder
description: Scaffold a config-driven NextJS landing page that uses a shared UI components package. Use this skill when creating startup landing pages with email capture, analytics, and modern design. Each landing is a standalone NextJS app driven by an app.json config file.
---

# Micro Landing Builder

Create config-driven NextJS landing pages for startups.

## Concept

Each landing page is a standalone NextJS app where:
- Content is defined in `app.json` config file
- UI comes from `@agenticindiedev/ui`
- Deploy independently to any domain via Vercel

## Prerequisites

You need a published landing UI components package. The skill expects:
- Package name (default: `@agenticindiedev/ui`)
- Components: Hero, Features, Pricing, FAQ, CTA, Testimonials, Stats, EmailCapture, Header, Footer

## Usage

```bash
# Show help
python3 ~/.cursor/skills/micro-landing-builder/scripts/scaffold.py --help

# Create a new landing
python3 ~/.cursor/skills/micro-landing-builder/scripts/scaffold.py \
  --slug mystartup \
  --name "My Startup" \
  --domain "mystartup.com" \
  --concept "AI-powered analytics"

# With custom UI package
python3 ~/.cursor/skills/micro-landing-builder/scripts/scaffold.py \
  --slug mystartup \
  --name "My Startup" \
  --ui-package "@myorg/landing-kit"

# Allow outside current directory
python3 ~/.cursor/skills/micro-landing-builder/scripts/scaffold.py \
  --root ~/www/landings \
  --slug mystartup \
  --allow-outside
```

## Generated Structure

```
mystartup/
├── app.json              # All content/config here
├── package.json          # Depends on UI package
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── vercel.json           # Vercel deployment config
├── public/
│   └── (images go here)
└── app/
    ├── layout.tsx
    ├── page.tsx          # Renders sections from app.json
    └── globals.css
```

## app.json Config

The landing is entirely driven by `app.json`. See `references/config-schema.md` for full schema.

```json
{
  "name": "My Startup",
  "slug": "mystartup",
  "domain": "mystartup.com",
  "meta": {
    "title": "My Startup - Tagline",
    "description": "SEO description"
  },
  "theme": {
    "primary": "#6366f1",
    "accent": "#f59e0b"
  },
  "analytics": {
    "plausible": "mystartup.com"
  },
  "sections": [
    { "type": "hero", "headline": "...", "subheadline": "..." },
    { "type": "features", "items": [...] },
    { "type": "pricing", "plans": [...] },
    { "type": "faq", "items": [...] },
    { "type": "cta", "emailCapture": { "enabled": true } }
  ]
}
```

## Section Types

- `hero` - Main hero with headline, CTA buttons
- `stats` - Key metrics/numbers
- `features` - Feature grid with icons
- `pricing` - Pricing plans
- `testimonials` - Customer quotes
- `faq` - Accordion FAQ
- `cta` - Call to action with email capture

## Deployment

```bash
cd mystartup
vercel
```

## Workflow

1. Run scaffold to create landing structure
2. Edit `app.json` with your content
3. Add images to `public/`
4. Deploy with `vercel`

## Customization

To add custom sections or override components:
1. Add component to `app/components/`
2. Import in `app/page.tsx`
3. Add to section renderer

## References

- `references/config-schema.md` - Full JSON schema
- `references/sections-reference.md` - Section types and props
