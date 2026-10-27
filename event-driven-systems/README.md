# Event-driven systems · Kafka & Rails

Beginner builds the model. Intermediate adds real constraints, failure cases, and tradeoffs. Follow the sequence below. Folder names and module IDs stay stable for saved progress.

## Beginner

- 01. [Events, commands, queues, and a retained log](01-events-logs-queues/README.md): Choose messaging from responsibility, history, replay, and timing needs.
- 02. [Topics, partitions, keys, and local order](02-events-partitions/README.md): Predict record placement and explain the scope and limits of ordering.
- 03. [Kafka layers: clients, brokers, storage, replicas, controllers](03-events-layers/README.md): Follow one record through discovery, batching, append storage, replication, and consumer fetch.
- 04. [Producers: acknowledgements, idempotence, and duplicate business events](04-events-producer/README.md): Distinguish client retry deduplication from repeated application publication.
- 05. [Consumers: groups, positions, stored offsets, and commits](05-events-consumers/README.md): Predict replay from the committed next offset and avoid acknowledging unfinished work.
- 06. [Event envelopes, evolution, and privacy](06-events-schemas/README.md): Define event identity, entity key, business version, time, and a compatible payload contract.

## Intermediate

- 07. [Rails transactional outbox: save intent with the change](07-events-outbox/README.md): Close the DB/publish loss gap while accepting and handling duplicate publication.
- 08. [Consumer inbox: one local effect for a repeated event](08-events-inbox/README.md): Commit deduplication and projection changes together, then acknowledge Kafka progress.
- 09. [Retries, poison events, and the ordering tradeoff](09-events-retries/README.md): Choose blocking retry, retry topics, or quarantine from the required per-entity behavior.
- 10. [Lag, rebalances, retention, and the debugging checklist](10-events-operations/README.md): Diagnose slow or missing processing from broker, group, DB, and event identity evidence.
- 11. [Read the Rails/Kafka app one file at a time](11-events-rails-lab/README.md): Run and explain the complete multi-file path from HTTP completion to a repeat-safe reporting projection.
- 12. [Replay, rebuild, and explain the complete event system](12-events-replay-capstone/README.md): Design a safe projection rebuild and explain which effects may and may not be replayed.
