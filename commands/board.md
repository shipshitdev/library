# Board - GitHub Projects v2 Kanban Setup

One entry point for GitHub Projects v2 board configuration: create the canonical
board, audit an existing one against it, fix drift, or clone a board's shape to
another project.

## Usage

```bash
/board              # show the current board shape (status)
/board init         # create the canonical board (Backlog · In Progress · Human Review · Done · Deferred + P0–P3)
/board audit        # check an existing board against the canonical shape
/board normalize    # fix a drifted board to match the canonical shape
/board copy <src>   # clone a board's configuration to another project
```

## Workflow

Use the `gh-project-board` skill, passing the mode (`init` / `audit` /
`normalize` / `copy`) through. The canonical shape is the Ship Shit Dev
board-as-truth model: a `Status` field of Backlog · In Progress · Human Review ·
Done · Deferred, plus a `Priority` field of P0–P3.

1. **Parse the mode** from the argument (`status` default / `init` / `audit` /
   `normalize` / `copy`). Unknown argument → print Usage, don't guess.
2. **Detect the target project** (current repo's linked Project v2, or an
   explicit project number/URL argument). If none can be resolved, ask.
3. **Run the mode** via `gh-project-board` — `status`/`audit` are read-only;
   `init`/`normalize`/`copy` mutate the board behind the skill's confirmation gate.

## Gates

- `status` and `audit` are read-only — they never change a board.
- `init`, `normalize`, and `copy` mutate Projects v2 config — honor the
  `gh-project-board` skill's confirmation gate before applying changes.
- Never delete existing board fields or columns without explicit confirmation.
