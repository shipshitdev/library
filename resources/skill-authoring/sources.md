# Sources

First-hand, primary documentation only — vendor docs and vendor engineering posts. No third-party blog posts or tutorials. Gathered and read 2026-06-12 (13 reachable of 16 discovered).

- **[Extend Claude with skills](https://code.claude.com/docs/en/skills)** — Anthropic
  - Full Claude Code skills authoring reference: directory layout, all frontmatter fields with semantics, invocation control, subagent execution, dynamic context injection, and troubleshooting.
- **[Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)** — Anthropic
  - Detailed authoring guidance: frontmatter validation rules, description writing, progressive disclosure, allowed-tools MCP syntax, directory layout, naming conventions, evaluation-driven iteration, and explicit anti-patterns.
- **[Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)** — Anthropic
  - Three-level progressive disclosure model, frontmatter constraints, cross-surface portability, environment differences (claude.ai vs Claude API vs Claude Code), and skill-scope table.
- **[Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)** — Anthropic Engineering
  - Origin post for Agent Skills: progressive disclosure design rationale, skill-as-onboarding-guide mental model, security audit guidance, and evaluation-first development methodology.
- **[anthropics/skills — canonical open standard spec (agentskills.io)](https://github.com/anthropics/skills)** — Anthropic
  - Formal SKILL.md spec with strict frontmatter syntax rules, name validation constraints, description imperative-framing guidance, triggering eval methodology with train/validation split, and Gotchas section pattern.
- **[Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)** — Anthropic Engineering
  - Tool design principles that apply to skill-bundled scripts: unambiguous naming, high-signal return values, namespace prefixing, error message specificity, and avoiding bloated tool sets.
- **[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** — Anthropic Engineering
  - General agent context principles: minimal-set philosophy, XML/Markdown section structure, dynamic loading via identifiers, tool set minimalism, few-shot examples, and compaction strategies.
- **[Codex Skills reference](https://developers.openai.com/codex/skills)** — OpenAI
  - Codex SKILL.md structure, three-phase progressive loading, implicit/explicit invocation, agents/openai.yaml tool dependency declarations, and four explicit best practices.
- **[Codex Skills authoring (skills.md)](https://developers.openai.com/codex/skills.md)** — OpenAI
  - Full Codex skills authoring page: directory layout, scoped discovery locations, invocation modes, allow_implicit_invocation, context budget cap (2% / 8k chars), and agents/openai.yaml UI metadata.
- **[Codex customization concepts](https://developers.openai.com/codex/concepts/customization)** — OpenAI
  - Two-tier model (AGENTS.md for durable rules, Skills for reusable workflows), three-phase loading rationale, and explicit AGENTS.md vs Skills division of responsibility.
- **[Codex best practices](https://developers.openai.com/codex/learn/best-practices)** — OpenAI
  - Skill authoring best practices: description-first design, single-job scope, start-small iteration, stabilize-then-package workflow, and personal vs team storage tiers.
- **[AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)** — OpenAI
  - How Codex discovers, merges, and applies AGENTS.md across global/project/subdirectory scopes, file naming, 32 KiB size limit, override semantics, and verification commands.
- **[openai/codex — docs/agents_md.md](https://github.com/openai/codex/blob/main/docs/agents_md.md)** — OpenAI
  - Canonical AGENTS.md discovery chain implementation details: two-scope hierarchy, override file semantics, size cap enforcement, fallback filename config, and session rebuild behavior.

## Provenance

- Discovered: 16 first-hand sources. Read: 13. Practices extracted: 12 fields + the rule sets in [anthropic.md](anthropic.md) and [codex.md](codex.md).
- The canonical open standard is **agentskills.io** (mirrored at `github.com/anthropics/skills`). Anthropic and OpenAI both build on it.
