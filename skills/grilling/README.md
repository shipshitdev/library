# grilling

The reusable interview primitive: map a plan as a design tree, ask the whole frontier each round, recommend an answer, and stop when the frontier is empty.

Orchestrators such as `interview` and `shape` invoke this skill. They own repo grounding and the handoff artifact.

## Upstream

Derived from **[mattpocock/skills](https://github.com/mattpocock/skills)** (MIT).

| Field | Value |
|-------|-------|
| Source | [`skills/productivity/grilling/SKILL.md`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `8b78b531ab96` |
| Last synced | 2026-08-14 |
| License | MIT |

**Local modifications:** Adapted to house style: Contract block, platform-neutral imperative prose, round format without emoji, and composition with this catalog's `interview` / `shape` orchestrators. Attribution only — not a sync target.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`skills/productivity/grilling/SKILL.md`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) on `main` since commit `8b78b531ab96`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
