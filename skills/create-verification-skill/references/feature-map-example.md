# Feature map example

Index file `features/README.md` lists one line per feature file.

Each feature file uses these four headings:

## Sub-features

What the user can do inside this feature.

## How to get to it (user POV)

Routes, commands, menus, or prompts. Real ones from this repo.

## Driving it with the harness

Selectors, commands, or HTTP calls. Stable handles (ARIA, data
attributes, prompt strings, route paths) over coordinates.

## Gotchas

Auth, seed data, timing, or isolation notes.

Example shape for a notes app:

```markdown
# Create note

## Sub-features

- Title and body persist after reload
- Empty title is rejected

## How to get to it (user POV)

Open `/notes`, click New note.

## Driving it with the harness

Click `getByRole('button', { name: 'New note' })`. Fill title. Save.
Reload. Expect the title in the list.

## Gotchas

Needs a signed-in session. Doctor must confirm auth before drive.
```
