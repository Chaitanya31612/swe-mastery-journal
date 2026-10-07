# Autocomplete: derived indexes, top-K, and fresh snapshots — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Capacity and index

600 million autocomplete requests/day ≈6,944/s average, 34,722/s peak. Build aggregate eligible popularity data and a versioned prefix/top-K index; replicate/cache hot serving paths. Prefix trie top-K or a compact prefix index is defensible when measured memory/build costs fit. The one-hour freshness goal permits batched publication, but five-second blocked-term removal needs an independent fast policy/filter and controlled caching. Track publication age, serving latency, and removal leakage. Request volume does not directly determine RAM without vocabulary/node/top-K size.

## P2 — Tenant directory

Scope index/cache keys to authorized tenant/directory/version and perform appropriate access checks. Index the canonical names rather than collecting global search popularity by default. An indexed relational prefix lookup may suffice within a bounded tenant; compact per-tenant indexes are another option at measured scale. Names are personal data; avoid cross-tenant sharing and query-history exposure. Tenant count alone does not justify global public top-K.

## P3 — Two different races

Assign an input/request sequence and only display the response matching the current query/version. Cancellation can reduce work but does not by itself prove an older response cannot arrive. During server rebuild, construct a new immutable version, validate, then switch the published pointer; retain old version for rollback. The client request race and server snapshot race require different fixes.

## Checkpoint explanations

1. **B.** B is precomputation. A ignores cost; C is unacceptable/unnecessary; D adds a different matching requirement.

2. **C.** Different freshness classes require another mechanism. A/D violate removal; B does not change policy state.

3. **D.** D addresses the client race. A/B/C do not order asynchronous responses.

4. **A.** A protects isolation/freshness. B/D can leak cross-tenant results; C is irrelevant.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
