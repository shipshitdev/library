### Bug fix

**You own this task.** Every shipped line traces to runtime evidence.
Belt-and-suspenders that "might help" does not ship.

1. Reproduce it yourself on the matching surface. Do not hand the repro to
   the user unless the surface is unreachable and you say why. A bug you
   cannot reproduce, you cannot prove fixed.
2. Binary-search the cause. Seed hypotheses with `how` over the affected
   subsystem and `why` for regression history. Confirm the surviving
   mechanism with runtime evidence before planning the fix.
3. Plan the fix. If it crosses a function boundary, run `architect` first.
   Delegate implementation to a subagent on the strong instruction-following
   tier with a specific scope. Review the diff yourself.
4. Verify on the same surface. The original repro now passes. Inconclusive
   or wrong-surface is not a pass.
5. Stage the failing repro before the fix. Run the `tdd` skill when the bug
   has a cheap local test path. Skip it when the test would be expensive,
   integration-heavy, or unclear.
6. Run Opening a PR.

**Reply:** what was broken, root cause, fix, how you verified. Paste
failing-then-passing repro output.
