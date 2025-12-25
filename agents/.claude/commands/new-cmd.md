# New Command - Create Custom Command

Create a new custom command for the project.

## When to Use

- Need a repeatable workflow
- Common task pattern identified
- Team productivity improvement

## Command Structure

Commands are markdown files in .claude/commands/ with:
- Clear purpose statement
- Step-by-step workflow
- Examples and templates
- Related commands

## Creation Steps

### Step 1: Define Purpose

What problem does this command solve?
- What workflow is it automating?
- When should it be used?
- Who will use it?

### Step 2: Design Workflow

Break down into steps:
- What information is needed?
- What actions are taken?
- What is the output?

### Step 3: Create Command File

File location: .claude/commands/[command-name].md

Template:
# Command Name - Brief Description

Purpose statement.

## When to Use
- Scenario 1
- Scenario 2

## Workflow

### Step 1: [Action]
Details...

### Step 2: [Action]
Details...

## Examples
Show usage examples.

## Related Commands
- /related-command

### Step 4: Test Command

Verify the command works:
- Run through workflow
- Check edge cases
- Validate output

## Best Practices

Good commands:
- Solve a real problem
- Are well-documented
- Have clear steps
- Include examples

Bad commands:
- Too complex
- Unclear purpose
- Missing documentation
- No examples
