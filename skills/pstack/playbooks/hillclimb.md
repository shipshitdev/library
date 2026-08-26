### Hillclimb

**You own the metric.** One change, one measurement, keep or revert. A
one-off fix is Bug fix or Perf issue.

1. Run `how` over the target. Fix one metric, the better direction, and a
   checkable stop predicate that pairs a target with a floor on attempts.
2. Build the measurement harness, prove its sensitivity, then freeze it.
   Record the baseline and a green regression gate before any change.
3. Open a decision trail via `show-me-your-work`.
4. Ground each hypothesis in a named mechanism.
5. Loop, one hypothesis per iteration. Delegate the change to a subagent.
   Parallel independent hypotheses each get their own worktree. Accept
   only when the metric moves past noise and the gate stays green.
   Otherwise revert in full. One commit per accepted fix.
6. Push past the first plateau. Pivot category before concluding the hill
   is climbed.
7. Stop when the predicate is met, or remaining ideas are marginal.
8. Run Opening a PR with accepted commits stacked in landing order.

**Reply:** metric and target, baseline to final, iterations kept vs
reverted, each accepted fix, the trail path, the next idea if pushed.
