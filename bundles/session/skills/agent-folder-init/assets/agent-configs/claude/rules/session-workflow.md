# Session Workflow Standards

Standards for managing AI coding sessions across projects.

---

## Session Start

### Read Critical Documentation First

Before any work:

1. Read project-specific rules (if they exist)
2. Check for recent session documentation
3. Understand what was done before

---

### Check for Previous Related Work

```bash
# Search for similar work in session history
grep -r "keyword" .agents/SESSIONS/*.md 2>/dev/null || true
```

If previous work exists:

- Read how it was done
- Use the same patterns
- Don't re-implement

---

## During Session

### Track Progress

For multi-step tasks:

- Use todo lists to track steps
- Mark items complete as you go
- Keep user informed of progress

---

### Document Decisions

When making non-obvious choices:

- Note what you chose and why
- Document alternatives considered
- Record any trade-offs

---

## Session End

### Before Clearing Context

When user is about to clear session (/clear):

1. **Document what was done:**

   - Files created/modified
   - Features implemented
   - Bugs fixed
   - Decisions made

2. **Note incomplete work:**

   - What remains to be done
   - Blockers encountered
   - Next steps

3. **Save to session file:**
   - Location: `.agents/SESSIONS/YYYY-MM-DD.md`
   - One file per day
   - Multiple sessions append to same file

---

### Session File Format

```markdown
# Session: YYYY-MM-DD

## Session 1 (HH:MM AM/PM)

### Goal

What was requested

### Changes Made

- file1.ts: Added X feature
- file2.ts: Fixed Y bug

### Decisions

- Chose approach A over B because...

### Incomplete

- Still need to do Z

---

## Session 2 (HH:MM AM/PM)

[Next session in same day...]
```

---

## Session File Rules

### One File Per Day

**CORRECT:**

```
.agents/SESSIONS/2025-01-15.md
.agents/SESSIONS/2025-01-16.md
```

**WRONG:**

```
.agents/SESSIONS/2025-01-15-feature-name.md
.agents/SESSIONS/2025-01-15-bug-fix.md
```

Multiple sessions on same day go in the same file.

---

### Session Directory Structure

```
.agents/
└── SESSIONS/
    ├── README.md          # Format documentation
    ├── TEMPLATE.md        # Optional template
    ├── 2025-01-15.md      # Date-based files only
    ├── 2025-01-16.md
    └── ...
```

---

## Cross-Session Continuity

### Maintain Context

Each session should be able to understand:

- What the project is
- What was done recently
- What patterns to follow
- What decisions were made

---

### Don't Repeat Mistakes

If a mistake was made and corrected in a previous session:

- The fix should be documented
- Future sessions should reference it
- The same mistake shouldn't happen again

---

## When to Document

### Always Document

- New features implemented
- Bugs fixed
- Architecture decisions
- Pattern changes
- Breaking changes
- Incomplete work

### Skip Documentation For

- Simple questions answered
- No code changes made
- Just exploring/reading code
- Trivial fixes (typos)

---

## Session Memory Best Practices

### For Ongoing Work

When working on something over multiple sessions:

1. Start by reading previous session notes
2. Continue from where you left off
3. Update documentation at the end

---

### For New Work

When starting something new:

1. Search for related past work
2. Note any relevant patterns found
3. Document the new work for future reference
