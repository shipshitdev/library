---
name: readme-sync
description: |
  Regenerate the README.md skills table from the filesystem.
  Run after adding, removing, or renaming skills.
metadata:
  version: "1.0.0"
  tags: "readme, sync, maintenance, automation"
---

# README Sync

Regenerate the README.md skills table from the actual `skills/` directory.

## When to Run

- After adding new skills
- After removing or renaming skills
- After importing skills from external repos
- When README skill count doesn't match filesystem

## Process

### 1. Generate Table Rows

```bash
find skills -maxdepth 1 -mindepth 1 -type d | sed 's|skills/||' | sort | while read skill; do
  desc=$(grep -m1 "^description:" "skills/$skill/SKILL.md" 2>/dev/null | sed 's/^description: *//' | tr -d '"' | head -c 75)
  echo "| [$skill](https://skills.sh/shipshitdev/skills/$skill) | $desc | \`npx skills add shipshitdev/skills --skill $skill\` |"
done
```

### 2. Update README

Replace the skills table in README.md between `## Skills` and the next `##` heading.

### 3. Update Counts

- Header tagline: "250+ AI agent skills" → update to match
- Directory structure: "(252 skills)" → update to actual count

### 4. Validate

```bash
bunx markdownlint-cli README.md
```

## Edge Cases

- Skills with multiline YAML descriptions need the awk-based extractor
- Skills with special characters in descriptions (em dashes, backticks) need escaping
- Some descriptions start with "When the user wants..." — these are trigger phrases, consider rewriting for the table
