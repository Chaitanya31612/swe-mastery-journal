# The idea

A model validation gives readable feedback before a save. A database constraint protects stored data even when two requests race or a different code path writes the table. Use both when the rule matters.

For example, task keys unique within a workspace need a composite unique index on workspace_id and key. Decide how blank values and case differences should behave. PostgreSQL NULL and collation rules are part of that decision. Do not assume the model and database interpret values identically.

A migration changes shared data structures. Think about existing rows and overlapping application versions. Adding a non-null column to a populated table requires a plan for those rows. A reversible migration method does not mean every business data change is safely reversible.
