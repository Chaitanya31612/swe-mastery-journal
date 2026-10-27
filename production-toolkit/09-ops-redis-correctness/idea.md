## Understand the idea

A pipeline batches network operations for efficiency; it does not by itself make them one indivisible business operation.

MULTI/EXEC and scripts provide different atomic-execution tools, but Redis transactions do not behave like a relational transaction with automatic rollback of every runtime error.

Persistence and replication are separate from command atomicity. RDB snapshots and AOF policies have different recovery/loss/performance tradeoffs.

A replica/failover configuration can still have a data-loss window under its contract. Select it from the role of the data, not the word persistent alone.

A lock with an expiry is a lease. Worker A can pause, its lease expire, and worker B acquire it.

A can resume as a stale owner. Use the authority’s conditional write/version or fencing design where correctness requires excluding stale writers.

A random token and compare-delete protect release ownership, not every business write.