---
name: de-slop
description: Removes AI-generated artifacts and code sloppiness from a codebase — console statements, `any` types, unused imports, commented-out code, debug statements, redundant comments, unnecessary defensive try-catch on trusted paths, and over-nesting that should use early returns. Can scope to only the lines introduced on the current branch (diff-only) or sweep the whole tree. Use when asked to clean up AI-generated code, remove slop, fix code quality issues, or tidy up a codebase after AI-assisted development.
disable-model-invocation: true
metadata:
  version: "1.0.0"
  tags: "code-quality, cleanup, ai-artifacts, maintenance"
---

# De-Slop

## What Gets Cleaned

1. **Console statements** — Replace with logger service
2. **`any` types** — Replace with proper types/interfaces
3. **Unused imports** — Remove completely
4. **Commented-out code** — Remove dead code blocks
5. **Temporary/debug code** — Remove TODO/FIXME debug statements
6. **Obvious AI comments** — Remove redundant comments
7. **Unused variables** — Remove if truly unused
8. **Unnecessary defensive checks** — Remove try-catch and null guards on trusted
   internal paths that cannot actually fail; keep guards on real external boundaries
9. **Over-nesting** — Collapse deep `if`/`else` pyramids into early returns, matching
   the surrounding file's existing style

## Workflow

### Step 1: Detect Project Structure

Determine if monorepo or single project:

```bash
ls packages/ 2>/dev/null || ls pnpm-workspace.yaml 2>/dev/null || true
```

If monorepo: process each package separately.

### Step 2: Identify Artifacts

Search for each artifact type across the codebase.

### Step 3: Execute Cleanup (Per Package)

For each package/project:

1. Console statements — Replace with logger
2. `any` types — Create interfaces, replace types
3. Unused imports — Remove
4. Commented code — Remove blocks
5. Debug code — Remove temporary code
6. Obvious comments — Remove redundant comments
7. Unused variables — Remove

### Step 4: Verify

```bash
bun run type-check || tsc --noEmit
bun run test
```

### Step 5: Document

Log cleanup in today's session file (`.agents/sessions/YYYY-MM-DD.md`) with packages cleaned and artifact counts.

## Scope

- Default: clean the current package/project directory
- To clean across an entire monorepo, explicitly ask for all packages
- To preview without making changes, ask for a dry run first

### Diff-only mode (`--changed`)

To clean only what the current branch introduced — the safest scope for a PR, and
the right default when tidying after AI-assisted work on a branch — restrict edits
to the changed lines rather than the whole tree:

```bash
BASE="$(git merge-base HEAD origin/HEAD 2>/dev/null || git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)"
git diff --name-only "$BASE"..HEAD           # files this branch touched
git diff "$BASE"..HEAD                         # the exact introduced lines
```

Only de-slop the files (and ideally the hunks) that appear in that diff. Do not
touch pre-existing slop elsewhere in the tree in this mode — that keeps the cleanup
reviewable and scoped to your own change. Fall back to whole-tree cleanup only when
explicitly asked.

## Modes

- **default** — clean the current package/project directory and apply the fixes
- **`--changed`** — clean only the files/hunks this branch introduced (the diff-only
  mode above); the safest scope for a PR
- **`all`** — sweep every package in a monorepo, processing each separately
- **`dry-run`** — run detection only: report every artifact that would be cleaned,
  grouped by type with counts, and make no edits. Combine with any scope, e.g.
  dry-run over `--changed`.

## Safety Rules

- Never delete critical files (README, configs, entry points)
- Respect logger service patterns
- Be careful with side-effect imports (CSS, polyfills)
- Keep comments that explain "why", remove comments that restate "what"
