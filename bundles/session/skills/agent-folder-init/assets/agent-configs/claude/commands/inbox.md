# Inbox - View Task Inbox

Display current inbox tasks awaiting action.

## Usage

/inbox

## What This Command Does

Reads and displays .agents/TASKS/INBOX.md showing:

1. Human QA tasks - Blocking production
2. Features to prompt - Ready for implementation

## Workflow

### Step 1: Read Inbox

cat .agents/TASKS/INBOX.md

### Step 2: Display by Category

Format output as:

## Human QA (Blocking Production)

Tasks requiring manual testing before production.

## Features to Prompt

Tasks ready for AI implementation.

### Step 3: Show Count

Total tasks: X

- Human QA: X
- Features: X

## Inbox Management

Add to inbox:

- Quick captures go here
- Ideas for later
- Blocked items

Remove from inbox:

- When task is created
- When completed
- When no longer relevant
