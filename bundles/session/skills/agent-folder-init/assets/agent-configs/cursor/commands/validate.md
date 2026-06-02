# Validate - Unified Validation Command

**Purpose:** Validate documentation structure, session files, and codebase integrity with a single command

## Usage

```bash
/validate docs      # Validate documentation structure
/validate sessions  # Validate session file naming
/validate all       # Run all validation checks
```

## What This Command Does

1. **Documentation Validation** - Checks required files and broken links
2. **Session Validation** - Ensures ONE FILE PER DAY naming convention
3. **All Validation** - Runs all checks and reports comprehensive results

---

## Option 1: Validate Documentation

**Purpose:** Validates `.agents/` documentation structure and content

### What This Checks

1. **Checks Required Files** - Ensures the lean canonical structure is present
2. **Validates Links** - Finds broken internal references
3. **Checks Formatting** - Validates markdown tables and code blocks
4. **Reports Issues** - Clear output of what needs fixing

### Files to Check

#### Workspace Level

- [ ] `.agents/README.md` exists
- [ ] `.agents/memory/` directory exists
- [ ] `.agents/SESSIONS/` directory exists

#### Per-Project (if monorepo)

- [ ] `[project]/.agents/README.md` exists (if project has its own `.agents/`)
- [ ] `[project]/.agents/memory/` exists

### Validation Script

Run this check:

```bash
#!/bin/bash

echo "Validating .agents/ documentation..."
echo ""

ERRORS=0

# Check workspace files
echo "Checking workspace files..."
WORKSPACE_FILES=(
  ".agents/README.md"
  ".agents/memory"
  ".agents/SESSIONS"
)

for file in "${WORKSPACE_FILES[@]}"; do
  if [ ! -e "$file" ]; then
    echo "  Missing: $file"
    ((ERRORS++))
  else
    echo "  Found: $file"
  fi
done

echo ""

# Check for broken links (basic)
echo "Checking for broken internal links..."

find .agents -name "*.md" -type f | while read -r file; do
  grep -oE '\[([^\]]+)\]\(([^)]+)\)' "$file" | sed -E 's/.*\(([^)]+)\).*/\1/' | while read -r link; do
    if [[ ! "$link" =~ ^https?:// ]]; then
      dir=$(dirname "$file")
      target="$dir/$link"
      if [ ! -f "$target" ] && [ ! -d "$target" ]; then
        echo "  Broken link in $file: $link"
        ((ERRORS++))
      fi
    fi
  done
done

echo ""

if [ $ERRORS -eq 0 ]; then
  echo "Documentation validation passed! No errors found."
  exit 0
else
  echo "Documentation validation failed with $ERRORS error(s)."
  echo ""
  echo "Fix the errors above and run again."
  exit 1
fi
```

### What Gets Checked

- **File Existence** — Required files present
- **Broken Links** — Internal references work
- **Structure** — Lean canonical folder organization

---

## Option 2: Validate Sessions

**Purpose:** Ensure session files follow the ONE FILE PER DAY rule

### What This Checks

1. **Checks all SESSIONS folders** in workspace and projects
2. **Finds violations** - Files NOT following `YYYY-MM-DD.md` format
3. **Auto-consolidates** violations into proper date-based files
4. **Reports results** - Shows what was fixed

### Validation Rules

**Allowed filenames:**

- `README.md`
- `TEMPLATE.md`
- `YYYY-MM-DD.md` (e.g., `2025-10-09.md`)

**Forbidden filenames:**

- `2025-10-09-feature-name.md`
- `SECURITY-AUDIT-2025-10-09.md`
- `CODE-AUDIT-*.md`
- `FEATURE-*.md`
- Any descriptive names

### AI Agent Process

When user runs `/validate sessions`:

#### Step 1: Check for Violations

