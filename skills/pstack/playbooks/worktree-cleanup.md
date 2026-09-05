### Worktree cleanup

**Execution boundary:** Carry the caller's authorized target, action scope,
report-only mode, host and provider limits into every step. Scheduling, model
selection, account choice and worktree placement remain harness-owned. Publication,
external messages, destructive actions and configuration changes require authority
covering that action. The procedure supplies no new permission.

Use the canonical `git-cleanup` skill's packaged cleanup helper and the active
harness session inventory. This supersedes upstream's worktree-audit script.
Read-only disk tools may supplement the plan; size and age never prove safety.

1. Resolve `git-cleanup` through the active catalog and read its proof rules.
   Run its packaged `scripts/cleanup.py dry-run --root <repository> --scope worktrees`
   on the harness-approved host. Record exact paths, candidate and trunk object
   IDs, merge evidence and skipped reasons. Preserve the exact JSON output as
   a plan file in the caller-approved artifact directory; keep report-only
   requests within their allowed output scope.
2. Cross-check candidates against active and pinned tasks, child worktrees and
   operations in progress. Preserve the main checkout, caller's worktree, locked,
   inaccessible, symlinked or in-use worktrees.
3. Preserve tracked, untracked, ignored and submodule changes. An untracked file
   is user work until proven otherwise; a `scratch:N` label is not proof.
   Preserve unpushed or unproven commits and both sides of open PRs.
4. Present the exact plan. Existing authorization covers only its named cleanup
   scope. If deletion is not authorized, stop at the report.
5. After confirming exclusive access to the selected worktrees and authority for
   the printed plan, run the same installed helper:
   `python3 scripts/cleanup.py prune --root <repository> --scope worktrees --plan <saved-plan.json> --confirmed --exclusive-worktrees`.
   The flags record existing authorization and verified exclusivity; they do not
   grant either. If exclusivity cannot be established, preserve the worktrees.
   The helper re-derives merge proof and current state rather than trusting the
   saved plan. A changed candidate needs a fresh plan. Do not use forced worktree
   removal, recursive directory deletion, broad registration pruning or a shell
   fallback when the helper refuses.
6. Re-list and report removed and preserved paths with reasons. Worktree-only
   scope preserves branches and all remote references.

Simulator, transcript, editor, package and build-cache deletion are separate
actions. Inventory them only when requested; never include them in worktree
cleanup or infer that age makes user state disposable.

**Reply:** the plan, immutable proof, removed worktrees and each preservation reason.
