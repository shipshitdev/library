### Autonomous run

**You own the exit condition.** Drive to it without stopping. For
"going to bed", "run until done", or "loop until X".

1. State the exit condition as a checkable predicate before the first
   iteration.
2. Pick a wake mechanism: an event (CI, a merge, a ref advancing) or a
   fixed-interval heartbeat sized to when the result is worth
   re-checking.
3. Each iteration makes the smallest change the evidence justifies,
   verifies it against the predicate, commits if it advanced, discards
   changes that did not help.
4. Mid-run discoveries are yours. Put out-of-band fixes in their own
   PR. Surface only irreversible actions, genuine product calls, or a
   real dead end.
5. Checkpoint every iteration via `show-me-your-work`.
6. Stop when the predicate is met. A plateau is not a stop. Surface a
   genuine dead end rather than spinning. Never relax the predicate.

**Reply:** the exit condition, iterations run, what landed, what was
discarded, final predicate state.
