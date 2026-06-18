# Repo Gap Analysis — this repo vs. official guidance

How `shipshitdev/skills` measures against the first-hand Anthropic + OpenAI Codex guidance captured in this directory. Audited 2026-06-12 against `.agents/memory/system/skill-standards.md`, `.agents/memory/system/platform-adaptations.md`, `.agents/memory/system/skill-management.md`, and `scripts/validate-skill-sync.sh`.

**Verdict:** the repo's standards are strong and substantially aligned with the official spec — and in places (platform-neutral writing rules, Contract blocks, dual Claude+Codex validation) go beyond it. The gaps below are mostly *currency* drift: the official docs moved (new fields, live bugs) since the standards were written.

## Where the repo already matches the official guidance

- `name` / `description` constraints, no-consecutive-hyphens, directory-name match. ✓
- `description` ≤ 1,024 chars and combined `description` + `when_to_use` ≤ 1,536 chars. ✓
- `version` / `tags` confined to the `metadata` block as strings. ✓
- `disable-model-invocation` for side-effectful skills; `user-invocable: false` for background skills. ✓
- Progressive disclosure with a < 500-line SKILL.md and detail pushed to `references/`. ✓
- Imperative, tool-name-free, platform-neutral writing style (the repo's own value-add; stricter than either vendor requires). ✓
- `plugin.json` kept in sync; bundles regenerated, never hand-edited. ✓

## Gaps (official guidance not yet reflected here)

Severity: **S1** = correctness/safety (a current rule or live bug the repo contradicts or omits); **S2** = missing-but-useful; **S3** = minor wording.

| # | Sev | Gap | Repo location | Official source |
|---|-----|-----|---------------|-----------------|
| G1 | S1 | `paths` is presented as usable, with no warning that it is **currently broken** — skills with `paths` set become undiscoverable (issue #49835, as of v2.1.84). Correct monorepo scoping is a nested `.claude/skills/` dir. | `skill-standards.md` line 32; validator allows `paths` silently | [Claude Code docs](https://code.claude.com/docs/en/skills) |
| G2 | S1 | `disallowed-tools` is a valid Claude Code field (removes tools from the pool while a skill is active — e.g. block `AskUserQuestion` in autonomous loops) but is **absent from the validator's `allowed_fields`**, so any skill using it gets flagged "Unsupported top-level frontmatter field." Also undocumented in the standards. | `validate-skill-sync.sh` lines 138–156; `skill-standards.md` extension table | [Claude Code docs](https://code.claude.com/docs/en/skills) |
| G3 | S1 | `allowed-tools` is described only as "tools without per-use prompts," which reads as a sandbox. It is an **auto-approve allowlist, not a restriction**: unlisted tools stay callable and fall through to normal permission prompts. Narrowing it does not block anything. | `skill-standards.md` line 158 | [Claude Code docs](https://code.claude.com/docs/en/skills) |
| G4 | S1 | The standards' own example frontmatter models `allowed-tools: Bash(git *)`, which auto-approves **every** git subcommand including `push`, `commit`, `reset`, `branch -D`. Read-only skills should use per-subcommand colon patterns (`Bash(git log:*)`). | `skill-standards.md` line 49 | [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| G5 | S2 | `context: fork` lacks two caveats: a guidelines-only skill (no actionable task) returns **empty output** when forked, and runtime enforcement may be incomplete via the Skill tool (issue #17283). | `skill-standards.md` line 29 | [Claude Code docs](https://code.claude.com/docs/en/skills) |
| G6 | S2 | `name` constraint omits the **reserved-word** rule: no `anthropic` or `claude` in the name. | `skill-standards.md` line 13 | [anthropics/skills spec](https://github.com/anthropics/skills) |
| G7 | S3 | `description` guidance says "front-load" (good) but not "**write in third person**," which the official best-practices call out explicitly. | `skill-standards.md` lines 14, 126–146 | [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| G8 | S3 | No guidance to use **fully-qualified `ServerName:tool_name`** for MCP tools in `allowed-tools` / instructions, which prevents "tool not found" when multiple MCP servers are present. | `skill-standards.md` allowed-tools row | [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| G9 | S3 | No stated rule that file references stay **one level deep** (no A→B→C reference chains), which the official progressive-disclosure guidance requires. | `skill-standards.md` structure section | [Claude best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |

## Recommended edits (highest leverage first)

1. **Validator (G2):** add `disallowed-tools` to `allowed_fields` in `scripts/validate-skill-sync.sh`. One-line fix; unblocks a legitimate field.
2. **Validator (G1, optional):** emit a warning when `paths:` is present, pointing at the nested-`.claude/skills/` workaround, until #49835 is confirmed fixed.
3. **skill-standards.md (G1, G3, G4, G5):** annotate `paths` and `context: fork` as currently buggy; rewrite the `allowed-tools` row to say "allowlist, not sandbox"; change the example away from `Bash(git *)` to a scoped pattern; add the reserved-word rule to `name`.
4. **skill-standards.md (G7-G9):** small additions — third-person descriptions, MCP qualified names, one-level reference depth.

These are documentation/validator changes only — no shipped skill needs to change to be correct today. Treat this file as the checklist for a follow-up PR against `.agents/memory/system/`.

## Method

Findings are grounded in the 13 first-hand sources listed in [sources.md](sources.md) and cross-checked against the live repo files named above. Live-bug claims (#49835, #17283) and version-specific behavior are flagged as time-sensitive in [checklist.md](checklist.md#open-questions--known-issues) — re-verify against the current Claude Code release before acting.
