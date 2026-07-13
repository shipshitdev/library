# advanced-evaluation

Master LLM-as-a-Judge techniques — direct scoring, pairwise comparison, rubric generation, and bias mitigation (position, length, verbosity, authority).

## Upstream

Derived from **[muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)** (MIT).

| Field | Value |
|-------|-------|
| Source | [`skills/advanced-evaluation/SKILL.md`](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/advanced-evaluation/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `25e1fa79a33f` |
| Last synced | 2026-06-13 |
| License | MIT |

**Local modifications:** Imported 2026-01-20 (this repo's commit ef42a98) from muratcankoylan/Agent-Skills-for-Context-Engineering at v1.0.0-era content (then pinned to creation commit 0b9a3b81bfea). Ported forward 2026-06-13 to upstream HEAD (commit 25e1fa79a33f); local body now tracks upstream v2.1.0 — carried full direct-scoring and pairwise prompt templates, the Metric Selection Framework table, three worked JSON examples, a 10-item Guidelines section, 8-entry Gotchas, a Scaling Evaluation section, the claim-advanced-evaluation-position-swap ID, and a fully rewritten scripts/evaluation_example.py. references/full-guide.md was renamed to references/evaluation-pipeline.md to match upstream. Reference to a sibling not vendored here (harness-engineering) was stripped; cross-links to tool-design (vendored) are retained. Local divergence: concrete vendor model names in references were genericized. To diff: compare the upstream path on main since commit 25e1fa79a33f; restructured 2026-07-10: long examples moved to references/.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`skills/advanced-evaluation/SKILL.md`](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/advanced-evaluation/SKILL.md) on `main` since commit `25e1fa79a33f`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
