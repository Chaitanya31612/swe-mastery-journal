# Data access, caches, and atomic boundaries — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Preserve the inventory invariant

Atomically claim a ticket/hold in the authoritative store with a conditional transition and a unique scoped request identity. Only one client wins. Return a hold/job state rather than treating approximate cache inventory as authority. Persist payment attempt identity and provider reference; use provider idempotency if offered, query/reconcile uncertain outcomes, and transition confirmation under a transaction after the outcome is known. Coordinate hold expiration with payment-in-flight/confirmed states so a sold ticket is not released by a blind timer.

A serialized transaction/row lock is another viable allocation mechanism; a process-local mutex is insufficient across instances. Exactly how long holds last and how failed payment releases inventory are product decisions. If the provider supplies no deduplication/status cooperation, do not claim exactly one remote charge under arbitrary timeouts.

## P2 — Freshness and races

Keep a versioned profile in the store. A source read of version 3 started before a writer commits version 4 can populate stale content after invalidation. A policy needs an explicit freshness bound or stronger version-aware write/read publication; blindly deleting the key is incomplete. Return the committed update to the writer and use a consistency/version token or authoritative reads where read-your-writes matters. Bound TTL and invalidation/propagation delay for other users. Five seconds is a requirement, not evidence that every invalidation path achieves it. On cache loss, bound DB fallback and coalesce popular misses.

### A concrete freshness design

One conservative starting choice is to read the small profile from the authoritative primary while measuring whether 2,000 indexed reads/s fit the deployment. Return the committed profile to the writer. This avoids making a freshness claim from a cache protocol you have not proved. If a cache is needed, use version-aware publication and an absolute freshness deadline tied to the source-read snapshot time, not a new full TTL starting whenever a delayed stale reader finishes. Reject/refetch results that are already beyond that deadline, and account for client/edge caching and response delay. Invalidations improve freshness; the explicit bounded policy supplies the stated limit under documented timing assumptions. This costs more source work or more metadata coordination than a blind TTL cache.

## P3 — Correct the order

Checking cached availability is not an atomic claim. Charging before claiming allows multiple charges for one ticket; a timeout can be followed by a duplicate charge; a later DB failure strands the external effect. Use a durable request/state machine, authoritative claim, retry-safe provider request, and reconciliation before confirmation. The local transaction covers local records, not the remote payment call. Define compensation and manual recovery for unresolved outcomes.

## Checkpoint explanations

1. **B.** B makes one shared decision. A has a gap; C does not cover other instances; D can worsen stale reads.

2. **C.** An earlier reader can repopulate old data. A/B/D overstate an invalidation action.

3. **D.** The local transaction boundary excludes arbitrary provider effects. A/B/C conflate boundaries.

4. **A.** Access and correctness needs guide the model. B/C are shortcuts; D moves schema responsibility rather than removing it.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
