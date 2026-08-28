### Autopilot-full

**You own the verdicts, never the PRs.** One owner runs each independent
PR from build to merge. Nothing merges without a clean swarm verdict.

1. Mark the operator's items. Execution starts only on an explicit go.
   Items the operator names stay theirs to click.
2. Spawn one owner per PR. Each owns build, self-proof on the real
   artifact, review-bot triage, a named `deslop` / `no-comments` pass,
   babysit to green, and the merge itself. The merge is gated by step 4.
   Each owner keeps a `show-me-your-work` trail.
3. Run owners in parallel when PRs are self-contained. One writer per
   branch. Overlapping work serializes. Self-contained PRs branch from
   trunk.
4. Swarm-verify every merge-ready head before its merge. Fan out via
   `swarm`. Lanes: re-run gates at that SHA, prove load-bearing behavior
   live, audit receipts and the diff. No merge without the root's clean
   verdict.
5. On a clean verdict the owner merges from a trunk-current head. If
   trunk moved, the Shipping patch-id rule governs re-verification.
6. Audit owners on a regular tick. Count only side effects as progress.
   Stand down a stuck lane and dispatch a replacement.
7. Stand down instantly on the operator's stop.

**Reply:** the queue with each PR's owner, state, and head SHA; each
verdict; what merged; open operator gates; where the trails live.
