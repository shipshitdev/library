# tdd

Test-driven development with a red-green-refactor loop. Build or fix one vertical slice at a time, through the public interface. A cheap local path writes the failing check first. An expensive path names why and uses the closest executable proof.

## Upstream

Derived from **[mattpocock/skills](https://github.com/mattpocock/skills)** (MIT), with bug-fix rigor adapted from **[Lauren Tan's pstack](https://github.com/cursor/plugins/tree/main/pstack)** (MIT).

| Field | Value |
|-------|-------|
| Source | [`skills/engineering/tdd/SKILL.md`](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `8b78b531ab96` |
| Last synced | 2026-08-26 |
| License | MIT |

**Also adapted from:** [`pstack/skills/tdd/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/tdd/SKILL.md) at `cursor/plugins` `bdf7aa355337` (2026-08-26). Cheap-path gate, skip-when-impractical, failing-before evidence, and the red-then-green commit story.

**Local modifications:** Adapted to house style: Contract block, vertical-slice and mocking rules, bug-fix path via `debug`, a pointer at `codebase-design` for seam vocabulary, and pstack's cheap-path / prove-it-works discipline. Attribution only — not a sync target.

**Checking for upstream changes:** when either upstream has moved ahead of the synced marker above, diff the mattpocock source on `main` since commit `8b78b531ab96` and the pstack source on `main` since commit `bdf7aa355337`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
