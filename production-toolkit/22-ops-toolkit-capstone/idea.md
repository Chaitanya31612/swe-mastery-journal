## Understand the idea

A production architecture is a set of responsibilities. Packaging, orchestration, storage, messaging, observation, delivery, scheduling, and product analytics are different jobs. Several products can cover overlapping parts. Choose a coherent minimum and justify each additional tool.

For the support app, Docker packages; Compose runs the local lab; ECS or Kubernetes orchestrates; PostgreSQL owns business data; Redis may cache; Kafka carries retained events; Debezium can replace the polling outbox publisher; observability helps investigate; SendGrid/Pendo are optional external integrations with different data policies.

Practice one incident: reports are late, database connections are full, and users repeatedly click Export. Trace the oldest pending work, retries, DB waits, provider latency, and UI status. A full diagram is useful only if you can follow one item through it.
