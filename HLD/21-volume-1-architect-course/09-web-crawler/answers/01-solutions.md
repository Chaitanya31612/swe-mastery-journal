# Crawler scheduling, bounded exploration, and safe fetching — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Capacity and pipeline

Ten million/day ≈116 fetches/s average, 231/s peak. At 0.5 s mean stable fetch time, approximately 58 average or 116 peak in-flight requests under simplifying assumptions. Raw body flow is about 11.6 MB/s average; 30 days of fully retained unique content would be 30 TB decimal before replicas/compression/metadata. Distinctness and retention policies can reduce it; do not assume they do.

Use durable frontier entries with host schedule/ownership, bounded workers, fetch deadlines/body/redirect limits, normalized-URL identity, content fingerprints, and replay-safe persisted results. One host is limited to 0.5/s regardless of aggregate worker capacity; scaling workers cannot defeat the allowed host schedule. Coordinate host leases and completion fencing during reassignment. Only fetch permitted destinations, validating resolved/redirected addresses and egress. Separate parse/store stages when measurements justify it.

## P2 — Refresh

Retain last fetch, observed changes, importance, error history, and next eligible time. Update predicted refresh intervals from observed changes while capping minimum/maximum and preserving a fairness budget. Conditional fetching can avoid unchanged bodies when supported. Failures back off and raise freshness risk; do not repeatedly hammer a failing site. Monitor age versus target rather than merely queue length.

## P3 — Repair

A non-atomic membership check duplicates tasks; unbounded spawns exhaust resources; host limits are missing; visited-before-success can strand failures; there is no durable retry/lease or destination policy. Insert/claim durable deduplicated tasks, choose eligible work by host/time, process within bounded concurrency and time/size budgets, persist outcome, then schedule retries/discovered tasks. “Visited” needs states, not only a boolean.

## Checkpoint explanations

1. **D.** D respects host scheduling. A/B/C confuse capacity with permission/policy.

2. **A.** A is the relevant probabilistic trade-off. B/C/D overstate the mechanism.

3. **B.** A safe initial URL can redirect elsewhere. A/C/D do not address the fetch trust boundary.

4. **C.** Durable task states support replay. A loses recovery semantics; B/D are unrelated.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
