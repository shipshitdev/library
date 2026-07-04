# Skill Authoring & Audit Checklist

A single pass/fail checklist distilled from all 13 first-hand sources. Run it against any SKILL.md before shipping. Sourced 2026-06-12; House style / Model references / Provenance sections added 2026-07-04 from the field-leading skill repos (mattpocock/skills, vercel-labs/agent-skills, cursor team-kit).

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

## House style (editorial)

The spec checklist above proves a skill is *valid*. These prove it is *well-written*.
Distilled from the skills the field rates highest (mattpocock/skills, vercel-labs,
cursor team-kit). Run every item against the SKILL.md body, not just the frontmatter.

- [ ] **Literal-word triggers.** The description names the words a user would actually type ("Use when the user says 'diagnose', 'debug this', or reports something failing"), not abstract categories ("Use for debugging scenarios"). One trigger per real branch; synonyms that rename one branch are duplication, not coverage.
- [ ] **Minimal frontmatter.** Only fields that change behavior. Volatile config (paths, labels, tracker names, model) is externalized to per-repo docs or the routing block, not baked into the skill.
- [ ] **Checkable completion criteria.** Every phase/step ends on a criterion you can verify — "done when you can paste the command and its output", not "when the analysis is thorough". A vague criterion invites premature completion.
- [ ] **Negatives at the failure point.** Each "never/do not" sits where the mistake would happen and states *why*, not collected in a generic Safety Rules block at the bottom that the agent reads before it can apply it.
- [ ] **Evidence before a claim counts.** Findings must cite `file:line` or quote the source (spec line, standard, commit). No citation, no finding. Sub-agent briefs say this explicitly.
- [ ] **No-op sentence test.** Every sentence changes agent behavior versus the default. Test each in isolation; when one is a no-op ("be careful", restating what the model already does), delete the whole sentence — do not trim it to fewer words.
- [ ] **Progressive disclosure.** SKILL.md reads as an index; depth lives one hop away in `references/`. Rule-catalog skills use one file per rule with paired Incorrect/Correct examples rather than prose lists.
- [ ] **Word caps in delegated prompts.** Sub-agent briefs carry an explicit output budget ("Under 400 words") so fan-out does not flood the orchestrator's context.

## Model references

- [ ] No concrete model name appears in the body, `references/`, or `scripts/` — no tier+version IDs (`claude-3-7-sonnet-20250219`, `claude-opus-4.5`, `gpt-5.5`), dated snapshots, or bare family name used as a routing key
- [ ] If the skill is an orchestrator (spawns sub-agents), model choice is expressed as a **capability tier** in prose ("cheapest tier for finders, strongest for the verdict"), with the concrete mapping deferred to the repo routing block
- [ ] The `model:` frontmatter field (if present) is a harness-resolved tier alias, not a version-pinned ID — and is omitted unless the skill genuinely needs a fixed tier
- [ ] External tools (Codex, `gh`, a CLI) may be named as dependencies; the models they run may not

## Provenance

Applies only to skills derived from an upstream; in-house skills need none.

- [ ] `metadata.source` and `metadata.last_synced` are set (the validator also expects `upstream_repo`/`upstream_ref`/`upstream_commit`/`license`)
- [ ] `README.md` has a `## Upstream` section: field table, a **Local modifications** line, and a **Checking for upstream changes** line
- [ ] The vendored-vs-adapted kind is legible from the Local modifications line — vendored (tool-vendor upstream, verbatim) vs adapted (individual/community upstream, house-style rewrite)
- [ ] A **vendored** skill has not been hand-edited to diverge; local needs are met by re-syncing, fixing upstream, or promoting to adapted
- [ ] `last_synced` is within 90 days (validator warns past that — re-diff upstream and bump `upstream_commit` + `last_synced`)

## Open questions & known issues

Live ambiguities and bugs in the platforms as of June 2026 — verify against current releases before depending on the affected field.

- **The paths frontmatter field bug (issue #49835): is it fixed in any current Claude Code release, or is the workaround (nested .claude/skills/ directories) still required?**
  - *Status:* Unresolved as of June 2026. The fix was not confirmed in the official docs or release notes. Authors should avoid the paths field until explicitly confirmed fixed.
  - *Source:* [Claude Code docs](https://code.claude.com/docs/en/skills)
- **context: fork runtime enforcement: GitHub issue #17283 indicates context:fork may not be honored when skills are invoked via the Skill tool. Is this fixed or still an open limitation?**
  - *Status:* Unresolved as of June 2026. The documented semantics exist but runtime enforcement may be incomplete.
  - *Source:* [Claude Code docs](https://code.claude.com/docs/en/skills)
- **The allowed-tools field is marked 'experimental' in the agentskills.io spec and 'support varies between agent implementations'. What is the exact behavior difference between Claude Code, claude.ai, and the Claude API for this field?**
  - *Status:* Partially documented. Claude Code behavior is described (grants bypass for project skills after workspace trust). Cross-surface behavior differences are not fully specified.
  - *Source:* [anthropics/skills spec](https://github.com/anthropics/skills)
- **The 1,536-character combined description+when_to_use cap was raised from 250 chars in v2.1.105. Is this cap now stable across Claude Code versions, or does it vary by version?**
  - *Status:* The current docs reflect 1,536 chars as the current cap. Version-specific behavior before v2.1.105 is different. Authors targeting older installs should test.
  - *Source:* [Claude Code docs](https://code.claude.com/docs/en/skills)
- **The Anthropic docs describe skill body content being re-attached after compaction up to 5,000 tokens per skill and 25,000 combined. Are these limits configurable or fixed?**
  - *Status:* These limits are documented as behavioral facts but no configuration mechanism for them was found in the sources read.
  - *Source:* [Claude Code docs](https://code.claude.com/docs/en/skills)
- **For the Codex `allow_implicit_invocation: false` flag in agents/openai.yaml — is there an equivalent field in the Anthropic Claude Code spec, or is `disable-model-invocation: true` the closest equivalent?**
  - *Status:* Functionally equivalent but different fields in different specs. The Anthropic field (`disable-model-invocation`) also prevents subagent preloading, which the Codex field may not. Cross-spec portability of this behavior is unverified.
  - *Source:* [Codex skills.md](https://developers.openai.com/codex/skills.md)
- **The agentskills.io spec requires the name field to match the parent directory name. The Claude Code docs describe the directory name as the command source and the frontmatter name as display-only. Are there authoritative rules for what happens when they differ?**
  - *Status:* The Claude Code docs are explicit that the directory name governs the command, and the name field is display-only for directory-based skills. The agentskills.io spec adds the constraint that they must match. Whether mismatch causes validation failure or is merely a warning is not specified.
  - *Source:* [anthropics/skills spec](https://github.com/anthropics/skills)
