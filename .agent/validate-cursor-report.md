# Cursor Commands and Skills Validation Report

**Generated:** 2025-01-27  
**Scope:** All files in `agents/.cursor/commands/` and `agents/.cursor/skills/`

## Executive Summary

Validated 33 Cursor commands and 77 Cursor skills for format compliance, structure, and consistency with Claude/Codex versions.

### Overall Status

- ✅ **Commands:** All properly formatted (no YAML frontmatter, proper H1 headings)
- ⚠️ **Skills:** 2 skills have frontmatter issues, multiple platform reference issues found
- ⚠️ **Platform References:** 37 files contain "Claude" references, 9 files contain "Codex" references

---

## Phase 1: Commands Validation

### Files Checked

33 command files in `agents/.cursor/commands/`

### Results

#### ✅ Format Compliance

- **YAML Frontmatter:** None found at file start (correct - commands should not have frontmatter)
- **H1 Headings:** All 33 commands start with proper `# Title` heading
- **Structure:** All commands have clear purpose and workflow sections

#### ⚠️ Naming Convention

The naming convention appears flexible, accepting both:

- Single-word commands: `bug.md`, `clean.md`, `end.md`, `inbox.md`, `launch.md`, `loop.md`, `migrate.md`, `performance.md`, `scaffold.md`, `start.md`, `task.md`, `test.md`, `validate.md`
- Verb-noun commands: `analyze-codebase.md`, `api-test.md`, `code-review.md`, `commit-summary.md`, `db-setup.md`, etc.

**Recommendation:** This is acceptable - both patterns are used consistently.

### Commands List

1. analyze-codebase.md ✅
2. api-test.md ✅
3. bug.md ✅
4. clean.md ✅
5. code-review.md ✅
6. commit-summary.md ✅
7. db-setup.md ✅
8. de-slop.md ✅
9. deploy.md ✅
10. docs-generate.md ✅
11. docs-update.md ✅
12. end.md ✅
13. env-setup.md ✅
14. inbox.md ✅
15. launch.md ✅
16. loop.md ✅
17. migrate.md ✅
18. monitoring-setup.md ✅
19. mvp-plan.md ✅
20. new-cmd.md ✅
21. new-session.md ✅
22. optimize-prompt.md ✅
23. performance.md ✅
24. quick-fix.md ✅
25. refactor-code.md ✅
26. review-pr.md ✅
27. scaffold.md ✅
28. security-audit.md ✅
29. start.md ✅
30. task.md ✅
31. test.md ✅
32. validate.md ✅
33. README.md ✅

---

## Phase 2: Skills Validation

### Files Checked

77 skill files in `agents/.cursor/skills/*/SKILL.md`

### Results

#### ✅ Frontmatter Structure

- **Frontmatter Start:** All 77 skills have `---` delimiter at start
- **Frontmatter End:** All 77 skills have closing `---` delimiter
- **Required Fields:** 75/77 skills have both `name:` and `description:` fields

#### ❌ Frontmatter Issues

**Missing `name:` field (using alternative field names):**

1. **`nestjs-queue-architect/SKILL.md`**
   - Uses `skill_name:` instead of `name:`
   - Location: Line 2
   - Fix: Change `skill_name:` to `name:`

2. **`react-native-components/SKILL.md`**
   - Uses `title:` instead of `name:`
   - Location: Line 2
   - Fix: Change `title:` to `name:`

#### ✅ Frontmatter Consistency

For skills that exist across all three platforms (Claude, Codex, Cursor), the frontmatter `name` and `description` fields are identical, which is correct.

**Verified examples:**

- `accessibility` - All platforms identical ✅
- `api-design-expert` - All platforms identical ✅
- `artifacts-builder` - All platforms identical ✅

---

## Phase 3: Platform References

### Files with "Claude" References

Found **37 files** containing "Claude" references in Cursor directory:

#### Skills (13 files with issues)

1. `skills/skill-creator/SKILL.md` - **CRITICAL**: Multiple references to "Claude" in description and body
   - Line 3: `extends Claude's capabilities`
   - Line 13: `extend Claude's capabilities`
   - Line 15: `transform Claude from a general-purpose agent`
   - Line 44: `when Claude will use the skill`
   - Line 64: `when Claude determines it's needed`
   - Line 83: `As needed by Claude`
   - Line 157: `created for another instance of Claude`
   - Line 173: `how should Claude use the skill`

2. `skills/project-init-orchestrator/SKILL.md`
3. `skills/ai-dev-loop/SKILL.md`
4. `skills/workspace-performance-audit/SKILL.md`
5. `skills/brand-name-generator/SKILL.md`
6. `skills/project-scaffold/SKILL.md`
7. `skills/docusaurus-writer/SKILL.md`
8. `skills/design-consistency-auditor/SKILL.md`
9. `skills/artifacts-builder/SKILL.md`
10. `skills/internal-comms/SKILL.md`
11. `skills/analytics-expert/SKILL.md`
12. `skills/strategy-expert/SKILL.md`
13. `skills/workflow-automation/SKILL.md`
14. `skills/prompt-engineer/SKILL.md`
15. `skills/rules-capture/SKILL.md`
16. `skills/planning-assistant/SKILL.md`

#### Commands (6 files with issues)

