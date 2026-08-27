### Visual parity

**You own pixel-exact equivalence.** The baseline is the spec. You do
not touch it.

1. Establish the baseline first: a visual regression harness that
   screenshots the current component across its states.
2. Hold the anti-shortcut clauses: no harness modifications, no
   baseline tampering, no component restructuring to make a diff pass.
   If the baseline looks wrong, stop and ask.
3. Migrate one component at a time. Parallelize across worktrees. Shared
   primitives migrate first as a blocking phase.
4. Verify each component against its baseline via image diff. A nonzero
   diff is a fail.
5. Run Opening a PR per component or per safe batch.

**Reply:** components migrated, the diff result for each, the baseline
harness location, what's left.
