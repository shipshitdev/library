# Anthropic — Official Skill-Authoring Guidance

Extracted verbatim-in-substance from Anthropic's first-hand documentation (Claude Code docs, Claude API best-practices/overview, and Anthropic Engineering posts) and the agentskills.io open standard. Every rule links to its source. Last gathered 2026-06-12.

These are the platform rules for **Claude Code / Claude API / claude.ai**. For the cross-platform field reference see [frontmatter-field-spec.md](frontmatter-field-spec.md); for OpenAI's equivalent see [codex.md](codex.md).

## Frontmatter

- **Only `name` and `description` are required frontmatter fields. All others are optional.**
  - _Why:_ The system pre-loads only name+description at startup; all other fields are capability extensions. Omitting unneeded fields keeps SKILL.md minimal.
  - _Source:_ [Claude overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- **`name`: max 64 characters, lowercase letters/numbers/hyphens only, must not start or end with a hyphen, no consecutive hyphens (--), no XML tags, no reserved words ('anthropic', 'claude'). Must match the parent directory name.**
  - _Why:_ The name is used as a display label and plugin-root command identifier. Violating these constraints causes validation failure or ambiguous routing.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **`description`: must be non-empty, max 1,024 characters, no XML tags. The combined `description` + `when_to_use` text is truncated at 1,536 characters in the skill listing.**
  - _Why:_ The description is the sole automatic-triggering signal Claude uses. Exceeding limits causes silent truncation that strips trigger keywords.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **`when_to_use`: appends supplementary trigger phrases or example requests to `description` in the skill listing, sharing the same 1,536-character combined cap. Put the highest-priority keywords in `description` first.**
  - _Why:_ Truncation hits the combined text. Front-loading in `description` protects the most critical trigger terms from being cut.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **`disable-model-invocation: true` removes the skill description from Claude's auto-invocation context (Claude cannot see or trigger it automatically) and prevents preloading into subagents. The full skill body still loads when the user invokes it manually via /skill-name.**
  - _Why:_ Side-effectful workflows (deploy, commit, send-slack-message) must not fire at Claude's discretion. This field is the correct gate.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **`user-invocable: false` hides the skill from the / menu but does NOT block Claude from loading it automatically. It only controls menu visibility, not Skill tool access.**
  - _Why:_ Background knowledge skills (conventions, reference patterns) should load automatically but not clutter the command palette.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **`context: fork` runs the skill in an isolated subagent with no conversation history. Only use it for skills with explicit actionable task instructions — guidelines-only skills return empty output from a forked subagent.**
  - _Why:_ A forked subagent receives the skill body as its entire prompt. Without an actionable task embedded in the skill, there is nothing for it to do.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **`paths`: documented to limit automatic activation to files matching glob patterns for monorepo scoping, but this field has an active bug (skills with `paths` set become undiscoverable as of v2.1.84). For monorepo package scoping, place skills in a nested `.claude/skills/` directory within the specific package instead.**
  - _Why:_ The correct monorepo mechanism is directory-based discovery, not the `paths` field, which is currently broken.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **`hooks`: scopes lifecycle hooks to this skill's lifecycle only, not globally.**
  - _Why:_ Skill-scoped hooks are cleaned up when the skill finishes, avoiding persistent side effects on the main session.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **`argument-hint`: shown in autocomplete to indicate expected arguments (e.g., `[issue-number]` or `[filename] [format]`).**
  - _Why:_ Improves discoverability and correct usage at the command palette.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **`compatibility`: optional, max 500 chars. Include only when the skill has specific environment requirements (system packages, network access, target agent product). Most skills do not need it.**
  - _Why:_ Unnecessary compatibility fields add noise; the field exists only to surface real environment constraints.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)

## Naming

