# OpenAI Codex — Official Skill-Authoring Guidance

Extracted from OpenAI's first-hand Codex documentation (Codex Skills reference, skills.md, customization concepts, best-practices, and the AGENTS.md guides). Every rule links to its source. Last gathered 2026-06-12.

Codex consumes the **Agent Skills base spec plus the skill body**. It does not read Claude-only frontmatter extensions. Where Codex diverges from Anthropic, the difference is called out. For the shared field reference see [frontmatter-field-spec.md](frontmatter-field-spec.md).

## Frontmatter

- **Required frontmatter fields: `name` and `description`. Optional skill-level metadata and tool dependencies go in `agents/openai.yaml`, not inline in SKILL.md.**
  - _Why:_ Separation of concerns: SKILL.md carries instructions; openai.yaml carries UI presentation and tool dependencies.
  - _Source:_ [Codex Skills](https://developers.openai.com/codex/skills)
- **The `description` field should explain exactly when the skill should AND should not trigger, not just what it does.**
  - _Why:_ Explicit negative scoping prevents false positives where a related-but-different task fires the skill.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)

## Naming

- **If two Codex skills share the same `name`, Codex does not merge them; both can appear in skill selectors. Name collisions across discovery tiers must be managed explicitly.**
  - _Why:_ Unlike Claude Code (which has explicit override precedence), Codex exposes both conflicting skills.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)

## Writing the description

- **The description is the most important part of a Codex skill. It must state what the skill does and when to use it. Include trigger phrases a user would actually say. Scope to one job with 2-3 concrete use cases. Define clear inputs and outputs.**
  - _Why:_ Implicit matching depends entirely on the description field. Weak descriptions cause missed triggers.
  - _Source:_ [Codex best-practices](https://developers.openai.com/codex/learn/best-practices)
- **Front-load the key use case and trigger words so Codex can still match the skill if descriptions are shortened when the skills list is large.**
  - _Why:_ The initial skills list is capped at ~2% of context window or 8,000 chars. Descriptions shorten first when many skills are installed.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)
- **AGENTS.md instructions should be concrete and actionable — specify exact commands to run, not vague principles.**
  - _Why:_ Vague AGENTS.md rules are interpreted inconsistently across sessions.
  - _Source:_ [openai/codex docs](https://github.com/openai/codex/blob/main/docs/agents_md.md)

## Skill structure & file layout

- **Codex skill directory layout: `SKILL.md` (required), `scripts/` (optional), `references/` (optional), `assets/` (optional), `agents/openai.yaml` (optional). Do not include scripts or assets unless they measurably improve reliability.**
  - _Why:_ Unnecessary supporting files add maintenance burden without improving skill behavior.
  - _Source:_ [Codex best-practices](https://developers.openai.com/codex/learn/best-practices)
- **Skills are discovered from: `.agents/skills` in CWD or parent dirs up to repo root (repo-scoped), `$HOME/.agents/skills` (user-level), `/etc/codex/skills` (admin), and system-bundled. Codex follows symlinked skill folders.**
  - _Why:_ Understanding discovery order is required to place skills in the right scope and debug missing skills.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)
- **Global preferences that apply across all repos go in `~/.codex/AGENTS.md`. Repo-level norms go in the project root `AGENTS.md`. Subdirectory overrides (`AGENTS.override.md`) apply to that subtree only.**
  - _Why:_ Layered scope inheritance lets team-wide conventions coexist with package-specific rules.
  - _Source:_ [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- **AGENTS.md files are concatenated root-to-cwd with blank lines between them. Files closer to the current directory take effective precedence because they appear later in the combined prompt. The combined size limit is 32 KiB (configurable via `project_doc_max_bytes`).**
  - _Why:_ Closer files override earlier guidance by appearing later in the merged prompt seen by the model.
  - _Source:_ [openai/codex docs](https://github.com/openai/codex/blob/main/docs/agents_md.md)
- **Within each directory, Codex checks for `AGENTS.override.md` first, then `AGENTS.md`, then fallback filenames registered in `project_doc_fallback_filenames`. At most one file per directory is included.**
  - _Why:_ The override file provides a mechanism for temporary high-priority rules without deleting the base file.
  - _Source:_ [openai/codex docs](https://github.com/openai/codex/blob/main/docs/agents_md.md)
- **Write imperative steps with explicit inputs and outputs in the SKILL.md body.**
  - _Why:_ Codex agents follow procedural instructions more reliably than open-ended capability descriptions.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)
- **Use skills for reusable processes. Keep AGENTS.md focused on durable project rules only. Do not bloat AGENTS.md with repeatable workflow content.**
  - _Why:_ AGENTS.md is static project context; skills are invocable, composable workflows. Mixing them degrades both.
  - _Source:_ [Codex customization](https://developers.openai.com/codex/concepts/customization)
- **When Codex makes repeated mistakes, codify corrections in AGENTS.md so future sessions inherit the fix.**
  - _Why:_ AGENTS.md persists across sessions; skills are invoked per-task. Persistent corrections belong in AGENTS.md.
  - _Source:_ [Codex customization](https://developers.openai.com/codex/concepts/customization)

## Progressive disclosure

- **Codex loads skills in three phases: (1) name+description+file path at discovery; (2) full SKILL.md body when selected; (3) scripts/references/assets only during execution. The initial skills list is capped at ~2% of the model's context window, or 8,000 characters when the context window is unknown.**
  - _Why:_ The budget applies only to the listing phase. When a skill is selected, the full SKILL.md is read regardless of the budget.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)
- **If many Codex skills are installed, descriptions are shortened first to fit the budget. For very large skill sets, some skills may be omitted entirely with a warning.**
  - _Why:_ Description front-loading and conciseness are the defense against omission from the listing.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)

## Invocation & triggering

- **Two Codex invocation modes: explicit (user names the skill via `/skills` or `$skill`) and implicit (Codex auto-selects when task description matches). Set `allow_implicit_invocation: false` in `agents/openai.yaml` to require explicit invocation.**
  - _Why:_ Side-effectful skills should require explicit invocation to prevent unintended automatic triggering.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)
- **Test prompts against the skill description to confirm correct trigger behavior before deploying.**
  - _Why:_ Description matching is the sole implicit-invocation mechanism. Unverified descriptions cause silent mis-triggering.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)

## Tool permissions (allowed-tools / disallowed-tools)

- **Declare tool dependencies (MCP servers) in `agents/openai.yaml` under `dependencies.tools` with `type`, `value`, `description`, `transport`, and `url`.**
  - _Why:_ Declared dependencies enable smoother tool availability when the skill is invoked, without assuming the tool is pre-configured globally.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)

