# Consistent hashing, placement, and migration — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Placement

Before: 5→A, 20→B, 40→B, 60→C, 90→A. After adding D=30: 5→A, 20→D, 40→B, 60→C, 90→A. Ownership interval (15,30] moves from B to D. Old clients may still read/write B. For disposable cache data, tolerate misses with bounded rewarming and update membership consistently; avoid saturating the backing store. For authoritative data, mixed routing needs a correctness protocol, not just a config push.

## P2 — Migration

Create a new routing epoch; snapshot the interval; transfer and replay concurrent changes under a single authoritative writer or an explicitly coordinated dual-write scheme; verify catch-up/checksums; cut over with fencing/versioned routes; retain a recovery/rollback window. Reads can route to the authoritative source until verified or use safe fallback under the selected contract. Blind dual writes can diverge, so describe ordering/reconciliation. A hot key needs special serving/admission/ownership strategies; ring balance averages key placement, not request popularity.

## P3 — Repair

Choose distinct physical/failure domains for replicas. Hashing is only ownership mapping; durability, versioning, repair, and health/membership are separate mechanisms. Do not delete the source before transfer/catch-up and compatible routing have been verified. Avoid assuming exact uniformity or that virtual nodes split a single serialized key operation.

## Checkpoint explanations

1. **D.** D follows successor placement. A/B ignore the ring; C overstates movement independent of positions/data.

2. **A.** Virtual positions do not create independent hardware. B/C/D mistake logical placement for fault independence.

3. **B.** B identifies load skew. A/D are unrelated; C cannot automatically divide the hot key.

4. **C.** C requires additional protocols. A/B/D describe the placement algorithm.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
