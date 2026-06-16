# Loop - Autonomous task execution

Claim the next agent-ready issue from the GitHub queue and work it end-to-end:
branch, implement, QA, PR. One invocation handles exactly one task — this is a pull
loop you trigger, not a daemon.

## Usage

```bash
/loop            # claim and work one ready-for-agent issue
/loop --status   # show the task currently claimed by this agent (if any)
/loop --list     # list ready-for-agent candidates, sorted by priority
```

## Workflow

Use the `executing-plans` skill.

1. Parse the argument:
   - `--status` → show the issue this agent currently holds (`claimed` label + a
     claim comment whose `Claimed-By` is this platform), with its state and branch.
     Take no other action.
   - `--list` → list candidates and stop. Do not claim.
   - _(no argument)_ → claim and work one issue.
2. Build the candidate queue (the `ready-for-agent` gate is the human opt-in):

   ```bash
   gh issue list --label "ready-for-agent" --label "status:todo" \
     --json number,title,labels,assignees,comments --jq '.'
   ```

3. Sort by priority (`priority:high` > `priority:medium` > `priority:low`). Skip any
   issue whose most recent claim comment is < 30 minutes old (active claim).
4. Follow `executing-plans` for the chosen issue: claim it → branch
   `feature/<n>-<slug>` → implement → run `qa-reviewer` → open a PR with `Closes #<n>`
   → move it to Testing.
5. On completion, transition the labels:

   ```bash
   gh issue edit <n> --remove-label "status:todo,claimed,ready-for-agent" \
     --add-label "status:testing"
   ```

6. Return control to the user. If no candidates exist, say so and exit cleanly.

## Rules

- One invocation = one task. Never loop in the background or spawn a daemon.
- Respect the 30-minute claim lock; treat older claims as stale and reclaimable.
- Never touch `HITL` issues — they lack `ready-for-agent` by design.
- `--status` and `--list` are read-only; they never claim, edit, or comment.
- The dispatch gate is `ready-for-agent`; the kanban columns stay `status:todo` /
  `status:testing`. See `docs/agents/triage-labels.md` in the target repo.
- `/loop` is the **Claude lane**. The Codex/GPT lane (`ready-for-codex`) is
  push-only — it runs via `codex-dispatch.yml` on GitHub Actions, not locally here.
