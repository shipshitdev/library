# Board - GitHub Projects v2 Front Door

One entry point for everything board: configure the canonical shape, reconcile
board items against repo reality, plan the next sprint, and triage the human
review lane. Same pattern as `/cleanup` — one command, explicit modes, dry-run
first.

## Usage

```bash
/board                  # show the current board shape (status)
/board init             # create the canonical board (Backlog · In Progress · Human Review · Done · Deferred + P0–P3)
/board audit            # check an existing board against the canonical shape
/board normalize        # fix a drifted board to match the canonical shape
/board copy <src>       # clone a board's configuration to another project
/board sync             # diff board items against repo reality — report only
/board sync --apply     # sync, then fix Status/Priority drift with per-category confirmation
/board schedule [days]  # sprint focus: milestones due within the horizon (default 7d) + their open issues
/board review           # triage the Human Review lane — what's waiting on the human gate
```

## Workflow

Two engines behind one door. Shape modes (`init` / `audit` / `normalize` /
`copy`) go to the `gh-project-board` skill. Truth modes (`sync` / `schedule` /
`review`) go to the `gh-board-sync` skill. The canonical shape is the Ship
Shit Dev board-as-truth model: a `Status` field of Backlog · In Progress ·
Human Review · Done · Deferred, plus a `Priority` field of P0–P3.

1. **Parse the mode** from the argument (`status` default / `init` / `audit` /
   `normalize` / `copy` / `sync` / `schedule` / `review`). Unknown argument →
   print Usage, don't guess.
2. **Detect the target project** (current repo's linked Project v2, or an
   explicit project number/URL argument). If none can be resolved, ask.
3. **Route the mode:**
   - **status / init / audit / normalize / copy →** `gh-project-board`.
     `status`/`audit` are read-only; the rest mutate behind the skill's
     confirmation gate.
   - **sync →** `gh-board-sync`, full eight-check reconciliation. Report-only
     unless `--apply`, and even then only after per-category confirmation.
   - **schedule [days] →** `gh-board-sync` with `--horizon <days>` (default 7),
     reporting only the sprint-readiness check: milestones due within the
     horizon, overdue flags, and each milestone's open issues as the sprint
     focus list. When the coming sprint needs milestones created or re-dated,
     hand off to `roadmap-to-milestones`.
   - **review →** `gh-board-sync`, reporting only the Human Review lane:
     every item in the lane, starved PRs first (approved with green checks, or
     already merged). Read-only — the human gate is the human's to clear.

`/board sync` checks, in severity order: merged-but-not-Done, Done-but-not-merged
(false green), stale In Progress, Human Review starvation, untracked work,
epic/parent drift, sprint readiness, and Priority hygiene. It ends with a
verdict: is the board trustworthy right now.

## Gates

- `status`, `audit`, `sync` (without `--apply`), `schedule`, and `review` are
  read-only — they never change a board.
- `init`, `normalize`, and `copy` mutate Projects v2 config — honor the
  `gh-project-board` skill's confirmation gate before applying changes.
- `sync --apply` sets item `Status`/`Priority` values only, one confirmation
  per check category — it never closes issues, merges PRs, or touches
  milestones.
- `schedule` never creates or edits milestones — that is
  `roadmap-to-milestones`' job, behind its own confirmation.
- Never delete existing board fields or columns without explicit confirmation.
