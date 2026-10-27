## Trace the execution

Trace acquire → pause → expiry → new owner → old owner resumes. Identify which downstream store can reject the old write. Then trace a Redis crash and ask what persisted/replicated data is actually recoverable.

Test the failure model in the isolated lab. Measure the selected durability policy’s behavior, and document what data can be rebuilt versus what needs reconciliation.
