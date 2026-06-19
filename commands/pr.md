# PR - Create, Update, and Publish a Pull Request

Open or update a pull request with a clean title, a durable body, branch hygiene,
and safe push/PR gates — instead of hand-assembling `gh pr create` each time.

## Usage

```bash
/pr                  # publish the current branch as a PR (or update its existing one) — default
/pr draft            # open as a draft PR
/pr update           # refresh the title/body of the existing PR for this branch
/pr <base>           # target an explicit base branch instead of the auto-detected trunk
```

## Workflow

Use the `gh-pr-publish` skill.

1. Detect the current branch, the target base (auto-detected trunk unless given),
   and whether a PR already exists for the branch.
2. Ensure branch hygiene — never publish directly from the trunk; create or
   confirm a feature branch first.
3. Draft a clear title and a durable body (what changed, why, validation notes);
   follow the repo's PR template if present.
4. **Preview the title, body, base, and push plan, then confirm** before pushing
   and creating/updating the PR.

## Gates

- **Confirm before pushing and before creating/updating the PR** — both are
  outward-facing.
- Never force-push, and never push to `main`/`master`.
- If a PR already exists for the branch, update it — do not open a duplicate.

## Related

- `/pr` opens the PR; `/fix-ci` greens its checks, `/address` resolves its
  comments, `/merge` lands it into the trunk.
