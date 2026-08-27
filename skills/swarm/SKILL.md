---
name: swarm
description: Fan out N parallel workers, drain them, and return one report. Use for swarm this, or parallel coverage, races, gauntlets, and exploration partitions.
disable-model-invocation: true
license: MIT
metadata:
  version: "1.0.0"
  tags: "fan-out, coverage, race, report"
  author: Ship Shit Dev
  source: https://github.com/cursor/plugins/blob/main/pstack/skills/swarm/SKILL.md
  upstream_repo: cursor/plugins
  upstream_ref: main
  upstream_commit: bdf7aa355337
  last_synced: "2026-08-26"
  license: MIT
when_to_use: "swarm this, parallel coverage, race N workers, gauntlet"
---

# Swarm

Fan out N parallel workers. They may cover separate slices, race the
same brief, or mix both. The parent waits, aggregates, and returns one
report.

Companion to `arena`, which picks a base and grafts. Companion to
`multi-agent-patterns`, which designs architectures. This skill runs
one operational fan-out.

## Contract

Inputs:

- A done predicate and the report the swarm must return
- Shape: partition, race, or mix
- Optional N

Outputs:

- One consolidated report with a result table, issue one-liners, and
  gaps or dropouts

Creates/Modifies:

- Per-worker output under worktrees or
  `.tmp/swarm-<slug>/worker-<n>/` when workers write

External Side Effects:

- None beyond what each worker's brief authorizes

Confirmation Required:

- None for the swarm itself

Delegates To:

- `worktree` when workers need isolated checkouts

## Phases

Open a todo list: Frame, Fan out, Aggregate, Report.

### A. Frame

State the done predicate. Choose the shape. For a race, declare
`first pass`, `rank all`, or `best-of` before spawning. Set N. Default
workers to the fast cheap tier. For a model-family race, name each
arm's capability tier up front.

### B. Fan out

Spawn all N workers in one message. Every brief stands alone: goal,
scope, slice or race arm, how to verify, what to report. Reports use
`PASS`, `ISSUES`, or `BLOCKED` with evidence.

### C. Aggregate

Read the terminal results. For coverage, every required slice needs a
result. For a race, apply the selection rule declared up front. Do not
paste raw worker dumps.

### D. Report

Return one in-chat report: table, issue one-liners, gaps or dropouts,
and the race rule when used.
