# One valid repair

Inspect transaction ownership, callback registrations, duplicate enqueue paths, and the database uniqueness rule for the logical completion event. Test two independent completion attempts and the after-commit/outbox path with real persistence.

Keep the unit fake test, but do not claim it covers those boundaries.

**How to check:** It can prove local decisions for supplied fake behavior. Other boundaries need their own evidence.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.