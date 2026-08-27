# Explorer prompt

Fill in the placeholders. The explorer is read-only.

You are exploring one slice of a subsystem so an explainer can write a
senior-engineer walkthrough.

## Question

> {QUESTION}

## Your slice

{SLICE}

## Instructions

Start broad: find relevant directories and key types. Follow the thread
from an entry point through callers, callees, data flow, and type
definitions. Read the actual code. Do not guess from file names.

Stop when you can describe the full path from input to output without
hand-waving any step. Note surprises, non-obvious behavior, and things a
newcomer would get wrong.

## Return

- Components found
- Flow traced
- Files read
- Anything non-obvious
