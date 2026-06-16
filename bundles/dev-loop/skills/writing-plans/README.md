# writing-plans

Turn a spec into a bite-sized, TDD-structured implementation plan that agentic workers can execute reliably.

## Upstream

Derived from **[obra/superpowers](https://github.com/obra/superpowers)** (MIT).

| Field | Value |
|-------|-------|
| Source | [`skills/writing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `f2cbfbefebbf` |
| Last synced | 2026-06-12 |
| License | MIT |

**Local modifications:** Vendored as a standalone, platform-neutral marketplace plugin (Claude Code + Codex). The prior `author: Ship Shit Dev` frontmatter was incorrect and has been removed — this skill derives from obra/superpowers. **Storage diverges from upstream** (`metadata.version` `1.1.0`): the plan is posted as a `## Implementation Plan` comment on the work/PRD GitHub issue (issue-as-source-of-truth), not saved to a local `docs/plans/*.md` file. This aligns the skill with the dev loop — the executor and both dispatch lanes (`agent-dispatch.yml`, `codex-dispatch.yml`) read the issue's comments, so the plan crosses to CI for either engine. **Preserve this divergence on future syncs** — do not let an upstream pull re-introduce the `docs/plans/` default.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`skills/writing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) on `main` since commit `f2cbfbefebbf`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
