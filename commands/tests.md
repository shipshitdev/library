# Tests - Run the Right Tests and Make Red Go Green

Run the project's tests at the right scope, then on failure read the output and
traces, apply a minimal fix, and rerun until green or blocked. Defaults to
changed-only — matching "scoped tests locally, full suite in CI."

## Usage

```bash
/tests                  # changed-only: tests related to your dirty worktree (default)
/tests full             # the whole suite (what CI runs)
/tests unit | integration | e2e
/tests coverage         # full run + coverage; gate via husky-test-coverage
/tests types            # tsc --noEmit and clear the errors in a loop
/tests <path|pattern>   # focused run
/tests --since <ref>    # tests related to a commit range
/tests --no-fix         # run and report only; make no edits
```

## Workflow

Use the `test-runner` skill.

1. Detect the runner (Vitest / Jest / Bun test / Playwright) and package manager
   from `package.json` + `bun.lock`; prefer the repo's own `test*` scripts.
2. Resolve scope. For `changed`/`--since`, compute the file set with
   `git diff --name-only` and map to related tests (`vitest related`,
   `jest --findRelatedTests`); fall back to the closest safe superset and say so.
3. Run the resolved command and capture full output.
4. On failure: read the real error (Playwright traces first), reproduce in
   isolation, fix the root cause, and rerun until the scope is green or blocked.
5. Re-run any fixed test once more to catch flakiness before declaring success.

## Gates

- Never weaken, skip, or delete a test to force a pass — surface it instead.
- Scope edits to the failure; no unrelated refactors, no `--no-verify`.
- Confirm before an expensive full/e2e run when a quick check was requested, and
  before editing source beyond the file(s) under test.
- Use `bun`/`bunx`, never `npm`/`npx`. To set up a framework use
  `playwright-e2e-init` / `testing-cicd-init`; for coverage gates use
  `husky-test-coverage`.
