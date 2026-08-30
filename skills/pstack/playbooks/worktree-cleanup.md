### Worktree cleanup

**You own the disk and the safety gate.** Prune merged or abandoned
git worktrees. Deletion is irreversible. Creating worktrees is the
`worktree` skill. This playbook only reclaims.

1. Snapshot disk use, then list worktrees from `git worktree list`.
   Never hand-type paths. Classify each by size, age, merge state,
   uncommitted work, and PR state.
2. The classification is advice, not permission. Cross-check every
   candidate against work the human still has pinned or in flight.
3. Pause on irreversible loss. Tracked uncommitted edits need a
   decision first. Untracked throwaway is safe to drop when named.
4. Prune the confirmed set. Per path, `git worktree remove` then
   `git worktree prune`. Branch refs survive. Confirm disk use after.
5. Name `git-cleanup` when the ask is merged-branch residue rather
   than worktrees.

Do not delete the main checkout, active worktrees, or anything holding
uncommitted work without an explicit yes.

**Reply:** disk use before and after, the worktrees pruned, and a
one-line reason for each held back.
