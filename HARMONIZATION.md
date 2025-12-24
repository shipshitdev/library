# Skills Harmonization - Gap Analysis & Replication Plan

## Overview

This document tracks the harmonization of skills across Claude, Codex, and Cursor platforms. The goal is to ensure **complete parity** - all platforms have access to all skills, with each skill being completely independent on each platform.

## Current State (Before Harmonization)

### Skills Count
- **Claude:** 16 skills
- **Codex:** 36 skills
- **Cursor:** 20 skills

### Skills by Platform

#### Claude (16 skills)
- agent-folder-init
- analytics-expert
- changelog-generator
- design-consistency-auditor
- fullstack-workspace-init
- internal-comms
- micro-landing-builder
- planning-assistant
- project-scaffold
- qa-reviewer
- roadmap-analyzer
- session-documenter
- skill-creator ⭐ (unique to Claude)
- strategy-expert
- webapp-testing
- workflow-automation

#### Codex (36 skills)
- accessibility ⭐
- agent-folder-init
- analytics-expert
- artifacts-builder ⭐
- changelog-generator
- component-library ⭐
- content-script-developer ⭐
- copywriter ⭐
- design-consistency-auditor
- docs ⭐
- docusaurus-writer ⭐
- expo-architect ⭐
- fullstack-workspace-init
- gh-address-comments ⭐
- gh-fix-ci ⭐
- internal-comms
- landing-page-vercel ⭐
- mcp-builder ⭐
- micro-landing-builder
- mongodb-migration-expert ⭐
- nestjs-queue-architect ⭐
- nestjs-testing-expert ⭐
- package-architect ⭐
- planning-assistant
- plasmo-extension-architect ⭐
- project-scaffold
- prompt-engineer ⭐
- qa-reviewer
- react-native-components ⭐
- roadmap-analyzer
- rules-capture ⭐
- serializer-specialist ⭐
- session-documenter
- strategy-expert
- webapp-testing
- workflow-automation

#### Cursor (20 skills)
- agent-folder-init
- analytics-expert
- api-design-expert ⭐
- changelog-generator
- design-consistency-auditor
- error-handling-expert ⭐
- fullstack-workspace-init
- internal-comms
- micro-landing-builder
- performance-expert ⭐
- planning-assistant
- project-scaffold
- qa-reviewer
- roadmap-analyzer
- security-expert ⭐
- session-documenter
- strategy-expert
- testing-expert ⭐
- webapp-testing
- workflow-automation

⭐ = Platform-specific (needs replication)

## Replication Plan

### Phase 1: Codex → Claude & Cursor (21 skills)

Copy these Codex-only skills to both Claude and Cursor:

1. accessibility
2. artifacts-builder
3. component-library
4. content-script-developer
5. copywriter
6. docs
7. docusaurus-writer
8. expo-architect
9. gh-address-comments
10. gh-fix-ci
11. landing-page-vercel
12. mcp-builder
13. mongodb-migration-expert
14. nestjs-queue-architect
15. nestjs-testing-expert
16. package-architect
17. plasmo-extension-architect
18. prompt-engineer
19. react-native-components
20. rules-capture
21. serializer-specialist

### Phase 2: Cursor → Claude & Codex (5 skills)

Copy these Cursor-only skills to both Claude and Codex:

1. api-design-expert
2. error-handling-expert
3. performance-expert
4. security-expert
5. testing-expert

### Phase 3: Claude → Cursor (1 skill)

Copy this Claude-only skill to Cursor:

1. skill-creator

## Post-Harmonization State

### Target Skills Count (All Platforms)
- **Claude:** ~37 skills (16 + 21 from Codex + 5 from Cursor)
- **Codex:** ~37 skills (36 + 5 from Cursor)
- **Cursor:** ~37 skills (20 + 21 from Codex + 1 from Claude)

### Complete Skill List (All Platforms Will Have)

1. accessibility
2. agent-folder-init
3. analytics-expert
4. api-design-expert
5. artifacts-builder
6. changelog-generator
7. component-library
8. content-script-developer
9. copywriter
10. design-consistency-auditor
11. docs
12. docusaurus-writer
13. error-handling-expert
14. expo-architect
15. fullstack-workspace-init
16. gh-address-comments
17. gh-fix-ci
18. internal-comms
19. landing-page-vercel
20. mcp-builder
21. micro-landing-builder
22. mongodb-migration-expert
23. nestjs-queue-architect
24. nestjs-testing-expert
25. package-architect
26. performance-expert
27. planning-assistant
28. plasmo-extension-architect
29. project-scaffold
30. prompt-engineer
31. qa-reviewer
32. react-native-components
33. roadmap-analyzer
34. rules-capture
35. security-expert
36. serializer-specialist
37. session-documenter
38. skill-creator
39. strategy-expert
40. testing-expert
41. webapp-testing
42. workflow-automation

**Total: 42 unique skills** (some may be duplicates in the list above, need to verify)

## Key Principles

1. **Complete Independence:** Each platform has its own complete copy of every skill
2. **No Shared Dependencies:** Skills don't depend on other skills being present
3. **Platform-Specific Paths:** All script paths in SKILL.md files use correct platform paths:
   - Claude: `~/.claude/skills/[skill-name]/scripts/`
   - Codex: `~/.codex/skills/[skill-name]/scripts/`
   - Cursor: `~/.cursor/skills/[skill-name]/scripts/`
4. **Full Parity:** All platforms can do the same things

## Verification Checklist

After replication:
- [ ] All Codex-only skills exist on Claude
- [ ] All Codex-only skills exist on Cursor
- [ ] All Cursor-only skills exist on Claude
- [ ] All Cursor-only skills exist on Codex
- [ ] skill-creator exists on Cursor
- [ ] All skills have correct platform paths in SKILL.md
- [ ] All skills are independent (no cross-skill dependencies)
- [ ] README.md updated with complete skill lists

## Notes

- **Extensions:** Browser extensions remain separate - use `project-scaffold` for extensions, `fullstack-workspace-init` does NOT include extensions
- **Platform Capabilities:** Need to verify that all platforms can execute the same Python scripts (to be tested)

