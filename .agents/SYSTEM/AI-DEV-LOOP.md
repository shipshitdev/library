# The AI Dev Loop

Board-driven autonomous task execution with a human opt-in gate and a human QA
gate. A human moves an issue to **To Do** on the board and applies one
dispatch-gate label, and an agent claims it, works it on a branch, and opens a PR
that lands the issue in **Testing** for review.

**Status is a board field, not a label.** Where an issue sits — Backlog / To Do /
Testing / Done — is the GitHub Projects v2 `Status` single-select field, the sole
source of truth. There are no `status:*` labels.

**Two engine lanes, one contract.** The gate label picks the engine:

- `dispatch:claude` → **Claude lane** (`anthropics/claude-code-action`).
- `dispatch:codex` → **Codex/GPT lane** (`openai/codex-action`).

Both obey the identical claim → branch → implement → QA → PR → **Testing** flow.
An issue carries at most one gate at a time. Everything below applies to both
lanes; the engine-specific bits are called out where they differ.

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

So the gate label hands a fully-planned issue to the **executor**; planning
already happened (human-driven) and QA happens twice — once by the executor
(automated checklist) and once by the human (PR review).

Both planning artifacts live **on the issue**, never in a local file:
`writing-prds` stores the PRD in the issue **body**, and `writing-plans` posts the
implementation plan as a `## Implementation Plan` **comment** on the same issue.
Because the executor and both dispatch lanes read the issue body plus all
comments, the plan crosses to CI for either engine — there is no `docs/plans/`
sidecar to drift out of sync.

## Concept

**One invocation = one task.** The loop is NOT a daemon. Each run:

1. Builds the candidate queue: issues carrying the `dispatch:claude` gate **and**
   sitting in the board's **To Do** column.
2. Claims the top-priority candidate — adds the `claim:active` label and a
   timestamped claim comment (a 30-minute lock).
3. Implements the slice on a `feature/<n>-<slug>` branch (TDD for behavior).
4. Runs the `qa-reviewer` skill (lint, tests, types, regressions).
5. Opens a PR with `Closes #<n>` and flips the board `Status` to **Testing**.
6. Exits. The human reviews the PR.

`dispatch:claude` is the safety property: nothing runs until a human deliberately
opts an issue in. An issue can sit in **To Do** untouched indefinitely.

## Workflow diagram

```
┌───────────────────────────────────────────────────────────────────┐
│                          THE AI DEV LOOP                            │
│              (Status = board field, gate = label)                  │
└───────────────────────────────────────────────────────────────────┘

   BACKLOG          TO DO              TESTING            DONE
  ┌───────┐       ┌─────────┐        ┌─────────┐       ┌───────┐
  │Status:│       │Status:  │        │Status:  │       │Status:│
  │Backlog│ ───▶  │To Do    │ ─────▶ │Testing  │ ───▶  │ Done  │
  │       │       │+dispatch│  loop  │         │ merge │  ✓    │
  └───────┘       │:claude  │        └─────────┘       └───────┘
                  └─────────┘             │
                       ▲                  │ QA reject
                       │   re-arm gate    ▼
                       │  (Status→To Do + dispatch:claude,
                       └───  rejection:N bumped)
```

The human controls the two gates: applying `dispatch:claude` (start) and merging
or rejecting the PR (finish).

## Label vocabulary

Status is **not** in this table — it is the board `Status` field. These are the
labels that ride alongside it:

| Label | Role |
| ----- | ---- |
| `claim:active` | An agent holds the issue. Paired with a timestamped claim comment (30-min lock). |
| `priority:high` / `priority:medium` / `priority:low` | Queue ordering. High first. |
| `rejection:N` | QA rejection count, bumped on each kickback from Testing → To Do. |
| `dispatch:claude` | **Dispatch gate → Claude lane (human opt-in).** Nothing runs autonomously until a human applies it. |
| `dispatch:codex` | **Dispatch gate → Codex/GPT lane (human opt-in).** The Codex-lane twin of `dispatch:claude`; apply at most one gate per issue. |
| `type:feature` | Applied by `feature-intake` to PRD epics and their sub-issues. |
| `wontfix` | Closed; will not be actioned. |

