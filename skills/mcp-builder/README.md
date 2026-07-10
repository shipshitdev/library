# mcp-builder

Build Model Context Protocol servers — tools, resources, and prompts — to extend agent capabilities.

## Upstream

Derived from **[anthropics/skills](https://github.com/anthropics/skills)** (Apache-2.0).

| Field | Value |
|-------|-------|
| Source | [`skills/mcp-builder/SKILL.md`](https://github.com/anthropics/skills/blob/main/skills/mcp-builder/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `ef740771ac90` |
| Last synced | 2026-06-12 |
| License | Apache-2.0 |

**Local modifications:** Vendored from Anthropic's official skills repo as a standalone marketplace plugin. One behavioral change: `scripts/evaluation.py` and `references/evaluation.md` no longer pin a specific model default — the eval model now comes from the `ANTHROPIC_MODEL` env var (or `-m`), so the skill never ships a version that goes stale. On re-sync, re-apply this de-pinning if upstream still hardcodes a model ID; restructured 2026-07-10: long examples moved to references/.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`skills/mcp-builder/SKILL.md`](https://github.com/anthropics/skills/blob/main/skills/mcp-builder/SKILL.md) on `main` since commit `ef740771ac90`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
