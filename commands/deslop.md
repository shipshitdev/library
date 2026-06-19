# Deslop - Remove AI Slop From Code

Strip AI-generated artifacts and code sloppiness while keeping the project
buildable: console statements, `any` types, unused imports, dead/commented-out
code, redundant comments, unnecessary defensive checks, and over-nesting.

## Usage

```bash
/deslop              # clean the current package/project directory
/deslop --changed    # clean only the lines this branch introduced (diff-only)
/deslop all          # sweep every package in a monorepo
/deslop dry-run      # preview the cleanup, change nothing
```

## Workflow

Use the `de-slop` skill.

1. Detect project structure (monorepo vs single package); in `--changed` mode,
   compute the branch diff (`git diff <merge-base>...HEAD`) and limit edits to those
   files/hunks.
2. Identify artifacts: console statements, `any`, unused imports/vars, commented-out
   code, debug code, redundant comments, defensive try-catch on trusted paths,
   over-nesting.
3. Apply cleanup, replacing console with the project logger and `any` with real
   types; collapse deep nesting into early returns matching the file's style.
4. Verify: `bun run type-check || bunx tsc --noEmit`, then `bun run test`.

## Gates

- Never delete critical files (README, configs, entry points) or strip
  side-effect imports (CSS, polyfills).
- Keep comments that explain "why"; remove only those that restate "what".
- In `--changed` mode, do not touch pre-existing slop elsewhere — keep the cleanup
  scoped and reviewable.
- This skill edits and removes code. For a read-only structural review that only
  flags issues, use `structural-review` / `/review` instead.