```bash
# Check workspace sessions
violations=$(find .agents/SESSIONS -type f -name "*.md" \
  ! -name "README.md" \
  ! -name "TEMPLATE.md" \
  ! -regex ".*/[0-9]{4}-[0-9]{2}-[0-9]{2}\.md")

# Check all project sessions
for project in [project-1] [project-2] [project-3]; do
  if [ -d "$project/.agents/SESSIONS" ]; then
    violations+=$(find "$project/.agents/SESSIONS" -type f -name "*.md" \
      ! -name "README.md" \
      ! -name "TEMPLATE.md" \
      ! -regex ".*/[0-9]{4}-[0-9]{2}-[0-9]{2}\.md")
  fi
done

if [ -n "$violations" ]; then
  echo "VIOLATIONS FOUND:"
  echo "$violations"
else
  echo "All session files compliant"
fi
```

#### Step 2: Extract Date from Filename

For each violation, extract the date:

```bash
date=$(echo "$filename" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)

if [ -z "$date" ]; then
  date=$(date -r "$filename" +%Y-%m-%d)
fi
```

#### Step 3: Consolidate Violations

For each violation:

1. **Read the file content**
2. **Determine target file:** `YYYY-MM-DD.md` (extracted date)
3. **If target exists:** Append violation content to it
4. **If target doesn't exist:** Rename violation to proper name
5. **Delete violation file**

**Example:**

```bash
# Violation: .agents/SESSIONS/CODE-AUDIT-2025-10-09.md
# Date extracted: 2025-10-09
# Target file: .agents/SESSIONS/2025-10-09.md

# If 2025-10-09.md exists:
cat CODE-AUDIT-2025-10-09.md >> 2025-10-09.md
rm CODE-AUDIT-2025-10-09.md

# If 2025-10-09.md doesn't exist:
mv CODE-AUDIT-2025-10-09.md 2025-10-09.md
```

#### Step 4: Update Session Numbers

If consolidating into existing file:

1. **Count existing sessions** in target file
2. **Increment session number** for new content
3. **Update total sessions count** at bottom

#### Step 5: Report Results

```markdown
Session validation complete!

**Fixed violations:**

- Consolidated CODE-AUDIT-2025-10-09.md → 2025-10-09.md
- Consolidated SECURITY-AUDIT-2025-10-09.md → 2025-10-09.md

**Result:**

- 2 violations fixed
- All sessions now follow YYYY-MM-DD.md format
```

### Manual Checklist for AI Agent

- [ ] Check all SESSIONS folders (workspace + all projects)
- [ ] Find files NOT matching: README.md, TEMPLATE.md, or YYYY-MM-DD.md
- [ ] For each violation:
  - [ ] Extract date from filename or use file date
  - [ ] Check if proper date file exists
  - [ ] Consolidate content into proper file
  - [ ] Delete violation file
- [ ] Update session numbers if consolidating
- [ ] Report results to user

---

## Option 3: Validate All

**Purpose:** Run all validation checks and provide comprehensive report

### What This Does

1. Runs documentation validation
2. Then runs session validation
3. Provides comprehensive summary

### Process

When user runs `/validate all`:

1. **Documentation Validation:**
   - Check required files
   - Validate links
   - Check formatting

2. **Session Validation:**
   - Check naming conventions
   - Auto-fix violations
   - Report fixes

3. **Comprehensive Report:**
   - Total errors found
   - Total violations fixed
   - Recommendations
   - Next steps

---

## Command Flow

```
/validate
  ├─ docs      → Validate documentation structure
  ├─ sessions  → Validate session file naming
  └─ all       → Run all validation checks
```

## Safety Checks

**Before validation:**

- Verify directories exist
- Check read permissions
- Create backups if auto-fixing

**After validation:**

- Report all issues found
- Provide fix suggestions

## Error Handling

**If validation fails:**

- Report specific errors
- Provide fix suggestions
- Offer auto-fix options

**If auto-fix fails:**

- Report which files couldn't be fixed
- Suggest manual intervention

---

**Created:** 2025-11-21
**Updated:** 2026-06-02 — removed task/PRD validation (tasks live in GitHub Issues now)
**Purpose:** Unified validation command for docs and session structure
