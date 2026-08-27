# Design red flags

Screen every candidate before synthesis.

## Shallow module

A large interface that hides little complexity. Callers coordinate
several methods to complete one operation. Public options expose
internal stages.

## Information leakage

A representation, policy, or protocol detail appears in more than one
place. Public re-exports of transport or wire types are leakage.

## Temporal decomposition

Modules organized by execution order (load, validate, transform, save)
instead of the knowledge they own.

## Pass-through method

Forwards the same arguments to another method with the same shape.
Remove it or move responsibility to the module that can finish the job.
