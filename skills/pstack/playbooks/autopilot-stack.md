### Autopilot-stack

**You own the stack, never the landing.** Build and verify the queue,
then hand the operator one linear stack they review and land.

Sibling of Autopilot-full. The owner loop and verification gate are the
same. The terminal differs: a clean verdict appends a link. Nothing
auto-ships.

1. Run the owner loop unchanged. Owners parallelize when the work is
   self-contained. Each keeps a `show-me-your-work` trail.
2. Audit on a regular tick. Count only side effects as progress. Stand
   down a stuck lane.
3. Hold the operator gates. A request to state the plan is not a go.
4. Verify at STACK-READY via `swarm`. Findings go back to the owner.
   Nothing enters the stack unverified.
5. Append on a clean verdict. No owner merges, arms auto-merge, or
   closes. Use `gh` to keep the ordered stack visible.
6. Single writer on topology. Parallel writers on builds. Absorb trunk
   drift at the root, then re-verify what moved via patch-id.
7. Deliver one linear chain of verified PRs, reviewable bottom-up. The
   operator lands it.

Choose Autopilot-full when PRs are independent and landing authority is
granted. Choose Autopilot-stack when the operator wants review before
landing, or the work is sequenced.

**Reply:** links to the stack root and tip, a one-line verdict per
link, anything parked or excluded.
