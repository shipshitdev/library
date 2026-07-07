# Product Slop Catalog

The tells that make an AI-built app feel unfinished to a paying customer, with the
fix for each. Stack assumed: Next.js 16, React 19, Tailwind v4, shadcn/ui. Every rule
is Incorrect → Correct; apply the judgment, not the literal string.

## Contents

- [Copy](#copy)
- [UI](#ui)
- [UX](#ux)

---

## Copy

### C1 — Marketing filler verbs

The AI reaches for "seamlessly / effortlessly / elevate / empower / unlock / supercharge".

- **Incorrect:** "Seamlessly elevate your workflow and unlock your team's potential."
- **Correct:** "Assign a task in two clicks. Your team sees it instantly."

Say the concrete thing the product does. If a sentence survives deleting the adverb,
delete the adverb.

### C2 — Empty-state copy that says nothing

- **Incorrect:** "No items to display."
- **Correct:** "No invoices yet. Create your first one to start tracking payments." + the action button.

An empty state is the highest-intent moment in the app — use it to teach the next step.

### C3 — Error messages with no recovery

- **Incorrect:** "Something went wrong." / "An error occurred."
- **Correct:** "Couldn't save — your session expired. Sign in again and we'll keep your draft."

Name what failed and what the user does next. Never surface a raw stack trace or code.

### C4 — Em-dash and triad overuse

The AI signature: em-dashes everywhere and rule-of-three lists ("fast, simple, powerful").

- **Incorrect:** "It's fast — really fast — and simple, powerful, and delightful."
- **Correct:** "Pages load in under a second."

One claim, backed by a number, beats three adjectives.

### C5 — Placeholder copy shipped as real

- **Incorrect:** "Lorem ipsum", "Your Company", "example@email.com" left in a shipped view.
- **Correct:** real product copy, the user's actual data, or a labeled example (`e.g. jane@acme.com`).

---

## UI

### U1 — The untouched-shadcn look

Default shadcn components + a purple/indigo gradient hero = "an AI made this."

- **Incorrect:** `bg-gradient-to-r from-purple-500 to-indigo-600` hero, default `Card`
  everywhere, no brand token.
- **Correct:** a real brand palette in the Tailwind v4 `@theme` block; components
  restyled to it. shadcn is a starting point, not the finished skin.

### U2 — Inconsistent spacing and radius

- **Incorrect:** `p-4` here, `p-5` there, `rounded-md` next to `rounded-xl`, ad hoc
  per component.
- **Correct:** a spacing/radius scale in `@theme`, used consistently. Cross-check with
  `deslop-ui`.

### U3 — Missing loading states

- **Incorrect:** a blank screen or a layout that pops in when data arrives.
- **Correct:** a skeleton or spinner that matches the final layout's shape, so nothing
  jumps.

### U4 — Missing or unstyled error/empty states

- **Incorrect:** a component that renders nothing (or crashes) when the fetch fails or
  returns `[]`.
- **Correct:** every data view handles three states — loading, empty, error — each
  styled to match the app.

### U5 — Raw HTML where the UI kit has a component

- **Incorrect:** `<button>`, `<input>`, `<select>` hand-styled when `Button` / `Input`
  from the kit exist.
- **Correct:** the kit's primitives, so states (hover, focus, disabled) and tokens
  come for free and stay consistent.

### U6 — No focus / keyboard states

- **Incorrect:** `outline-none` with nothing replacing it; mouse-only interactions.
- **Correct:** visible focus rings, keyboard-reachable controls. Route deeper a11y
  work to the `accessibility` skill.

---

## UX

### X1 — Dead controls

- **Incorrect:** a button, link, or menu item wired to nothing (`onClick={() => {}}`,
  `href="#"`), or a settings toggle that does not persist.
- **Correct:** every visible control does something, or is not shown. Hide what isn't
  built yet rather than shipping a decoy.

### X2 — Flows that dead-end

- **Incorrect:** a "Create" that succeeds but leaves the user on the same empty form
  with no confirmation and no next step.
- **Correct:** success feedback + a clear next action (view the thing, create another,
  go back to the list).

### X3 — Placeholder pages behind real nav

- **Incorrect:** a nav item routing to "Coming soon" or a blank page that looks
  shippable.
- **Correct:** ship the nav item when the page is real; until then, omit it or mark it
  clearly disabled with a reason.

### X4 — Forms with no validation or feedback

- **Incorrect:** a form that accepts anything, submits silently, and gives no success
  or failure signal.
- **Correct:** inline validation, a disabled submit until valid, and explicit
  success/error feedback. Use the project's form stack (e.g. `react-hook-form`).

### X5 — No optimistic or pending feedback on actions

- **Incorrect:** clicking "Save" with no visible change until a full round-trip
  completes; double-clicks fire twice.
- **Correct:** immediate pending state (disable + spinner or optimistic update), so the
  user knows the click registered and can't double-fire.

### X6 — Destructive actions with no guard

- **Incorrect:** a "Delete" that fires immediately with no confirm and no undo.
- **Correct:** a confirm step (or an undo window) proportional to how irreversible the
  action is.
