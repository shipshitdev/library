# The AI Dev Loop

Board-driven autonomous task execution with a human opt-in gate and a human QA
gate. A human puts an issue in **Backlog** and applies one dispatch-gate label; an
agent claims it (board → **In Progress**), works it on a branch, and opens a PR that
lands the issue in **Human Review** — auto-assigned to the reviewer.

**Columns are for humans; labels carry the AI loop.** The board `Status` field is
the sole source of truth for the human-facing column. The loop's own sub-phases ride
as `loop:*` labels *inside* In Progress, so the board stays readable while the labels
show exactly where the agent is. This mirrors **ShipCode** (the productized version
of this workflow): macro columns for humans, `shipcode:pipeline:*` sub-state labels
for the loop; this repo is the open, `gh`-driven version of the same pipeline.

**Two engine lanes, one contract.** The gate label picks the engine:

- `dispatch:claude` → **Claude lane** (`anthropics/claude-code-action`).
- `dispatch:codex` → **Codex/GPT lane** (`openai/codex-action`).

(ShipCode equivalents: `shipcode:agent:claude` / `shipcode:agent:codex`.) Both obey
the identical claim → branch → implement → QA → PR → **Human Review** flow. An issue
carries at most one gate at a time.

Two ways to run it, same contract:

- **Phase 1 — local pull (`/loop`).** You trigger one task at a time from your
  editor (Claude lane). Cheap, fully under your hand.
- **Phase 2 — push dispatch (GitHub Actions).** Applying a gate label fires its
  dispatch workflow (`agent-dispatch.yml` for Claude, `codex-dispatch.yml` for
  Codex), which runs the loop headlessly. Truly AFK.

The runtime behavior lives in the **`executing-plans`** skill — this doc is the
operator's map; that skill is the implementation.

## Where the planner / executor / QA roles live

The loop has the classic planner → executor → QA split, but it lives at the
**skill layer mapped to lifecycle stages**, not as three separate CI agents:

| Role | Skill(s) | Who runs it |
| ---- | -------- | ----------- |
| **Planner** | `feature-intake` → `writing-prds` / `writing-plans` | Human, before the gate. Creates the issue + PRD + acceptance criteria. |
| **Executor** | `executing-plans` | The dispatched agent (Claude or Codex). What the loop runs. |
| **QA** | `qa-reviewer` | The executor runs it before opening the PR; the human reviews after. |

Both planning artifacts live **on the issue**, never in a local file: `writing-prds`
stores the PRD in the issue **body**, and `writing-plans` posts the implementation
plan as a `## Implementation Plan` **comment**. The executor and both dispatch lanes
read the body plus all comments, so the plan crosses to CI for either engine.

## Concept

**One invocation = one task.** The loop is NOT a daemon. Each run:

1. Builds the candidate queue: issues carrying a dispatch gate **and** sitting in the
   board's **Backlog** column.
2. Claims the top-priority candidate — flips the board to **In Progress**, adds the
   `claim:active` label + a timestamped claim comment (a 30-minute lock), and starts
   the phase labels at `loop:planning`.
3. Implements the slice on a `feature/<n>-<slug>` branch (TDD for behavior),
   advancing `loop:planning → loop:executing → loop:testing → loop:shipping`.
4. Runs the `qa-reviewer` skill (lint, tests, types, regressions) — the `loop:testing`
   phase. Automated tests + PR CI are the test gate; there is no Testing column.
5. Opens a PR with `Closes #<n>`, flips the board `Status` to **Human Review**, and
   auto-assigns the reviewer.
6. Exits. The human reviews the PR.

The gate is the safety property: nothing runs until a human deliberately opts an
issue in. An issue can sit in **Backlog** untouched indefinitely.

## Workflow diagram

```
┌───────────────────────────────────────────────────────────────────┐
│                          THE AI DEV LOOP                            │
│        (board columns = humans · loop:* labels = the AI loop)       │
└───────────────────────────────────────────────────────────────────┘

   BACKLOG          IN PROGRESS        HUMAN REVIEW         DONE
  ┌─────────┐      ┌───────────┐      ┌───────────┐      ┌───────┐
  │ open +  │ ───▶ │ agent     │ ───▶ │ PR open;  │ ───▶ │  ✓    │
  │ gate    │ loop │ builds    │  PR  │ assigned  │ merge│       │
  │(opt-in) │      │ (loop:*)  │      │ to you    │      │       │
  └─────────┘      └───────────┘      └───────────┘      └───────┘
       ▲                                    │
       │   re-arm gate (reject)             │ QA reject
       └──── Status→Backlog + gate, ────────┘
             rejection:N bumped        (Deferred = parked / wontfix)

  loop:planning → loop:executing → loop:testing → loop:shipping  (labels in In Progress)
```

