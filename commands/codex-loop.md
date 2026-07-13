# Codex Loop - Autonomous task execution (Codex lane)

Claim the next `dispatch:codex` issue from the GitHub queue and work it end-to-end
through `codex exec`: branch, implement, QA, PR. One invocation handles exactly one
task — a local pull loop you trigger, not a daemon. The board/label safety model is identical to `/loop`; only the engine
differs (the local Codex CLI instead of Claude).

## Prerequisites

- **Codex CLI** installed and authenticated locally (`codex` on PATH, logged in).
- **GitHub CLI** installed and authenticated (`gh auth status`), with `project`
  scope so it can read/write the board.
- **Board env file** present: `.github/agent-loop.env` (written by
  `setup-dev-loop.sh`). Status lives on the GitHub Projects board, not in labels.

## Usage

```bash
/codex-loop            # claim and work one dispatch:codex issue via codex exec
/codex-loop --status   # show the task currently claimed by this agent (if any)
/codex-loop --list     # list dispatch:codex candidates, sorted by priority
```

## Workflow

Use the `executing-plans` skill — the same contract `/loop` runs, executed here
through `codex exec`.

**Step 0 — load the board ids.** Status lives on the GitHub Projects board (columns
Backlog · In Progress · Human Review · Done · Deferred), not in labels, so source the
committed board node ids first:

```bash
source .github/agent-loop.env   # PROJECT_OWNER, PROJECT_NUMBER, STATUS_*_OPTION_ID, …
```

1. Parse the argument:
   - `--status` → show the issue this agent currently holds (`claim:active` label +
     a claim comment whose `Claimed-By` is this platform), with its state and branch.
     Take no other action.
   - `--list` → list candidates and stop. Do not claim.
   - _(no argument)_ → claim and work one issue.
2. Build the candidate queue. A candidate carries the `dispatch:codex` gate (the
   human opt-in) **and** sits in the board's **Backlog** column:

   ```bash
   # Gate-labeled issues (human opt-in).
   gh issue list --label "dispatch:codex" \
     --json number,title,labels,assignees,comments --jq '.'
   # Numbers currently in the board's Backlog column.
   gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" --format json -L 500 \
     | jq -r '.items[] | select(.status == "Backlog") | .content.number'
   ```

   Keep only the gate-labeled issues whose number appears in the Backlog set.

3. Sort by priority (`priority:high` > `priority:medium` > `priority:low`). Skip any
   issue whose most recent claim comment is < 30 minutes old (active claim). Pick the
   top remaining issue as `N`.

4. Hand the chosen issue to `codex exec`, which runs the full `executing-plans`
   contract for issue `N` — the same inlined contract `codex-dispatch.yml` uses, so
   local and CI runs follow the same workflow contract. Model, effort, sandbox, and
   approval policy come from the effective Codex app/config layers; this reusable
   command does not override them:

   ```bash
   N=<chosen-issue-number>
   codex exec \
     "$(cat <<PROMPT
   Run the autonomous dev loop on issue #$N in this repository.

   This issue carries the \`dispatch:codex\` gate, so treat it as opted-in. The board
   \`Status\` field is the human-facing column; the AI-loop sub-phases are \`loop:*\`
   labels. Source the board ids first:

   source .github/agent-loop.env
   set_status() { local id; id=\$(gh project item-list "\$PROJECT_NUMBER" \\
     --owner "\$PROJECT_OWNER" --format json -L 500 \\
     | jq -r --argjson n "$N" '.items[] | select(.content.number == \$n) | .id'); \\
     gh project item-edit --id "\$id" --field-id "\$STATUS_FIELD_ID" \\
     --project-id "\$PROJECT_NODE_ID" --single-select-option-id "\$1"; }

   1. Claim it: move the board Status to In Progress, add \`claim:active\` +
      \`loop:planning\`, and comment an ISO-8601 \`Claimed-By: codex-cli\` / \`Claimed-At\`
      stamp.
      set_status "\$STATUS_IN_PROGRESS_OPTION_ID"; gh issue edit "$N" --add-label "claim:active,loop:planning"
   2. Read the issue body, the linked PRD/context, and ALL comments. If a trusted
      maintainer comment is headed \`## Implementation Plan\`, follow its tasks in
      order — that is the authoritative plan. Do not create any \`docs/plans\` file.
   3. Create branch \`feature/$N-<slug>\`. Advance the phase label as you go:
      \`loop:planning\` -> \`loop:executing\` -> \`loop:testing\` -> \`loop:shipping\`.
   4. Implement the vertical slice. Use TDD for behavior changes.
   5. Run the project's QA checklist (lint, tests, types, regressions) before finishing.
   6. Open a PR whose body says \`Closes #$N\`.
   7. Hand off to a human: move the board Status to Human Review, assign the reviewer,
      and clear the gate/claim/phase labels:
      set_status "\$STATUS_HUMAN_REVIEW_OPTION_ID"
      gh issue edit "$N" --add-assignee "<reviewer>" --remove-label "claim:active,dispatch:codex,loop:shipping"

   This is an AFK run: do not stop to ask questions. If a genuine HITL decision is
   required that the issue and its comments do not answer, post a comment explaining
   what is blocked, remove \`claim:active\` and any \`loop:*\` label to release the
   issue, and stop without opening a PR.
   PROMPT
   )"
   ```

5. Return control to the user. If no candidates exist, say so and exit cleanly.

## Rules

- One invocation = one task. Never loop in the background or spawn a daemon.
- Respect the 30-minute claim lock; treat older claims as stale and reclaimable. The
  lock is shared with `/loop` and the push workflows, so local and CI runs never
  double-claim.
- Never touch `HITL` issues — they lack `dispatch:codex` by design.
- `--status` and `--list` are read-only; they never claim, edit, or comment.
- Read the plan from the issue's `## Implementation Plan` comment — never from a
  `docs/plans` file. Need a reviewed plan first? Apply `dispatch:plan` (see
  `/loop` and `docs/agents/triage-labels.md`).
- The dispatch gate is `dispatch:codex`; the kanban columns are the board's
  **Status** field (Backlog / In Progress / Human Review / Done / Deferred), not
  labels. The AI-loop sub-phases are `loop:*` labels inside In Progress. Do not use
  retired names (`ready-for-codex`, `claimed`, `status:todo`, `status:testing`). See
  `docs/agents/triage-labels.md` and `docs/agents/issue-tracker.md` in the target repo.
- `/codex-loop` is the local **Codex lane**, symmetric with `/loop` (the Claude
  lane). The same gate also runs headlessly as `codex-dispatch.yml` on GitHub
  Actions; the OpenRouter lane (`dispatch:openrouter`) stays push-only.
