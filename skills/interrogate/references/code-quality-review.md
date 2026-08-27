# Code-quality lens

Apply in addition to the rubric. Still high-conviction only.

- Dead paths and leftover comments that hide a workaround.
- Types that admit illegal states.
- One-caller wrappers and pass-through methods.
- Validation scattered inside trusted code.
- A comment that exists because the code cannot say the constraint.
  Flag the symbol, not the prose.
