# Review - One Front Door for Every Code Review

Review whatever you point it at — your working changes, a single PR, every open
PR, the last N commits, or a time window — through the same review engine. One
command instead of remembering which review skill fits which scope.

## Usage

```bash
/review                  # review uncommitted + current-branch changes vs trunk (default, quick)
/review <PR#>            # review one open PR by number
/review pr <PR#>         # explicit single-PR form
/review prs              # review every open PR — one summary table, per-PR verdict
/review commits <N>      # review the last N commits (HEAD~N..HEAD)
/review <duration>       # review commits in a time window: 24h, 7d, 2w
/review --deep [target]  # full multi-dimension review (structural + security + devex) on any target
```

`--deep` combines with any target, e.g. `/review --deep 142`, `/review --deep commits 5`.

## Depth

- **Default (quick):** the `code-review` skill — correctness + security gate.
  Fast, high-conviction, the right call for most reviews.
- **`--deep`:** the `full-code-review` skill — three parallel lenses
  (structural, security, devex/flags), adversarial verification, Opus synthesis.
  Use for high-risk changes or production-readiness passes.

## Workflow

Use the `review-dispatch` skill. It resolves the target, gathers the diff(s)
with read-only `git`/`gh`, routes to the chosen depth, and renders the verdict.

1. **Parse the argument** into a target mode (none / PR# / `pr <n>` / `prs` /
   `commits <n>` / duration) and a depth flag (`--deep` present or not).
2. **Resolve the target to diffs** — branch vs trunk, `gh pr diff`, a commit
   range, or a `git log --since` window.
3. **Route by depth** — apply `code-review` (quick) or `full-code-review`
   (deep) to each resolved diff.
4. **Render** — a single verdict for one target, or a summary table (one verdict
   line per PR) for `prs`, with a `/review <PR#>` drill-down hint.

## Gates

- Read-only. This command reports; it never edits files, pushes, or merges.
- `prs` defaults to quick depth — `--deep prs` fans out a full orchestrated
  review per PR and is token-heavy; the dispatcher warns before running it on
  more than a few PRs.

## Related

- `/merge review` runs the same per-PR review sweep before landing PRs into the
  trunk — `/review prs` is the standalone, report-only version.
