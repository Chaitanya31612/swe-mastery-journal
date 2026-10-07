# News feed: projections, fan-out, and privacy — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Hybrid design

Post writes average about 4.63/s; feed reads average 231.5/s before peaks. Push to ordinary active-viewer feeds asynchronously, with idempotent viewer/post projection updates and lag monitoring. Pull or specially process high-fan-out authors; a ten-million-recipient publication is different from the average case. Merge canonical references by a deterministic time/ID order and cursor with a stated paging window.

Thirty-second feed freshness does not allow thirty-second private access leakage. Check authoritative/appropriately bounded permission state at serving and filter removed/private posts even when references remain in projections. Persist source posts plus durable event intent; rebuild projections and replay under retention assumptions. Choose peak factors from explicit workload assumptions and benchmark the actual fan-out/read merge.

## P2 — Tenant dashboard

Small bounded groups can use simpler synchronous indexed reads or modest push projections; a celebrity strategy may be unnecessary. Keys and queries must include the tenant/project authorization boundary. Preserve canonical event deletion/policy checks and measure freshness. Prefer a simple queryable store until measured read volume justifies materialization.

## P3 — Repair

Full bodies with long-lived private caching can outlive permission/deletion changes. Synchronous huge fan-out couples posting latency to millions of updates. Offset pagination shifts under inserts/deletes. Store references, separate source/derived views, enforce access at serving, perform bounded async fan-out, and use cursor/snapshot semantics. State that a cursor alone cannot freeze a dynamically changing ranked list.

## Checkpoint explanations

1. **C.** C captures heavy-tail fan-out. A ignores distribution; B/D miss semantics/work.

2. **D.** A projection is not necessarily authoritative. A leaks; B/C do not enforce policy.

3. **A.** A describes materialization. B/C/D invent guarantees.

4. **B.** Paging behavior under changes matters. A/C/D are incidental to that guarantee.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
