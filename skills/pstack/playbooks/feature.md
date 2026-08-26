### Feature

**You own the design.** Delegate implementation. Stay in the lead.

1. Run `how` over the affected subsystem.
2. Run `architect` for parallel design exploration. Skipping stays as
   `architect skipped: <reason>`.
3. Write the throughput checkpoint as four todo items. A dimension that
   does not apply keeps its item with `n/a: <reason>`:
   - Blocking first steps.
   - Independent workstreams.
   - Shared mutable state (default: split the target).
   - Smallest safe decomposition.
4. Delegate code-writing to a subagent on the fast cheap tier with a
   specific scope, named data shape, and success criteria. Review the
   diff yourself. When the implementation admits multiple valid shapes,
   use `arena` instead. Surgical edits. Commit liberally.
5. Verify on the matching surface. Inconclusive is not a pass.
6. Rebase into small, ordered commits. Sequence verifiable units.
7. If the design is contested, run `interrogate` before shipping.
8. Run Opening a PR.

**Reply:** what you built, what you chose and why, open decisions.
