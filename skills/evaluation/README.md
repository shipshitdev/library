# evaluation

Build evaluation frameworks for agent systems — deterministic validation plus model-judged quality, with attention to token/tool/model performance drivers.

## Upstream

Derived from **[muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)** (MIT).

| Field | Value |
|-------|-------|
| Source | [`skills/evaluation/SKILL.md`](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/evaluation/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `25e1fa79a33f` |
| Last synced | 2026-06-13 |
| License | MIT |

**Local modifications:** Imported 2026-01-20 (this repo's commit ef42a98) from muratcankoylan/Agent-Skills-for-Context-Engineering at v1.0.0-era content. Ported forward 2026-06-13 to upstream HEAD (commit 25e1fa79a33f); local body now tracks upstream v1.2.0 — carried the deterministic-validation concept, Examples 3-4 (deterministic gate + quality-gate dimensions), 8-entry Gotchas, the claim-evaluation-browsecomp-variance ID, and the softened Performance Drivers table (concrete 80%/~10%/~5% -> qualitative Primary/Secondary labels). Reference to a sibling not vendored here (harness-engineering) was stripped. Local divergence: scripts/evaluator.py adopts the upstream citation-detection fix (naive bracket-matching -> academic-citation regex). references/metrics.md is byte-identical to upstream. A 2026-06-13 review-hardening pass (CodeRabbit on PR #21) further diverges scripts/evaluator.py: evaluation_history and samples are now bounded deques (10k/50k) to cap memory growth, and two no-op f-string prefixes were removed (Ruff F541) — candidates to push upstream. To diff: compare the upstream path on main since commit 25e1fa79a33f.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`skills/evaluation/SKILL.md`](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/evaluation/SKILL.md) on `main` since commit `25e1fa79a33f`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
