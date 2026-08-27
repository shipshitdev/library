### Shipping

**You own what lands.** Verify each PR independently, land only the
verified run from the root. Green is not safe. This is the half after
Babysit.

1. **Verify every PR independently before arming anything.** One
   subagent per PR, each exercising the real surface against parent
   versus head. Each returns `PASS`, `PASS+NOTES`, or `FAIL`. Safe
   means a verdict from an agent that did not write the code. CI green
   is not a verdict.
2. **Land only the contiguous verified run rooted at the bottom.** Walk
   up from the lowest unmerged PR and stop at the first one without a
   passing verdict. Report the ceiling as a PR number.
3. **Re-check that the verdicts still describe the code.** Compare
   `git patch-id` at the verdict SHA against the current head. Re-verify
   anything that drifted.
4. **Land with `gh`, not a stack-collapsing auto-merge.** Name
   `finishing-a-development-branch` or `merge-open-prs` for the land
   path the human confirmed. Never enable GitHub auto-merge on stacked
   children that target unprotected parents.
5. **Once the queue is draining, stop mutating it.** Independent work
   gets re-parented onto trunk and shipped on its own.
6. **Stop at the ceiling.** Report what landed, the next unverified PR,
   and what verifying it would take.

**Reply:** the verified run and its ceiling, each PR's verdict and who
produced it, what landed, what the next gap needs.
