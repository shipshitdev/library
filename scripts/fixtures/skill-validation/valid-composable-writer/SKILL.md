---
name: valid-composable-writer
description: Exercises a callable writer with an in-body authorization gate.
metadata:
  version: "1.0.0"
  tags: "fixture, validation"
allowed-tools: Write
---

# Composable Writer Fixture

## Contract

Inputs:

- Authorized target file

Outputs:

- Updated file

Creates/Modifies:

- Only the target covered by the user's explicit request

External Side Effects:

- Local writes only

Confirmation Required:

- Obtain explicit authorization before writing outside the requested scope

Delegates To:

- None
