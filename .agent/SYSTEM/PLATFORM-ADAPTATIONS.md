# Platform-Specific Adaptations Guide

This document details the specific conventions, patterns, and adaptations needed when creating skills for Claude vs Codex platforms.

## Frontmatter Differences

### Claude Frontmatter

```yaml
---
name: skill-name
description: Comprehensive description of what the skill does and when to use it. This skill should be used when...
license: Complete terms in LICENSE.txt
---
```

**Required fields:**

- `name`: Skill name (lowercase, hyphenated)
- `description`: Comprehensive description with triggering information

**Optional fields:**

- `license`: Reference to license file

### Codex Frontmatter

```yaml
---
name: skill-name
description: Comprehensive description of what the skill does and when to use it. This skill should be used when...
metadata:
  short-description: Brief description
---
```

**Required fields:**

- `name`: Skill name (lowercase, hyphenated)
- `description`: Comprehensive description with triggering information

**Optional fields:**

- `metadata.short-description`: Brief description for UI display

**Note**: Codex does NOT use `license` field in frontmatter.

## Writing Style Conventions

### Claude Writing Style

**Use third-person instructional language:**

```markdown
**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when Claude will use the skill. Be specific about what the skill does and when to use it. Use the third-person (e.g. "This skill should be used when..." instead of "Use this skill when...").

This skill activates automatically when you're:
- Creating or reviewing UI components
- Implementing interactive elements
```

**Characteristics:**

- Third-person perspective ("Claude will use", "This skill activates")
- Descriptive and explanatory
- Can be more verbose when clarity is needed
- Uses "should be used when" patterns

### Codex Writing Style

**Use imperative/infinitive form (verb-first instructions):**

```markdown
Extract text with pdfplumber:
[code example]

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

For simple edits, modify the XML directly.
```

**Characteristics:**

- Imperative/infinitive form ("To accomplish X, do Y")
- Direct, action-oriented
- Concise and to-the-point
- Avoids unnecessary explanations

**Example transformation:**

| Claude Style | Codex Style |
|-------------|-------------|
| "This skill should be used when you need to..." | "Use when you need to..." |
| "Claude will use the skill to..." | "To accomplish X, do Y" |
| "The skill activates automatically when..." | "Activates when..." |

## Platform-Specific Principles

### Codex: "Concise is Key"

Codex emphasizes extreme brevity and token efficiency:

```markdown
## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Codex needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Codex is already very smart.** Only add context Codex doesn't already have. Challenge each piece of information: "Does Codex really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.
```

**When to include**: Add this section to Codex skills that would benefit from brevity guidance, especially skills that might become verbose.

### Codex: "Degrees of Freedom"

Codex uses a freedom-based approach to instruction specificity:

```markdown
### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Codex as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).
```

**When to include**: Add to skills that involve scripting, automation, or procedural tasks where freedom level matters.

### Claude: Progressive Disclosure

Claude has progressive disclosure but is less strict:

```markdown
### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited*)

*Unlimited because scripts can be executed without reading into context window.
```

**Codex version** is more strict:

```markdown
### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Codex (Unlimited because scripts can be executed without reading into context window)

Keep SKILL.md body to the essentials and under 500 lines to minimize context bloat. Split content into separate files when approaching this limit.
```

## Platform References

### Correct Platform References

**Claude skills should say:**

- "extends Claude's capabilities"
- "Claude will use the skill"
- "Claude determines"
- "Claude reads"
- "for Claude to use"

**Codex skills should say:**

- "extends Codex's capabilities"
- "Codex reads"
- "Codex determines"
- "Codex needs"
- "for Codex to use"

### Common Mistakes

❌ **Wrong**: Codex skill saying "Claude will use"
✅ **Right**: Codex skill saying "Codex reads"

❌ **Wrong**: Claude skill saying "Codex determines"
✅ **Right**: Claude skill saying "Claude will use"

## Path References

### Skill Paths

**Claude**: `~/.claude/skills/`
**Codex**: `~/.codex/skills/`

