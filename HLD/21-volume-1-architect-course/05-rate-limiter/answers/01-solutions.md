# Distributed rate limiting and overload control — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Exact contract first

A per-account sliding timestamp log is a defensible choice for exact rolling enforcement at modest per-account activity. Atomically evict entries outside the selected interval, count remaining accepted operations, reject at 120, or append a unique request identity/timestamp. Specify endpoint/account identity, interval endpoints, server time policy, memory overhead, and durable/failover assumptions. Estimate active-account count × retained entries × per-entry overhead; 15,000/s alone cannot size memory.

A token bucket with refill 120/minute and positive burst capacity does not enforce the exact rolling contract. An approximate alternative is acceptable only if the product changes its requirement. On uncertain checker results, define retry/dedup behavior; fail closed for these protected writes or use a mechanism whose bounded emergency admissions still fit the promise. Do not claim exact enforcement across data-losing failover without a stronger store/protocol.

## P2 — Assigned capacity

Partition the provider budget into regional shares, e.g. 6,000/s and 4,000/s. Rebalance ownership with disjoint allocations and fencing/expiry assumptions. During partition use only the already safe share/emergency allocation, not a fresh full quota. Dynamic leased tokens improve utilization but need safe lease expiration/clock behavior and prevent two owners spending the same allocation. Static shares are simpler but can strand capacity.

## P3 — Race and interval

Two instances read the same count and both allow, losing an increment/overshooting. An atomic increment alone does not encode rolling timestamps or reject consistently. Implement the whole check/record/window eviction atomically on shared state for the chosen algorithm. Clarify retries, TTL cleanup, time assumptions, and failure/failover policy. A process lock is not a distributed repair.

## Checkpoint explanations

1. **C.** Stored tokens permit an initial burst. A/B ignore capacity; D is unrelated.

2. **D.** D binds the policy to a verified principal. A/C are forgeable; B fails for shared/rotating addresses.

3. **A.** Independent allocations can double spending. B/C/D do not coordinate budget ownership.

4. **B.** Admission by rate and in-flight capacity are distinct. A/C can worsen load; D does not directly bound ongoing work.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
