# PR - Pull Request Lifecycle

One entry point for the pull-request lifecycle: open or update a PR, review it,
digest its comments, tidy it for reviewers, apply review fixes, repair failing
CI, or post inline suggestions. A thin dispatcher over the PR skills — it routes
to the right one based on the subcommand.

## Usage

```bash
/pr                 # create or update the PR for the current branch (default)
/pr review          # full multi-dimension review of the PR/branch
/pr comments        # read-only digest of the PR's review feedback
/pr tidy            # rewrite the PR description to be easy to review
/pr address         # apply review-comment fixes + draft replies
/pr fix-ci          # diagnose and fix failing CI checks on the PR
/pr suggest         # post inline suggested changes on the PR
```

`/pr comments` accepts the same arguments as the `pr-comments` skill, e.g.
`/pr comments <number>`, `/pr comments unresolved`, `/pr comments from <reviewer>`.

## Workflow

Route by subcommand:

1. **`/pr` (default)** — use the `gh-pr-publish` skill to create or update the PR
   from local changes: branch hygiene, a durable title/body, validation notes, and
   safe push/PR gates.
2. **`/pr review`** — use the `full-code-review` skill (structural + security +
   devex dimensions, adversarially verified) against the PR diff. For a fast
   correctness-only pass, use `code-review` instead.
3. **`/pr comments`** — use the `pr-comments` skill to fetch and prioritize review
   feedback as a read-only action list. To then act on it, hand off to
   `gh-address-comments`.
4. **`/pr tidy`** — use the `gh-pr-publish` skill's reviewability pass to rewrite an
   existing PR's description for reviewers (TL;DR, generated-vs-core separation,
   risk callouts, migration/rollout order). It rewrites the description only — it
   does not reorder commits or force-push.
5. **`/pr address`** — use the `gh-address-comments` skill to fetch review threads,
   map them to code, propose fixes, and draft replies for approval.
6. **`/pr fix-ci`** — use the `gh-fix-ci` skill to diagnose failing GitHub Actions
   checks on the PR and apply targeted fixes (optionally looping until green).
7. **`/pr suggest`** — use the `gh-review-suggestions` skill to post precise inline
   suggested changes as GitHub suggestion blocks on the PR.

## Gates

- Honor every `gh-pr-publish` push/PR gate: confirm before staging broad files,
  committing, pushing, or marking a draft ready.
- `/pr review` and `/pr comments` are read-only — they never edit code or post
  changes.
- `/pr tidy` edits the PR description text only; it never rewrites git history.
- `/pr address`, `/pr fix-ci`, and `/pr suggest` mutate (code fixes or posted
  comments) — honor each skill's own confirmation gate before applying or posting.
