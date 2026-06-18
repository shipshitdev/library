---
name: de-slop
description: Removes AI-generated artifacts and code sloppiness from a codebase — console statements, `any` types, unused imports, commented-out code, debug statements, and redundant comments. Use when asked to clean up AI-generated code, remove slop, fix code quality issues, or tidy up a codebase after AI-assisted development.
disable-model-invocation: true
metadata:
  version: "1.0.0"
  tags: "code-quality, cleanup, ai-artifacts, maintenance"
---

# De-Slop

Remove AI-generated artifacts and code sloppiness while maintaining project structure.

## What Gets Cleaned

1. **Console statements** — Replace with logger service
2. **`any` types** — Replace with proper types/interfaces
3. **Unused imports** — Remove completely
4. **Commented-out code** — Remove dead code blocks
5. **Temporary/debug code** — Remove TODO/FIXME debug statements
6. **Obvious AI comments** — Remove redundant comments
7. **Unused variables** — Remove if truly unused

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

## Safety Rules

- Never delete critical files (README, configs, entry points)
- Respect logger service patterns
- Be careful with side-effect imports (CSS, polyfills)
- Keep comments that explain "why", remove comments that restate "what"
