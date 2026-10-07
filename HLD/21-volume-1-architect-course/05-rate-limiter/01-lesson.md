# Distributed rate limiting and overload control

Learning outcome: Choose an algorithm from the exact admission contract, enforce an atomic decision, and handle store/region failure.

## A rate is a contract, not an algorithm name

Define identity, scope, operation cost, burst allowance, and interval semantics. “100/minute” can mean a fixed calendar window, any sliding 60 seconds, or an average refill rate with bursts. Those are not interchangeable. Authentication supplies a reliable account identity; IP addresses are imperfect proxies because of NAT, IPv6 rotation, and shared clients.

A fixed-window counter is compact but allows a boundary burst. A sliding log tracks request timestamps precisely but costs memory/work proportional to activity; the record/check must be atomic. A sliding counter approximates traffic across windows. A token bucket caps stored tokens and refills at rate r, allowing a burst of capacity B. Over duration t, admission can approach B+r×t, rather than r×t alone. A leaky-bucket/shaper smooths work but adds queueing/rejection decisions.

## State and the decision must share an atomic boundary

For a token bucket, read tokens and last time, compute bounded elapsed refill, cap at B, subtract cost if available, and store the result as one atomic operation. Separate shared-store reads/writes let competing gateways spend the same tokens. A local mutex does not cover other machines. Redis scripting can provide local atomic execution; it is not automatically a global multi-region or failover durability guarantee.

Partition by limiter identity to distribute accounts. A single abusive identity remains hot. Local reservations of token budgets can reduce shared-store calls but introduce bounds on overshoot/unused capacity; quantify them. Per-region quotas can deliberately partition a global budget. Independent full budgets in each region violate a global cap.

## Store failure is a product choice

Fail-open preserves access but may destroy protection; fail-closed protects a backend but can reject everyone when the checker fails. Use endpoint-specific policy, bounded fallback budgets, or another explicit degraded mode. A denied response should provide meaningful retry guidance when possible; clients need backoff rather than synchronized retries.

Rules need versioning, propagation, and rollback. Separate rate limiting from concurrency limiting: a slow dependency may require a cap on in-flight work even when arrival rate is acceptable. Admission control should protect the actual scarce resource.

## Verify operation

Measure check latency/errors, rejection by rule, downstream saturation, and unexpected admissions. Avoid per-user metrics with unbounded cardinality. Test two callers with the last token, failover, rule updates, and a hot identity. Explain any precision versus availability trade-off instead of claiming one algorithm guarantees all goals.

## Retrieve before practicing

Compare exact rolling limits with bursty token refill. Trace a last-token race and global-budget isolation.
