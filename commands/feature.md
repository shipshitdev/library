# Feature - Client Requirement Intake

Capture a rough client or stakeholder requirement, turn it into a PRD epic, split
it into scoped sub-issues, and push approved issues to a GitHub Projects kanban.

## Usage

```bash
/feature [client requirement or feature idea]
```

## Workflow

Use the `feature-intake` skill.

1. Read the command arguments as the feature idea.
2. Confirm the target repository and GitHub Project board.
3. Search existing issues and board items for duplicates or nearby work.
4. Read relevant product, roadmap, and memory context.
5. Ask at most three focused stakeholder questions only if required details are
   missing.
6. Draft one parent PRD issue plus scoped sub-issues.
7. Show the draft and wait for approval.
8. Create the GitHub issues, link sub-issues, and add approved items to the
   kanban.

## Rules

- Do not create GitHub issues before draft approval.
- Do not create sidecar PRD files unless explicitly requested.
- Prefer updating a true duplicate over creating a parallel epic.
- Keep PRD requirements product-readable and agent-verifiable.