## References & scripts

- **Prefer instructions over scripts as the Codex default. Use scripts only when you need deterministic behavior or external tooling.**
  - _Why:_ Instructions are more maintainable and readable. Scripts add complexity that is only justified for deterministic operations.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)
- **Register custom fallback filenames (e.g., `TEAM_GUIDE.md`, `.agents.md`) in `project_doc_fallback_filenames` in config.toml so existing team docs are recognized as instruction files without renaming.**
  - _Why:_ Teams with existing documentation should not need to rename it to get Codex to use it.
  - _Source:_ [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)

## Testing & evaluation

- **Do not try to cover every edge case upfront. Start with one representative task, get it working well, then turn that workflow into a skill. A good rule of thumb: if you keep reusing the same prompt or correcting the same workflow, it should become a skill.**
  - _Why:_ Premature comprehensiveness creates skills that are too broad before the core use case is validated.
  - _Source:_ [Codex best-practices](https://developers.openai.com/codex/learn/best-practices)
- **Verify AGENTS.md instruction loading by asking Codex to summarize current instructions (`codex --ask-for-approval never "Summarize current instructions."`). Use `--cd subdir` to confirm nested overrides function correctly.**
  - _Why:_ Instruction loading issues (empty files, unexpected overrides, size cap truncation) are silent without explicit verification.
  - _Source:_ [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- **Codex detects skill changes automatically. If an update does not appear, restart Codex. AGENTS.md instruction chains rebuild on every run — there is no cache to clear.**
  - _Why:_ Understanding live-reload vs restart requirements prevents confusion during development iteration.
  - _Source:_ [Codex skills.md](https://developers.openai.com/codex/skills.md)

## Anti-patterns

- **Do not create empty AGENTS.md files — Codex silently ignores them.**
  - _Why:_ Empty files appear in the filesystem but contribute nothing to the instruction chain.
  - _Source:_ [openai/codex docs](https://github.com/openai/codex/blob/main/docs/agents_md.md)
- **Do not place unexpected `.override.md` files in directories — they silently block discovery of the regular `AGENTS.md`. Check for unexpected override files if instructions are not loading as expected.**
  - _Why:_ Override files take priority. An unexpected override prevents the intended base file from loading.
  - _Source:_ [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- **Do not ignore truncation at the 32 KiB AGENTS.md size cap. Either raise `project_doc_max_bytes` or split large files across nested directories.**
  - _Why:_ Truncated instructions cause silent partial loading of guidance — the model proceeds as if the missing content does not exist.
  - _Source:_ [openai/codex docs](https://github.com/openai/codex/blob/main/docs/agents_md.md)
- **Do not include scripts or asset files in a Codex skill unless they measurably improve reliability.**
  - _Why:_ Supporting files add complexity. The benefit must outweigh the maintenance cost.
  - _Source:_ [Codex best-practices](https://developers.openai.com/codex/learn/best-practices)
- **Do not attempt comprehensive edge-case coverage before validating the core workflow. Do not graduate to automation before the skill is reliable in manual use.**
  - _Why:_ Premature automation of an unreliable workflow amplifies failures.
  - _Source:_ [Codex best-practices](https://developers.openai.com/codex/learn/best-practices)
