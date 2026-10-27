## Trace the execution

Request span begins → child SQL/client spans → context crosses a supported boundary → collector processes → backend receives → investigator queries. Inspect dropped/export-failed telemetry separately from application failures.

For a Kafka event, choose whether to propagate a trace context or use a span link, and keep event identity for business replay. Trace identity is not an idempotency key.
