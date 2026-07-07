---
name: deslop-ui
description: Audit and fix AI-generated UI slop in existing frontend projects. Use when asked to deslop, polish, audit, redesign, improve taste, enforce a design system, remove visual debt, or make UI feel professional without changing product scope.
disable-model-invocation: true
argument-hint: "[target | --audit-only]"
metadata:
  version: "1.0.0"
  tags: "ui, design, frontend, cleanup, ai-artifacts, product-polish"
  short-description: "Audit then fix UI slop"
---

# Deslop UI

## Goal

Make an existing UI conform to its project design system first, then improve
taste. Preserve product intent, navigation, and information architecture unless
the user explicitly asks for a redesign.

Do not turn this skill into a giant checklist. Derive the actual rules from the
target codebase, design docs, shared components, and screenshots.

## Contract

Inputs:

- A target frontend project, route, screen, component, screenshot, or diff.
- Optional `--audit-only` mode to report findings without edits.

Outputs:

- Findings first, then applied changes, verification evidence, and remaining
  recommendations.

Creates/Modifies:

- Edits frontend source files unless running in `--audit-only`.

External Side Effects:

- None beyond local file edits and local verification.

Confirmation Required:

- Confirm before changing product scope, navigation, information architecture,
  adding dependencies, or running heavy local checks.

## Workflow

### 1. Discover The Local System

Before judging taste, inspect the local source of truth:

- Design docs, tokens, theme files, CSS variables, Tailwind config, or equivalent.
- Shared UI primitives such as cards, buttons, inputs, dialogs, tables, tabs,
  nav, badges, tooltips, menus, and loading states.
- Three nearby good examples in the same app or package.
- The target screen/component code and rendered output when available.

Create a short working inventory:

- Approved tokens and spacing/radius/shadow patterns.
- Shared primitives and their variants.
- Local examples that already look production-ready.
- Target files and routes affected.

### 2. Audit For Drift

Treat slop as drift away from the local system, not as a universal list of bad
classes. Identify the highest-signal issues in these four buckets:

- **System drift**: one-off colors, shadows, borders, spacing, typography, or
  effects where the design system already has a pattern.
- **Component drift**: raw or duplicated local UI where a shared primitive or
  named variant should carry the contract.
- **Semantic drift**: interactions that look real but are broken, inaccessible,
  or semantically wrong.
- **Taste drift**: weak hierarchy, visual noise, generic AI copy, cramped layout,
  or decorative treatment that makes the surface feel generated.

Use targeted searches when they help, but do not rely on regexes as the design
authority. Examples worth searching for include arbitrary Tailwind values,
`href="#"`, raw interactive primitives, repeated class clusters, and local
component copies.

For each finding, record the file/component, the observed drift, the local pattern
it should follow, and whether it is fixed or deferred.

### 3. Fix In Priority Order

Fix objective design-system drift before subjective taste. Prefer:

1. Existing shared primitives and variants.
2. Existing semantic tokens and documented recipes.
3. Small local consolidation when repeated code has no shared home.
4. New tokens or variants only when the same missing concept appears repeatedly.

Keep changes scoped to the audited surface. Remove decorative complexity instead
of masking weak structure with glow, blur, gradients, animation, or nested cards.
When a proposed fix needs product judgment, defer it with a concrete note instead
of inventing intent.

### 4. Taste Pass

After system drift is fixed or explicitly deferred, make the UI calmer and easier
to scan:

- Clarify primary, secondary, and tertiary hierarchy.
- Make repeated items comparable.
- Tighten copy to concrete nouns and verbs.
- Verify responsive behavior, overflow, focus states, loading/empty/error states,
  and keyboard behavior for touched controls.

## Verification

Run the smallest checks that prove the change:

- Formatter or linter on changed files.
- Design-token or design-system checks if present.
- Targeted searches showing removed drift patterns.
- Route smoke test or screenshot/browser inspection when the app can run.

Avoid heavy local test suites unless project rules explicitly allow them.

## Output Format

Start with findings, then fixes:

1. Findings: `file:line` or component, problem, local pattern to follow.
2. Changes made: concise list of actual edits.
3. Verification: commands/checks run, plus anything skipped and why.
4. Recommendation: fix now, defer, or turn into a reusable detector/check.

## Good Taste Bar

The final UI should feel calmer, more intentional, less generated, easier to
scan, consistent with the product's own system, and production-ready without
looking over-designed.
