---
name: deslop-ui
description: Audit and fix AI-generated UI slop in existing frontend projects. Use when asked to deslop, polish, audit, redesign, improve taste, remove visual debt, or make a UI feel professional without changing product scope.
disable-model-invocation: true
argument-hint: "[target | --audit-only]"
metadata:
  version: "1.0.0"
  tags: "ui, design, frontend, cleanup, ai-artifacts, product-polish"
  short-description: "Audit then fix UI slop"
---

# Deslop UI

## Goal

Remove AI-generated UI slop from existing interfaces while preserving product
intent, codebase patterns, and the local design system.

This skill is not for making a new visual concept from scratch. It is for taking
an existing UI and making it sharper, calmer, more coherent, and more
production-ready.

## Contract

Inputs:

- A target frontend project, route, screen, component, or screenshot. Optional
  `--audit-only` mode reports findings without edits.

Outputs:

- Findings first, then applied UI changes, verification evidence, and any
  remaining design-debt recommendation.

Creates/Modifies:

- Edits frontend source files unless running in `--audit-only`.

External Side Effects:

- None beyond local file edits and local verification.

Confirmation Required:

- Confirm before changing product scope, navigation, information architecture,
  adding dependencies, or running heavy local checks.

## Operating Rule

Audit first, then fix. Do not jump straight into edits.

For every issue, identify:

- The visual problem.
- The affected file or component.
- The likely cause.
- The design-system-compliant fix.
- The verification method.

## Inputs To Inspect

Before editing, read:

- Design system docs such as `DESIGN.md`, `design.md`, `tokens`, `theme`, or
  `tailwind.config`.
- Shared UI primitives in `packages/ui`, `components/ui`, or equivalent.
- Three nearby examples of good existing UI in the same app.
- The target screen or component code.
- Screenshots when available.

If screenshots are not available and the app can run, start the smallest local
dev server needed and inspect the target routes visually.

## Slop Detectors

Look for these patterns first.

### Token Drift

Flag:

- Hardcoded hex colors.
- Arbitrary Tailwind colors such as `bg-[#...]`.
- Repeated one-off color values.
- Unsupported semantic tokens.
- Gradients that should be brand or platform tokens.
- Local component tokens that duplicate global tokens.

Fix:

- Use existing semantic tokens.
- Add tokens only when the design system genuinely lacks a reusable concept.
- Update docs or checks if tokens are added.

### Fake Depth

Flag:

- Arbitrary shadows like `shadow-[...]`.
- Glow effects.
- Blur-heavy panels.
- Translucent white overlays such as `bg-white/[0.04]`.
- Card-on-card nesting.
- Decoration pretending to be hierarchy.

Fix:

- Use existing shadow and border primitives.
- Prefer spacing, type, contrast, and structure over glow.
- Remove purely decorative panels when content can stand on layout alone.

### Hierarchy Slop

Flag:

- Too many same-weight cards.
- Equal-grid layouts where one item is clearly primary.
- Oversized headings inside compact UI.
- Uppercase or wide tracking used as a crutch.
- Hero styling reused in dashboards or operational surfaces.
- Weak scan paths.

Fix:

- Establish primary, secondary, and tertiary hierarchy.
- Vary layout spans intentionally.
- Reduce decorative typography.
- Make repeated items dense and comparable.

### Layout Slop

Flag:

- Fragile fixed heights.
- Text that can overflow buttons or cards.
- Controls that resize on hover or loading.
- Cramped mobile layouts.
- Inconsistent section rhythm.
- UI cards inside other UI cards.

Fix:

- Use responsive constraints, aspect ratios, min/max widths, and stable control
  dimensions.
- Verify mobile and desktop.
- Keep cards for repeated items, modals, and framed tools only.

### Semantic Slop

Flag:

- Links with `href="#"`.
- Buttons used for navigation.
- Anchors styled as disabled actions.
- Clickable divs.
- Missing focus states.
- Icon-only actions without accessible names.

Fix:

- Navigation uses links with real hrefs.
- Actions use buttons.
- Preserve keyboard and screen-reader behavior.
- Keep focus states visible.

### Copy Slop

Flag:

- Generic AI marketing copy.
- Repeated adjectives.
- Visible text explaining the UI instead of supporting the workflow.
- Inflated labels.
- Vague CTAs.

Fix:

- Use concrete nouns and verbs.
- Shorten labels.
- Remove explanatory filler.
- Keep copy aligned to the user's immediate task.

## Fixing Rules

- Match the existing codebase style.
- Prefer shared UI primitives over local one-offs.
- Keep edits scoped to the audited surfaces.
- Do not redesign product scope, navigation, or information architecture unless
  explicitly requested.
- Do not introduce a new visual language.
- Do not add dependencies unless there is no local pattern that works.
- Do not hide design debt with animation, gradients, blur, or glow.
- Do not create local task markdown files.

## Verification

Run the smallest checks that prove the change:

- Formatter or linter on changed files.
- Design-token or design-system checks if present.
- Targeted grep for removed slop patterns.
- Route smoke test if the app runs.
- Screenshots or browser inspection for affected screens when available.

Avoid heavy local test suites unless project rules explicitly allow them.

## Output Format

Start with findings, then fixes.

Use this shape:

1. Findings
   - `file:line` or component.
   - Problem.
   - Fix direction.
2. Changes made
   - Concise list of actual edits.
3. Verification
   - Commands or checks run.
   - Anything not run and why.
4. Recommendation
   - Whether remaining issues should be fixed now, deferred, or turned into a
     reusable detector or check.

## Good Taste Bar

The final UI should feel:

- Calmer.
- More intentional.
- Less generated.
- Easier to scan.
- Consistent with the product's own system.
- Production-ready without looking over-designed.
