# Domain docs

> Seed for `docs/agents/domain.md`. Pick the layout that matches the repo, then
> delete the other section.

The domain glossary is the shared vocabulary the dev-loop skills read so PRDs,
issues, and code use the same terms for the same concepts.

## Single-context (default for a solo or single-product repo)

One `CONTEXT.md` at the repo root holds the living glossary:

- Core entities and their relationships.
- Ubiquitous terms (the words used in code, issues, and PRDs — kept consistent).
- Key invariants and business rules.
- Bounded edges: what this product is and is not responsible for.

Skills append to `CONTEXT.md` as they learn the domain; it is a living document, not
a one-time artifact.

## Multi-context (for a monorepo spanning several products or bounded contexts)

A `CONTEXT-MAP.md` at the root indexes one `CONTEXT.md` per context:

```
CONTEXT-MAP.md            # index: which context owns what, and how they relate
packages/<a>/CONTEXT.md   # glossary for context A
packages/<b>/CONTEXT.md   # glossary for context B
```

`CONTEXT-MAP.md` records the relationships between contexts (shared kernel, upstream/
downstream, anti-corruption layers) so a change in one context's language does not
silently break another.

## Architecture decisions

When a choice is hard to reverse **and** surprising **and** carries a genuine
trade-off, record it under `docs/adr/` as a short ADR. Routine choices do not need
one — the three-gate filter keeps the ADR log signal-dense.
