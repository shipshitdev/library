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
| `dispatch:plan` | **Planning gate → drafts a plan for human review (human opt-in).** Runs `writing-plans`, posts a `## Implementation Plan` comment, and lands the issue in Human Review. Applies **no** execution gate — a human picks the engine afterward. |
| `dispatch:claude` | **Dispatch gate → Claude lane (human opt-in).** Nothing runs autonomously until a human applies this. |
| `dispatch:codex` | **Dispatch gate → Codex/GPT lane (human opt-in).** The Codex-lane twin of `dispatch:claude`; apply at most one gate per issue. |
| `dispatch:openrouter` | **Dispatch gate → OpenRouter lane (human opt-in).** Hosts the Codex CLI pointed at OpenRouter; apply at most one gate per issue. |
| `type:feature` | Applied by `feature-intake` to PRD epics and their sub-issues. |
| `wontfix` | Closed; will not be actioned. Record durable reasoning under `.out-of-scope/`. |

## The dispatch gates: `dispatch:claude` / `dispatch:codex`

A dispatch gate is what turns a written-up issue into running work, and which gate
you apply picks the engine:

- `dispatch:claude` → **Claude lane** (`anthropics/claude-code-action`).
- `dispatch:codex` → **Codex/GPT lane** (`openai/codex-action`).
- `dispatch:openrouter` → **OpenRouter lane** (Codex CLI via OpenRouter's OpenAI-compatible API).

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

## The planning gate: `dispatch:plan`

`dispatch:plan` is a separate, **upstream** gate that drafts an implementation plan
for human review — it never executes. It exists so planning becomes a repeatable
queue step without letting an agent run an unreviewed plan.

- **Candidate query:** an issue carrying `dispatch:plan` **and** sitting in the
  board's **Backlog** column. A human applies it deliberately, like any gate.
- **What runs:** `plan-dispatch.yml` fires the Claude lane on the `writing-plans`
  contract. It claims the issue (board `Status` → In Progress, `claim:active` +
  `loop:planning`), drafts the plan, and posts (or updates) a trusted
  `## Implementation Plan` maintainer comment on the issue.
- **On completion:** it clears `dispatch:plan` and the `claim:active` / `loop:*`
  labels it used, moves board `Status` to **Human Review**, and assigns the
  gate-applier — then stops. It applies **no** execution gate.
- **Human handoff:** a human reviews the plan. If accepted, they move the issue
  back to **Backlog** and apply exactly one execution gate (`dispatch:claude`,
  `dispatch:codex`, or `dispatch:openrouter`). Planning never auto-advances into
  execution — that human validation is the point of the gate.

Apply at most one gate per issue at a time; `dispatch:plan` and the execution gates
are mutually exclusive.

## AFK vs HITL (body markers, not labels)

Mark each issue body with one:

- **`AFK`** — an agent can complete it end-to-end from the written context.
- **`HITL`** — a human decision is required mid-task.

**HITL issues must never receive any dispatch gate** — not the execution gates
(`dispatch:claude` / `dispatch:codex` / `dispatch:openrouter`) and not the planning
gate (`dispatch:plan`). Split HITL decisions out of AFK implementation work at
task-creation time so the loop only ever picks up work it can actually finish.
