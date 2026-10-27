## Follow a concrete example

```text
Delivery: Git → CI → image digest → chosen orchestrator
Request: edge/proxy → Rails → PostgreSQL → response
Async: outbox → Kafka → inbox/projection
Cache: scoped Redis copy → bounded fallback
Observation: OTel/Datadog or chosen metrics/log stack
Product: confirmed outcome → minimal analytics event
```

Write an alternative design with fewer tools and explain which requirements it still meets. Cassandra, Kubernetes, and Debezium are options, not badges.