The human controls the two gates: applying a dispatch label (start) and merging or
rejecting the PR (finish).

## Label vocabulary

Status is **not** in this table — it is the board `Status` field. These are the
labels that ride alongside it:

| Label | Role |
| ----- | ---- |
| `claim:active` | An agent holds the issue. Paired with a timestamped claim comment (30-min lock). |
| `loop:planning` / `loop:executing` / `loop:testing` / `loop:shipping` | AI-loop sub-phase **inside In Progress** (observability; mirrors `shipcode:pipeline:*`). |
| `priority:high` / `priority:medium` / `priority:low` | Queue ordering. High first. |
| `rejection:N` | QA rejection count, bumped on each kickback from Human Review → Backlog. |
| `dispatch:claude` | **Dispatch gate → Claude lane (human opt-in).** Nothing runs autonomously until a human applies it. |
| `dispatch:codex` | **Dispatch gate → Codex/GPT lane (human opt-in).** Apply at most one gate per issue. |
| `type:feature` | Applied by `feature-intake` to PRD epics and their sub-issues. |
| `wontfix` | Closed; will not be actioned (often paired with the Deferred column). |

**AFK vs HITL are body markers, not labels.** Mark each issue body `AFK` (an agent
can finish from written context) or `HITL` (a human decision is required mid-task).
**HITL issues must never receive a dispatch gate.**

## One-time setup (per repo)

```bash
# 1. Provision labels + the board + both Phase-2 workflows + the auth secrets.
#    Normalizes the board Status to Backlog/In Progress/Human Review/Done/Deferred
#    and writes .github/agent-loop.env (idempotent).
bash scripts/setup-dev-loop.sh            # or: --repo owner/name, --project N, --dry-run

# 2. Pick which model each lane runs (repo VARIABLES, not secrets — optional):
gh variable set AGENT_MODEL  --body claude-opus-4-8   # Claude lane; defaults to Sonnet
gh variable set CODEX_MODEL  --body gpt-5.5           # Codex lane; unset = provider default
gh variable set CODEX_EFFORT --body xhigh             # Codex reasoning effort

# 3. Write this repo's routing block so the loop skills know its tracker + labels.
#    Run in Claude Code:
/setup-agent-routing
```

`setup-dev-loop.sh` creates the label vocabulary above, provisions the Projects
board (Status options Backlog/In Progress/Human Review/Done/Deferred) and writes its
node ids to `.github/agent-loop.env`, copies both dispatch workflows into
`.github/workflows/`, and arms `CLAUDE_CODE_OAUTH_TOKEN` (Claude lane),
`OPENAI_API_KEY` (Codex lane), and `PROJECTS_TOKEN` (the `project`-scoped PAT the
workflows use to write the board).

**Board auth: `PROJECTS_TOKEN`, not `GITHUB_TOKEN`.** The Actions default token
cannot read/write an org-owned Projects v2 board, so the dispatch workflows use a
`project`-scoped PAT stored as the `PROJECTS_TOKEN` secret. You create and paste it
at the setup script's hidden prompt; it is never generated or echoed by the tooling.
Local `/loop` runs under your own `gh` auth, which already has `project` scope.

## Phase 1 — local pull (`/loop`)

```bash
/loop            # claim and work one dispatch:claude issue
/loop --status   # show the task this agent currently holds (read-only)
/loop --list     # list dispatch:claude candidates by priority (read-only)
```

The candidate query is the dispatch contract — the gate label intersected with the
board's Backlog column:

```bash
source .github/agent-loop.env
gh issue list --label "dispatch:claude" \
  --json number,title,labels,assignees,comments --jq '.'
gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" --format json -L 500 \
  | jq -r '.items[] | select(.status == "Backlog") | .content.number'
```

On claim, flip the board to In Progress (`STATUS_IN_PROGRESS_OPTION_ID`) + add
`claim:active,loop:planning`. On completion, flip to Human Review and assign the
reviewer:

```bash
ITEM_ID=$(gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" --format json -L 500 \
  | jq -r --argjson n <n> '.items[] | select(.content.number == $n) | .id')
gh project item-edit --id "$ITEM_ID" --field-id "$STATUS_FIELD_ID" \
  --project-id "$PROJECT_NODE_ID" --single-select-option-id "$STATUS_HUMAN_REVIEW_OPTION_ID"
gh issue edit <n> --add-assignee "<reviewer>" \
  --remove-label "claim:active,dispatch:claude,loop:shipping"
```

## Phase 2 — push dispatch (GitHub Actions)

Two workflows, one per engine lane. Both run on `issues: labeled`, gate on their own
label, key concurrency per issue, and run the same `executing-plans` contract
headlessly. Both authenticate `gh` with `PROJECTS_TOKEN` so the claim and completion
steps can write the board.

### Claude lane — `agent-dispatch.yml`

