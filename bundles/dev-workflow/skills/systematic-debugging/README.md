# systematic-debugging

A disciplined root-cause debugging methodology — reproduce, isolate, hypothesize, verify — instead of guess-and-check. The escalation lane behind `debug`, which is the front door for first contact with a failure.

## Upstream

Derived from **[obra/superpowers](https://github.com/obra/superpowers)** (MIT).

| Field | Value |
|-------|-------|
| Source | [`skills/systematic-debugging/SKILL.md`](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md) |
| Upstream ref | `main` |
| Synced at commit | `030a222af19c` |
| Last synced | 2026-06-12 |
| License | MIT |

**Local modifications:** Adapted from obra/superpowers as a standalone, platform-neutral marketplace plugin. The four phases, the Iron Law, and the red flags are unchanged from upstream. Locally narrowed to the **escalation lane**: `description` and `when_to_use` now trigger on failed-fix and recurring-defect wording rather than on any bug, and an `## Entry Point` section names `debug` as the front door that hands cases here. That keeps the two skills' trigger phrases disjoint in this catalog — upstream ships no `debug` counterpart, so the split does not travel back.

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, diff [`skills/systematic-debugging/SKILL.md`](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md) on `main` since commit `030a222af19c`, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
