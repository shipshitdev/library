# Triage labels

> Seed for `docs/agents/triage-labels.md`. The roles are fixed; rename the label
> strings to match this repo if needed, then update every skill that references them.

## Status is a board field, not a label

Where an issue sits — **Backlog / In Progress / Human Review / Done / Deferred** —
is the GitHub Projects board `Status` single-select field, the sole source of truth.
These are the human-facing columns; there are no `status:*` labels. The AI loop's own
sub-phases ride as `loop:*` labels inside In Progress. The labels below ride
alongside the board.

## Label vocabulary

| Label | Role |
| ----- | ---- |
| `claim:active` | An agent currently holds the issue. Paired with a timestamped claim comment (30-min lock). |
| `loop:planning` / `loop:executing` / `loop:testing` / `loop:shipping` | AI-loop sub-phase **inside the In Progress column** (observability; mirrors ShipCode's `shipcode:pipeline:*`). |
| `priority:high` / `priority:medium` / `priority:low` | Queue ordering. High is picked first. |
| `rejection:N` | QA rejection count, bumped on each kickback from Human Review → Backlog. |
| `dispatch:claude` | **Dispatch gate → Claude lane (human opt-in).** Nothing runs autonomously until a human applies this. |
| `dispatch:codex` | **Dispatch gate → Codex/GPT lane (human opt-in).** The Codex-lane twin of `dispatch:claude`; apply at most one gate per issue. |
| `type:feature` | Applied by `feature-intake` to PRD epics and their sub-issues. |
| `wontfix` | Closed; will not be actioned. Record durable reasoning under `.out-of-scope/`. |

## The dispatch gates: `dispatch:claude` / `dispatch:codex`

A dispatch gate is what turns a written-up issue into running work, and which gate
you apply picks the engine:

- `dispatch:claude` → **Claude lane** (`anthropics/claude-code-action`).
- `dispatch:codex` → **Codex/GPT lane** (`openai/codex-action`).

Both are applied **by a human**, deliberately — never automatically by
`feature-intake` or any creation step. Apply at most one gate per issue. The flow
is identical for either gate (substitute the gate label you used):

- **Candidate query:** an agent works an issue only when it carries a gate label
  **and** sits in the board's **Backlog** column (opted in **and** in Backlog).
- **Local pull** (`/loop`, Claude only): lists `dispatch:claude` issues, intersects
  them with the board's Backlog column, sorts by priority, and claims one.
- **On claim:** the agent flips the board `Status` to **In Progress** and advances
  the `loop:*` phase labels as it works.
- **Push dispatch** (GitHub Actions): applying `dispatch:claude` fires
  `agent-dispatch.yml`; applying `dispatch:codex` fires `codex-dispatch.yml`.
- **On completion:** the agent flips the board `Status` to **Human Review**,
  auto-assigns the reviewer, and removes `claim:active`, the gate label, and the
  `loop:*` label.

This keeps the safety property: an issue sits inert in Backlog until a human opts it
into execution. On QA **rejection**, the reviewer's reject action re-arms the gate
(sets `Status` back to Backlog + re-applies the gate label) so the loop retries — the
reject is the deliberate "try again". To stop a rejected issue instead, leave the
gate off and move it to **Deferred** (or close it `wontfix`).

## AFK vs HITL (body markers, not labels)

Mark each issue body with one:

- **`AFK`** — an agent can complete it end-to-end from the written context.
- **`HITL`** — a human decision is required mid-task.

**HITL issues must never receive a dispatch gate** (`dispatch:claude` or
`dispatch:codex`). Split HITL decisions out of AFK implementation work at
task-creation time so the loop only ever picks up work it can actually finish.
