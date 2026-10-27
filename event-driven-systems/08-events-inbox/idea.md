## Understand the idea

A consumer can receive a record again after a crash/rebalance/replay. A seen? query followed by a write races when two processes overlap. Use a unique consumer-specific event key at the authority that stores the effect.

An inbox row and projection update in one DB transaction make the local effect repeat-safe: either both commit or neither does. A later Kafka offset commit remains a separate step. If that commit fails, replay checks the inbox and avoids repeating the local projection.

This does not atomically include email, another database, or every external API. Each side-effect boundary needs its own intent/idempotency/reconciliation design. “Exactly once” must name the scope where it is enforced.
