# Open Source Checker — Full Guide

Reference material for the publish gate: the one-time audit of a private
repository at the moment it is proposed for public release.

Scope note: this guide covers what changes **once**, when a repository crosses
from private to public. Commit-time secret blocking, destructive-operation
gating, ignore rules, pre-commit hooks, and the history rewrite itself belong to
the `git-safety` skill and are not repeated here.

---

## 1. Preflight — Establish the Audit Scope

An audit that misses a ref misses everything in it. Fetch first.

```bash
git fetch --all --tags --prune

# Scope of the audit
git log --all --oneline | wc -l              # commits
git branch -a | wc -l                        # branches, local + remote
git tag -l | wc -l                           # tags
git stash list                               # NOT covered by --all
git count-objects -vH                        # repo size; large packs hide old blobs
```

Record these numbers. The verdict cites them, and they are what makes a
`PUBLISH` verdict auditable rather than a vibe.

Two refs that hide content from `--all`:

```bash
# Dangling and unreachable objects — a deleted branch's commits may still exist
git fsck --lost-found --unreachable 2>/dev/null | head -20

# Notes, if the team used them
git log --all --show-notes='*' --oneline | head
```

If the repository will be published by pushing a fresh clone rather than
flipping visibility, unreachable objects will not travel — note which path the
owner intends, because it changes what is in scope.

---

## 2. License and Attribution

### 2.1 The outgoing license

```bash
ls -1 LICENSE* COPYING* NOTICE* 2>/dev/null
head -5 LICENSE 2>/dev/null
grep -i '"license"' package.json 2>/dev/null
```

A public repository with no license grants no rights. Readers may look but
legally may not use, fork, or contribute. Confirm the owner has picked one
before the audit passes.

### 2.2 Dependency license compatibility

The outgoing license cannot be more permissive than what the strongest incoming
dependency license allows.

```bash
# JavaScript / TypeScript
bunx license-checker --summary
bunx license-checker --failOn 'GPL-3.0;AGPL-3.0;SSPL-1.0'

# Python
pip-licenses --summary

# Rust
cargo license --tsv | cut -f6 | sort | uniq -c

# Go
go-licenses report ./... 2>/dev/null
```

| Dependency license | Publishing under MIT / Apache-2.0 |
|--------------------|-----------------------------------|
| MIT, ISC, BSD-2/3 | Compatible. Keep the notice files. |
| Apache-2.0 | Compatible. Preserve `NOTICE` and patent terms. |
| MPL-2.0 | Compatible at file granularity; modified MPL files stay MPL. |
| LGPL | Compatible when dynamically linked; static linking pulls obligations in. |
| GPL-2.0 / GPL-3.0 | **Incompatible.** Distributing the combined work requires GPL. |
| AGPL-3.0 | **Incompatible**, and network use counts as distribution. |
| SSPL, BUSL, Elastic | **Not open source.** Source-available; check the terms directly. |
| "UNLICENSED" / none | **Blocker.** No grant exists — remove or get written permission. |

Devtime-only dependencies (test runners, linters, build tools) do not ship in
the artifact and rarely constrain the outgoing license. Runtime dependencies do.
Check which bucket each copyleft hit falls in before calling it a blocker.

### 2.3 Borrowed and vendored code

Snippets pasted from elsewhere carry their origin's terms whether or not anyone
recorded that.

```bash
grep -rniE 'adapted from|based on|copied from|taken from|source: https?:' \
  --include='*.*' . | grep -v node_modules | head -40

# Vendored trees that are not dependency-managed
find . -type d \( -name vendor -o -name third_party -o -name external \) \
  -not -path '*/node_modules/*'

# License headers already present
grep -rl 'SPDX-License-Identifier' --include='*.*' . | grep -v node_modules | head -20
```

For each hit: attribute it in a `NOTICE` or header, replace it with original
code, or remove it.

### 2.4 Copyright ownership

```bash
grep -rniE 'copyright.*[0-9]{4}' --include='*.*' . | grep -v node_modules \
  | sed -E 's/.*[Cc]opyright[^A-Za-z]*//' | sort -u | head -20
```

Confirm the named entity is the one publishing, that the year range is current,
and that headers are consistent. Code written under an employment agreement may
not be the author's to release — settle that before the flip, not after.

Ends when: license chosen and present, no incompatible runtime dependency, every
borrowed block attributed, copyright naming the publishing entity.

---

## 3. Secrets Across Full History

### 3.1 Tooling does the pattern matching

Hand-written regexes work for a staged diff of five files. They do not work
across thousands of commits — the false-negative rate is what gets repositories
burned. Run scanners over full history and triage their output.

