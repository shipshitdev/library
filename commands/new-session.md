# Create New Session

Quickly create a new session file from template.

## What This Command Does

1. **Creates Session File** - Generates dated session file
2. **Uses Template** - Pre-fills from `.agents/SESSIONS/TEMPLATE.md`
3. **Auto-fills Metadata** - Sets date, project name
4. **Opens in Editor** - Ready to document your work

## Usage

```bash
./scripts/sh/new-session.sh [project-name]
```

### Examples

```bash
./scripts/sh/new-session.sh               # Workspace-level session
./scripts/sh/new-session.sh api           # API project session
./scripts/sh/new-session.sh frontend      # Frontend session
./scripts/sh/new-session.sh extension     # Extension session
```

## Script

```bash
#!/bin/bash

# New Session Script
# Usage: ./scripts/sh/new-session.sh [project-name]

PROJECT=$1
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)

# Determine session file path
if [ -z "$PROJECT" ]; then
  # Workspace-level session
  SESSION_FILE=".agents/SESSIONS/${DATE}.md"
  PROJECT_NAME="Workspace"
else
  # Project-specific session
  SESSION_FILE=".agents/SESSIONS/${DATE}-${PROJECT}.md"
  PROJECT_NAME="$PROJECT"
fi

# Check if template exists
TEMPLATE=".agents/SESSIONS/TEMPLATE.md"
if [ ! -f "$TEMPLATE" ]; then
  echo "❌ Error: Template not found: $TEMPLATE"
  echo ""
  echo "Create the template first:"
  echo "  cp .agents/SESSIONS/TEMPLATE.md $TEMPLATE"
  exit 1
fi

# Check if session file already exists
if [ -f "$SESSION_FILE" ]; then
  echo "⚠️  Session file already exists: $SESSION_FILE"
  echo ""
  echo "Options:"
  echo "  1. Edit existing: code $SESSION_FILE"
  echo "  2. Create with suffix: ./scripts/new-session.sh ${PROJECT}-part2"
  exit 1
fi

echo "📝 Creating new session..."
echo "  Date: $DATE"
echo "  Time: $TIME"
echo "  Project: $PROJECT_NAME"
echo "  File: $SESSION_FILE"
echo ""

# Copy template
cp "$TEMPLATE" "$SESSION_FILE"

# Replace placeholders
sed -i.tmp "s/DATE/$DATE/g" "$SESSION_FILE"
sed -i.tmp "s/PROJECT/$PROJECT_NAME/g" "$SESSION_FILE"
sed -i.tmp "s/HH:MM/$TIME/g" "$SESSION_FILE"

# Clean up temp file
rm "$SESSION_FILE.tmp" 2>/dev/null

echo "✅ Session file created!"
echo ""

# Open in default editor (VS Code if available, otherwise default)
if command -v code &> /dev/null; then
  echo "📂 Opening in VS Code..."
  code "$SESSION_FILE"
elif command -v cursor &> /dev/null; then
  echo "📂 Opening in Cursor..."
  cursor "$SESSION_FILE"
else
  echo "📂 File created at: $SESSION_FILE"
  echo "   Open manually to start documenting"
fi

echo ""
echo "💡 Tips:"
echo "  - Document as you work, not at the end"
echo "  - Include decisions and their reasoning"
echo "  - Note what didn't work (helps future you)"
echo "  - Link to relevant tasks and files"
echo ""
echo "Happy coding! 🚀"
```

## Session File Structure

The generated file will have:

```markdown
# Session - 2025-10-07

**Date:** 2025-10-07
**Project:** api
**Duration:** X hours
**Status:** In Progress

## 🎯 Session Goals

- [ ] Goal 1
- [ ] Goal 2

## ✅ Accomplishments

### Major Changes

1. **Feature Name**
   - Description
   - Files: `path/to/file.ts`

## 🔍 Decisions Made

### Decision 1: [Title]

**Context:** ...
**Decision:** ...
**Impact:** ...

## 📝 Code Changes

### Files Created

- `path/to/file.ts` - Purpose

### Files Modified

- `path/to/file.ts` - Changes

## ⚠️ Issues & Blockers

### Issue 1: [Title]

**Problem:** ...
**Resolution:** ...

## 🔄 Incomplete Work

- [ ] Task 1 - What's left

## 📋 Next Steps

### Immediate

1. Step 1
2. Step 2

## 💡 Learnings & Notes

- Learning 1
- Pattern observed

## 🔗 References

- Related Task: `path/to/task.md`
```

## Best Practices

### During Development

- Open session file at start
- Update as you work (not at end)
- Document decisions in real-time
- Note blockers immediately

### At Session End

- Mark status as "Complete"
- Fill in duration
- Complete all sections
- Add next steps

### Regular Maintenance

- Review old sessions monthly
- Archive sessions older than 3 months
- Extract patterns to SOPs

## Setup

1. Create the script:

```bash
mkdir -p scripts/sh
# Copy the script above to scripts/sh/new-session.sh
chmod +x scripts/sh/new-session.sh
```

1. Make template available:

```bash
# Ensure .agents/SESSIONS/TEMPLATE.md exists
```

1. Run from project root

## Shell Alias (Optional)

Add to your `.zshrc` or `.bashrc`:

```bash
alias session='./scripts/sh/new-session.sh'
```

Then use:

```bash
session api          # Create API session
session              # Create workspace session
```

---

**Pro Tip:** Keep session file open in split pane while coding. Update it as you go!