When referencing skill paths in instructions, use the correct platform path.

### Example

**Claude version:**

```markdown
```bash
python3 ~/.claude/skills/project-scaffold/scripts/scaffold.py
```

```

**Codex version:**
```markdown
```bash
python3 ~/.codex/skills/project-scaffold/scripts/scaffold.py
```

```

## Progressive Disclosure Patterns

### Codex: More Aggressive Splitting

Codex skills should split content more aggressively:

```markdown
## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

**Key differences:**

- Keep SKILL.md under 500 lines
- Move detailed content to references/ early
- Use links extensively
- Prefer examples over explanations

### Claude: More Inline Content

Claude skills can include more detail:

```markdown
## Form Filling

Use pdfplumber for form filling. Here's how:

1. Load the PDF
2. Extract form fields
3. Fill values
4. Save

[Detailed code example here]

For more advanced patterns, see [FORMS.md](FORMS.md).
```

**Key differences:**

- Can include more detail in SKILL.md
- Less aggressive about splitting
- Can explain more context inline

## Platform Markers

Use HTML comments to mark platform-specific sections:

```markdown
<!-- PLATFORM-SPECIFIC-START: codex -->
## Core Principles

### Concise is Key
The context window is a public good...
<!-- PLATFORM-SPECIFIC-END: codex -->

## Shared Content

This content is identical for both platforms.

<!-- PLATFORM-SPECIFIC-START: claude -->
**Note**: Claude will automatically load this skill when...
<!-- PLATFORM-SPECIFIC-END: claude -->
```

**Benefits:**

- Sync tools can preserve platform-specific sections
- Clear documentation of differences
- Easier maintenance

## Adaptation Checklist

When adapting a skill from one platform to another:

### Frontmatter

- [ ] Update platform name in description if needed
- [ ] Add/remove `metadata.short-description` (Codex only)
- [ ] Add/remove `license` field (Claude only)
- [ ] Keep `name` and core `description` identical

### Content

- [ ] Update all platform references ("Claude" ↔ "Codex")
- [ ] Adapt writing style (third-person ↔ imperative)
- [ ] Add/remove platform-specific principles sections
- [ ] Adjust progressive disclosure emphasis
- [ ] Update path references if present

### Structure

- [ ] Keep core functionality identical
- [ ] Keep scripts and assets identical (unless platform-specific)
- [ ] Keep references identical (unless platform-specific)
- [ ] Mark platform-specific sections with comments

## Examples

### Example 1: Skill Creator Frontmatter

**Claude:**

```yaml
---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---
```

**Codex:**

```yaml
---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Codex's capabilities with specialized knowledge, workflows, or tool integrations.
metadata:
  short-description: Create or update a skill
---
```

### Example 2: Writing Style

**Claude:**

```markdown
**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when Claude will use the skill. Be specific about what the skill does and when to use it.
```

**Codex:**

```markdown
Every SKILL.md consists of:

- **Frontmatter** (YAML): Contains `name` and `description` fields. These are the only fields that Codex reads to determine when the skill gets used, thus it is very important to be clear and comprehensive in describing what the skill is, and when it should be used.
```

### Example 3: Platform-Specific Section

**Codex only:**

```markdown
<!-- PLATFORM-SPECIFIC-START: codex -->
## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Codex needs...

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability...
<!-- PLATFORM-SPECIFIC-END: codex -->
```

## Quick Reference

| Aspect | Claude | Codex |
|--------|--------|-------|
| **Writing Style** | Third-person | Imperative/infinitive |
| **Frontmatter** | `license` field | `metadata.short-description` |
| **Brevity** | Can be verbose | Must be concise |
| **Progressive Disclosure** | Flexible | Strict (<500 lines) |
| **Platform Name** | "Claude" | "Codex" |
| **Principles** | Standard | "Concise is Key", "Degrees of Freedom" |

## Questions?

Refer to:

- [SKILL-MANAGEMENT.md](SKILL-MANAGEMENT.md) for workflow guidelines
- Existing skills for examples
- Validation script for consistency checks