**gitleaks**

```bash
# Full history, every ref
gitleaks detect --source . --verbose

# Machine-readable, for triage
gitleaks detect --source . --report-format json --report-path gitleaks.json

# Bound the scan to a range when re-auditing after a rewrite
gitleaks detect --source . --log-opts="HEAD~200..HEAD"

# Custom allowlist for known-fake fixture values
gitleaks detect --source . --config .gitleaks.toml
```

```toml
# .gitleaks.toml — allowlist fixtures, never real values
[extend]
useDefault = true

[[rules]]
id = "internal-domain"
description = "Internal hostname"
regex = '''[a-z0-9-]+\.(internal|corp|local)\b'''

[allowlist]
paths = [
  '''tests/fixtures/.*''',
  '''.*\.example$''',
]
```

**truffleHog** — verifies candidates against the live provider, so a hit means
the credential still works.

```bash
trufflehog git file://. --only-verified
trufflehog git file://. --include-detectors all      # widen, more noise
trufflehog git https://github.com/org/repo.git       # after publication, as a check
```

Run both. gitleaks has better entropy coverage; truffleHog tells you which hits
are live. A verified truffleHog hit is a rotate-now item.

### 3.2 All-refs commands the scanners complement

```bash
# Every file that ever existed in the repository
git log --all --pretty=format: --name-only --diff-filter=A | sort -u

# Sensitive filenames, with when they were added
git log --all --full-history --diff-filter=A \
  --pretty=format:"%h %ad %s" --date=short -- \
  "*.env" ".env" ".env.*" "credentials.json" "service-account*.json" \
  "*.pem" "*.key" "id_rsa*" "secrets.*" ".npmrc" "*.secret"

# Content added or removed anywhere in history
git log -p --all -S 'API_KEY' --source -- ':(exclude)*.lock'
git log -p --all -G 'AKIA[0-9A-Z]{16}' --source
```

### 3.3 Files deleted from the tree

The most common miss: someone removed `.env` in a later commit and assumed that
handled it.

```bash
# Everything ever deleted
git log --all --pretty=format: --name-only --diff-filter=D | sort -u \
  | grep -iE '\.(env|pem|key|secret)$|credentials|secrets\.'

# Recover the content of a deleted file to judge severity
git log --all --full-history --diff-filter=D -- path/to/file.env
git show <commit-before-deletion>:path/to/file.env
```

### 3.4 Stashes

`--all` does not cover the stash reflog. Stashes are local, so they do not
travel on publication — but they reveal what was being handled carelessly, and
the same values usually landed in a commit somewhere.

```bash
git stash list
for i in $(seq 0 $(($(git stash list | wc -l) - 1))); do
  echo "=== stash@{$i} ==="
  git stash show -p "stash@{$i}" 2>/dev/null | grep -iE '(api.?key|password|secret|token)' || true
done
```

### 3.5 Merge commits

A merge commit can introduce content present in neither parent — a conflict
resolved by hand-typing a value.

```bash
git log --all --merges --oneline | head -30
git diff <merge-commit>^1..<merge-commit>
git diff <merge-commit>^2..<merge-commit>
```

### 3.6 Every branch and tag

```bash
for branch in $(git branch -a | sed 's/^[* ]*//' | grep -v HEAD); do
  hits=$(git ls-tree -r --name-only "$branch" 2>/dev/null | grep -iE '\.(env|pem|key)$')
  [ -n "$hits" ] && printf '=== %s ===\n%s\n' "$branch" "$hits"
done

for tag in $(git tag -l); do
  hits=$(git ls-tree -r --name-only "$tag" 2>/dev/null | grep -iE '\.(env|pem|key)$')
  [ -n "$hits" ] && printf '=== tag %s ===\n%s\n' "$tag" "$hits"
done
```

Stale release branches are frequently the only ref still holding a config file
that `main` cleaned up years ago.

### 3.7 Triage

For each finding, record: the value's provider, the commit that introduced it,
whether the repository was ever public or shared, and whether truffleHog
verified it as live.

| Finding | Action |
|---------|--------|
| Live credential, any ref | Rotate immediately, then rewrite. Blocker. |
| Dead or already-rotated credential | Rewrite for hygiene. Blocker until confirmed dead. |
| Fixture or documented placeholder | Allowlist it in `.gitleaks.toml`. Not a blocker. |
| Internal-only value with no external auth (a dev seed password) | Judgment call; usually rewrite. |

Rotation and history rewriting are performed by the `git-safety` skill. This
audit produces the list; it does not run the rewrite.

Ends when: both scanners return clean across full history, every earlier hit has
a confirmed rotation, and stashes, merges, branches, and tags are each swept.

