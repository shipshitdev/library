# Skill Replication Management Guidelines

This document provides guidelines for managing skills that are replicated across Claude and Codex platforms.

## Core Principle

**Most skills should be functionally identical across platforms, with only platform-specific adaptations where necessary.**

## When Skills Should Be Identical

Skills should be **identical** (or nearly identical) when they contain:

- **Domain expertise** (accessibility, security, testing, API design, etc.)
- **Workflows and procedures** (step-by-step instructions)
- **Scripts and assets** (executable code, templates, resources)
- **Reference documentation** (detailed guides, schemas, examples)
- **Core functionality** (what the skill does, not how it's presented)

**Rule**: If the skill content doesn't reference platform-specific behavior, capabilities, or principles, it should be identical across platforms.

### Examples of Identical Content

- Accessibility guidelines and WCAG compliance rules
- Security best practices and OWASP recommendations
- Testing strategies and patterns
- API design principles
- Database migration procedures
- Component library standards

## When Skills Should Differ

Skills should have **platform-specific adaptations** when they involve:

### 1. Platform-Specific Principles

**Codex-specific principles** that don't apply to Claude:

- **"Concise is Key"** - Codex emphasizes extreme brevity and token efficiency
- **"Degrees of Freedom"** - Codex uses high/medium/low freedom patterns
- **Progressive disclosure** - Codex has stricter requirements for context management

**Action**: Add Codex-specific sections only when these principles meaningfully change the skill's approach.

### 2. Metadata Differences

**Codex supports additional frontmatter fields:**

```yaml
metadata:
  short-description: Brief description
```

**Claude uses:**

```yaml
license: Complete terms in LICENSE.txt
```

**Action**: Use platform-appropriate frontmatter fields. Keep `name` and `description` identical.

### 3. Platform References

Skills should reference the correct platform:

- Codex skills: "extends Codex's capabilities", "Codex reads", "Codex determines"
- Claude skills: "extends Claude's capabilities", "Claude will use", "Claude determines"

**Action**: Always use the correct platform name. Never reference the wrong platform.

### 4. Writing Style Guidance

**Codex**: Use imperative/infinitive form (verb-first instructions)

- "To accomplish X, do Y"
- "Extract text with pdfplumber"
- "Use docx-js for new documents"

**Claude**: Use third-person instructional language

- "This skill should be used when..."
- "Claude will use the skill when..."
- "The skill activates automatically when..."

**Action**: Adapt writing style to match platform conventions, but keep core instructions identical.

### 5. Context Window Management

**Codex** has stricter progressive disclosure requirements:

- Emphasizes keeping SKILL.md under 500 lines
- More aggressive about moving content to references/
- Stronger emphasis on token efficiency

**Claude** is more flexible:

- Can include more detail in SKILL.md
- Less strict about progressive disclosure

**Action**: Codex versions should be more concise, but core content should remain the same.

## Update Workflow

### Standard Workflow

1. **Create/Update Skill**: Start with one platform (usually Claude)
2. **Identify Platform-Specific Needs**: Review content for platform-specific adaptations
3. **Sync Core Content**: Use sync tool or copy core content to other platform
4. **Apply Platform Adaptations**: Make platform-specific changes
5. **Validate**: Run validation script to check consistency
6. **Test**: Verify skill works on both platforms

### Using Platform Markers

For skills with platform-specific sections, use markers:

```markdown
<!-- PLATFORM-SPECIFIC-START: codex -->
## Core Principles

### Concise is Key
The context window is a public good...
<!-- PLATFORM-SPECIFIC-END: codex -->

<!-- Shared content here - identical for both platforms -->

<!-- PLATFORM-SPECIFIC-START: claude -->
**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when Claude will use the skill.
<!-- PLATFORM-SPECIFIC-END: claude -->
```

### Sync Tool Usage

Use `scripts/sync-skill.sh` to:

- Sync core content from source to target platform
- Preserve platform-specific sections (marked with comments)
- Update platform references automatically
- Validate changes before applying

```bash
# Sync from Claude to Codex
./scripts/sync-skill.sh accessibility claude codex

# Dry run to preview changes
./scripts/sync-skill.sh accessibility claude codex --dry-run
```

## Validation Checklist

Before considering a skill "synced", verify:

- [ ] Platform references are correct (Codex vs Claude)
- [ ] Frontmatter uses platform-appropriate fields
- [ ] Writing style matches platform conventions
- [ ] Core functionality is identical
- [ ] Platform-specific principles are properly applied
- [ ] Scripts and assets are identical (unless platform-specific)
- [ ] References are identical (unless platform-specific)

## Common Mistakes to Avoid

1. **Copy-paste errors**: Forgetting to change "Claude" to "Codex" in Codex skills
2. **Over-adaptation**: Making unnecessary changes that should be identical
3. **Under-adaptation**: Not applying platform-specific principles when needed
4. **Drift**: Skills gradually diverging over time without documentation
5. **Inconsistent frontmatter**: Using wrong metadata fields for platform

## Maintenance

- **Regular validation**: Run `scripts/validate-skill-sync.sh` periodically
- **Document differences**: When skills legitimately differ, document why
- **Review updates**: When updating a skill, check if sync is needed
- **Test both platforms**: Verify skills work correctly on both platforms

## Decision Tree

```
Is this a new skill or major update?
├─ Yes → Create/update on primary platform (Claude)
│         └─ Sync to other platform with adaptations
│
└─ No → Is this a platform-specific change?
        ├─ Yes → Update only that platform
        └─ No → Update both platforms (or use sync tool)
```

## Examples

### Example 1: Accessibility Skill

**Should be identical**: Core WCAG guidelines, ARIA patterns, testing procedures

**Should differ**:

- Platform references ("Claude" vs "Codex")
- Codex version might be more concise
- Writing style (third-person vs imperative)

### Example 2: Skill Creator

**Should be identical**: Skill structure, creation process, bundled resources

**Should differ**:

- Codex-specific principles ("Concise is Key", "Degrees of Freedom")
- Writing style guidance
- Progressive disclosure emphasis
- Frontmatter metadata fields

### Example 3: Project Scaffold

**Should be identical**: Scaffolding logic, templates, scripts

**Should differ**:

- Platform references in instructions
- Path references (if different: `~/.claude/skills/` vs `~/.codex/skills/`)

## Questions?

When in doubt:

1. Check this guide
2. Review similar skills for patterns
3. Run validation script
4. Test on both platforms
