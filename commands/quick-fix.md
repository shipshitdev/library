# Quick Fix - Daily Task List

**Purpose:** Create a simple daily task list in markdown format for personal productivity tracking.

## What This Command Does

1. **Creates Daily Task File** - Generates a simple markdown task list for today
2. **Manual Task Entry** - You add your own tasks to the list
3. **Simple Format** - Clean, readable markdown format
4. **Daily Focus** - One file per day for task tracking
5. **No Automation** - You control what goes on the list

## Usage

```bash
# Create today's task list
/quick-fix

# Create for specific date
/quick-fix --date="2025-01-16"
```

## Workflow Steps

### Step 1: Create Daily Task File

**AI Actions:**

1. **Generate today's date:**

```bash
DATE=$(date +%Y-%m-%d)
```

1. **Create task file:**

```bash
TASK_FILE=".agents/SESSIONS/${DATE}-tasks.md"
```

1. **Use simple template:**

```markdown
# Daily Tasks - 2025-01-15

**Date:** 2025-01-15
**Status:** Planning
**Focus:** Today's priorities

## 🎯 Today's Tasks

### High Priority

- [ ] Task 1
- [ ] Task 2

### Medium Priority

- [ ] Task 3
- [ ] Task 4

### Low Priority

- [ ] Task 5

## 📝 Notes

- Add your own tasks here
- Check off as you complete them
- Move incomplete tasks to tomorrow

## ✅ Completed

- [x] Task completed earlier

---

**Tomorrow's Preview:** Move any incomplete tasks here
```

### Step 2: Present to User

**AI Actions:**

1. **Show the created task file**
2. **Explain how to add tasks**
3. **Open file for editing**
4. **Let user add their own tasks**

## File Output

**Location:** `.agents/SESSIONS/YYYY-MM-DD-tasks.md`

**Structure:**

- Simple daily task list
- Manual task entry
- Priority sections
- Notes section
- Completed tasks tracking

## Example Output

```markdown
# Daily Tasks - 2025-01-15

**Date:** 2025-01-15
**Status:** Planning
**Focus:** Studio video features

## 🎯 Today's Tasks

### High Priority

- [ ] Studio/videos: check if producing the video with a reference will use the reference as a placeholder
- [ ] Add settings for video, images and articles
- [ ] Fix video generation

### Medium Priority

- [ ] Review PR #123
- [ ] Update documentation

### Low Priority

- [ ] Clean up old files
- [ ] Plan next week

## 📝 Notes

- Focus on video generation fixes
- Test with different reference types
- Check performance impact

## ✅ Completed

- [x] Fixed login bug
- [x] Updated API docs

---

**Tomorrow's Preview:** Move any incomplete tasks here
```

## Integration with Other Commands

### With Session Management

- Links to daily session file
- Tracks task completion
- Documents progress

### With Task Management

- References original task files
- Updates task status
- Links to PRDs

## Best Practices

### Daily Planning

- Run `/quick-fix` at start of day
- Add your specific tasks
- Set realistic priorities
- Review at end of day

### Task Management

- Use descriptive task names
- Group related tasks
- Set clear priorities
- Track time estimates

### Weekly Review

- Review completed tasks
- Move incomplete tasks
- Plan next week
- Adjust priorities

## Examples

### Example 1: Studio Focus

```markdown
## 🎯 Today's Tasks

### High Priority

- [ ] Studio/videos: check if producing the video with a reference will use the reference as a placeholder
- [ ] Add settings for video, images and articles
- [ ] Fix video generation

### Medium Priority

- [ ] Test video generation with different references
- [ ] Update video generation documentation
```

### Example 2: API Focus

```markdown
## 🎯 Today's Tasks

### High Priority

- [ ] Fix API authentication bug
- [ ] Add video generation endpoint
- [ ] Update API documentation

### Medium Priority

- [ ] Add API rate limiting
- [ ] Test API performance
```

### Example 3: Mixed Focus

```markdown
## 🎯 Today's Tasks

### High Priority

- [ ] Fix video generation
- [ ] Update dashboard analytics
- [ ] Review PR #123

### Medium Priority

- [ ] Add new settings page
- [ ] Test mobile responsiveness
```

## Troubleshooting

### File Not Created

- Check `.agents/SESSIONS/` directory exists
- Verify write permissions
- Check date format

### Template Issues

- Ensure template is simple
- Check markdown formatting
- Verify file structure

### Task Management

- Use clear task descriptions
- Set realistic priorities
- Track completion status

---

**Created:** 2025-01-15
**Purpose:** Simple daily task list for personal productivity
**Integration:** Works with session management and task tracking
