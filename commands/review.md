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
/review --structural [target]  # structural/maintainability lens only (the thermo-nuclear pass)
```

`--deep` and `--structural` combine with any target, e.g. `/review --deep 142`,
`/review --structural commits 5`. They are mutually exclusive; `--deep` wins if both are given.

## Depth

- **Default (quick):** the `code-review` skill — correctness + security gate.
  Fast, high-conviction, the right call for most reviews.
- **`--deep`:** the `full-code-review` skill — three parallel lenses
  (structural, security, devex/flags), adversarial verification, Opus synthesis.
  Use for high-risk changes or production-readiness passes.
- **`--structural`:** the `structural-review` skill alone — the
  structural/maintainability "thermo-nuclear" lens (file size, abstraction,
  layering, design purity, directness-vs-magic), without the security/devex fan-out.

## Workflow

Use the `review-dispatch` skill. It resolves the target, gathers the diff(s)
with read-only `git`/`gh`, routes to the chosen depth, and renders the verdict.

1. **Parse the argument** into a target mode (none / PR# / `pr <n>` / `prs` /
   `commits <n>` / duration) and a depth flag (`--deep`, `--structural`, or
   default quick).
2. **Detect the trunk** — resolve the default branch and verify it exists before
   diffing; stop and ask for a base if it can't be resolved.
3. **Resolve the target to diffs** — branch vs trunk, `gh pr diff`, a commit
   range, or a `git log --since` window.
4. **Route by depth** — apply `code-review` (quick), `full-code-review` (deep),
   or `structural-review` (structural) to each resolved diff.
5. **Render** — a single verdict for one target, or a summary table (one verdict
   line per PR) for `prs`, with a `/review <PR#>` drill-down hint.

## Gates

- Read-only. This command reports; it never edits files, pushes, or merges.
- `prs` defaults to quick depth — `--deep prs` fans out a full orchestrated
  review per PR and is token-heavy; the dispatcher warns before running it on
  more than a few PRs.

## Related

- `/merge review` runs the same per-PR review sweep before landing PRs into the
  trunk — `/review prs` is the standalone, report-only version.
