# Production practice: service objectives, security, and safe evolution — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — What a good review contains

The answer depends on observed evidence. For the learning app, inspect the real frontend dataset loads, progress persistence, and optional backend paths before drawing them. A cross-device progress service would be a proposed new requirement, not an observed component. Choose an SLI representing the actual user action; label load/cost numbers unknown until measured. Cite code/config for flow claims, identify a plausible failure and metric that would confirm it, and compare a small improvement with its operational cost. Passing evidence distinguishes facts from architectural imagination.

## P2 — Compatible evolution

Add optional/default version metadata without breaking old readers. Deploy compatible readers, then writers that conditionally update versions under an authoritative mapping transition. Backfill from a checkpointed source while tracking concurrent updates so it cannot overwrite newer state. Validate counts/versions/behavior, canary cutover, and retain old paths/data through a rollback window. If old writers cannot preserve the new edit invariant, fence/remove their writes before enabling edits. Rolling back code that ignores required versions can be unsafe; rollback policy must preserve the introduced contract or disable the feature safely.

## P3 — Stabilize and verify

Set end-to-end/dependency deadlines, retry-safe bounded attempts with jitter, and admission/concurrency controls. Classify provider errors/unknowns and reconcile where needed. Worker scaling is limited by provider quotas and the actual resource; inspect queue age and completion rate. Restore-test backups against RPO/RTO rather than asserting recovery. Stage schema evolution, validate canaries, retain compatibility/rollback, and remove old representation only after proof and the agreed window.

## Checkpoint explanations

1. **C.** C measures useful completion. A/B/D are diagnostic inputs, not sufficient user success.

2. **D.** D is retry amplification. A/B/C are false guarantees.

3. **A.** Restoration and loss windows require validation. B/C/D conflate different mechanisms.

4. **B.** B addresses online evolution. A/C/D omit state and deployment correctness.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
