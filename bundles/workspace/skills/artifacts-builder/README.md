# artifacts-builder

Build elaborate multi-component claude.ai HTML artifacts with shared UI and state management.

## Upstream

Derived from **[anthropics/skills](https://github.com/anthropics/skills)** (Apache-2.0).

| Field | Value |
|-------|-------|
| Source | [`skills/web-artifacts-builder/SKILL.md`](https://github.com/anthropics/skills/blob/main/skills/web-artifacts-builder/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `ef740771ac90` |
| Last synced | 2026-06-12 |
| License | Apache-2.0 |

**Local modifications:** Vendored from Anthropic's `web-artifacts-builder` (renamed locally to `artifacts-builder`); the shared-UI import was repointed to `@agenticindiedev/ui` for this marketplace. Otherwise tracks upstream.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`skills/web-artifacts-builder/SKILL.md`](https://github.com/anthropics/skills/blob/main/skills/web-artifacts-builder/SKILL.md) on `main` since commit `ef740771ac90`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
