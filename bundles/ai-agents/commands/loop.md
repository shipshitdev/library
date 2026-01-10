# AI Development Loop - Autonomous Task Execution

Execute the next available task from the queue with full autonomy.

## When to Use

Run `/loop` when:
- You want an AI agent to pick up and complete the next task
- You're building features autonomously with QA gates
- You want to maximize subscription usage across platforms

## Loop Behavior

Each `/loop` invocation processes ONE task:

1. **Find Next Task**
   - Scan `.agent/TASKS/` for `Status: To Do`
   - Sort by Priority: High > Medium > Low
   - Skip tasks with active claims (< 30 min old)

2. **Claim Task**
   - Update task file with:
     - `**Claimed-By:** [platform]-[session-id]`
     - `**Claimed-At:** [ISO timestamp]`

3. **Read Context**
   - Read the task file completely
   - Read linked PRD if `**PRD:**` field exists
   - Check `.agent/SESSIONS/` for related past work

4. **Implement**
   - Follow the task requirements
   - Update `**Agent-Notes:**` with progress
   - Create branch: `feature/[task-id]`
   - Make commits with clear messages

5. **Quality Check**
   - Run the qa-reviewer skill
   - Update `**QA-Checklist:**` items
   - Ensure code compiles/lints

6. **Complete**
   - Update task: `**Status:** Testing`
   - Set `**Completed-At:** [timestamp]`
   - Add final notes to `**Agent-Notes:**`

7. **Prompt for Next**
   - Show: "Task moved to Testing. Run /loop for next task or review in Kaiban.md"

## Task Selection Priority

```
Priority: High > Medium > Low
Within same priority: First created wins
Skip if: Claimed-At < 30 minutes ago (another agent working)
```

## Claim Expiration

Claims expire after 30 minutes. If an agent crashes or rate-limits mid-task:
- Task remains in To Do
- Claim expires
- Next `/loop` can pick it up
- Previous `**Agent-Notes:**` provide context

## Multi-Platform Usage

```bash
# Claude CLI
claude
> /loop   # Process task
> /loop   # Next task
> /loop   # Keep going...

# Rate limited? Switch platform
# Open same project in Cursor
# Continue with /loop there
```

## Rate Limit Handling

When rate limited:
1. Agent saves progress to `**Agent-Notes:**`
2. Agent sets `**Claimed-By:**` to empty (releases claim)
3. Agent prompts: "Rate limited. Switch to [Cursor/Codex] or wait"

## No Background Processes

This is NOT a daemon. Each `/loop`:
- Runs in foreground
- Completes one task
- Returns control to user
- User decides to continue or stop

## Integration with Kaiban.md

After `/loop` moves task to Testing:
1. Open Kaiban.md extension in VS Code
2. Task appears in Testing column
3. Click to see PRD preview
4. Approve (drag to Done) or Reject (click reject button)

Rejected tasks return to To Do with rejection notes for next `/loop`.

## Example Session

```
User: /loop

Agent: Scanning .agent/TASKS/ for available tasks...

Found 3 tasks in To Do:
1. [High] add-reject-button - Kaiban.md reject functionality
2. [Medium] improve-prd-preview - Better markdown rendering
3. [Low] add-keyboard-shortcuts - Accessibility improvements

Claiming: add-reject-button

Reading task file... Done.
Reading linked PRD... Done.

Implementing add-reject-button:
- Adding reject button to kanbanView.ts
- Adding rejectTask handler to taskParser.ts
- Updating CSS for reject button styling

Running qa-reviewer...
- [x] Code compiles
- [x] No linting errors
- [ ] Tests pass (CI will verify)
- [ ] User acceptance (you'll verify)

Task moved to Testing.

Run /loop for next task, or review in Kaiban.md.
```

## Task File Updates

During loop, task file is updated:

```markdown
### Agent Metadata

**Claimed-By:** claude-cli-abc123
**Claimed-At:** 2025-12-28T10:30:00Z
**Completed-At:** 2025-12-28T11:15:00Z

---

### Progress

**Agent-Notes:**
- 10:30 - Started implementation
- 10:45 - Added reject button component
- 11:00 - Wired up message handler
- 11:10 - Styled button, tested locally
- 11:15 - QA passed, moving to Testing

**QA-Checklist:**
- [x] Code compiles/lints
- [x] Tests pass (CI)
- [ ] User acceptance
- [ ] Visual review
```
