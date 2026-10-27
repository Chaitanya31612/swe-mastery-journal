# What can go wrong

Catching an exception inside the transaction and continuing may commit earlier work. Nested transactions are not necessarily independent commits.

Read savepoint behavior before promising that an inner rollback undoes everything.

**Memory cue:** One rule. One boundary.

One failure timeline.

Close this lesson. Draw the five steps.

Explain one failure in your own words before opening Practice.