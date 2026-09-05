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

**Local modifications:** Adapted from Anthropic's official skills repo with a scoped authorization contract and long examples in references. The bundled evaluator remains in `scripts/evaluation.py`, with its guide in `references/evaluation.md`. It requires an explicitly configured model through `-m`/`--model` or `ANTHROPIC_MODEL` instead of a fixed default. Maintain these local behaviors when selectively incorporating upstream changes; the source marker records attribution to the adapted snapshot.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`skills/mcp-builder/SKILL.md`](https://github.com/anthropics/skills/blob/main/skills/mcp-builder/SKILL.md) on `main` since commit `ef740771ac90`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
