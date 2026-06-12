# Upstream Tracking

> **Purpose:** Every skill in this marketplace that was *derived* from someone else's work records where it came from, so we can check whether the original author shipped improvements worth porting home. This file is the index; each derived skill also carries machine-readable provenance in its `SKILL.md` `metadata:` block and a human-readable `## Upstream` section in its `README.md`.

## How provenance works

Three layers, kept in sync:

1. **`SKILL.md` frontmatter** — under `metadata:`: `source` (the exact upstream file URL), `upstream_repo`, `upstream_ref`/`upstream_commit` (rolling upstreams) or `upstream_version`/`upstream_latest` (tagged upstreams), `last_synced`, `license`.
2. **`README.md` `## Upstream` section** — the same facts in a table plus a "Checking for upstream changes" instruction.
3. **The validator** — `scripts/validate-skill-sync.sh` `check_provenance()`: any skill with `metadata.source` must have a README `## Upstream` section and a `last_synced` ≤ 90 days old, else it warns (non-fatal).

**Two provenance modes:**

- **`tagged`** — upstream cuts releases (e.g. `skill-vX.Y.Z`). We pin `upstream_version` (forked-at tag) and record `upstream_latest`. Check = diff against the forked-at tag.
- **`rolling`** — upstream ships on `main`/`master` with no releases. We pin `upstream_commit` (12-char SHA). Check = diff the path since that commit.

**Honesty rule:** never record an upstream that wasn't verified by fetching the real file. A guessed URL is worse than none — the whole point is to diff against a *real* source. Unverifiable → treat as in-house.

## Checking for upstream changes (general recipe)

Rolling upstream:

```bash
# latest commit that touched the upstream path
gh api 'repos/<owner>/<repo>/commits?path=<path>&per_page=1' --jq '.[0].sha[0:12]'
# if it differs from metadata.upstream_commit, diff and port:
gh api 'repos/<owner>/<repo>/compare/<synced_commit>...<latest_commit>' --jq '.files[].filename'
```

Tagged upstream: compare the repo's latest `skill-v*` tag against `metadata.upstream_version`, then diff the file at each tag.

After porting anything worth bringing home: bump `metadata.upstream_commit` (or `upstream_version`) **and** `metadata.last_synced` in both `SKILL.md` and the README table.

---

## Bucket 1 — External upstreams (26 skills, public + trackable)

These derive from third-party public repos. Diff against the pinned marker to find new upstream work.

### pbakaus/impeccable — Apache-2.0 — `tagged` (forked at `skill-v2.1.1`)

Design-quality reference skills. Vendored standalone; these never invoked the `/impeccable` orchestrator (the original dependency that was removed).

| Skill | Upstream path |
|-------|---------------|
| audit | `skill/reference/audit.md` |
| clarify | `skill/reference/clarify.md` |
| critique | `skill/reference/critique.md` |
| layout | `skill/reference/layout.md` |
| polish | `skill/reference/polish.md` |
| quieter | `skill/reference/quieter.md` |
| shape | `skill/reference/shape.md` |

### obra/superpowers — MIT — `rolling` (`main`)

Agent workflow skills. **The prior `author: Ship Shit Dev` frontmatter on three of these was incorrect and has been removed** — they are obra/superpowers ports, not in-house.

| Skill | Synced commit |
|-------|---------------|
| writing-plans | `f2cbfbefebbf` |
| systematic-debugging | `030a222af19c` |
| verification-before-completion | `48410c7f1973` |
| receiving-code-review | `1455ac0631e2` |
| finishing-a-development-branch | `f2cbfbefebbf` |

### anthropics/skills — Apache-2.0 — `rolling` (`main`)

| Skill | Synced commit | Note |
|-------|---------------|------|
| frontend-design | `2235be7c60b5` | |
| mcp-builder | `ef740771ac90` | |
| skill-creator | `b0cbd3df1533` | |
| artifacts-builder | `ef740771ac90` | upstream name is `web-artifacts-builder`; shared-UI import repointed to `@agenticindiedev/ui` |
| theme-factory | `ef740771ac90` | |
| internal-comms | `ef740771ac90` | |

### Dimillian/Skills — MIT — `rolling` (`main`)

