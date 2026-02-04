# Validate - Unified Validation Command

**Purpose:** Validate documentation structure, session files, tasks, and codebase integrity with a single command

## Usage

```bash
/validate docs      # Validate documentation structure
/validate sessions  # Validate session file naming
/validate tasks     # Validate task files (metadata, PRD links, format)
/validate all       # Run all validation checks
```

## What This Command Does

1. **Documentation Validation** - Checks required files and broken links
2. **Session Validation** - Ensures ONE FILE PER DAY naming convention
3. **Task Validation** - Validates task metadata, status values, PRD links, and format
4. **All Validation** - Runs all checks and reports comprehensive results

---

## Option 1: Validate Documentation

**Purpose:** Validates `.agents/` documentation structure and content

### What This Checks

1. **Checks Required Files** - Ensures all projects have necessary docs
2. **Validates Links** - Finds broken internal references
3. **Checks Formatting** - Validates markdown tables and code blocks
4. **Reports Issues** - Clear output of what needs fixing

### Files to Check

#### Workspace Level

- [ ] `.agents/README.md` exists
- [ ] `.agents/SYSTEM/WORKSPACE-ARCHITECTURE.md` exists
- [ ] `.agents/SYSTEM/critical/CROSS-PROJECT-RULES.md` exists
- [ ] `.agents/SYSTEM/PROJECT-MAP.md` exists
- [ ] `.agents/TASKS/README.md` exists
- [ ] `.agents/SESSIONS/README.md` exists
- [ ] `.agents/SESSIONS/TEMPLATE.md` exists

#### For Each Project (discover from project structure)

- [ ] `[project]/.agents/README.md` exists
- [ ] `[project]/.agents/SYSTEM/ARCHITECTURE.md` exists (if applicable)
- [ ] `[project]/.agents/SYSTEM/RULES.md` exists (if applicable)
- [ ] `[project]/.agents/SYSTEM/SUMMARY.md` exists
- [ ] `[project]/.agents/TASKS/README.md` exists

### Validation Script

Run this check:

```bash
#!/bin/bash

echo "🔍 Validating .agents/ documentation..."
echo ""

ERRORS=0

# Check workspace files
echo "📁 Checking workspace files..."
WORKSPACE_FILES=(
  ".agents/README.md"
  ".agents/SYSTEM/WORKSPACE-ARCHITECTURE.md"
  ".agents/SYSTEM/critical/CROSS-PROJECT-RULES.md"
  ".agents/SYSTEM/PROJECT-MAP.md"
  ".agents/TASKS/README.md"
  ".agents/SESSIONS/README.md"
  ".agents/SESSIONS/TEMPLATE.md"
)

for file in "${WORKSPACE_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "  ❌ Missing: $file"
    ((ERRORS++))
  else
    echo "  ✅ Found: $file"
  fi
done

echo ""

# Check project files
# Detect projects dynamically or use generic placeholder
PROJECTS=("[project-1]" "[project-2]" "[project-3]")

for project in "${PROJECTS[@]}"; do
  echo "📁 Checking $project..."

  # Required files
  if [ ! -f "$project/.agents/README.md" ]; then
    echo "  ❌ Missing: $project/.agents/README.md"
    ((ERRORS++))
  else
    echo "  ✅ Found: README.md"
  fi

  if [ ! -f "$project/.agents/SYSTEM/SUMMARY.md" ]; then
    echo "  ❌ Missing: $project/.agents/SYSTEM/SUMMARY.md"
    ((ERRORS++))
  else
    echo "  ✅ Found: SUMMARY.md"
  fi

  # Optional but recommended
  if [ ! -f "$project/.agents/SYSTEM/ARCHITECTURE.md" ]; then
    echo "  ⚠️  Recommended: $project/.agents/SYSTEM/ARCHITECTURE.md"
  else
    echo "  ✅ Found: ARCHITECTURE.md"
  fi

  if [ ! -f "$project/.agents/TASKS/README.md" ]; then
    echo "  ❌ Missing: $project/.agents/TASKS/README.md"
    ((ERRORS++))
  else
    echo "  ✅ Found: TASKS/README.md"
  fi

  echo ""
done

# Check for broken links (basic)
echo "🔗 Checking for broken internal links..."
echo "  Searching for links to non-existent files..."

# Find all markdown files
find .agent -name "*.md" -type f | while read -r file; do
  # Extract markdown links like [text](path.md)
  grep -oE '\[([^\]]+)\]\(([^)]+)\)' "$file" | sed -E 's/.*\(([^)]+)\).*/\1/' | while read -r link; do
    # Skip external links (http/https)
    if [[ ! "$link" =~ ^https?:// ]]; then
      # Get directory of current file
      dir=$(dirname "$file")
      # Resolve relative path
      target="$dir/$link"

      # Check if target exists
      if [ ! -f "$target" ] && [ ! -d "$target" ]; then
        echo "  ❌ Broken link in $file: $link"
        ((ERRORS++))
      fi
    fi
  done
done

echo ""

# Summary
if [ $ERRORS -eq 0 ]; then
  echo "✅ Documentation validation passed! No errors found."
  exit 0
else
  echo "❌ Documentation validation failed with $ERRORS error(s)."
  echo ""
  echo "💡 Fix the errors above and run again."
  exit 1
fi
```

