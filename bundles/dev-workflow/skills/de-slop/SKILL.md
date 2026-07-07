---
name: de-slop
description: >-
  Strip AI-generated slop from a codebase and product. Code slop — console
  statements, `any` types, unused imports, commented-out code, redundant comments,
  needless defensive try-catch on trusted paths, over-nesting. Product slop (with
  --product) — marketing-filler copy, generic AI phrasing, default-shadcn look,
  unstyled loading/error states, dead buttons and half-wired flows that make an app
  feel unfinished. UI-only slop delegates to deslop-ui. Can scope to the current
  branch's diff or sweep the whole tree. Use when asked to clean up AI-generated
  code, remove slop, or make an app feel finished before shipping to customers.
disable-model-invocation: true
argument-hint: "[ui | --changed | all | dry-run | --product]"
metadata:
  version: "1.2.0"
  tags: "code-quality, cleanup, ai-artifacts, product-polish, maintenance"
---

# De-Slop

AI-assisted development leaves two kinds of slop. **Code slop** compiles but reads as
machine-written — dead code, `any`, defensive noise. **Product slop** ships but feels
unfinished to a paying customer — filler copy, default styling, half-wired flows.
This skill removes both. Code slop is the default; `--product` adds the product pass.

Edits and removes code, so it runs behind a confirmation gate and prefers the branch
diff. For a read-only pass that only flags, use `structural-review` / `/review`.

## Contract

Inputs:

- A package or repo to clean; optional scope (`--changed`, `all`, `dry-run`) and
  dimension (`--product` to add the product pass, `ui` to route to `deslop-ui`).

Outputs:

- Applied edits (or, in `dry-run`, a grouped report of what would change), plus a
  short count of artifacts removed by type.

Creates/Modifies:

- Edits source files. Never deletes entry points, configs, or READMEs.

External Side Effects:

- None beyond local file edits. Runs type-check and tests to verify.

Delegates To:

- `deslop-ui` when invoked with `ui`, or when product slop is primarily
  design-system, component primitive, or UI consistency drift.
- `polish` for the final micro-detail pass after the structural slop is gone.
- `refactor-code` when a fix is a real refactor, not a mechanical strip.

## Code slop (default)

Remove, matching the surrounding file's existing style:

1. **Console statements** → the project logger.
2. **`any` types** → real types or `unknown` + a type guard.
3. **Unused imports / variables** → delete.
4. **Commented-out code** → delete (git remembers it).
5. **Debug / temporary code** → delete leftover TODO/FIXME debug lines.
6. **Redundant comments** — remove those that restate *what*; keep those that explain
   *why*.
7. **Needless defensive checks** — drop try-catch and null guards on trusted internal
   paths that cannot fail; keep guards on real external boundaries.
8. **Over-nesting** — collapse deep if/else pyramids into early returns.

## Product slop (`--product`)

The layer that decides whether an app feels finished. See
[references/product-slop.md](references/product-slop.md) for the full Incorrect →
Correct catalog; the three families:

- **Copy** — marketing filler ("Seamlessly elevate your workflow"), generic AI
  phrasing, em-dash overuse, empty-states and error messages that say nothing useful.
- **UI** — the untouched-shadcn-plus-purple-gradient look, inconsistent
  spacing/radius, loading and error states left unstyled or absent.
- **UX** — buttons wired to nothing, flows that dead-end, placeholder pages behind
  real-looking nav, forms with no validation or success feedback.

Product slop needs judgment, not just deletion — flag anything ambiguous rather than
guessing at intended copy or behavior.

## UI slop (`ui`)

When the first argument is `ui`, delegate to `deslop-ui` and pass any remaining
target or flags through unchanged. Do not run the code cleanup workflow first.

## Workflow

1. **Route UI mode** — if the first argument is `ui`, apply `deslop-ui` and stop.
2. **Detect structure** — monorepo vs single package (`ls packages/ 2>/dev/null`).
   Process each package separately.
3. **Scope** — in `--changed`, limit edits to the branch diff:

   ```bash
   BASE="$(git merge-base HEAD origin/HEAD 2>/dev/null || git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)"
   git diff --name-only "$BASE"..HEAD    # files this branch touched
   ```

   Touch only those files/hunks; do not clean pre-existing slop elsewhere in this mode.
4. **Strip code slop** by the categories above; add the product pass if `--product`.
5. **Verify** — the change must still build and pass:

   ```bash
   bun run type-check || bunx tsc --noEmit
   bun run test
   ```

6. **Document** — log packages cleaned and per-type counts in
   `.agents/sessions/YYYY-MM-DD.md`.

## Modes

- **default** — code slop, current package, edits applied.
- **`ui`** — route to `deslop-ui` for UI/design-system slop.
- **`--changed`** — only the files/hunks this branch introduced (safest for a PR).
- **`--product`** — add the product-slop pass (copy/UI/UX).
- **`all`** — sweep every package in a monorepo, each processed separately.
- **`dry-run`** — detect only; report every artifact grouped by type with counts, edit
  nothing. Combines with any scope.

## Anti-Patterns

- **Cleaning the whole tree when a branch scope was meant** — `--changed` keeps a PR
  reviewable; whole-tree edits need confirmation.
- **Deleting side-effect imports** (CSS, polyfills) or critical files (README,
  configs, entry points).
- **Removing a "why" comment** because it looks redundant — only *what*-restating
  comments go.
- **Guessing at product copy or intended behavior** — flag ambiguous product slop for
  the user instead of inventing a fix.
- **Rewriting logic under the banner of cleanup** — a behavior change is a refactor
  (`refactor-code`), not de-slop.
