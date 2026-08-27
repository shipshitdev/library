### Refactoring

**You own the contract.** The structure changes. The behavior does not.
Large or cross-cutting structural work routes to `figure-it-out`.

1. Pin the behavior contract first. Run `how` over the affected subsystem,
   then write a characterization test, snapshot, or equivalence harness
   before any structure moves. Type check and lint are not a pin.
2. Name the structure the code is missing (Model the Domain).
3. Name the target shape. If it crosses a function boundary, run
   `architect` first.
4. Subtract before you add. Delete dead weight, then introduce the new
   shape. The smallest change that reaches the target ships.
5. Move in small behavior-preserving steps, each keeping the pin green.
   For API reshapes, migrate every caller and delete the old API in the
   same wave. Delegate mechanical edits to a subagent on the fast cheap
   tier. Review the diff.
6. Prove behavior is unchanged on the real artifact. For larger reshapes,
   run an equivalence check: old-vs-new outputs, a recorded baseline, or
   a smoke run on the matching surface.
7. Confirm reader load dropped. If the diff does not lower it somewhere,
   revert.
8. Rebase into small ordered commits. Run Opening a PR.

**Reply:** the structure that changed, the pin, the equivalence proof, the
reader-load delta, what shipped and what got reverted.
