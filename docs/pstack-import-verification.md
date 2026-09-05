# Pstack import verification

The source ledger covers 184 Open Pstack files and 158 files from the original
Cursor Pstack subtree. Each file has a canonical disposition. Archived source
coverage is not a claim that every harness supports every workflow.

## Automated evidence

The repository regression suite exercises source integrity, complete mappings,
destination changes, executable bits, candidate additions and removals, local
conflicts, immutable candidate output, archive path safety, and packaging that
excludes installed dependencies. See:

- `scripts/tests/test_pstack_sync.py`
- `scripts/tests/test_bundle_resources.py`
- `scripts/tests/test_pstack_model_boundary.py`
- `scripts/tests/test_skill_composition.py`

The packaged runtime retains upstream watcher, orchestration, bootstrap, plan
checker and provider-runner tests. Its CLI requires explicit provider, model and
effort values. Provider alias parsing and receipt fixtures are compatibility data;
they do not select runtime defaults.

Run the repository suite and the packaged runtime on the approved verification
host. CI repeats both, checks strict runtime types, validates skill composition
and versions, and verifies generated bundle content.

## Deliberate adaptations

- One Shipshit execution router replaces upstream poteto-mode entry points.
- Existing deslop code, product, UI and prose modes remain available.
- Principle procedures are installed resources rather than separate catalog skills.
- User-owned roles, accounts, host limits and provider opt-ins take precedence.
- Cleanup retains immutable merge proof and preservation of tracked, untracked,
  ignored, unpushed and active work; upstream deletion shortcuts are not imported.
- Session hooks and native agent definitions are explicit setup templates.
- Benny and Bot UI preserve their procedures behind capability and authority checks.
  Their inclusion does not schedule a routine or expose a service.
- The native model/effort template matrix becomes a configured-role adapter.
  Setup verifies selected roles without requiring unused providers.

## Installed-artifact and live boundaries

The official skills installer was exercised on Studio with all 188 canonical
skills selected for Codex, Claude Code and Cursor. The shared agent directory and
Claude-specific copies contain every selected skill with no extra identities,
missing resources or source-byte differences. No dependency directory was copied.
The installed runtime then passed all 155 tests (561 assertions) and strict
TypeScript checks, independent of the upstream checkouts.

A full live provider cutover additionally requires backed-up configuration
changes and a fresh-session routing check. Unit tests and static adapter review
cannot substitute for that evidence. Preserve user-generated routing sheets
and their source of truth when disabling duplicate plugins.
