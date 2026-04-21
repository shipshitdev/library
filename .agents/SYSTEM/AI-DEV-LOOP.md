# The AI Dev Loop

The `/loop` command enables autonomous task execution with human QA gates.

## Concept

**One invocation = one task.** The loop is NOT a daemon that runs continuously. Each `/loop` invocation:

1. Picks the highest priority task from GitHub Issues
2. Claims it (assigns to self, adds "in-progress" label)
3. Implements the solution
4. Runs automated QA
5. Opens a PR and moves the issue to "Testing" / awaiting review
6. Exits

The human reviews the PR and either approves (merges / closes issue as Done) or requests changes (issue goes back to open).

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

Query GitHub Issues:

```
Find issues where:
  - status = open
  - label = "to-do" or no in-progress label
Order by:
  - priority label DESC
  - created ASC
Pick first match
```

### 2. Claim Task

Add "in-progress" label and self-assign the issue to signal it is being worked on.

### 3. Implement

- Read task requirements from the issue body
- Check related PRD sections or linked issues
- Implement the solution
- Follow project conventions

### 4. QA Gate

- Run linting
- Run tests
- Run type checking
- Check for regressions

### 5. Move to Testing

Open a PR referencing the issue. Remove "in-progress" label and add "testing" label. The issue is now awaiting human review.

### 6. Exit

Loop ends. Human reviews the work.

## Human Review

After `/loop` completes, check GitHub Issues / PRs for items in "Testing":

**Approve:** Merge the PR — issue closes automatically (or close manually).

**Reject:** Request changes on the PR with specific feedback. Remove "testing" label, add "to-do" so the loop can pick it up again.

## Multi-Platform Usage

The file-based session system enables platform switching:

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

All platforms read/write the same `.agents/SESSIONS/` files and GitHub Issues.

## Rate Limit Handling

The GitHub Issue claim system handles rate limits gracefully:

| Scenario | What Happens |
|----------|--------------|
| Agent completes task | PR opened, issue moves to Testing |
| Agent rate limited | Remove in-progress label, issue stays open |
| Agent crashes | Manually remove in-progress label |
| User switches platforms | Other agent picks up open issue |

## Why This Works

| Benefit | How |
|---------|-----|
| No external dependencies | File-based sessions + GitHub Issues |
| Multi-platform | Any tool can read/write markdown and GitHub |
| Handles failures | Re-open issue to re-queue |
| Human oversight | Testing gate requires PR approval |
| Context preservation | Session docs + issue history |

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
