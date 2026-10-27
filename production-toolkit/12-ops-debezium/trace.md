## Trace the execution

Initial snapshot → catch-up log position → committed changes → routed records → consumer effects. Restart at the connector’s saved position and expect the selected delivery/recovery contract, including possible repeats.

Trace event_id from outbox row through connector/topic to the consumer inbox. Raw CDC delete/tombstone behavior and business cancellation semantics are different questions.