---

## 4. Private References

No scanner finds these. They are not credentials — they are internal facts that
were never meant to leave, and they are the pass that most often produces
findings in an otherwise clean repository.

### 4.1 Internal hosts and networks

```bash
# Internal TLDs
grep -rniE '\.(internal|corp|intranet|local|lan)\b' . | grep -v node_modules | head -40

# RFC1918 addresses
grep -rniE '\b(10\.[0-9]+|192\.168|172\.(1[6-9]|2[0-9]|3[01]))\.[0-9]+\.[0-9]+\b' . \
  | grep -v node_modules | head -40

# Staging and internal environments
grep -rniE '(staging|preprod|internal|admin|vpn)[.-][a-z0-9-]+\.(com|net|io|dev)' . \
  | grep -v node_modules | head -40
```

`127.0.0.1` and `localhost` are fine. A hostname that only resolves inside the
company is a finding.

### 4.2 People

```bash
# Company and personal email addresses in source
grep -rniE '[a-z0-9._%+-]+@(yourcompany|gmail|outlook)\.[a-z]{2,}' . \
  | grep -v node_modules | head -40

# Intent and blame left in comments
grep -rniE '(TODO|FIXME|HACK|XXX|NOTE)[:( ].*(ask|per|check with|@[a-z]+)' \
  --include='*.*' . | grep -v node_modules | head -40

# Slack and ticket references
grep -rniE '(slack\.com/archives|#[a-z-]+-team|JIRA-[0-9]+|[A-Z]{2,}-[0-9]{2,})' . \
  | grep -v node_modules | head -40
```

### 4.3 Commit metadata

Every author name and email in history becomes public with the repository. This
is frequently overlooked because it is not in any file.

```bash
git log --all --format='%an <%ae>' | sort -u
git log --all --format='%cn <%ce>' | sort -u
```

Options: accept it (most open-source projects do), or normalize identities with
a `.mailmap` — which changes the display name, not the underlying commit object.
Genuinely removing an email from history requires a rewrite via `git-safety`.

```
# .mailmap — display name and address remapping
Real Name <public@example.com> <internal@yourcompany.local>
```

Get consent from each contributor before publishing their address.

### 4.4 Customers and commercial detail

```bash
# Client names — supply the list; no generic pattern finds these
for name in "Acme Corp" "BigClient" "ProjectCodename"; do
  echo "=== $name ==="
  grep -rniF "$name" . --exclude-dir=node_modules --exclude-dir=.git | head -10
  git log --all --oneline --grep="$name" | head -10
done

# Production data leaked into fixtures
grep -rniE '(ssn|social.security|credit.?card|passport|date.?of.?birth)' \
  --include='*.json' --include='*.csv' --include='*.sql' . | head -20
```

Also check: pricing and discount logic, unreleased product names, feature flags
naming unannounced work, and comments describing internal roadmap or headcount.

### 4.5 Infrastructure identifiers

```bash
grep -rniE '\b[0-9]{12}\b' --include='*.tf' --include='*.yml' --include='*.yaml' . | head -20   # AWS account IDs
grep -rniE '(s3://|arn:aws:|projects/[a-z0-9-]+/)' . | grep -v node_modules | head -30
grep -rniE '(cluster|namespace|bucket)[-_ ]?(name)?[=: ]+["\x27][a-z0-9-]+' . | head -20
```

Account IDs and bucket names are not secrets, but they narrow an attacker's
target list. Decide deliberately rather than by omission.

### 4.6 The judgment rule

For each hit, ask: **would a stranger reading this learn something the company
would not say publicly?**

- A link to public documentation — not a finding.
- A link to the internal runbook wiki — finding.
- `localhost:3000` — not a finding.
- `deploy-01.eng.corp` — finding.
- A generic `TODO: refactor` — not a finding.
- `TODO: ask Priya why the Acme contract needs this` — finding, twice over.

Ends when: every category above has been searched and each hit is redacted,
replaced with a neutral placeholder, or explicitly accepted by the owner.

---

## 5. Publication Readiness

### 5.1 The first thirty seconds

```bash
ls -1 README* CONTRIBUTING* CODE_OF_CONDUCT* SECURITY* .env.example 2>/dev/null
grep -rniE 'internal|confidential|do not distribute|proprietary|ask the team|#eng' \
  README* docs/ 2>/dev/null | head -20
```

A README written for colleagues assumes access a stranger does not have. Rewrite
onboarding steps that route through internal Slack, wikis, or VPN.

### 5.2 Can an outsider actually run it?

