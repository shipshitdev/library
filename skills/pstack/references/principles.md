# pstack principles

Twenty-one rules from Lauren Tan's pstack (MIT). Read a leaf in full when you
apply it. Cite the principle and the choice it changed.

These are not standalone catalog skills. Existing overlaps:
`verification-before-completion` owns completion claims,
`domain-modeling` owns glossary work, `typescript-expert` owns TypeScript
syntax, `context-optimization` owns token budgets,
`systematic-debugging` owns failed-fix loops.

## Core

### Laziness Protocol

Bias to deletion and the smallest change that solves the problem. Prefer a
flat call hierarchy. Consolidate decisions. Question new signal threading.
If a human would find the code exhausting to maintain, it is a bad solution.

### Foundational Thinking

Get the data shape right before writing logic. Structural decisions protect
option value. Code-level decisions protect simplicity. DRY the structure, not
every line.

### Redesign from First Principles

When integrating a new requirement, redesign as if it had been foundational
from day one. Propagate through types, docs, and examples. Deliver the
redesign incrementally.

### Subtract Before You Add

Remove dead weight first, then build on the simpler base. Sequence removal
before construction. Leave the design slightly simpler than you found it.

### Minimize Reader Load

Count layers and hidden state. Collapse one-caller wrappers. Shrink mutable
scope. If the reader traces more than three files to answer one question,
flatten it.

### Outcome-Oriented Execution

Planned rewrites and migrations converge on the target architecture. Do not
preserve throwaway compatibility states. Planned breakage during fill-in is
fine when scoped.

### Experience First

Choose user delight over implementation convenience. The user is whoever
consumes the work: end user, importing colleague, or next maintainer. Ship
less, ship better.

### Exhaust the Design Space

A novel interaction or architectural decision with no precedent earns 2-3
competing sketches before commit. A second flavor of the first shape does
not count.

### Build the Lever

For non-trivial work, build the tool that does or proves it: a codemod,
script, or generator. The tool is the artifact a reviewer reruns. Skip only
when the task is a couple of obvious edits.

## Architecture

### Model the Domain

Encode the domain in a structure (state machine, typed model, table or
registry, reducer, boundary) instead of scattered conditionals. For glossary
work, use `domain-modeling`.

### Boundary Discipline

Guards at system boundaries. Trust internal types. Keep business logic pure.
Do not re-export transport or wire types through the public surface.

### Type System Discipline

Make illegal states unrepresentable. Brand primitives. Parse external data
at boundaries. Do not lie to the type checker. For TypeScript syntax, use
`typescript-expert`.

### Make Operations Idempotent

Commands, lifecycle steps, and loops that run amid crashes and retries
converge to the same end state.

### Migrate Callers Then Delete Legacy APIs

Introduce a new internal API, migrate every caller, and delete the old API
in one wave. No compatibility shims.

### Separate Before Serializing Shared State

Concurrent actors that might write the same file, branch, key, or object:
eliminate the sharing first. Serialize only when one shared write target is
a real invariant.

## Verification

### Prove It Works

Verify against the real artifact, not a proxy or "it compiles". Inspect the
delegate's diff, not its summary. Script the check when you can. Completion
claims also follow `verification-before-completion`.

### Fix Root Causes

Reproduce first. Ask why until you reach the cause. Resist symptom guards.
When a restart bug appears, suspect stale state before code. For loops that
already failed, use `systematic-debugging`.

### Sequence Work into Verifiable Units

Break work into small units that each end in a check. Verify each before the
next. Order delivery so the sequence proves itself: failing test, then fix.

## Delegation

### Guard the Context Window

Route bulk to subagents. Keep summaries in the main thread. File pointers,
not inlined dumps. For token-budget design, use `context-optimization`.

### Never Block on the Human

On reversible work, proceed and present the result. Reserve questions for
irreversible writes and genuine product or preference calls.

## Meta

### Encode Lessons in Structure

The second time you write the same instruction, encode it as a lint,
metadata flag, runtime check, or script, then delete the instruction.
