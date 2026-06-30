---
name: design-consistency-auditor
description: Audits and maintains design system consistency across frontend applications — color palettes, UI/UX patterns, component styling, and accessibility. Triggers when asked to audit design consistency, review component styling, check color palette usage, validate accessibility compliance, or identify design debt.
metadata:
  version: "1.0.0"
  tags: "design, ux, ui, consistency, audit, tailwind, accessibility"
---

# Design Consistency Auditor

Before auditing, discover the project's frontend structure from documentation.

Ensures:

- Color palettes are used consistently
- UI/UX patterns follow best practices
- Components maintain visual harmony
- Accessibility standards are met
- Design system is properly applied
- No design debt accumulates

## When to Use

- Auditing design consistency across apps
- Reviewing color palette usage
- Checking UI/UX patterns
- Validating component styling
- Ensuring accessibility compliance
- Identifying design inconsistencies
- Reviewing new features for design standards

## Quick Reference

### Color Rules

**DO:** Use semantic tokens (`bg-primary`, `text-base-content`, `bg-base-100`)
**DON'T:** Hardcode hex colors (`#000000`) or arbitrary values (`bg-[#123456]`)

### Component Patterns

Discover the project's component class conventions from its design system or existing codebase. Common patterns to look for:

- Cards: project-specific card class or component (e.g. `card`, `.card`, design-system Card component)
- App shells / layouts: project-specific shell wrapper class
- Modals / dialogs: project dialog component pattern
- Inputs: project form input class or component
- Buttons: project button variants (primary, secondary, ghost)

Identify the actual class names from the codebase before auditing — do not assume a specific naming convention.

### Spacing

**DO:** Use Tailwind scale (`p-4`, `m-6`, `gap-4`)
**DON'T:** Use arbitrary values (`p-[17px]`)

### Accessibility

- Semantic HTML (`<button>`, `<nav>`, `<main>`)
- ARIA labels on interactive elements
- 4.5:1 contrast for text, 3:1 for UI
- Focus states: `focus:outline-none focus:ring-2 focus:ring-primary`

### Responsive

- Mobile-first with `sm:`, `md:`, `lg:`, `xl:` modifiers
- Responsive typography: `text-3xl sm:text-4xl`

## Audit Phases

1. **Color Palette** - Scan for hardcoded colors, verify theme tokens
2. **Component Patterns** - Check cards, buttons, forms use theme classes
3. **Spacing & Layout** - Verify consistent spacing scale
4. **Typography** - Check heading hierarchy and text styles
5. **Accessibility** - Run automated checks, keyboard testing

## AI Slop Prevention

Audit for generic "AI-generated" aesthetics:

- Generic fonts (Inter, Roboto everywhere)
- Purple gradients on white
- Predictable layouts without character
- Safe, boring color choices

Push for distinctive, branded designs with personality.

---

**For detailed checklists, examples, reporting templates, and audit commands, see:** `references/full-guide.md`
