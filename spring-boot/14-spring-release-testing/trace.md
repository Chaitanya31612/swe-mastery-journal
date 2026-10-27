## Trace the execution

Build an immutable artifact → verify its configuration → apply a deliberate migration → start and check readiness → send a smoke request → observe → promote or roll back. Keep migration execution separate from ordinary request scaling.

Tests should show both permitted and denied behavior, transaction rollback, and an adapter failure. A green health endpoint alone does not prove the feature works.
