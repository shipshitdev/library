### Investigation

**You own the answer.** Read-only requests: how does X work, why was Y built
this way, are we sure about Z, should we do X or Y. Cited explanation or
recommendation, not a code change.

1. Route through the `how` skill (Explain for narrow questions, Critique for
   "are we sure?"). For motivation questions, also route through `why`.
2. Throughput checkpoint stays one line: `throughput checkpoint: n/a,
   read-only investigation`.
3. Produce the how-shaped output, or a recommendation with a tradeoffs table
   if the request is a decision between alternatives.
4. Apply `skills/de-slop/references/prose-slop.md` to the reply.

No PR, no babysit, no `architect` unless the investigation precedes a code
change. If it does, hand back and re-route to Bug fix or Feature.

**Reply:** the investigation output. For "are we sure?" include real judgment.
Push back if the premise is wrong.
