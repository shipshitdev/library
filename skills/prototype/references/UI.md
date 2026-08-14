# UI Prototype

Generate **several radically different UI variations** on a single route, switchable from a floating bottom bar. The user flips between variants in the browser, picks one (or steals bits from each), then throws the rest away.

If the question is about logic/state rather than what something looks like — wrong branch. Use [LOGIC.md](LOGIC.md).

## When this is the right shape

- "What should this page look like?"
- "I want to see a few options for this dashboard before committing."
- "Try a different layout for the settings screen."
- Any time the user would otherwise spend a day picking between three vague mockups in their head.

## Two sub-shapes — strongly prefer sub-shape A

A UI prototype is much easier to judge when it is **butting up against the rest of the app** — real header, real sidebar, real data, real density. A throwaway route on its own is a vacuum: every variant looks fine in isolation. Default to sub-shape A whenever there is a plausible existing page to host the variants. Only reach for sub-shape B if the prototype genuinely has no nearby home.

### Sub-shape A — adjustment to an existing page (preferred)

The route already exists. Variants are rendered **on the same route**, gated by a `?variant=` URL search param. The existing data fetching, params, and auth all stay — only the rendering swaps.

If the prototype is for something that does not yet have a page but *would naturally live inside one* (a new section of the dashboard, a new card on the settings screen) — that is still sub-shape A. Mount the variants inside the host page.

### Sub-shape B — a new page (last resort)

Only use this when the thing being prototyped genuinely has no existing page to live inside.

Create a **throwaway route** following whatever routing convention the project already uses. Name it so it is obviously a prototype (include the word `prototype` in the path or filename). Same `?variant=` pattern.

Before committing to sub-shape B, sanity-check: is there really no existing page this could be embedded in?

In both sub-shapes the floating bottom bar is identical.

## Process

### 1. State the question and pick N

Default to **3 variants**. More than 5 stops being radically different and starts being noise — cap there.

Write down the plan in one line, in the prototype's location or a top-of-file comment:

> "Three variants of the settings page, switchable via `?variant=`, on the existing `/settings` route."

**Done when:** N is chosen and the one-line plan exists.

### 2. Generate radically different variants

Draft each variant. Hold each one to:

- The page's purpose and the data it has access to.
- The project's component library / styling system.
- A clear exported component name, e.g. `VariantA`, `VariantB`, `VariantC`.

Variants must be **structurally different** — different layout, different information hierarchy, different primary affordance, not just different colours. If two drafts come out too similar, redo one with explicit "use a different layout primitive" guidance.

### 3. Wire them together

Create a single switcher component on the route. Read `variant` from the URL search param (default `A`) and render that variant plus the `PrototypeSwitcher`.

For sub-shape A: keep all the existing data fetching above the switcher; only the rendered subtree changes per variant.

For sub-shape B: the throwaway route under `/prototype/<name>` mounts the same switcher.

### 4. Build the floating switcher

A small fixed-position bar at the bottom-centre of the screen with three pieces:

- **Left arrow** — cycles to the previous variant (wraps around).
- **Variant label** — shows the current variant key and, if the variant exports a name, that name too.
- **Right arrow** — cycles forward (wraps around).

Behaviour:

- Clicking an arrow updates the URL search param so the variant is shareable and reload-stable.
- Keyboard: left and right arrow keys also cycle. Leave arrow keys alone when an input, textarea, or contenteditable is focused.
- Visually distinct from the page so it is obviously not part of the design being evaluated.
- Hidden in production builds — gate on the project's non-production check.

Put the switcher in a single shared component so both sub-shapes can reuse it.

### 5. Hand it over

Surface the URL (and the `?variant=` keys). The interesting feedback is usually **"I want the header from B with the sidebar from C"** — that's the actual design they want.

### 6. Capture the answer and clean up

Once a variant has won, capture the answer — which variant and why — then capture the prototype the way the skill describes. Fold the winner into the real code and move the rest onto the throwaway branch, not into main:

- **Sub-shape A** — fold the winner into the existing page; drop the losing variants and the switcher from main.
- **Sub-shape B** — promote the winning variant to a real route; drop the throwaway route and the switcher from main.

The full set of variants is the primary source, so it lands on the throwaway branch.

## Anti-patterns

- Variants that differ only in colour or copy. Real variants disagree about structure.
- Sharing too much code between variants. A shared header is fine; a shared layout defeats the point.
- Wiring variants to real mutations. Point mutations at a stub — the question is "what should this look like".
- Promoting the prototype directly to production. Rewrite it properly when you fold it in.