| Skill | Synced commit |
|-------|---------------|
| react-component-performance | `3db84e63d050` |

### vercel-labs/agent-browser — Apache-2.0 — `rolling` (`main`)

| Skill | Synced commit |
|-------|---------------|
| agent-browser | `d33bdb36f3f7` |

### muratcankoylan/Agent-Skills-for-Context-Engineering — MIT — `rolling` (`main`)

Ported to upstream v2.x on **2026-06-12** (commit `cbc2c978133d`, 2026-05-15 corpus): body, references, and scripts now match upstream. Cross-references to upstream sibling skills **not vendored here** (`context-compression`, `filesystem-context`, `project-development`, `latent-briefing`) were stripped so routing only names skills present in this marketplace. Re-check by diffing the upstream path since `cbc2c978133d`.

| Skill | Synced commit | Local version |
|-------|---------------|---------------|
| context-fundamentals | `cbc2c978133d` | v2.2.0 (routing framework + gotchas) |
| context-optimization | `cbc2c978133d` | v2.1.0 |

### pproenca/dot-skills — MIT — `rolling` (`master`)

| Skill | Upstream path | Synced commit |
|-------|---------------|---------------|
| shadcn | `skills/.curated/shadcn/SKILL.md` | `b94ecb3dae52` |
| tailwind | `skills/.curated/tailwind/SKILL.md` (formerly `tailwindcss-v4-style`) | `91a64a6e7d49` |

### ⚠️ License flags

Two external upstreams ship **no LICENSE file** — content is all-rights-reserved by default and redistribution permission is unconfirmed. Verified by hand (GitHub license API returns 404, repo root has no LICENSE/COPYING):

| Skill | Upstream | Status |
|-------|----------|--------|
| changelog-generator | ComposioHQ/awesome-claude-skills | no LICENSE — **review before relying on it** |
| humanizer | ankshvayt/humanizer | no LICENSE — **review before relying on it** |

These are tracked for *provenance*, not cleared for *redistribution*. Decide whether to keep, relicense-on-request, or replace.

---

## Bucket 2 — Internal ports from private `vitae` repo (4 skills)

Ported from Vincent's own private spec-pipeline repo. No public upstream → nothing to diff externally, so no `metadata.source` and no `## Upstream` README (validator-exempt by design). Listed here for completeness.

| Skill | Origin |
|-------|--------|
| writing-prds | private `vitae` spec-pipeline |
| prd-quality-gate | private `vitae` spec-pipeline |
| context-engineering | private `vitae` spec-pipeline |
| execution-debugging | private `vitae` spec-pipeline |

If `vitae` ever goes public, promote these to Bucket 1 with a real `source` + commit.

---

## Bucket 3 — Own-repo re-homes & name-collisions (informational)

Not third-party — no external author to track — but worth recording so they aren't mistaken for imports.

| Skill | Note |
|-------|------|
| x-algorithm-optimizer | Re-homed from Vincent's own public `shipshitdev/library` (commit `c4345ca`, "import 40 external skills"). Own work — no third-party upstream. |
| executing-plans | Name collides with obra/superpowers' `executing-plans`, but this is the marketplace's own in-house skill (v2.1.0), **not** a port. Do not auto-attribute it to superpowers. |

---

## Bucket 4 — In-house original (≈148 skills)

Everything else (≈148 of 178) is Ship Shit Dev's own work — the solo-founder GTM + engineering toolkit. No upstream, no `metadata.source`, validator-exempt. These were classified by a 144-agent verification sweep that defaulted to in-house and only marked a skill external after fetching and matching a real upstream file.

---

## Maintenance

- **Re-verify cadence:** `last_synced` older than 90 days trips a validator warning. When you see one, run the check recipe above.
- **Adding a new import:** record provenance in `scripts/provenance-manifest.json`, run `python3 scripts/apply-provenance.py scripts/provenance-manifest.json`, then add a row here.
- **Source of truth for ports:** git commit messages (e.g. PR #16 documented the original spec-pipeline ports) are the highest-precision provenance signal — consult them before trusting frontmatter labels, which have been wrong before.

*Last updated: 2026-06-12.*
