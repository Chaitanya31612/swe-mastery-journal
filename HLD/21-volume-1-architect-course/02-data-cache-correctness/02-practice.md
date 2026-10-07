# Data access, caches, and atomic boundaries — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Inventory claim

Sell the last concert ticket across four application instances. Reads can show approximate availability; a confirmed purchase must never oversell. Payment is external and can time out after success. Define schemas, operation identities, reservation/confirmation states, and authoritative claim path. Trace two competing clients and a retried request.

## P2 — Cached profile updates

A profile API has 2,000 reads/s, 20 writes/s, and a five-second visibility goal. Propose cache keys, update policy, read-your-writes behavior, and an unavailable-cache path. A stale reader began before an update and finishes afterward: include this interleaving.

## P3 — Fix bad pseudocode

```text
if cache.get(ticket_id).available > 0:
    charge(user)
    db.set_available(ticket_id, 0)
    return "confirmed"
```

Identify race/uncertainty cases. Replace this with a state-transition protocol and distinguish what a local database guarantees from what the payment provider must cooperate with.

## Delayed gate

Trace a stale-cache repopulation after invalidation; then explain the single-unit claim boundary and why an external timeout differs.
