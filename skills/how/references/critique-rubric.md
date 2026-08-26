# Architectural critique rubric

Review through whichever lenses apply.

## Abstraction fit

Does each abstraction represent a real concept, or an "in case" layer?
Are boundaries in the right place? Is business logic entangled with
framework wiring?

## Data model

Do structures match actual access patterns? Are types honest about
runtime shape?

## Boundary discipline

Is validation concentrated at entry points? Do data cross boundaries in
typed shapes? Can the subsystem be tested in isolation?

## Evolution readiness

If the most probable next requirement landed tomorrow, how much would
change? Are leftover compatibility paths still depended on?

## Reader load

How many files must a newcomer open to answer one question? Are there
one-caller wrappers or hidden mutable state?
