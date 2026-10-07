# Async workflows, retries, and notification delivery — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Capacity and states

Average arrivals ≈57.9/s; 10× peak ≈579/s exceeds the combined nominal 500/s. Burst duration and routing/content limits matter; if both providers truly serve the same pool, backlog grows about 79/s during that peak, then can drain when arrivals fall. Do not assume the combined quota is usable for all messages.

Record business intent/outbox atomically, dispatch durably, and retain notification/attempt identity with queued/attempting/known-success/unknown/permanent-failure states. Enforce preferences, expiry, per-provider quotas, and retry budgets. Retrying an unknown A attempt through B can duplicate an email even if each provider deduplicates only within itself. Reconcile or accept/document the duplicate trade-off; a cross-provider exactly-once claim needs additional cooperation not stated here. Failover is a semantic decision, not just routing.

## P2 — Reports

Record a durable job, claim with a safe lease/fencing policy, write output to a job/version-specific object, verify it, then publish completion transactionally in metadata. A repeat can reuse/recognize the same verified object. Users receive status and authorized access; abandoned uploads can be collected later. Unlike an arbitrary email effect, the application can often control deterministic output publication and make retries naturally replay-safe.

## P3 — Two failure gaps

The first crash loses the event after a committed order: use a transactional outbox or another durable intent/dispatch protocol. The second can repeat the external email: use stable provider idempotency/status support where available, local deduplication/attempt records, and reconcile unknown results. Local deduplication alone cannot prove a remote send happened exactly once when the provider response is lost. Ack only after the chosen durable outcome/state is recorded; replay remains expected.

## Checkpoint explanations

1. **B.** B is the local atomic boundary. A/C/D require separate cooperation/mechanisms.

2. **C.** Timeout cannot distinguish lost response from failed effect. A/B/D assume facts not observed.

3. **D.** Positive spare capacity is needed. A ignores assumptions; B has no net drain; C can add work.

4. **A.** A detects delayed service. B may help diagnosis but misses backlog consequences; C/D are not service indicators.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
