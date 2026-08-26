### Orchestrate

**You own the program, never the code.** Author briefs, drain the queue,
keep the frontier green, decide. One task driven to a predicate is
Autonomous run. One ambitious bespoke workflow is `figure-it-out`. Route
here when the work outlives any single agent.

Three rules carry the rest:

- Completions are queue events, not interrupts.
- Every spawn and every resume carries the standing orders verbatim.
- The brief is the product. A vague brief fails quietly.

#### Roles

- **Coordinator (this chat).** Frames, authors briefs, drains the inbox,
  owns the human report. It never authors or edits product code.
- **Sub-coordinator.** One per track, only when one drain cannot manage
  the program. Cap in-flight children at what one drain can process.
- **Worker / verifier.** Fast cheap tier unless judgment is required.
  Run a unit's verifier on a different capability tier from its worker.
  One writer per worktree or branch.

#### Brief template

Every spawn carries goal, scope, context pointers, checkable acceptance,
verify commands, timebox, forbidden actions, report shape, and standing
orders. A field you cannot fill is a unit you have not scoped yet.

#### Steps

1. **Frame.** State a countable done predicate. If one agent could finish
   inside the budget, stop and run Autonomous run instead.
2. **Install the runtime.** Open a trail via `show-me-your-work`. Write
   standing orders before any spawn. Store program state under the
   current repo `.tmp/orchestrate/<slug>/`.
3. **Pilot.** Push one unit through brief, worker, verification, and
   land. Fix the contract from pilot evidence before fan-out.
4. **Scale.** Spawn a rolling window of workers. Relay upstream reports
   into downstream briefs.
5. **Drain.** Classify completions (landed, needs-verify, failed,
   abandoned). Do not review a diff inside a drain.
6. **Land.** Integration starts with the first verified unit. Keep the
   frontier green. Name `finishing-a-development-branch` for each land
   the human authorized.
7. **Close.** Reconcile every spawned agent to a terminal row. Confirm
   the predicate on the real artifact. Audit the trail.

Workers never rebase shared stacks. Escalation reaches the human only
for irreversible actions, genuine product calls, or a program-level
dead end.

**Reply:** the predicate and the count against it, tracks and what each
landed, the frontier, verdicts, abandoned units, gates awaiting the
human, the store path, the trail path.
