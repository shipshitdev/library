# Loop - Autonomous task execution

Claim the next `dispatch:claude` issue from the GitHub queue and work it end-to-end:
branch, implement, QA, PR. One invocation handles exactly one task — this is a pull
loop you trigger, not a daemon.

## Usage

```bash
/loop            # claim and work one dispatch:claude issue
/loop --status   # show the task currently claimed by this agent (if any)
/loop --list     # list dispatch:claude candidates, sorted by priority
```

## Workflow

Use the `executing-plans` skill.

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
2. Build the candidate queue. A candidate carries the `dispatch:claude` gate (the
   human opt-in) **and** sits in the board's **Backlog** column:

   ```bash
   # Gate-labeled issues (human opt-in).
   gh issue list --label "dispatch:claude" \
     --json number,title,labels,assignees,comments --jq '.'
   # Numbers currently in the board's Backlog column.
   gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" --format json -L 500 \
     | jq -r '.items[] | select(.status == "Backlog") | .content.number'
   ```

   Keep only the gate-labeled issues whose number appears in the Backlog set.

3. Sort by priority (`priority:high` > `priority:medium` > `priority:low`). Skip any
   issue whose most recent claim comment is < 30 minutes old (active claim).
4. Claim the chosen issue: flip the board Status to **In Progress**, add
   `claim:active` + `loop:planning`, and comment a `Claimed-At` timestamp. Then work
   it per `executing-plans`: branch `feature/<n>-<slug>` → implement → run
   `qa-reviewer` → open a PR with `Closes #<n>`, advancing the phase label as you go
   (`loop:planning → loop:executing → loop:testing → loop:shipping`).
5. On completion, flip the board Status to **Human Review**, assign the reviewer
   (so it lands in their queue), and clear the gate / claim / phase labels:

   ```bash
   ITEM_ID=$(gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" \
     --format json -L 500 | jq -r --argjson n <n> \
     '.items[] | select(.content.number == $n) | .id')
   gh project item-edit --id "$ITEM_ID" --field-id "$STATUS_FIELD_ID" \
     --project-id "$PROJECT_NODE_ID" --single-select-option-id "$STATUS_HUMAN_REVIEW_OPTION_ID"
   gh issue edit <n> --add-assignee "<reviewer>" \
     --remove-label "claim:active,dispatch:claude,loop:shipping"
   ```

6. Return control to the user. If no candidates exist, say so and exit cleanly.

## Rules

- One invocation = one task. Never loop in the background or spawn a daemon.
- Respect the 30-minute claim lock; treat older claims as stale and reclaimable.
- Never touch `HITL` issues — they lack `dispatch:claude` by design.
- `--status` and `--list` are read-only; they never claim, edit, or comment.
- `/loop` executes; it never plans. To get a reviewed plan first, apply the
  `dispatch:plan` planning gate: an agent drafts an `## Implementation Plan` comment
  (via `plan-dispatch.yml`) and stops at **Human Review** without applying an
  execution gate. A human approves the plan, then moves the issue back to Backlog and
  applies `dispatch:claude` so `/loop` can pick it up. `/loop` reads that trusted
  `## Implementation Plan` comment if present.
- The dispatch gate is `dispatch:claude`; the kanban columns are the board's
  **Status** field (Backlog / In Progress / Human Review / Done / Deferred), not
  labels. The AI-loop sub-phases are `loop:*` labels inside In Progress. See
  `docs/agents/triage-labels.md` and `docs/agents/issue-tracker.md` in the target repo.
- `/loop` is the **Claude lane**. The Codex/GPT lane (`dispatch:codex`) has a local
  twin — run **`/codex-loop`** to claim and work one `dispatch:codex` issue locally
  via `codex exec`, symmetric with `/loop`. Both lanes also run as push workflows
  (`agent-dispatch.yml` / `codex-dispatch.yml`); the OpenRouter lane
  (`dispatch:openrouter`) remains push-only via `openrouter-dispatch.yml`.
