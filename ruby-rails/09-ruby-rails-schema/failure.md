# What can go wrong

update_all bypasses model callbacks and validations. That can be useful for a deliberate batch update, but database constraints still apply.

A rollback that drops a filled column destroys values.

**Memory cue:** Validation explains. Constraint enforces.

Close this lesson. Draw the five steps.

Explain one failure in your own words before opening Practice.