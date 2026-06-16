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

**Step 0 — load the board ids.** Status lives on the GitHub Projects board, not in
labels, so source the committed board node ids first:

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
   human opt-in) **and** sits in the board's **To Do** column:

   ```bash
   # Gate-labeled issues (human opt-in).
   gh issue list --label "dispatch:claude" \
     --json number,title,labels,assignees,comments --jq '.'
   # Numbers currently in the board's To Do column.
   gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" --format json -L 500 \
     | jq -r '.items[] | select(.status == "To Do") | .content.number'
   ```

   Keep only the gate-labeled issues whose number appears in the To Do set.

3. Sort by priority (`priority:high` > `priority:medium` > `priority:low`). Skip any
   issue whose most recent claim comment is < 30 minutes old (active claim).
4. Follow `executing-plans` for the chosen issue: claim it → branch
   `feature/<n>-<slug>` → implement → run `qa-reviewer` → open a PR with `Closes #<n>`
   → move it to Testing.
5. On completion, flip the board Status to **Testing** and clear the gate + claim
   labels (status is a board field, not a label):

   ```bash
   ITEM_ID=$(gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" \
     --format json -L 500 | jq -r --argjson n <n> \
     '.items[] | select(.content.number == $n) | .id')
   gh project item-edit --id "$ITEM_ID" --field-id "$STATUS_FIELD_ID" \
     --project-id "$PROJECT_NODE_ID" --single-select-option-id "$STATUS_TESTING_OPTION_ID"
   gh issue edit <n> --remove-label "claim:active,dispatch:claude"
   ```

6. Return control to the user. If no candidates exist, say so and exit cleanly.

## Rules

- One invocation = one task. Never loop in the background or spawn a daemon.
- Respect the 30-minute claim lock; treat older claims as stale and reclaimable.
- Never touch `HITL` issues — they lack `dispatch:claude` by design.
- `--status` and `--list` are read-only; they never claim, edit, or comment.
- The dispatch gate is `dispatch:claude`; the kanban columns are the board's
  **Status** field (Backlog / To Do / Testing / Done), not labels. See
  `docs/agents/triage-labels.md` and `docs/agents/issue-tracker.md` in the target repo.
- `/loop` is the **Claude lane**. The Codex/GPT lane (`dispatch:codex`) is
  push-only — it runs via `codex-dispatch.yml` on GitHub Actions, not locally here.