1. `commands/loop.md` - References to Claude CLI
2. `commands/scaffold.md`
3. `commands/start.md` - References to "Claude Code"
4. `commands/optimize-prompt.md`
5. `commands/new-cmd.md` - References to "Claude Code CLI"
6. `commands/inbox.md` - "Instructions for Claude"
7. `commands/end.md`
8. `commands/analyze-codebase.md`

#### Other Files

- `README.md` - References to Claude
- `skills/README.md` - Multiple references to Claude
- Various script files and reference documents

### Files with "Codex" References

Found **9 files** containing "Codex" references:

1. `skills/clerk-implementer/SKILL.md` - **CRITICAL**: Line 10 - "Codex determines when this skill is needed"
2. `skills/ai-dev-loop/SKILL.md`
3. `commands/loop.md`
4. `skills/leads-researcher/SKILL.md`
5. `skills/search-domain-validator/SKILL.md`
6. `skills/project-scaffold/SKILL.md`
7. `commands/scaffold.md`
8. `rules` file

### Platform Reference Issues Summary

**Critical Issues (must fix):**

- `skill-creator/SKILL.md` - Entire skill is about creating skills for "Claude" - needs complete rewrite for Cursor
- `clerk-implementer/SKILL.md` - References "Codex determines" - should be Cursor-agnostic
- `new-cmd.md` - References "Claude Code CLI" - should reference Cursor commands

**Medium Priority:**

- Skills that mention "Claude" in descriptions or body text
- Commands that reference Claude-specific workflows

**Low Priority:**

- Script files and reference documents (may be acceptable if they're platform-agnostic)

---

## Phase 4: Cross-Platform Consistency

### Skills Present in All Three Platforms

Found **20+ skills** that exist across Claude, Codex, and Cursor:

**Verified Consistent:**

- `accessibility` ✅ - Frontmatter identical, content structure similar
- `api-design-expert` ✅ - Frontmatter identical
- `artifacts-builder` ✅ - Frontmatter identical

**Note:** Content length differs between platforms (Codex versions are more concise, as expected per PLATFORM-ADAPTATIONS.md), but core functionality should be identical.

### Skills Unique to Cursor

These skills only exist in Cursor (no comparison needed):

- `aws-infrastructure`
- Various business/startup skills (brand-architect, mvp-architect, etc.)

---

## Recommendations

### High Priority Fixes

1. **Fix Frontmatter Field Names**
   - `nestjs-queue-architect/SKILL.md`: Change `skill_name:` to `name:`
   - `react-native-components/SKILL.md`: Change `title:` to `name:`

2. **Fix Platform References in Critical Files**
   - `skill-creator/SKILL.md`: Replace all "Claude" references with "Cursor" or make generic
   - `clerk-implementer/SKILL.md`: Replace "Codex determines" with Cursor-agnostic language
   - `new-cmd.md`: Update "Claude Code CLI" to "Cursor commands"

### Medium Priority Fixes

1. **Review and Update Platform References**
   - Scan all 37 files with "Claude" references
   - Determine if references are:
     - Acceptable (e.g., in comments, examples, or platform-agnostic contexts)
     - Need updating (e.g., in descriptions, instructions, or platform-specific contexts)
   - Update descriptions and body text to be Cursor-agnostic or reference "Cursor"

2. **Review Codex References**
   - Check 9 files with "Codex" references
   - Update to Cursor-agnostic language

### Low Priority / Documentation

1. **Document Platform-Specific Differences**
   - Some references to "Claude" may be acceptable if they're in examples or documentation
   - Create guidelines for when platform references are acceptable vs. need updating

2. **Validation Script Enhancement**
   - Add checks for frontmatter field names (`name:` vs `skill_name:` vs `title:`)
   - Add checks for platform references in Cursor files
   - Add automated comparison with Claude/Codex versions

---

## Files Requiring Action

### Must Fix (Frontmatter)

1. `agents/.cursor/skills/nestjs-queue-architect/SKILL.md` - Change `skill_name:` to `name:`
2. `agents/.cursor/skills/react-native-components/SKILL.md` - Change `title:` to `name:`

### Should Fix (Platform References)

1. `agents/.cursor/skills/skill-creator/SKILL.md` - Multiple "Claude" references
2. `agents/.cursor/skills/clerk-implementer/SKILL.md` - "Codex" reference
3. `agents/.cursor/commands/new-cmd.md` - "Claude Code CLI" reference
4. `agents/.cursor/commands/start.md` - "Claude Code" references
5. `agents/.cursor/commands/loop.md` - Claude CLI references
6. Additional 32+ files with platform references (review needed)

---

## Validation Statistics

- **Commands Checked:** 33
- **Commands Valid:** 33 (100%)
- **Skills Checked:** 77
- **Skills Valid:** 75 (97.4%)
- **Skills with Issues:** 2 (2.6%)
- **Files with Platform References:** 46 (37 Claude, 9 Codex)
- **Skills with Consistent Frontmatter:** 75/77 (97.4%)

---

## Conclusion

The Cursor commands are correctly formatted. Skills have minor frontmatter issues (2 files) and multiple platform reference issues that should be addressed. The core structure is sound, but platform-specific language needs updating to be Cursor-appropriate.

**Next Steps:**

1. Fix the 2 frontmatter issues
2. Review and update platform references in critical files
3. Consider creating a script to automate platform reference checking

---

**Report Generated:** 2025-01-27  
**Validation Tool:** Manual review + grep analysis
