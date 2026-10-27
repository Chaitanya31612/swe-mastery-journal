## Understand the idea

A transient outage and an invalid schema are different failures. Retrying malformed data forever does not repair it.

Classify failures, bound attempts/delay, and retain enough safe context for diagnosis.

Blocking a partition preserves its processing order but can hold back unrelated keys there. Sending a failed item to a retry topic lets later records advance, which can reorder one entity’s effects.

A dead-letter/quarantine path needs ownership, alerting, retention, and redrive rules; it is not a successful business outcome.

Never commit past required work silently. If the product permits skipping/quarantine, record that decision durably and explain the resulting projection completeness.

Replays must remain idempotent and schema-compatible.