# Requests, scale, and useful estimates — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Calculations and consequence

Views: 300 million/day ≈ 3,472/s average and 17,361/s peak. Reviews: 500,000/day ≈ 5.79/s average and 28.9/s peak. Four reads/view implies about 13,889 DB reads/s average and 69,444/s peak before caches/batching. Delivered pages use about 69.4 MB/s average, or 556 Mb/s; peak is roughly 347 MB/s or 2.78 Gb/s using decimal 20 KB. Three years of review bodies: `500,000 × 1,095 × 1,000` ≈ 547.5 GB raw, before copies/indexes.

Separate cacheable product data from owner-specific data; design useful keys/indexes, stateless serving, and controlled cache fallback. Unknown hit rate, distinct working set, request amplification, payload distribution, burst duration, and measured store capacity affect the design. The calculation does not prove that the chosen database handles the peak or that all responses are CDN-cacheable.

## P2 — Diagnosis

Stable mean in-flight work is `400 × 0.5 = 200`. This includes waiting, not necessarily 200 occupied CPU workers. Pool wait, slow queries, long transactions, locks, and dependency latency are hypotheses. Measure pool wait/active connections, query latency, lock wait, trace spans, and arrivals/completions. Fifty instances can permit 5,000 DB connections versus 1,000 initially and worsen saturation. Bound concurrency, optimize the problematic queries/transactions, consider an appropriate pooler, and load-test. Adding replicas helps only if the workload and freshness contract permit it.

## P3 — Capacity argument

The local benchmark may omit real payloads/dependencies, tail latency, burstiness, and redundancy. Size to a measured workload and target latency with headroom, account for peaks and one-instance failure, and validate warm-up/overload behavior. There is no universally correct headroom percentage; choose it from observed uncertainty and service objectives.

## Checkpoint explanations

1. **A.** L=λW estimates average in-flight work. B/C confuse concurrency with resources; D is not implied.

2. **B.** Wait measurements locate the limit. A/D assume it; C ignores blocked work.

3. **C.** The stored working set and policy matter. Daily traffic may repeatedly access the same objects; B/D do not size that set.

4. **D.** Buffering buys time, not unlimited sustainable throughput. A is finite; B lacks capacity evidence; C can increase load.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