### What Gets Checked

✅ **File Existence** - All required files present
✅ **Broken Links** - Internal references work
✅ **Structure** - Proper folder organization

### Auto-Fix Suggestions

If errors found, the script suggests:

- Which files to create
- Where to fix broken links
- How to resolve issues

---

## Option 2: Validate Sessions

**Purpose:** Ensure session files follow the ONE FILE PER DAY rule

### What This Checks

1. **Checks all SESSIONS folders** in workspace and projects
2. **Finds violations** - Files NOT following `YYYY-MM-DD.md` format
3. **Auto-consolidates** violations into proper date-based files
4. **Reports results** - Shows what was fixed

### Validation Rules

**✅ ALLOWED filenames:**

- `README.md`
- `TEMPLATE.md`
- `YYYY-MM-DD.md` (e.g., `2025-10-09.md`)

**❌ FORBIDDEN filenames:**

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
# Detect projects dynamically or use generic placeholder
for project in [project-1] [project-2] [project-3]; do
  if [ -d "$project/.agents/SESSIONS" ]; then
    violations+=$(find "$project/.agents/SESSIONS" -type f -name "*.md" \
      ! -name "README.md" \
      ! -name "TEMPLATE.md" \
      ! -regex ".*/[0-9]{4}-[0-9]{2}-[0-9]{2}\.md")
  fi
done

# Report violations
if [ -n "$violations" ]; then
  echo "❌ VIOLATIONS FOUND:"
  echo "$violations"
else
  echo "✅ All session files compliant"
fi
```

#### Step 2: Extract Date from Filename

For each violation, extract the date:

```bash
# Try to extract date from filename
date=$(echo "$filename" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)

# If no date found, use file modification date
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
✅ Session validation complete!

**Fixed violations:**

- Consolidated CODE-AUDIT-2025-10-09.md → 2025-10-09.md
- Consolidated SECURITY-AUDIT-2025-10-09.md → 2025-10-09.md
- Consolidated QUICK-WINS-2025-10-09.md → 2025-10-09.md

**Result:**

- 6 violations fixed
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

### Validation Script

Create `scripts/sh/validate-sessions.sh`:

```bash
#!/bin/bash

echo "🔍 Validating session file structure..."
echo ""

violations=0
fixed=0

# Function to validate sessions in a directory
validate_sessions() {
  local sessions_dir=$1
  local project_name=$2

  echo "📁 Checking: $project_name"

  # Find violations
  bad_files=$(find "$sessions_dir" -type f -name "*.md" \
    ! -name "README.md" \
    ! -name "TEMPLATE.md" \
    ! -regex ".*/[0-9]{4}-[0-9]{2}-[0-9]{2}\.md")

  if [ -n "$bad_files" ]; then
    echo "   ❌ Found violations:"
    echo "$bad_files" | while read file; do
      echo "      - $(basename $file)"
      violations=$((violations + 1))

      # Extract date
      date=$(echo "$file" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
      if [ -z "$date" ]; then
        date=$(date -r "$file" +%Y-%m-%d)
      fi

      # Target file
      target="$sessions_dir/$date.md"

      # Consolidate
      if [ -f "$target" ]; then
        echo "" >> "$target"
        echo "---" >> "$target"
        echo "" >> "$target"
        cat "$file" >> "$target"
        echo "      → Consolidated into $date.md"
      else
        mv "$file" "$target"
        echo "      → Renamed to $date.md"
      fi

      rm -f "$file"
      fixed=$((fixed + 1))
    done
  else
    echo "   ✅ Compliant"
  fi

  echo ""
}

# Validate workspace sessions
if [ -d ".agents/SESSIONS" ]; then
  validate_sessions ".agents/SESSIONS" "Workspace"
fi

# Validate project sessions
# Detect projects dynamically or use generic placeholder
for project in [project-1] [project-2] [project-3]; do
  if [ -d "$project/.agents/SESSIONS" ]; then
    validate_sessions "$project/.agents/SESSIONS" "$project"
  fi
done

# Summary
echo "================================"
if [ $violations -eq 0 ]; then
  echo "✅ PASS: All session files follow YYYY-MM-DD.md format"
  exit 0
else
  echo "✅ FIXED: $fixed violations consolidated"
  echo ""
  echo "All sessions now follow the ONE FILE PER DAY rule"
  exit 0
fi
```