- **Use gerund form (verb + -ing) as the preferred naming convention: `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`. Noun phrases and action-oriented names are acceptable alternatives.**
  - _Why:_ Gerund form clearly describes the activity the skill provides, making it discoverable by name alone.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Avoid vague names (helper, utils, tools), overly generic names (documents, data, files), reserved words (anthropic-helper, claude-tools), and inconsistent patterns within a skill collection.**
  - _Why:_ Vague names make it impossible for Claude or users to determine when to invoke the skill.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Plugin skills are namespaced as `plugin-name:skill-name`, preventing conflicts with personal and project skills.**
  - _Why:_ Namespace isolation lets multiple plugins define skills with overlapping names without overriding each other.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Use unambiguous parameter names in tool/script interfaces. Prefer `user_id` over `user`. Include technical identifiers only when needed for downstream tool calls.**
  - _Why:_ Ambiguous parameter names are a common source of agent tool-call errors.
  - _Source:_ [Anthropic Eng: Writing tools](https://www.anthropic.com/engineering/writing-tools-for-agents)

## Writing the description

- **Always write the description in third person. Injecting first-person or second-person text into the system prompt causes discovery problems.**
  - _Why:_ The description is injected verbatim into the system prompt. Inconsistent POV degrades Claude's ability to reason about when to trigger the skill.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Include both what the skill does AND when to trigger it. Use imperative framing ('Use this skill when...') rather than capability framing ('This skill does...'). Explicitly list contexts where the skill applies, including cases where the user doesn't name the domain directly.**
  - _Why:_ Claude may choose from 100+ skills using only the description. Passive capability descriptions do not give Claude the trigger signal it needs.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **Be specific and include domain-relevant key terms. Avoid vague descriptions like 'Helps with documents', 'Processes data', or 'Does stuff with files'.**
  - _Why:_ Vague descriptions cause under-triggering (skill missed) or over-triggering (skill fires on unrelated requests).
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Front-load the key use case and trigger words so truncation at the 1,536-character cap does not strip the most important terms.**
  - _Why:_ The listing truncates combined description+when_to_use at 1,536 chars. Keywords at the end are silently dropped.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **For reference skills (conventions, patterns applied inline) vs task skills (step-by-step actions), use distinct description styles. Task skills often need `disable-model-invocation: true` so Claude does not fire them at the wrong time.**
  - _Why:_ Reference content should auto-load; task content with side effects should be user-invoked.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Make tool descriptions (for scripts bundled in a skill) explicit about intended use, expected inputs, and expected outputs. Craft error messages to be specific and actionable, not opaque.**
  - _Why:_ Ambiguous tool descriptions and opaque errors are a primary cause of agent misbehavior inside skill workflows.
  - _Source:_ [Anthropic Eng: Writing tools](https://www.anthropic.com/engineering/writing-tools-for-agents)
- **If the description is too broad, Claude will over-trigger the skill. Tighten the description or add `disable-model-invocation: true` if only manual invocation is intended.**
  - _Why:_ Over-triggering wastes tokens and can fire side-effectful workflows at the wrong time.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)

## Skill structure & file layout

- **A skill is a named directory. `SKILL.md` is the required entrypoint. Supporting files (reference docs, scripts, templates) can live as flat siblings alongside `SKILL.md` or in subdirectories — both layouts are valid. The directory name determines the slash-command; the frontmatter `name` field is a display label only.**
  - _Why:_ The command name is derived from filesystem position, not frontmatter. Renaming the directory changes the command; renaming the frontmatter name does not.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Standard layout: `SKILL.md` (required) + optional `FORMS.md`, `reference.md`, `examples.md` siblings + optional `scripts/` subdirectory for executable utilities.**
  - _Why:_ Descriptive filenames (reference.md, examples.md) signal content to Claude without it needing to read them first.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Four skill scopes in precedence order: Enterprise (managed settings, highest) → Personal (~/.claude/skills/) → Project (.claude/skills/) → Plugin (<plugin>/skills/, namespaced as plugin-name:skill-name and therefore non-conflicting). When enterprise, personal, and project skills share a name, enterprise overrides personal, personal overrides project.**
  - _Why:_ Understanding scope precedence prevents surprising override behavior in enterprise or plugin environments.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Project skills load from `.claude/skills/` in the starting directory and every parent up to the repo root. Claude also discovers nested `.claude/skills/` on demand when working with files in subdirectories. This supports monorepos without the `paths` field.**
  - _Why:_ Directory-based scoping is the reliable monorepo mechanism. The `paths` field has an active bug.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Name files descriptively so their purpose is clear from the filename alone (form_validation_rules.md, not doc2.md). Organize directories by domain or feature, not generic names.**
  - _Why:_ Claude uses filenames to decide whether to load a file. Opaque names require loading to assess relevance.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Use explicit checklists for complex multi-step workflows. Provide a copyable checklist Claude tracks in its response to prevent skipping critical validation steps.**
  - _Why:_ Checklists reduce step-skipping in long workflows and make progress auditable.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Use a plan-validate-execute pattern for batch or destructive operations: Claude creates an intermediate plan file, a script validates it against a source of truth, then execution proceeds.**
  - _Why:_ Validation before execution catches plan-level errors before they cause irreversible consequences.
  - _Source:_ [Claude overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- **Use validation loops (run validator → fix errors → repeat) for quality-critical tasks. Provide scripts or reference checklists as the validator.**
  - _Why:_ Iterative self-validation dramatically improves output quality for both code and non-code tasks.
  - _Source:_ [Claude overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- **Use a Gotchas section for environment-specific facts that defy reasonable assumptions — concrete corrections to mistakes the agent will make without being told (e.g., soft-delete filters, field name mismatches across services, misleading health endpoint behavior).**
  - _Why:_ Gotchas are the highest-value content in many skills. They encode hard-won domain knowledge that generic training data does not contain.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **Use output format templates (inline in SKILL.md for short ones, in `assets/` for longer or conditional ones) rather than prose descriptions of format. Agents pattern-match against concrete structures more reliably than prose descriptions.**
  - _Why:_ Templates reduce output format variability without additional instruction tokens.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **Organize system prompts and SKILL.md content into distinct labeled sections using XML tags or Markdown headers (e.g., `<background_information>`, `## Instructions`, `## Gotchas`).**
  - _Why:_ Section structure lets Claude locate relevant content without reading the entire file.
  - _Source:_ [Anthropic Eng: Context](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **Match instruction specificity to task fragility: give the agent freedom (explain the why) when multiple approaches are valid; be prescriptive (exact commands, no extra flags) when operations are fragile, order matters, or consistency is required.**
  - _Why:_ Over-constraining simple tasks wastes tokens; under-constraining fragile tasks causes errors.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)

## Progressive disclosure

- **Three loading levels: Level 1 (always loaded) — name+description metadata only, ~100 tokens per skill. Level 2 (loaded when triggered) — full SKILL.md body, keep under 5,000 tokens / 500 lines. Level 3 (loaded as needed) — files in scripts/, references/, assets/; no context cost until accessed.**
  - _Why:_ This is the core cost model. Respecting it ensures skill-heavy environments remain token-efficient.
  - _Source:_ [Claude overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- **Keep SKILL.md under 500 lines. When approaching this limit, split content into separate files referenced from SKILL.md.**
  - _Why:_ SKILL.md body persists in context for the entire session. Every unnecessary line is a recurring per-turn token cost.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md. Avoid nested references (file A → file B → file C) because Claude may use `head -100` to preview deeply nested files, resulting in incomplete reads.**
  - _Why:_ Nested discovery chains cause Claude to partially read files and act on incomplete context.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **For reference files longer than 100 lines, include a table of contents at the top so Claude can assess the full scope even during partial reads.**
  - _Why:_ Claude may preview rather than fully read long files. A TOC lets it navigate to the relevant section without reading everything.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Tell the agent explicitly when to load each referenced file rather than using a generic 'see references/ for details'. Use conditional load triggers: 'Read `references/api-errors.md` if the API returns a non-200 status code'.**
  - _Why:_ On-demand conditional loading is more token-efficient than pre-loading all referenced files.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **Skill body content stays in context for the entire session once invoked (re-attached after compaction up to 5,000 tokens per skill, 25,000 combined). Write standing instructions, not one-time steps.**
  - _Why:_ Content that should only apply once should not be in SKILL.md — it will keep influencing Claude across subsequent turns.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Bundle large reference materials freely; files in scripts/, references/, and assets/ consume zero context tokens until actually read.**
  - _Why:_ There is no context penalty for bundled content that is not accessed during a task.
  - _Source:_ [Claude overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- **Organize bundled content by domain (reference/finance.md, reference/sales.md) to avoid loading irrelevant context. When a user asks about one domain, Claude should only need to read that domain's files.**
  - _Why:_ Domain isolation keeps per-task context load minimal even when the skill covers multiple functional areas.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## Invocation & triggering

- **Two invocation paths: (1) user types `/skill-name` directly; (2) Claude auto-triggers based on description match. Test both paths explicitly.**
  - _Why:_ A skill that only works on explicit invocation but not auto-trigger (or vice versa) has half the intended value.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **The description field carries the entire burden of triggering for automatic invocation. If the description does not convey when the skill is useful, Claude will not reach for it.**
  - _Why:_ Agents load only name+description at startup to decide relevance; the full SKILL.md is not read until after the decision.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **Include `ultrathink` anywhere in skill content to request deeper reasoning when the skill runs.**
  - _Why:_ Complex analytical skills benefit from extended reasoning chains.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **If a skill stops influencing behavior after the first response, strengthen the description and instructions, or use hooks to enforce behavior deterministically. Re-invoke the skill after compaction to restore full content.**
  - _Why:_ Skill content may be compressed or deprioritized after context compaction.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Run `/doctor` to diagnose whether the skill description budget is overflowing and which skills are losing descriptions due to the budget cap. Raise `skillListingBudgetFraction` or set low-priority skills to name-only in `skillOverrides` if needed.**
  - _Why:_ Budget overflow silently causes skills to disappear from Claude's context, preventing triggering.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)

## Tool permissions (allowed-tools / disallowed-tools)

- **`allowed-tools` grants per-use-approval bypass for listed tools while the skill is active. It does not restrict other tools — every tool remains callable and global permissions still govern the rest. For project skills, takes effect only after the user accepts the workspace trust dialog.**
  - _Why:_ Without allowed-tools, every tool call prompts the user even mid-skill. With it, listed tools run without prompts, enabling smooth automated workflows.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **`disallowed-tools` removes specific tools from Claude's available pool while a skill is active (e.g., `AskUserQuestion` for autonomous loop skills). The restriction clears when the user sends their next message.**
  - _Why:_ Autonomous background skills must never pause to ask the user questions. Disallowing AskUserQuestion enforces that guarantee.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **For MCP tool references in skill instructions, always use fully qualified names in the format `ServerName:tool_name` to avoid 'tool not found' errors when multiple MCP servers are available.**
  - _Why:_ Unqualified MCP tool names are ambiguous when multiple servers expose identically named tools.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Use a minimal viable set of tools per skill. Avoid bloated tool sets that create ambiguous decision points about which tool to use. If a human engineer cannot definitively say which tool to use in a given situation, Claude cannot be expected to do better.**
  - _Why:_ Tool ambiguity is one of the most common agent failure modes.
  - _Source:_ [Anthropic Eng: Context](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **Claude Code skills should install packages locally only, not globally, to avoid interfering with the user's computer.**
  - _Why:_ Global installs mutate the user's system state outside the task scope.
  - _Source:_ [Claude overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

## References & scripts

- **Use the `!\`command\`` inline syntax (or ` ```!``` ` fenced block for multi-line) to inject live shell output before Claude sees the skill. This is preprocessing — Claude receives the rendered result, not the command. Use `${CLAUDE_SKILL_DIR}` to reference bundled scripts regardless of cwd.**
  - _Why:_ Dynamic context injection (e.g., current git status, env vars) grounds the skill in runtime state without requiring Claude to run discovery commands.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **The `!\`command\`` syntax is only recognized when `!` appears at the start of a line or immediately after whitespace. `KEY=!\`cmd\`` leaves the placeholder as literal text.**
  - _Why:_ Misplacing `!` silently disables the injection without error.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Be explicit in instructions whether Claude should execute a script or read it as reference. Execution keeps script code out of the context window; reading loads it into context. Execution is preferred for most utility scripts.**
  - _Why:_ Executing a script is more token-efficient and deterministic than having Claude read and re-implement the logic.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Provide pre-made utility scripts for deterministic, repeatable operations rather than having Claude generate code at runtime. Pre-made scripts are more reliable, save tokens, and ensure consistency.**
  - _Why:_ LLM-generated code at runtime varies across invocations. Pre-made scripts are deterministic and faster.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Scripts should handle error conditions explicitly with specific, actionable error messages (e.g., 'Field signature_date not found. Available fields: customer_name, order_total') rather than bare exceptions or punting failures to Claude.**
  - _Why:_ Specific error messages enable Claude to self-correct without additional round trips.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Document every configuration parameter in scripts with a comment explaining why that value was chosen. Avoid 'voodoo constants' (magic numbers without justification).**
  - _Why:_ If the skill author does not know why a constant was chosen, Claude cannot determine the right value for edge cases.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Explicitly list all required packages in SKILL.md and verify they are available in the target runtime. Do not assume packages are installed.**
  - _Why:_ Runtime package availability differs between claude.ai (can install from npm/PyPI) and Claude API (no network access, no runtime installs).
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **When you notice Claude independently reinventing the same logic across runs, extract it into a tested script in `scripts/`. This is the signal that a script should be created.**
  - _Why:_ Repeated LLM-generated code is wasteful, inconsistent, and error-prone.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)

## Testing & evaluation

- **Build evaluations BEFORE writing extensive documentation. Identify gaps by running Claude on representative tasks without the skill, then create at least three evaluation scenarios and establish a baseline.**
  - _Why:_ Skills built without prior evaluation often solve imagined problems rather than real gaps.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Use a two-Claude iteration loop: Claude A (author/expert) designs and refines the skill; Claude B (fresh instance with skill loaded) tests it on real tasks. Bring Claude B's observations back to Claude A to refine.**
  - _Why:_ The author's familiarity with a skill biases their testing. A fresh instance with no context reveals genuine discovery and usability gaps.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Test triggering accuracy with ~20 queries: 8-10 should-trigger and 8-10 should-not-trigger (near-miss queries that share keywords but need something different). Run each query 3+ times and compute a trigger rate. Use a ~60/40 train/validation split to avoid overfitting the description to specific phrasings.**
  - _Why:_ Obvious negative test cases (completely unrelated topics) test nothing useful. Near-misses reveal whether the description is precise.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **When optimizing descriptions, address the general concept a cluster of failed queries represents — do not add specific keywords from individual failed queries. Overfitting to specific phrasings degrades robustness.**
  - _Why:_ Description overfitting makes triggering brittle to natural phrasing variation.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **Test with all models you plan to deploy: Haiku may need more explicit guidance; Opus should not be over-explained. Aim for instructions that work across Haiku, Sonnet, and Opus.**
  - _Why:_ Instruction specificity needs differ by model capability. Opus-optimized skills may fail on Haiku.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Observe actual navigation patterns during testing: unexpected file-read order, missed links, overreliance on one section, and never-accessed files all signal structural problems. Iterate based on observations, not assumptions.**
  - _Why:_ Claude's actual traversal reveals structural issues that static review cannot catch.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **When an agent makes a mistake requiring correction, add the correction to a Gotchas section in SKILL.md immediately. This is one of the most direct ways to improve a skill iteratively.**
  - _Why:_ Corrections captured at the moment of failure are the highest-fidelity skill improvements possible.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **Verify skills appear in `What skills are available?` before testing behavior. Invoke directly with `/skill-name` and also test auto-invocation with naturally phrased requests matching the description.**
  - _Why:_ A skill that does not appear in the listing will never trigger automatically.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Editing or adding a SKILL.md takes effect within the current session without restarting. Creating a brand-new top-level skills directory requires a session restart.**
  - _Why:_ Understanding live-reload behavior avoids confusion during authoring iteration.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)

## Anti-patterns

- **Do not put side-effectful workflows (deploy, commit, send messages) as auto-invocable skills. Add `disable-model-invocation: true`.**
  - _Why:_ Claude may trigger them at the wrong moment, causing irreversible consequences.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Do not add `context: fork` to skills that only contain reference guidelines without an actionable task.**
  - _Why:_ A forked subagent with no task prompt returns empty output.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Do not put long reference docs or large example collections directly in SKILL.md. Move them to separate referenced files.**
  - _Why:_ SKILL.md content persists in context all session — every unnecessary line is a recurring per-turn token cost.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Do not confuse `user-invocable: false` (hides from / menu only) with `disable-model-invocation: true` (blocks all programmatic invocation). Setting both leaves the skill unreachable from all paths.**
  - _Why:_ The two fields control different access dimensions. Conflating them creates skills that can never be invoked.
  - _Source:_ [Claude Code docs](https://code.claude.com/docs/en/skills)
- **Do not use Windows-style backslash paths anywhere in skills. Always use forward slashes.**
  - _Why:_ Backslash paths cause errors on Unix systems and Claude Code runs on Unix.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Do not offer multiple tool or library choices as equal options. Provide a single recommended default with one escape hatch for edge cases.**
  - _Why:_ Multiple equal options cause agent indecision and unproductive exploration.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Do not include time-sensitive information in the main body. Move deprecated or legacy content into a collapsible 'old patterns' section.**
  - _Why:_ Time-sensitive content becomes wrong and misleads Claude on future invocations.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Do not use inconsistent terminology for the same concept within a skill. Choose one term per concept and use it throughout.**
  - _Why:_ Terminological inconsistency forces Claude to maintain a mental alias map, increasing error rates.
  - _Source:_ [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- **Do not include content Claude already knows from general training. Only add project-specific conventions, domain-specific procedures, non-obvious edge cases, and particular tools or APIs to use.**
  - _Why:_ Explaining general knowledge wastes tokens and dilutes the signal of domain-specific instructions.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **Do not generate a skill using an LLM without providing domain-specific context. Generic LLM-generated skills produce vague procedures ('handle errors appropriately') rather than specific patterns and edge cases.**
  - _Why:_ The value of a skill is in capturing domain expertise that training data does not contain.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **Do not write skills that encode specific answers for specific instances. Skills should teach the agent how to approach a class of problems, not what to produce for one exact task.**
  - _Why:_ Instance-specific skills do not generalize and become stale when specifics change.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **Do not scope skills too narrowly (forces multiple skills to load for one task, risks conflicts) or too broadly (hard to trigger precisely). Design coherent units comparable to well-scoped functions.**
  - _Why:_ Scope extremes both degrade skill utility: narrow scope causes overhead, broad scope causes imprecision.
  - _Source:_ [anthropics/skills spec](https://github.com/anthropics/skills)
- **Do not install skills from untrusted sources without auditing code dependencies, bundled resources (images, scripts), and any instructions directing Claude to connect to external network sources.**
  - _Why:_ Malicious skills can direct Claude to exfiltrate data or take unintended actions.
  - _Source:_ [Anthropic Eng: Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **Do not stuff a laundry list of edge cases into a skill. Curate diverse, canonical examples instead.**
  - _Why:_ Exhaustive edge-case coverage makes skills harder to read and increases context load without improving typical-case performance.
  - _Source:_ [Anthropic Eng: Context](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
