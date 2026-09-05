# pstack

Lauren Tan's poteto-mode recut as a portable playbook orchestrator. Matches a task to a named playbook and routes to how, why, architect, arena, swarm, and related skills.

## Coexistence

Keep one orchestrator implementation and a consistent set of companion skills
for each run. The public adaptation resolves companions through the active skill
catalog; it does not require the upstream plugin. Installed upstream and public
adapted skills can coexist, but their provider routing and action gates may differ.
Do not silently mix them or treat this snapshot's attribution as a live dependency.

## Upstream

Derived from **[Lauren Tan's pstack](https://github.com/cursor/plugins/tree/main/pstack)** (MIT), shipped in [cursor/plugins](https://github.com/cursor/plugins).

| Field | Value |
|-------|-------|
| Source | [`pstack/skills/poteto-mode/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `bdf7aa355337` |
| Last synced | 2026-08-26 |
| License | MIT |

**Local modifications:** Recut for this catalog: model-agnostic capability tiers, no Cursor-only APIs, Graphite land paths, or named models, house-style Contract blocks, and routing to existing shipshitdev skills. Attribution only — not a sync target.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`pstack/skills/poteto-mode/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) on `main` since commit `bdf7aa355337`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
