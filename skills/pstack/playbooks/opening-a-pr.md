### Opening a PR

Invoked at the end of every other playbook.

**Worktree.** Prefer a git worktree off trunk. Multiple writers on the
same branch each get their own worktree. Dirty branch with unrelated
work: patch out, fresh worktree, apply. Use the `worktree` skill to
create one.

**Commits.** Commit liberally. Rebase into small, ordered commits before
opening PRs. Each commit is landable and tells the story.

**Cleanup.** Apply `references/prose-slop.md` from the selected `deslop` skill directory to titles,
descriptions, and commit bodies. Name `deslop` for a code strip and
`no-comments` before review. Write PR title, description, and commit
body with `technical-writing`. Apply every technical-writing layer
except Diátaxis.

**Titles.** Conventional Commits: `type(scope): subject`. Types: `feat`,
`fix`, `docs`, `refactor`, `test`, `chore`, `perf`. Short imperative
subject. No trailing period.

**Descriptions.** These sections in order. Drop a section when empty.

- `## Why`. Intent and why this approach fits.
- `## Scope`. Facts from the diff. Real symbols and paths.
- `## Tradeoffs`. Real choices only.
- `## Blast Radius`. Who and what the change touches.
- `## Verification`. How you ran each check and its outcome.

Prefer five narrow PRs to one large PR. Stack follow-ups with `gh`.
Branch from trunk only for independent work.

Open every PR ready. Name `finishing-a-development-branch` when the
human needs merge / PR / keep / discard options. Opening a PR does not
start a babysit. Post the URL and keep building.

A subagent that opens a PR runs `interrogate`, applies the prose
catalog, and names `no-comments`. It returns the URL and does not
babysit.
