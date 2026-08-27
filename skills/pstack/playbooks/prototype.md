### Prototype

**You own the design decision, not the code.** The prototype is throwaway.
The real build then follows Feature or the existing `prototype` skill.

1. Scope the decision the prototype exists to make. No decision means no
   prototype. Route to Feature.
2. Gather references when the design space is open. Skip when the
   direction is set.
3. Build throwaway in an isolated scratch dir under the current repo
   `.tmp/`, separate from production source. Lightest stack that renders
   the idea. No production framework, no tests, no abstractions.
4. When comparing alternatives, build them behind one switcher, each
   variant labeled.
5. Verify on the matching surface. The observation is the test: screenshot,
   timing log, or printed output.
6. Present alternatives, tradeoffs, and a recommendation. Hand the chosen
   direction to Feature or `architect`.

**Reply:** variants explored, evidence, tradeoffs, recommendation, scratch
path. Say plainly that the prototype is throwaway.
