# context-degradation

Recognize, diagnose, and mitigate context-degradation patterns (lost-in-middle, poisoning, distraction, confusion, clash) in agent systems.

## Upstream

Derived from **[muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)** (MIT).

| Field | Value |
|-------|-------|
| Source | [`skills/context-degradation/SKILL.md`](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/context-degradation/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `25e1fa79a33f` |
| Last synced | 2026-06-13 |
| License | MIT |

**Local modifications:** Imported 2026-01-20 (this repo's commit ef42a98) from muratcankoylan/Agent-Skills-for-Context-Engineering at v1.0.0-era content. Ported forward 2026-06-13 to upstream HEAD (commit 25e1fa79a33f); local body now tracks upstream v2.1.0 — carried the 7-entry Gotchas section, claim-* evidence IDs, Examples 3-4, Model-Specific Degradation Thresholds table, and negative-activation routing. References to siblings not vendored here (context-compression, filesystem-context) were stripped so routing names only marketplace skills. Local divergence: scripts/degradation_detector.py adopts the upstream numpy->stdlib rewrite (dependency removed); references/patterns.md is byte-identical to upstream. To diff: compare the upstream path on main since commit 25e1fa79a33f.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`skills/context-degradation/SKILL.md`](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/context-degradation/SKILL.md) on `main` since commit `25e1fa79a33f`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
