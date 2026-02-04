# Clean - Unified Cleanup Command

**Purpose:** Clean up completed tasks, session files, and documentation with a single command

## Usage

```bash
/clean tasks      # Clean completed task files
/clean sessions   # Merge and consolidate session files
/clean all        # Run all cleanup operations
```

## What This Command Does

1. **Task Cleanup** - Removes completed task files while keeping structure
2. **Session Cleanup** - Merges daily → monthly → yearly sessions
3. **All Cleanup** - Runs both operations in sequence

---

## Option 1: Clean Tasks

**Purpose:** Clean up completed task files by removing their content (keep files, empty content)

### What This Does

1. **Finds completed tasks** - Tasks where all checkboxes are checked `[x]`
2. **Empties file content** - Replaces content with minimal "Completed" marker
3. **Keeps file structure** - Files remain, just emptied
4. **Logs cleanup** - Records what was cleaned in session file

### Philosophy

- ✅ Keep file names (shows what was worked on)
- ✅ Empty content (remove bloat)
- ✅ MD files are the roadmap (source of truth)
- ✅ Lean .agent folder (fast for AI to read)

### Process

#### 1. Find Fully Completed Tasks

Search for task files where:

- All checkboxes are checked `[x]`
- OR file has "Status: Complete"
- In folders: api/, frontend/, general/, docs/, extension/, mobile/

#### 2. Empty Completed Files

For each completed task, replace content with:

```markdown
# [Original Task Name]

**Status:** ✅ Completed
**Completed:** [Date]

This task has been completed and is tracked in the roadmap (MD files).

See `.agents/SESSIONS/[date].md` for implementation details.
```

#### 3. Update Session Log

Add to `.agents/SESSIONS/[today].md`:

```markdown
## Cleaned Completed Tasks

**Emptied:**

- api/queue-migration-tasks.md
- frontend/video-generation-with-captions.md

**Reason:** Tasks completed and tracked in roadmap (MD files). Content removed to keep .agent lean.
```

### Manual Checklist for AI Agent

When user runs `/clean tasks`:

- [ ] Search all task files for completed checklists (all `[x]`)
- [ ] List found tasks for user confirmation
- [ ] For each confirmed task:
  - [ ] Get task name from file
  - [ ] Replace content with minimal completion marker
  - [ ] Keep filename unchanged
- [ ] Update `.agents/SESSIONS/[today].md` with cleaned files
- [ ] Report cleanup summary

### Example

**Before (queue-migration-tasks.md):**

```markdown
# Task: Complete BullMQ Queue Migration

**Status:** Complete
...
[300 lines of detailed prompt and specs]
```

**After (queue-migration-tasks.md):**

```markdown
# Task: Complete BullMQ Queue Migration

**Status:** ✅ Completed
**Completed:** 2025-10-07

This task has been completed and is tracked in the roadmap (MD files).

See `.agents/SESSIONS/2025-10-07.md` for implementation details.
```

**Result:** File exists (shows what was done), but content is minimal (no bloat).

---

## Option 2: Clean Sessions

**Purpose:** Merge daily sessions into monthly sessions and monthly sessions into yearly reviews

### What This Does

1. **Daily → Monthly:** Consolidates daily sessions (YYYY-MM-DD.md) into monthly files (YYYY-MM.md)

   - Triggers when current day > 1 (processes current month)
   - Only processes sessions from the current month

2. **Monthly → Yearly:** Consolidates monthly sessions (YYYY-MM.md) into yearly reviews (YYYY-yearly-review.md)
   - Processes sessions from previous years
   - Creates comprehensive yearly review files

### Safety Features

- **Backup Creation:** Creates compressed backups before making changes
- **Dry Run Mode:** Preview what would be done without modifying files
- **Preserves System Files:** Keeps README.md and TEMPLATE.md files intact
- **Rollback Support:** Backups can be restored if needed

### Examples

#### Preview Changes

```bash
./scripts/sh/sessions-clean.sh --dry-run
```

#### Run Cleanup

```bash
./scripts/sh/sessions-clean.sh
```

#### Restore from Backup

```bash
tar -xzf .agents/SESSIONS/backups/[backup-file] -C .
```

### File Structure After Cleanup

**Before:**

```
.agents/SESSIONS/
├── 2025-10-07.md
├── 2025-10-08.md
├── 2025-10-09.md
└── ...
```

**After (Daily → Monthly):**

```
.agents/SESSIONS/
├── 2025-10.md          # Consolidated monthly file
└── 2025-yearly-review.md  # If monthly files exist from previous year
```

### AI Agent Process

When user runs `/clean sessions`:

1. **Check Current Date:** Determine if cleanup should run
2. **Create Backups:** Compress existing sessions for safety
3. **Merge Daily Sessions:** Consolidate current month's daily files
4. **Merge Monthly Sessions:** Consolidate previous year's monthly files
5. **Report Results:** Show what was consolidated

### Triggers

- **Daily → Monthly:** Runs when current day > 1 (processes current month)
- **Monthly → Yearly:** Runs for any previous year's monthly files

### Output

The script provides colored output:

- 🔵 **Info:** What's being processed
- ✅ **Success:** Completed operations
- ⚠️ **Warning:** Dry run mode or non-critical issues
- ❌ **Error:** Critical problems

### Backup Location

Backups are stored in: `.agents/SESSIONS/backups/`

Format: `[project-name]-backup-YYYYMMDD-HHMMSS.tar.gz`

---

## Option 3: Clean All

**Purpose:** Run all cleanup operations in sequence

### What This Does

1. Runs task cleanup first
2. Then runs session cleanup
3. Provides comprehensive summary

### Process

When user runs `/clean all`:

1. **Task Cleanup:**

   - Find and empty completed tasks
   - Log to session file

2. **Session Cleanup:**

   - Create backups
   - Merge daily sessions to monthly
   - Merge monthly sessions to yearly

3. **Summary Report:**
   - Tasks cleaned count
   - Sessions consolidated count
   - Backup locations
   - Total space saved

---

## Command Flow

```
/clean
  ├─ tasks      → Clean completed task files
  ├─ sessions   → Merge and consolidate sessions
  └─ all        → Run both operations
```

## Safety Checks

**Before cleaning:**

- ✅ Verify files exist and are accessible
- ✅ Create backups (sessions only)
- ✅ User confirmation for destructive operations

**After cleaning:**

- ✅ Verify operations completed successfully
- ✅ Generate summary report
- ✅ Update session documentation

## Error Handling

**If no completed tasks found:**

- Inform user no tasks need cleaning
- Suggest checking task completion status

**If session cleanup fails:**

- Restore from backup automatically
- Report specific error
- Suggest manual intervention if needed

**If permissions denied:**

- Report which files cannot be accessed
- Suggest checking file permissions

---

**Created:** 2025-11-21
**Purpose:** Unified cleanup command to consolidate multiple cleanup operations
**Replaces:** `docs-clean.md`, `sessions-clean.md`, `tasks-clean.md`
