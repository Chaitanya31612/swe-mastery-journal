## Understand the idea

Change data capture reads database changes through a supported source mechanism. Debezium connectors can take an initial snapshot and continue from a log position.

This is useful for integration/projections, but a row change is not automatically a well-designed business event.

An outbox table stores a deliberate event with the business transaction. A connector/outbox router can publish that committed intent instead of relying on an application polling dispatcher.

This changes the delivery machinery, not the need for schema, keys, deduplication, and recovery.

Setup concept: verify database/connector versions, required replication/log settings and privileges, snapshot/log retention, connector offsets/state, outbox schema/routing, and monitoring.

CDC can retain database logs when it stops; monitor the source as well as Kafka.