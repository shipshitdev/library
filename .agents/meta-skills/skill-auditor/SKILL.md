---
name: skill-auditor
description: |
  Audit the skills library for duplicates, stale content, spec violations, and structural issues.
  Run periodically or before releases.
metadata:
  version: "1.0.0"
  tags: "audit, skills, quality, maintenance"
---

# Skill Auditor

Comprehensive audit of the skills library for quality and consistency.

## Audit Categories

### 1. Duplicate Detection

Find skills that overlap and should be consolidated:

- Compare descriptions for semantic similarity
- Check for skills with near-identical `when_to_use` triggers
- Flag naming collisions (e.g., `copywriter` vs `copywriting`)

### 2. Spec Compliance

For each SKILL.md, check:

- Frontmatter follows Agent Skills spec (see `.agents/SYSTEM/SKILL-STANDARDS.md`)
- `version`/`tags` inside `metadata:` block, not top-level
- No forbidden fields (`auto_activate`, `auto_trigger`, `risk`)
- `metadata.tags` is a comma-separated string, not YAML list

### 3. Structural Issues

- Orphaned nested directories (`skills/<name>/<name>/`)
- Empty skill directories (no SKILL.md)
- Skills in README that no longer exist in filesystem
- Skills in filesystem that are missing from README
- Broken references to non-existent files in skill content

### 4. Content Quality

- Empty or placeholder descriptions
- Hardcoded project-specific paths (`/workspace/`, `@genfeedai/`)
- Escaped backtick fences (`\`\`\``) instead of real fences
- Skills that reference scripts not bundled with the skill

### 5. README Sync

Compare `skills/` directory listing against README.md skills table:

```bash
# Get skills from filesystem
find skills -maxdepth 1 -mindepth 1 -type d | sed 's|skills/||' | sort > /tmp/fs-skills.txt

# Get skills from README table
grep -oE '\[([a-z0-9-]+)\]\(https://skills\.sh' README.md | sed 's/\[//' | sed 's/\](https:\/\/skills\.sh//' | sort > /tmp/readme-skills.txt

# Diff
comm -23 /tmp/fs-skills.txt /tmp/readme-skills.txt  # in fs, not README
comm -13 /tmp/fs-skills.txt /tmp/readme-skills.txt  # in README, not fs
```

## Output Format

Report findings as a table:

| Skill | Issue | Severity | Action |
|-------|-------|----------|--------|
| `code-refactoring-refactor-clean` | Duplicate of `refactor-code` | HIGH | Merge |
| `spec-to-code-compliance` | Empty directory | HIGH | Delete |
| `skill-capture` | tags as YAML list | MEDIUM | Fix to string |
