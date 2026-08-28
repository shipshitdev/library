### Multi-phase or multi-PR plan

**You own the plan, not the code.** The plan is a checklist an owner
runs box by box. Do not implement.

1. When the change is one or two files with an obvious approach, skip
   the plan. Say so and stop.
2. Settle open questions by Prototype before you write. Ask the
   operator only about a product or preference call.
3. Explore in read-only subagents on the fast cheap tier. Each returns
   file pointers, conventions, test commands, and entry points. No
   inlined dumps.
4. Write the plan under the current repo `.tmp/` unless the operator
   names a path. One section per PR. One PR is one change with its own
   evidence. Name the execution playbook: Autopilot-full,
   Autopilot-stack, or Orchestrate.
5. Write with `technical-writing` in how-to mode, then apply
   `skills/deslop/references/prose-slop.md`.
6. Hand back. Execution starts on the operator's explicit go.

**Verification rule.** Tests alone are not sufficient. A PR is verified
only when its unit, live, and perf boxes are all checked. The live
block is mandatory. The perf block names the metric, the probe, the
trunk baseline, and the fail rule.

Each PR section names: depends on, files, build steps, observable
result, unit / live / perf verification, review gate, merge rule.

**Reply:** the plan path, the PR ids with dependencies and the
review-gated set, what prototypes proved, what stays unproven.
