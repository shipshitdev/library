# The AI Dev Loop

The `/loop` command enables autonomous task execution with human QA gates.

## Concept

**One invocation = one task.** The loop is NOT a daemon that runs continuously. Each `/loop` invocation:

1. Picks the highest priority "To Do" task
2. Claims it (30-minute expiration)
3. Implements the solution
4. Runs automated QA
5. Moves task to "Testing"
6. Exits

The human reviews in `Kaiban.md` and either approves (Done) or rejects (back to To Do).

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        THE AI DEV LOOP                          │
└─────────────────────────────────────────────────────────────────┘

     BACKLOG          TO DO          TESTING          DONE
    ┌───────┐       ┌───────┐       ┌───────┐       ┌───────┐
    │       │       │       │       │       │       │       │
    │ Ideas │ ───▶  │ Ready │ ───▶  │  QA   │ ───▶  │  ✓    │
    │       │       │       │       │       │       │       │
    └───────┘       └───────┘       └───────┘       └───────┘
                        │               │
                        │    /loop      │   Human Review
                        │    ─────▶     │   ◀─────
                        │               │
                        │               ▼
                        │           ┌───────┐
                        │           │Reject │
                        └───────────│ + Fix │
                                    └───────┘
```

## Loop Behavior

When you run `/loop`:

### 1. Task Selection

```
Find tasks where:
  - status = "To Do"
  - (claimed_by is null OR expires_at < now)
Order by:
  - priority DESC
  - created ASC
Pick first match
```

### 2. Claim Task

```yaml
claimed_by: claude-code  # or cursor, codex
claimed_at: 2024-01-16T10:30:00Z
expires_at: 2024-01-16T11:00:00Z  # 30 min from now
status: In Progress
```

### 3. Implement

- Read task requirements
- Check related PRD sections
- Implement the solution
- Follow project conventions

### 4. QA Gate

- Run linting
- Run tests
- Run type checking
- Check for regressions

### 5. Move to Testing

```yaml
status: Testing
claimed_by: null
claimed_at: null
expires_at: null
```

### 6. Exit

Loop ends. Human reviews the work.

## Human Review

After `/loop` completes, check `Kaiban.md` for tasks in "Testing":

**Approve:** Move to "Done"

```yaml
status: Done
```

**Reject:** Move back to "To Do" with feedback

```yaml
status: To Do
---
## Rejection Feedback
- Issue 1: Description
- Issue 2: Description
```

## Multi-Platform Usage

The file-based system enables platform switching:

```
User on Claude Code    ─────▶  Rate limited
                                    │
                                    ▼
                              Claim expires (30 min)
                                    │
                                    ▼
User switches to Cursor ─────▶  Picks up same task
```

### Example Workflow

1. **Morning:** Work in Claude Code, run `/loop` 3 times
2. **Rate limited:** Switch to Cursor
3. **Cursor:** Previous claim expired, picks up next task
4. **Evening:** Back to Claude Code, continues where left off

All platforms read/write the same `.agent/TASKS/` files.

## Rate Limit Handling

The 30-minute claim expiration solves rate limits:

| Scenario | What Happens |
|----------|--------------|
| Agent completes task | Claim cleared, task moves to Testing |
| Agent rate limited | Claim expires after 30 min |
| Agent crashes | Claim expires after 30 min |
| User switches platforms | Other agent claims after expiration |

No manual intervention needed. The system self-heals.

## Kaiban.md Integration

`Kaiban.md` is an optional visual task board:

```markdown
# Kaiban

## Backlog
- [ ] Task idea 1
- [ ] Task idea 2

## To Do
- [ ] Task 001: Feature X (high)
- [ ] Task 002: Bug Y (medium)

## Testing
- [ ] Task 003: Feature Z - awaiting review

## Done
- [x] Task 000: Initial setup
```

Use it for:

- Quick visual overview
- Manual task prioritization
- Review queue management

## Why This Works

| Benefit | How |
|---------|-----|
| No external dependencies | File-based state |
| Multi-platform | Any tool can read/write markdown |
| Handles failures | Claim expiration |
| Human oversight | Testing gate requires approval |
| Context preservation | Session docs + task history |

## Commands

| Command | Effect |
|---------|--------|
| `/loop` | Process one task |
| `/loop --status` | Show current task state |
| `/loop --list` | List available tasks |

## Best Practices

1. **Keep tasks small** - One task = one PR's worth of work
2. **Write clear acceptance criteria** - Agent needs to know when done
3. **Review promptly** - Don't let Testing queue grow
4. **Document rejections** - Help agent learn from feedback
5. **Use PRDs** - Link tasks to product requirements
