# Transfer assessment and graduation evidence — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1A — Registry reasoning

Downloads average 11.6/s and bodies about 116 MB/s ≈0.93 Gb/s before peaks; publishes average 0.58/s and raw new artifacts grow about 500 GB/day. Separate immutable object bytes from authorized version metadata. Publish only verified objects; use tenant/version ownership and durable unique version creation. Immutability permits byte caching, but compromised-version blocking needs an access/revocation path whose client/CDN/token behavior fits five seconds. Long-lived public URLs can violate it. A hot package motivates replicated/CDN delivery and bounded origin misses, not automatic metadata sharding. Discuss egress, integrity, rollback, and policy metrics.

## P1B — Import reasoning

Use upload sessions, scoped durable job identity, input version/checksum, bounded parsing/workers, tenant authorization, and a job state machine. Row/batch effects and the progress marker should share an atomic boundary where possible; otherwise replay must use stable row/batch identity or another deduplicated reconciliation protocol. Concurrent imports need explicit per-record/version/ordering/conflict rules, not merely separate queues. A crash after batch commit can safely replay only if effects are idempotent or completion can be discovered durably. Report accepted versus complete, partial failure, lag, and retention. Validate untrusted files and isolate tenant resource consumption.

## P1C — Slot reasoning

Authoritative slot state has available/held/confirmed/cancelled plus version, owner/request identity, and hold deadline. Claim and transitions are conditional/transactional; cache reads only advertise approximate availability. Expiry and confirmation compete on the same version/state so only a permitted transition wins. A blind timer must not free a confirmed slot. Stable retry identities return prior results. Use a defined server clock/deadline model and recovery for crashed workers; delayed expiration can reduce availability while preserving safety. Explain fairness, load, authorization, and measured contention.

These sketches are comparison criteria, not unique final diagrams. A stronger/alternative protocol can pass if it meets the stated contract and failure assumptions.

## P2 — Evidence standard

Use actual code/config/log evidence for observed flows. Label unknown production scale and inferred failure risks. A proposal is supported by a metric/test, an alternative, migration compatibility, and rollback. The result cannot be prewritten as facts without examining the selected system.

## P3 — Honest completion

Reading/recognition, hinted matching, and MCQs do not prove unaided transfer or delayed retention. Missing evidence includes unfamiliar timed rounds, changed-constraint reasoning, intact invariants, later retrieval, and real-system application. Say “I completed the readings/practices; independent transfer remains unassessed” until evidence supports a stronger statement. No assessment proves you can solve every possible interview.

## Checkpoint explanations

1. **C.** C measures the skill sought. A/B/D are study artifacts or recognition.

2. **D.** MCQs test bounded understanding. A/B overclaim; C discards useful but limited information.

3. **A.** Correctness is a gate. B/C/D reward surface features despite broken service behavior.

4. **B.** B demonstrates architectural reasoning. A/C/D avoid the guarantee boundary.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
