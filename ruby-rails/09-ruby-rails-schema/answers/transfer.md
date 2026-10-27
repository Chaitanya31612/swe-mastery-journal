# One valid adaptation

Add a compatible nullable field, deploy code that can handle both old and new rows, backfill in bounded batches, verify coverage, then enforce non-null with a database-specific safe plan.

Remove compatibility code later. Consider locks and rollback for each step.

**Explain back:** Validation explains. Constraint enforces.

What changed in the new condition? What would make your answer fail?