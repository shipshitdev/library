# deslop

Strip AI slop from code, product surfaces, and prose. Code slop is the default. `--product` adds the unfinished-app pass. `prose` cuts AI tells from writing. `ui` audits design-system primitives.

The prose catalog lives in `references/prose-slop.md` so other skills can point at it without firing this skill.

## Upstream

Prose-slop rigor is derived from **[Lauren Tan's pstack](https://github.com/cursor/plugins/tree/main/pstack)** `unslop` skill (MIT), shipped in [cursor/plugins](https://github.com/cursor/plugins). Code, product, and UI slop are in-house.

| Field | Value |
|-------|-------|
| Source | [`pstack/skills/unslop/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `bdf7aa355337` |
| Last synced | 2026-08-26 |
| License | MIT |

**Local modifications:** Renamed the catalog skill to `deslop`; kept the code/product/UI passes, Contract block, and confirmation gate. Recut pstack `unslop` into `prose` mode and `references/prose-slop.md`. No Cursor-only APIs. Attribution only — not a sync target.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`pstack/skills/unslop/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md) on `main` since commit `bdf7aa355337`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
