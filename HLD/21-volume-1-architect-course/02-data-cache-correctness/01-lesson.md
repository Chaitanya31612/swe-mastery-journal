# Data access, caches, and atomic boundaries

Learning outcome: Choose keys/indexes from access patterns, preserve a concurrent invariant, and specify cache freshness/failure behavior.

## Model from operations, not brand names

An access pattern specifies what is read/written and how it is selected/ordered. A relational model is useful for relationships, constraints, and transactions; key-value, document, and wide-column models can serve other patterns. These categories do not determine an absolute capacity threshold. Start with entities, ownership, queries, and required atomicity.

An index accelerates eligible reads but costs storage and write work. A composite index must match useful filters/order; a partition key places data and bounds query locality. Replication copies data for durability/availability/eligible reads; partitioning divides ownership/work. A replica may lag. A request that needs read-your-writes requires a routing/version/progress mechanism, not an arbitrary assertion that five seconds is enough.

## Invariants cross execution steps

For one remaining item, two clients can both read `available=1` before either writes. A single conditional update `UPDATE inventory SET available=available-1 WHERE id=? AND available>0`, with affected-row checking, can atomically allocate one unit under suitable database semantics. A multi-row/multi-night invariant needs a transaction and appropriate isolation/locking/retries. Transaction syntax alone does not establish serial behavior.

An idempotency key represents the same logical operation across retries. Scope it to tenant/user and action, retain enough identity/result state, and reject reuse with conflicting input. A unique constraint plus a transaction is stronger than separate “exists?” and “insert” calls. If an external effect is outside that transaction, state how uncertainty is reconciled; a local flag cannot atomically control an arbitrary remote provider.

## Cache as a derived serving layer

In cache-aside, read cache, then source on miss, then populate. For writes, choose invalidation/update/versioning deliberately. TTL bounds some staleness only under assumptions; it does not make a cache authoritative for money/inventory. Concurrent stale readers can repopulate an old value after deletion. Version checks, bounded staleness, avoiding caches on critical reads, or a stronger publication protocol may be needed.

Eviction and expiration differ: capacity removes objects versus time policy removes freshness candidates. Hot keys, stampedes, and simultaneous expiration can overload the source. Request coalescing, jittered TTLs, bounded stale serving when permitted, and admission control are tools with costs. Do not serve stale authorization data if the contract requires prompt revocation.

## Observe and recover

Measure hit/miss rate, source load, stale-data incidents, query/lock latency, and version conflicts. Test a cold/unavailable cache and source saturation. Backup/restore protects durable truth; losing a cache should be recoverable. A cache offers a latency/load trade-off, not a magical consistency guarantee.

## Retrieve before practicing

Trace a stale-cache repopulation after invalidation; then explain the single-unit claim boundary and why an external timeout differs.
