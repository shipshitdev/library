# Skill Authoring & Audit Checklist

A single pass/fail checklist distilled from all 13 first-hand sources. Run it against any SKILL.md before shipping. Sourced 2026-06-12.

## Checklist

- [ ] SKILL.md exists at the root of each skill directory and begins with valid YAML frontmatter delimited by ---
- [ ] name field: max 64 chars, lowercase-alphanumeric-hyphens only, no leading/trailing/consecutive hyphens, no XML tags, no 'anthropic' or 'claude' reserved words, matches parent directory name
- [ ] description field is non-empty, under 1,024 chars, written in third person, includes both capability ('what it does') and trigger context ('when to use it') with front-loaded key terms
- [ ] Combined description + when_to_use length does not exceed 1,536 characters
- [ ] SKILL.md body is under 500 lines / 5,000 tokens
- [ ] All file references from SKILL.md are one level deep — no reference chains (A→B→C)
- [ ] Reference files longer than 100 lines include a table of contents at the top
- [ ] Referenced files are named descriptively (reference.md, not doc2.md; scripts/analyze_form.py, not scripts/a.py)
- [ ] All file paths use forward slashes — no Windows-style backslashes
- [ ] No time-sensitive information in SKILL.md main body (deprecated content moved to an 'old patterns' collapsible section)
- [ ] No inconsistent terminology — one term per concept used throughout
- [ ] Skills with side effects (deploy, commit, send messages) have disable-model-invocation: true
- [ ] Skills with context: fork contain explicit actionable task instructions, not guidelines only
- [ ] MCP tool references in instructions use fully qualified ServerName:tool_name format
- [ ] Scripts in scripts/ handle error conditions explicitly with specific, actionable error messages
- [ ] All required packages are listed explicitly in SKILL.md with install commands; no assumed availability
- [ ] Configuration constants in scripts have explanatory comments (no magic numbers)
- [ ] Instructions specify whether Claude should execute or read each script (not left ambiguous)
- [ ] Package installs in Claude Code skills use local install only (no global installs)
- [ ] Skills do not explain general knowledge Claude already has from training
- [ ] Skill teaches a class of problems, not hard-codes answers for one specific instance
- [ ] Skill scope is coherent — not so narrow that multiple skills must load for one task, not so broad that triggering is imprecise
- [ ] run /doctor to confirm no skill descriptions are being truncated by the budget cap
- [ ] Verify skill appears in 'What skills are available?' response
- [ ] Test auto-triggering with at least 3 should-trigger and 3 should-not-trigger (near-miss) queries
- [ ] Test manual invocation via /skill-name
- [ ] For project skills: inspect allowed-tools before accepting workspace trust dialog
- [ ] No content from untrusted external sources is referenced or fetched by bundled scripts without user awareness
- [ ] If disallowed-tools is set on an autonomous skill, AskUserQuestion is in the disallowed list
- [ ] Neither user-invocable: false nor disable-model-invocation: true is set alone when the intent is full inaccessibility — setting both is required for that, and that combination should be intentional
- [ ] Gotchas section exists and captures corrections to mistakes observed during real task execution
- [ ] Multi-step workflows use explicit checklists or validation loops (run validator → fix → repeat)
- [ ] Destructive/batch operations use plan-validate-execute pattern with intermediate plan validation
- [ ] paths field is NOT used (active bug as of v2.1.84 makes skills with paths set undiscoverable)

## Open questions & known issues

Live ambiguities and bugs in the platforms as of June 2026 — verify against current releases before depending on the affected field.

- **The paths frontmatter field bug (issue #49835): is it fixed in any current Claude Code release, or is the workaround (nested .claude/skills/ directories) still required?**
  - _Status:_ Unresolved as of June 2026. The fix was not confirmed in the official docs or release notes. Authors should avoid the paths field until explicitly confirmed fixed.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **context: fork runtime enforcement: GitHub issue #17283 indicates context:fork may not be honored when skills are invoked via the Skill tool. Is this fixed or still an open limitation?**
  - _Status:_ Unresolved as of June 2026. The documented semantics exist but runtime enforcement may be incomplete.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **The allowed-tools field is marked 'experimental' in the agentskills.io spec and 'support varies between agent implementations'. What is the exact behavior difference between Claude Code, claude.ai, and the Claude API for this field?**
  - _Status:_ Partially documented. Claude Code behavior is described (grants bypass for project skills after workspace trust). Cross-surface behavior differences are not fully specified.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **The 1,536-character combined description+when_to_use cap was raised from 250 chars in v2.1.105. Is this cap now stable across Claude Code versions, or does it vary by version?**
  - _Status:_ The current docs reflect 1,536 chars as the current cap. Version-specific behavior before v2.1.105 is different. Authors targeting older installs should test.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **The Anthropic docs describe skill body content being re-attached after compaction up to 5,000 tokens per skill and 25,000 combined. Are these limits configurable or fixed?**
  - _Status:_ These limits are documented as behavioral facts but no configuration mechanism for them was found in the sources read.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **For the Codex `allow_implicit_invocation: false` flag in agents/openai.yaml — is there an equivalent field in the Anthropic Claude Code spec, or is `disable-model-invocation: true` the closest equivalent?**
  - _Status:_ Functionally equivalent but different fields in different specs. The Anthropic field (`disable-model-invocation`) also prevents subagent preloading, which the Codex field may not. Cross-spec portability of this behavior is unverified.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)
- **The agentskills.io spec requires the name field to match the parent directory name. The Claude Code docs describe the directory name as the command source and the frontmatter name as display-only. Are there authoritative rules for what happens when they differ?**
  - _Status:_ The Claude Code docs are explicit that the directory name governs the command, and the name field is display-only for directory-based skills. The agentskills.io spec adds the constraint that they must match. Whether mismatch causes validation failure or is merely a warning is not specified.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
