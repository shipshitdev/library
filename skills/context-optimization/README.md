# context-optimization

Apply optimization techniques (compaction, observation masking, KV-cache, partitioning) to extend effective context capacity.

## Upstream

Derived from **[muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)** (MIT).

| Field | Value |
|-------|-------|
| Source | [`skills/context-optimization/SKILL.md`](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/context-optimization/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `cbc2c978133d` |
| Last synced | 2026-06-12 |
| License | MIT |

**Local modifications:** Ported to upstream v2.1.0 (2026-05-15 corpus, commit cbc2c978133d) on 2026-06-12 — body and references match upstream. Cross-references to upstream sibling skills not vendored here (context-compression, filesystem-context, project-development, latent-briefing) were removed so routing only names skills present in this marketplace. scripts/compaction.py carries two local hardening fixes over upstream (CodeRabbit-flagged, candidates to push back): ContextBudget now rejects total_limit<=0 and scales the reserved buffer so reservation_limit stays non-negative; calculate_cache_metrics now debits the unhit remainder of a partial cache hit from misses, where upstream counted only the hit fraction and so inflated hit_rate.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`skills/context-optimization/SKILL.md`](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/blob/main/skills/context-optimization/SKILL.md) on `main` since commit `cbc2c978133d`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
