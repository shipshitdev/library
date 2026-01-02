---
name: landing-page-vercel
description: Scaffold a static landing page (HTML, CSS, JS, data.json) and a Vercel config for review. Use when creating a simple micro-app landing page with hardcoded content and no backend.
---
# Landing Page (Vercel)

Use this skill to generate a static landing page bundle that is easy to deploy on Vercel.

## Deliverables

```
index.html
styles.css
script.js
data.json
vercel.json
```

## Workflow

1) Confirm the product name, value prop, CTA, and 3-5 key features.
2) Generate the static bundle with `scripts/scaffold.py` or write files manually.
3) Keep content in `data.json` and wire `script.js` to render it.
4) Ensure the page is responsive and readable on mobile.

## Script

```
python3 scripts/scaffold.py --out .
```

## Notes

- Keep it static: no backend, no frameworks.
- Use clean, semantic HTML and minimal JS.
- Keep CSS self-contained; avoid external dependencies unless requested.