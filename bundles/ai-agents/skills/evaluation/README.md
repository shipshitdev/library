# evaluation

Build evaluation frameworks for agent systems — deterministic validation plus model-judged quality, with attention to token/tool/model performance drivers.

## Upstream

Derived from **[muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)** (MIT).

| Field | Value |
|-------|-------|
| Source | [`skills/evaluation/SKILL.md`](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/evaluation/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `969441a5996a` |
| Last synced | 2026-01-20 |
| License | MIT |

**Local modifications:** Imported 2026-01-20 (this repo's commit ef42a98) from muratcankoylan/Agent-Skills-for-Context-Engineering at the v1.0.0-era content; the pinned commit 969441a5996a is the earliest upstream commit at this path and a verified ancestor of the vendored body. Local body is v1.0.0 and has NOT been ported forward. Upstream has since advanced to v1.2.0 (corpus commit cbc2c978133d, 2026-05-19 'v2.3.0 release'), adding a deterministic-validation concept, Examples 3-4 (deterministic gate + quality-gate YAML), an 8-entry Gotchas section, a claim-evaluation-browsecomp-variance ID, a 'Do not activate' block routing to advanced-evaluation, context-degradation, and a sibling not vendored here (harness-engineering); upstream also softened the local Performance Drivers table's concrete percentages (80%/~10%/~5%) to qualitative labels. Tracked for a future sync; on port, strip refs to non-vendored siblings. To diff: compare the upstream path on main since commit 969441a5996a.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`skills/evaluation/SKILL.md`](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/evaluation/SKILL.md) on `main` since commit `969441a5996a`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
