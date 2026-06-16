# Triage labels

> Seed for `docs/agents/triage-labels.md`. The roles are fixed; rename the label
> strings to match this repo if needed, then update every skill that references them.

## Label vocabulary

| Label | Role |
| ----- | ---- |
| `status:todo` | In the **To Do** column — backlog-ready, but not yet opted into agent execution. |
| `status:testing` | Implemented; in the **Testing** column awaiting human QA. |
| `claimed` | An agent currently holds the issue. Paired with a timestamped claim comment (30-min lock). |
| `priority:high` / `priority:medium` / `priority:low` | Queue ordering. High is picked first. |
| `rejection:N` | QA rejection count, bumped on each kickback from Testing → To Do. |
| `ready-for-agent` | **Dispatch gate → Claude lane (human opt-in).** Nothing runs autonomously until a human applies this. |
| `ready-for-codex` | **Dispatch gate → Codex/GPT lane (human opt-in).** The Codex-lane twin of `ready-for-agent`; apply at most one gate per issue. |
| `feature` | Applied by `feature-intake` to PRD epics and their sub-issues. |
| `wontfix` | Closed; will not be actioned. Record durable reasoning under `.out-of-scope/`. |

## The dispatch gates: `ready-for-agent` / `ready-for-codex`

A dispatch gate is what turns a written-up issue into running work, and which gate
you apply picks the engine:

- `ready-for-agent` → **Claude lane** (`anthropics/claude-code-action`).
- `ready-for-codex` → **Codex/GPT lane** (`openai/codex-action`).

Both are applied **by a human**, deliberately — never automatically by
`feature-intake` or any creation step. Apply at most one gate per issue. The flow
is identical for either gate (substitute the gate label you used):

- **Candidate query:** an agent works an issue only when it carries **both** a gate
  label and `status:todo` (opted in **and** in the To Do column).
- **Local pull** (`/loop`, Claude only): lists `ready-for-agent` + `status:todo`
  candidates, sorts by priority, and claims one.
- **Push dispatch** (GitHub Actions): applying `ready-for-agent` fires
  `agent-dispatch.yml`; applying `ready-for-codex` fires `codex-dispatch.yml`.
- **On completion:** the agent removes `status:todo`, `claimed`, and the gate label
  it ran under, then adds `status:testing`.

This keeps the safety property: an issue sits inert in To Do until a human opts it
into execution. On QA **rejection**, the reviewer's reject action re-arms the gate
(restores `status:todo` + the gate label) so the loop retries — the reject is the
deliberate "try again". To stop a rejected issue instead, leave the gate off and
close it `wontfix`.

## AFK vs HITL (body markers, not labels)

Mark each issue body with one:

- **`AFK`** — an agent can complete it end-to-end from the written context.
- **`HITL`** — a human decision is required mid-task.

**HITL issues must never receive a dispatch gate** (`ready-for-agent` or
`ready-for-codex`). Split HITL decisions out of AFK implementation work at
task-creation time so the loop only ever picks up work it can actually finish.