- `.env.example` lists every variable the app reads, with safe placeholders
- Setup instructions reference public package registries only
- No step requires an internal service, VPN, or SSO tenant
- Seed and fixture data is synthetic

```bash
# Variables the code reads, versus what the example documents
grep -rhoE 'process\.env\.[A-Z_]+|os\.environ\[.[A-Z_]+' src/ 2>/dev/null \
  | grep -oE '[A-Z_]{3,}' | sort -u > /tmp/used-vars
grep -oE '^[A-Z_]+' .env.example 2>/dev/null | sort -u > /tmp/documented-vars
comm -23 /tmp/used-vars /tmp/documented-vars     # read but undocumented
```

### 5.3 CI and repository configuration

```bash
cat .github/CODEOWNERS 2>/dev/null                 # internal team handles
grep -rniE 'secrets\.[A-Z_]+' .github/workflows/ | sort -u
grep -rniE '(registry|repository|runs-on).*(internal|corp|self-hosted)' .github/ 2>/dev/null
cat .github/ISSUE_TEMPLATE/* 2>/dev/null | grep -iE 'internal|jira|slack'
```

Workflows referencing self-hosted runners or an internal registry will fail on
every fork. Either make them fork-safe or gate them behind a condition.

### 5.4 Repository-level settings

Not visible in the tree, and worth checking before the flip:

- Wiki content and its history
- Existing issues and pull-request discussions — these become public too
- Release artifacts and their notes
- Repository description, topics, and homepage URL
- Branch protection and required-check names that reference internal systems

Ends when: a reader with no internal access can install, run, and contribute
from what is in the repository.

---

## 6. Verdict Report Template

```markdown
# Open Source Readiness — <repo>

Audited: <date> · Scope: <n> commits, <n> branches, <n> tags, <n> stashes

## Verdict: BLOCK | PUBLISH

## Pass 1 — License and attribution
- Outgoing license: <MIT | none — BLOCKER>
- Dependency conflicts: <n> (<list AGPL/GPL runtime deps>)
- Unattributed borrowed code: <n> locations

## Pass 2 — Secrets in history
- gitleaks: <n> findings · truffleHog verified: <n>
- Introduced in: <commits> · Deleted-but-present: <files>
- Rotation required: <list>

## Pass 3 — Private references
- Internal hosts: <n> · Employee references: <n>
- Customer names: <n> files, <n> commit messages
- Distinct author emails in history: <n>

## Pass 4 — Publication readiness
- README outsider-ready: <yes/no> · .env.example complete: <yes/no>
- CI fork-safe: <yes/no> · CODEOWNERS internal handles: <n>

## Blockers
1. <finding> → <action> → <owner>

## Handoff
- Rotate now: <credentials>
- Then run: git-safety clean — <paths to strip>
- Re-run passes 2 and 3 after the rewrite (commit hashes change)
```

---

## 7. Re-Audit After a Rewrite

A history rewrite changes every commit hash downstream of the earliest rewritten
commit. Findings referencing old hashes are stale, and the rewrite itself can
introduce new problems.

```bash
# Confirm the value is gone from every ref
git log --all --full-history -- .env             # expect empty
git log -p --all -S '<rotated-value>' --source   # expect empty

# Re-run the scanners against the new history
gitleaks detect --source . --verbose
trufflehog git file://. --only-verified

# Confirm the ref counts match pre-rewrite expectations
git log --all --oneline | wc -l
git tag -l | wc -l
```

Verify against a fresh clone of the rewritten remote, not the local working
copy — the local repository keeps the old objects in its reflog and packs until
they are pruned, which can mask an incomplete rewrite.

```bash
git clone --mirror <remote-url> /tmp/verify-clone
gitleaks detect --source /tmp/verify-clone --verbose
```

---

## 8. Quick Reference

```bash
# === PREFLIGHT ===
git fetch --all --tags --prune
git log --all --oneline | wc -l

# === PASS 1: LICENSE ===
ls LICENSE* && bunx license-checker --failOn 'GPL-3.0;AGPL-3.0'

# === PASS 2: HISTORY SECRETS ===
gitleaks detect --source . --verbose
trufflehog git file://. --only-verified
git log --all --pretty=format: --name-only --diff-filter=D | sort -u | grep -iE '\.env|\.pem'

# === PASS 3: PRIVATE REFERENCES ===
grep -rniE '\.(internal|corp|local)\b' . | grep -v node_modules
git log --all --format='%an <%ae>' | sort -u

# === PASS 4: READINESS ===
ls README* .env.example && cat .github/CODEOWNERS

# === HANDOFF ===
# Rotation, history rewrite, force-push, and the ongoing commit-time guard
# are the git-safety skill's job — this audit produces the list only.
```