**AFK vs HITL are body markers, not labels.** Mark each issue body `AFK` (an agent
can finish from written context) or `HITL` (a human decision is required
mid-task). **HITL issues must never receive a dispatch gate** — split the human
decision out of the implementation work at creation time so the loop only ever
picks up work it can finish.

## One-time setup (per repo)

```bash
# 1. Provision labels + the board + both Phase-2 workflows + the auth secrets.
#    Migrates legacy labels, deletes status:*, normalizes the board Status field
#    to Backlog/To Do/Testing/Done, and writes .github/agent-loop.env (idempotent).
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
board (Status options Backlog/To Do/Testing/Done) and writes its node ids to
`.github/agent-loop.env`, copies both `agent-dispatch.yml` and `codex-dispatch.yml`
into `.github/workflows/`, arms `CLAUDE_CODE_OAUTH_TOKEN` (Claude lane),
`OPENAI_API_KEY` (Codex lane), and `PROJECTS_TOKEN` (the `project`-scoped PAT the
workflows use to write the board), and prints the `gh variable set` commands for
model selection. `/setup-agent-routing` writes the `## Agent skills` block into
`CLAUDE.md`/`AGENTS.md` plus `docs/agents/{issue-tracker,triage-labels,domain}.md`,
so `executing-plans`, `feature-intake`, `writing-prds`, and `qa-reviewer` can
operate in a repo they have never seen.

**Board auth: `PROJECTS_TOKEN`, not `GITHUB_TOKEN`.** The Actions default token
cannot read or write an org-owned Projects v2 board, so the dispatch workflows use
a `project`-scoped PAT stored as the `PROJECTS_TOKEN` secret. You create and paste
it at the setup script's hidden prompt; it is never generated or echoed by the
tooling. Local `/loop` runs under your own `gh` auth, which already has `project`
scope — no PAT needed locally.

**Model selection is a repo variable, never hardcoded or secret.** The model id
is non-sensitive, so it lives in **Settings → Variables** (`AGENT_MODEL`,
`CODEX_MODEL`, `CODEX_EFFORT`) — change the engine without editing a workflow.
Only auth tokens are secrets.

## Phase 1 — local pull (`/loop`)

```bash
/loop            # claim and work one dispatch:claude issue
/loop --status   # show the task this agent currently holds (read-only)
/loop --list     # list dispatch:claude candidates by priority (read-only)
```

The candidate query is the dispatch contract — the gate label intersected with the
board's To Do column:

```bash
source .github/agent-loop.env
gh issue list --label "dispatch:claude" \
  --json number,title,labels,assignees,comments --jq '.'
gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" --format json -L 500 \
  | jq -r '.items[] | select(.status == "To Do") | .content.number'
```

Sort by `priority:high` > `priority:medium` > `priority:low`. Skip any issue whose
most recent claim comment is younger than 30 minutes (an active claim). On
completion, flip the board `Status` to Testing and clear the gate + claim labels:

```bash
ITEM_ID=$(gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" --format json -L 500 \
  | jq -r --argjson n <n> '.items[] | select(.content.number == $n) | .id')
gh project item-edit --id "$ITEM_ID" --field-id "$STATUS_FIELD_ID" \
  --project-id "$PROJECT_NODE_ID" --single-select-option-id "$STATUS_TESTING_OPTION_ID"
gh issue edit <n> --remove-label "claim:active,dispatch:claude"
```

## Phase 2 — push dispatch (GitHub Actions)

Two workflows, one per engine lane. Both run on `issues: labeled`, gate on their
own label, key concurrency per issue, and run the same `executing-plans` contract
headlessly on the one labeled issue. Both authenticate `gh` with `PROJECTS_TOKEN`
so the completion step can write the board.

### Claude lane — `agent-dispatch.yml`

Gates on `if: github.event.label.name == 'dispatch:claude'` and runs via
`anthropics/claude-code-action@v1`.

- **Auth: `CLAUDE_CODE_OAUTH_TOKEN`** for the model (generate with
  `claude setup-token`, billed to a Claude subscription — **never set
  `ANTHROPIC_API_KEY`**, which takes precedence and bills metered API) and
  **`PROJECTS_TOKEN`** as `github_token` for the board write.
