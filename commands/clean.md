# Clean - Unified Cleanup Command

Clean up completed tasks and consolidate session files.

## Usage

```bash
/clean tasks      # Clean completed task files
/clean sessions   # Merge and consolidate session files
/clean all        # Run all cleanup operations
```

## Option 1: Clean Tasks

Close out completed work tracked in GitHub Issues so the open backlog stays accurate.

### Process

1. Find issues that are done (all checklist items `[x]`, or work shipped/merged) but still open
2. Close each with a short completion comment linking the session:

```bash
gh issue close <number> --comment "Completed — see .agents/sessions/[date].md for details."
```

1. Log closed issues to today's session file

### Checklist

- [ ] List open issues that look complete (`gh issue list --state open`)
- [ ] Confirm with user before closing
- [ ] Close each with a completion comment
- [ ] Update session file with cleanup log

## Option 2: Clean Sessions

Merge daily sessions into monthly, monthly into yearly.

### Process

1. **Daily -> Monthly:** Consolidate `YYYY-MM-DD.md` files into `YYYY-MM.md`
2. **Monthly -> Yearly:** Consolidate `YYYY-MM.md` files into `YYYY-yearly-review.md`

### Safety

- Create backup before modifying: `.agents/sessions/backups/`
- Preserve `README.md`
- Dry-run mode available — preview without changes

### Checklist

- [ ] Back up existing sessions
- [ ] Merge daily files for past months
- [ ] Merge monthly files for past years
- [ ] Report what was consolidated

## Option 3: Clean All

Run task cleanup then session cleanup sequentially. Report summary of both.