Gates on `if: github.event.label.name == 'dispatch:claude'`, runs via
`anthropics/claude-code-action@v1`.

- **Auth:** `CLAUDE_CODE_OAUTH_TOKEN` for the model (never set `ANTHROPIC_API_KEY`)
  plus `PROJECTS_TOKEN` as `github_token` for the board write.
- **Model:** `claude_args: --model ${{ vars.AGENT_MODEL || 'claude-sonnet-4-6' }}`.

### Codex lane — `codex-dispatch.yml`

Gates on `if: github.event.label.name == 'dispatch:codex'`, runs via
`openai/codex-action@v1` (`sandbox: workspace-write`, `safety-strategy: drop-sudo`).

- **Auth:** `OPENAI_API_KEY` for the model; `GH_TOKEN`/`GITHUB_TOKEN` = `PROJECTS_TOKEN`.
- **Model:** `model: ${{ vars.CODEX_MODEL }}` / `effort: ${{ vars.CODEX_EFFORT }}`.
- The contract is inlined into the workflow `prompt:` so the run is self-contained.

### Shared properties

- **Auto-assign:** the completion step assigns the gate-applier (`$GITHUB_ACTOR`) so
  the PR lands in their Human Review queue.
- **Concurrency** is keyed per issue, so re-applying a gate label will not start a
  second run.
- **Trust boundary:** only issues a human deliberately labels are processed. Issue
  title/body stay untrusted; only the integer issue number and the validated
  `$GITHUB_ACTOR` handle are interpolated.

## Human review

After the loop completes, review the PRs / issues sitting in **Human Review** (each
auto-assigned to you):

- **Approve:** merge the PR — the issue closes via `Closes #<n>`; set board
  `Status` = Done.
- **Reject:** request changes, then re-arm the gate so the loop retries — set board
  `Status` = Backlog, re-apply the gate label, and bump `rejection:N`.

```bash
# Reject → re-queue (set Status=Backlog on the board, then re-arm the gate)
source .github/agent-loop.env
ITEM_ID=$(gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" --format json -L 500 \
  | jq -r --argjson n <n> '.items[] | select(.content.number == $n) | .id')
gh project item-edit --id "$ITEM_ID" --field-id "$STATUS_FIELD_ID" \
  --project-id "$PROJECT_NODE_ID" --single-select-option-id "$STATUS_BACKLOG_OPTION_ID"
gh issue edit <n> --add-label "dispatch:claude,rejection:1"   # bump rejection:N on each kickback

# Stop a rejected issue instead: move it to Deferred (leave the gate off) or close wontfix.
```

## Multi-platform + rate-limit handling

The claim mechanic is platform-agnostic — the 30-minute claim lock is what lets any
tool pick up where another left off.

| Scenario | What happens |
| -------- | ------------ |
| Agent completes the task | PR opened, board `Status` moves to Human Review, assigned to you. |
| Agent rate-limited / crashes | Claim comment ages out (30 min); the issue is reclaimable. |
| Switch editors mid-flight | The other agent sees the stale claim and reclaims the issue. |
| QA rejects | Gate re-armed (`Status` = Backlog + gate label, `rejection:N`). |

## Why this works

| Benefit | How |
| ------- | --- |
| Human opt-in | Nothing runs until a human applies a dispatch gate. |
| HITL safety | HITL issues never carry the gate, so the loop only takes finishable work. |
| Single source of truth | Status lives only on the board field — labels never duplicate it. |
| Loop observability | `loop:*` labels show the AI-loop phase without cluttering the board. |
| Human oversight | The Human Review column requires PR review before Done. |

## Commands & skills

| Entry point | Effect |
| ----------- | ------ |
| `/loop` | Claim and work one task locally, Claude lane (Phase 1). |
| `agent-dispatch.yml` | Push dispatch on `dispatch:claude` — Claude lane (Phase 2). |
| `codex-dispatch.yml` | Push dispatch on `dispatch:codex` — Codex/GPT lane (Phase 2). |
| `executing-plans` skill | The loop's runtime behavior (claim → branch → QA → PR). |
| `qa-reviewer` skill | The QA gate run before every PR. |
| `feature-intake` / `writing-prds` skills | Create the PRD epics + sub-issues the loop consumes. |
| `setup-dev-loop.sh` / `/setup-agent-routing` | One-time per-repo provisioning. |

## Best practices

1. **Keep tasks small** — one task = one PR's worth of work.
2. **Write clear acceptance criteria** — the agent needs a definition of done.
3. **Split HITL from AFK** at creation time — never gate a HITL issue.
4. **Review promptly** — don't let the Human Review queue grow.
5. **Document rejections** — rejection comments carry the context the retry needs.
6. **Use PRDs** — link tasks to product requirements via `feature-intake`.