- **Model:** `claude_args: --model ${{ vars.AGENT_MODEL || 'claude-sonnet-4-6' }}`.
  v1 has no `model:` input, so the model rides `claude_args`. `AGENT_MODEL` is a
  repo variable; unset → Sonnet.

### Codex lane — `codex-dispatch.yml`

Gates on `if: github.event.label.name == 'dispatch:codex'` and runs via
`openai/codex-action@v1` with `sandbox: workspace-write` and
`safety-strategy: drop-sudo`.

- **Auth: `OPENAI_API_KEY`** for the model; `GH_TOKEN`/`GITHUB_TOKEN` are set to
  `PROJECTS_TOKEN` in the step env so `gh` (including the board write) works inside
  the run.
- **Model:** `model: ${{ vars.CODEX_MODEL }}` and `effort: ${{ vars.CODEX_EFFORT }}`
  — both repo variables. Leave either unset for Codex's defaults (empty is valid).
- The 7-step `executing-plans` contract is inlined into the workflow `prompt:` so
  the run is self-contained even where the skill file is not loaded.

### Shared properties

- **Concurrency** is keyed per issue, so re-applying a gate label will not start a
  second run.
- **Trust boundary:** only issues a human deliberately labels are processed. Issue
  title/body stay untrusted (prompt-injection surface) and are never interpolated
  into the shell or the prompt — only the trusted integer issue number is.

## Human review

After the loop completes, review the PRs / issues sitting in **Testing**:

- **Approve:** merge the PR — the issue closes via `Closes #<n>`; set board
  `Status` = Done.
- **Reject:** request changes, then re-arm the gate so the loop retries — set board
  `Status` = To Do, re-apply `dispatch:claude`, and bump `rejection:N`. The reject
  is the deliberate "try again".

```bash
# Reject → re-queue (set Status=To Do on the board, then re-arm the gate)
source .github/agent-loop.env
ITEM_ID=$(gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" --format json -L 500 \
  | jq -r --argjson n <n> '.items[] | select(.content.number == $n) | .id')
gh project item-edit --id "$ITEM_ID" --field-id "$STATUS_FIELD_ID" \
  --project-id "$PROJECT_NODE_ID" --single-select-option-id "$STATUS_TODO_OPTION_ID"
gh issue edit <n> --add-label "dispatch:claude,rejection:1"   # bump rejection:N on each successive kickback

# Stop a rejected issue instead: leave dispatch:claude off and close it.
gh issue close <n> --comment "..." && gh issue edit <n> --add-label "wontfix"
```

## Multi-platform + rate-limit handling

The claim mechanic is platform-agnostic — the 30-minute claim lock is what lets
any tool pick up where another left off.

| Scenario | What happens |
| -------- | ------------ |
| Agent completes the task | PR opened, board `Status` moves to Testing. |
| Agent rate-limited / crashes | Claim comment ages out (30 min); the issue is reclaimable. |
| Switch editors mid-flight | The other agent sees the stale claim and reclaims the issue. |
| QA rejects | Gate re-armed (`Status` = To Do + `dispatch:claude`, `rejection:N`). |

All platforms read/write the same GitHub Issues, board, and `.agents/SESSIONS/`
files, so no external coordination service is needed.

## Why this works

| Benefit | How |
| ------- | --- |
| Human opt-in | Nothing runs until a human applies `dispatch:claude`. |
| HITL safety | HITL issues never carry the gate, so the loop only takes finishable work. |
| Single source of truth | Status lives only on the board field — labels never duplicate it. |
| Multi-platform | Any tool can read/write Markdown, the board, and `gh`. |
| Handles failure | The 30-minute claim lock makes stalled work reclaimable. |
| Human oversight | The Testing gate requires PR review before Done. |

## Commands & skills

| Entry point | Effect |
| ----------- | ------ |
| `/loop` | Claim and work one task locally, Claude lane (Phase 1). |
| `/loop --status` / `/loop --list` | Read-only: show the held task / list candidates. |
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
4. **Review promptly** — don't let the Testing queue grow.
5. **Document rejections** — rejection comments carry the context the retry needs.
6. **Use PRDs** — link tasks to product requirements via `feature-intake`.