### Example Output

**When violations exist:**

```
🔍 Validating session file structure...

📁 Checking: Workspace
   ❌ Found violations:
      - CODE-AUDIT-2025-10-09.md
      → Consolidated into 2025-10-09.md
      - SECURITY-AUDIT-2025-10-09.md
      → Consolidated into 2025-10-09.md
      - QUICK-WINS-2025-10-09.md
      → Consolidated into 2025-10-09.md

📁 Checking: [project-name]
   ✅ Compliant

================================
✅ FIXED: 3 violations consolidated

All sessions now follow the ONE FILE PER DAY rule
```

**When compliant:**

```
🔍 Validating session file structure...

📁 Checking: Workspace
   ✅ Compliant

📁 Checking: [project-name]
   ✅ Compliant

================================
✅ PASS: All session files follow YYYY-MM-DD.md format
```

---

## Option 3: Validate Tasks

**Purpose:** Validate all task files across workspace for proper format, metadata, and PRD links

### What This Checks

1. **Kanban Markdown Format** - Tasks follow structured metadata format
2. **Required Metadata** - All fields present (ID, Label, Description, Type, Status, Priority, Created, Updated, PRD)
3. **Valid Status Values** - Status matches allowed values (Backlog, To Do, Testing, Done, Not Started, In Progress, Complete, Blocked, Cancelled)
4. **Valid Type Values** - Type matches allowed values (Feature, Bug, Enhancement, Task, Migration, Audit, Planning)
5. **Valid Priority Values** - Priority matches allowed values (High, Medium, Low, CRITICAL)
6. **PRD Links** - PRD link exists and points to valid file
7. **Description Quality** - Description is at least 30 characters

### Validation Script

Run the task validation script:

```bash
node .agents/scripts/validate-tasks.js
```

### What Gets Checked

✅ **Task Format** - Kanban Markdown structure with metadata
✅ **Metadata Completeness** - All required fields present
✅ **Valid Values** - Status, type, and priority match standards
✅ **PRD Links** - Links exist and point to real files
✅ **Description Quality** - Minimum length requirement

### Auto-Fix Script

If validation finds issues, run the auto-fix script:

```bash
node .agents/scripts/fix-tasks.js
```

This will automatically fix:

- Invalid status values (e.g., "Completed" → "Complete")
- Invalid type values (e.g., "Integration" → "Feature")
- Invalid priority values (e.g., "P1-High" → "High")
- Short descriptions (expand to minimum 30 chars)
- Missing PRD fields (add placeholder)
- Create missing PRD files (skeleton)

### Validation Standards

**Valid Status Values:**

- Backlog
- To Do
- Testing
- Done
- Not Started
- In Progress
- Complete
- Blocked
- Cancelled

**Valid Type Values:**

- Feature
- Bug
- Enhancement
- Task
- Migration
- Audit
- Planning

**Valid Priority Values:**

- High
- Medium
- Low
- CRITICAL

**Quality Standards:**

- Minimum 30-character descriptions
- All tasks must have PRD links
- PRD files must exist and be accessible

### Example Output

```
📊 OVERALL STATISTICS

Total Tasks:       227
✅ Valid Tasks:     195 (67.0%)
❌ Invalid Tasks:   32 (14.0%)

⚠️  ISSUES BREAKDOWN

📄 Old Format: 31 tasks
🔗 Missing PRD Field: 1 tasks
```

### Reports

Detailed validation report saved to:

```
.agents/REPORTS/task-validation-YYYY-MM-DD.md
```

---

## Option 4: Validate All

**Purpose:** Run all validation checks and provide comprehensive report

### What This Does

1. Runs documentation validation
2. Then runs session validation
3. Then runs task validation
4. Provides comprehensive summary

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

3. **Task Validation:**
   - Check task format and metadata
   - Validate status/type/priority values
   - Check PRD links
   - Report issues

4. **Comprehensive Report:**
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
  ├─ tasks     → Validate task files (metadata, PRD links, format)
  └─ all       → Run all validation checks
```

## Safety Checks

**Before validation:**

- ✅ Verify directories exist
- ✅ Check read permissions
- ✅ Create backups if auto-fixing

**After validation:**

- ✅ Report all issues found
- ✅ Provide fix suggestions
- ✅ Update session documentation

## Error Handling

**If validation fails:**

- Report specific errors
- Provide fix suggestions
- Offer auto-fix options

**If auto-fix fails:**

- Report which files couldn't be fixed
- Suggest manual intervention
- Provide rollback instructions

**If permissions denied:**

- Report inaccessible files
- Suggest permission fixes

---

**Created:** 2025-11-21
**Purpose:** Unified validation command to consolidate multiple validation checks
**Replaces:** `docs-lint.md`, `validate-sessions.md`
