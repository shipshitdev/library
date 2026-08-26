# Interrogate rubric

Raise only issues you would block or request changes on.

- **Correctness.** Wrong behavior, missed edge, broken invariant.
- **Security.** Authz holes, injection, secret leak, unsafe defaults.
- **Data.** Loss, corruption, migration hazard, non-idempotent writes.
- **Concurrency.** Races, shared mutable state, lock inversion.
- **Compatibility.** Broken callers, silent schema drift.
- **Test gap.** A cheap local check that would have caught the bug is
  missing.

Do not raise style nits the surrounding file already practices.
