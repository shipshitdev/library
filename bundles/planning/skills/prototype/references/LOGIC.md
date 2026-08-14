# Logic Prototype

A single, self-contained HTML file — a **shareable demo** — that lets anyone drive a state model by clicking buttons. Use this when the question is about **business logic, state transitions, or data shape** — the kind of thing that looks reasonable on paper but only feels wrong once you push it through real cases.

Because it is one file with nothing to install, a non-developer — a designer, a PM, a domain expert — can feel the model for themselves. So it speaks their language, not the code's.

## When this is the right shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where..."
- "I want to feel out what the API should look like before writing it."
- Anything where someone wants to **press buttons and watch state change**.

If the question is "what should this look like" — wrong branch. Use [UI.md](UI.md).

## Process

### 1. State the question

Before writing code, write down what state model and what question you're prototyping. One paragraph, at the top of the demo (in a visible intro, not just a comment). A logic prototype that answers the wrong question is pure waste — make the question explicit so it can be checked later.

**Done when:** the question is visible in the demo.

### 2. Isolate the logic in a portable module

Put the actual logic — the bit that's answering the question — in a single `<script>` block written as a small, pure module that could be lifted out and dropped into the real codebase later. The page around it is throwaway; this module isn't.

The right shape depends on the question:

- **A pure reducer** — `(state, action) => state`. Good when actions are discrete events and state is a single value.
- **A state machine** — explicit states and transitions. Good when "which actions are even legal right now" is part of the question.
- **A small set of pure functions** over a plain data type. Good when there's no implicit current state — just transformations.
- **A class or module with a clear method surface** when the logic genuinely owns ongoing internal state.

Pick whichever shape best fits the question being asked. Keep it pure: no DOM, no `document`, no button handlers reaching inside it. The page calls into it; nothing flows the other direction. Once the question is answered, the validated reducer / machine / function set lifts into the real module on its own.

### 3. Build the shareable HTML file

One file, plain HTML/CSS/JS — no framework, no bundler, no server, everything inline so it opens by double-click and survives being emailed around.

Write it for a non-developer. Every label is in **domain language**, not code. Explain in plain words what's happening.

Lay it out with a clean hierarchy, top to bottom:

1. **Title and one-line explanation** of what this demo lets you explore (the question from step 1).
2. **Current state** — the full relevant state, rendered as a readable panel (labelled fields, not a raw JSON dump), re-rendered after every click so the change is visible.
3. **Free-play buttons** — one button per action, always available, so anyone can poke at the model in any order.
4. **Guided walkthroughs** — a set of **scenarios**, one per tab. Each tab holds a short plain-language description and the ordered **buttons to press** for that scenario. Starting a walkthrough resets to a known initial state.

Choose scenarios that demonstrate the awkward cases — the happy path, a tricky edge case, an attempt at something that should be illegal.

Keep it beautiful but restrained: clean typography, generous spacing, one accent colour. No animations, no gimmicks.

### 4. Hand it over

Send them the file, or open it for them. The interesting moments are when they say "wait, that shouldn't be possible" or "huh, I assumed X would be different" — those are the bugs in the *idea*.

### 5. Capture the answer and the prototype

Once the prototype has answered its question, capture the answer, then capture the prototype the way the skill describes. The validated reducer / machine / function set lifts into the real module; the HTML shell rides along to the throwaway branch.

## Anti-patterns

- A prototype that needs tests is no longer a prototype — skip the test suite.
- Wire to in-memory state. Hit a scratch DB only when the question is specifically about persistence.
- Answer one question. Leave "what if we wanted to support X later" out.
- Keep the page as a thin shell over a pure module. If the pure module references the DOM, it is no longer liftable.
- One file the recipient double-clicks. A React app or a dev server defeats "shareable".
- Keep the HTML shell off production. The logic module behind it is the bit worth keeping.
