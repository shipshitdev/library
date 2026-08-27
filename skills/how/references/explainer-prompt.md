# Explainer prompt

Fill in the placeholders. The explainer is read-only.

You are writing an architectural explanation for a senior engineer.

## Original question

> {QUESTION}

## Explorer findings

{EXPLORER_FINDINGS_ALL}

## Instructions

Reconcile overlapping or contradictory explorer findings by checking the
code. Weave the slices into one picture. Write an explanation a senior
engineer unfamiliar with this area could read and start working from.

You may re-read files to fill gaps. Do not re-explore from scratch.

## Output format

### Overview

1-2 paragraphs. What this is, what it does, why it exists.

### Key Concepts

The types, services, or abstractions needed to follow the rest.

### How It Works

Walk the flow in prose. Cite files and functions. Include a mermaid
diagram only when it clarifies a multi-component flow.

### Where Things Live

The files a newcomer opens first.

### Gotchas

Non-obvious edges and historical scars.
