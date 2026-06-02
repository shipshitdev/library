# Inbox - View Open Issues Backlog

Display the current GitHub Issues backlog awaiting action.

## Usage

/inbox

## What This Command Does

Fetches open GitHub Issues and displays them grouped by label/priority so you can see what needs attention.

## Workflow

### Step 1: List Open Issues

```bash
gh issue list --state open --limit 50
```

### Step 2: Display by Category

Format output as:

## High Priority / Blocking

Issues labeled `priority:high` or `blocking`.

## In Progress

Issues currently being worked on (labeled `in-progress` or assigned).

## Backlog

Remaining open issues ready for implementation.

### Step 3: Show Count

Total open: X

- High priority: X
- In progress: X
- Backlog: X

## Issue Management

Add to backlog:

```bash
gh issue create --title "Short description" --body "Details..." --label "backlog"
```

Close an issue:

```bash
gh issue close <number>
```

View a specific issue:

```bash
gh issue view <number>
```
