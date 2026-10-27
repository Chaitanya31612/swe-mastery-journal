# One valid repair

Measure SQL count for 1 versus 100 tasks. If it grows by roughly one per task, choose a DTO projection or a fetch join for the required to-one relation. Keep bounded pagination and deterministic ordering. Test query count and response shape, not just list size.

**How to check:** Flush synchronizes changes with the database connection. The transaction can still roll back before commit.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test. Code length and matching keywords are not evidence.
