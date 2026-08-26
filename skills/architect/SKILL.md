---
name: architect
description: Sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for architect this, design this, or non-trivial work where jumping to code would lock in the wrong shape.
disable-model-invocation: true
license: MIT
metadata:
  version: "1.0.0"
  tags: "architecture, design, types, modules"
  author: Ship Shit Dev
  source: https://github.com/cursor/plugins/blob/main/pstack/skills/architect/SKILL.md
  upstream_repo: cursor/plugins
  upstream_ref: main
  upstream_commit: bdf7aa355337
  last_synced: "2026-08-26"
  license: MIT
when_to_use: "architect this, design this first, sketch the types, module shape before code"
---

# Architect

Design before implementing. Sketch types, function signatures, class
shapes, and module boundaries with `not implemented` bodies. Synthesize
across parallel candidates, then fill in code against the chosen sketch.

Companion to `codebase-design`, which owns deep-module vocabulary. This
skill owns the pre-implementation sketch loop.

## Contract

Inputs:

- A change that crosses a function boundary, or non-trivial work whose
  shape is still unset

Outputs:

- A synthesized design package: caller usage first, then types,
  signatures, module map, and rationale
- Implementation against that sketch, or a scrap-and-redesign

Creates/Modifies:

- Design artifacts and, after agree, production code

External Side Effects:

- None beyond local files unless a later playbook opens a PR

Confirmation Required:

- Opt-in checkpoint when the invoker asks to see the sketch first

Delegates To:

- `how` for grounding, `why` when ownership or layering is the
  constraint, `arena` for candidate sketches, `interrogate` when the
  design is contested

## Phases

Open a todo list with one entry per phase: Ground, Sketch, Agree,
Implement, Scrap.

### A. Ground

Run `how` over every system the new code touches. If the design
redefines ownership or layering, also run `why` on the existing shape.
Skip only when the work is genuinely greenfield.

### B. Sketch

Run `arena` with the design-sketch task. Each candidate produces a
package shaped per
[references/rationale-template.md](references/rationale-template.md)
using [references/runner-prompt.md](references/runner-prompt.md).

Require at least two structurally distinct candidates. Screen every
candidate against
[references/design-red-flags.md](references/design-red-flags.md).
Prefer the design that hides more complexity behind a smaller public
surface.

### C. Agree

Default: proceed to implementation. Opt in to a checkpoint when the
invoker asks to see the sketch first. Human pushback is Phase A
evidence. Re-ground and re-run Phase B.

### D. Implement

Replace `not implemented` bodies. Deviations from the sketch are
signal. Surface them. Do not bolt them on silently.

### E. Scrap

If implementation keeps producing the same shape of friction, throw the
sketch out. Re-run `how` over what was built. Redesign as if the new
constraints were day-one assumptions. Subtract before adding. Return to
Phase B.
