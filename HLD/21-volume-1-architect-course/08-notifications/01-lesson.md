# Async workflows, retries, and notification delivery

Learning outcome: Separate accepted/processed/external effects, close the database-to-event gap, and design retries, quotas, and recovery.

## Promise a state transition, not “exactly once” without a boundary

A notification request may be accepted, queued, attempted, provider-accepted, device-delivered, or read. Define which state the API promises and which are observable. Queues decouple timing and buffer bursts; they do not guarantee the external provider performs an effect exactly once.

At-most-once attempts can drop work after failures. At-least-once handling permits duplicates after a crash/uncertain acknowledgment. Durable scoped operation identities, unique records, and replay-safe state transitions can prevent duplicate local effects. External email/push effects require provider cooperation or an explicitly weaker/reconciled promise.

## Close the dual-write gap

In a work queue, competing workers usually share responsibility for a logical task; redelivery still means more than one worker may attempt it over time. Pub/sub distributes an event to independent subscriber groups, such as email and analytics. A retained log/stream lets consumers track positions and replay within retention. These are behavioral models, not guarantees inferred from a product name. Partition-local order is not global order, and one consumer group’s completion does not imply another has completed.

Recording an order in a database and then publishing an event can fail between the two steps. An outbox stores the business update and event in the same local transaction. A dispatcher later publishes pending events and marks progress; publication/marking can still repeat after a crash, so downstream handling must tolerate duplicates. This pattern closes lost local intent under its transaction assumptions; it does not make all remote work atomic.

Represent attempts and retries durably. A worker claims/leases work, checks preferences/policy at the relevant boundary, renders versioned content, calls the provider with a stable identity if supported, and records a known outcome. A timeout is “unknown,” not automatically “failed.” Reconcile with provider status when possible. Preserve provider reference and request identity for investigation.

## Capacity, ordering, and backpressure

Estimate arrivals and sustained service capacity. If a provider allows 200 sends/s and arrivals sustain 300/s, queue length grows by 100/s until capacity/admission/work changes. Drain time for backlog B is B/(μ−λ) only when μ>λ under a stable simplified model. Prioritize urgent work, throttle by provider/tenant, and define overload/expiry policy.

Use bounded retry attempts/time, exponential backoff with jitter, and distinguish transient from permanent errors. A dead-letter queue is a triage/replay workflow, not a trash bin that magically fixes poison messages. Partition ordering should be only as strong as the application needs; global ordering can reduce parallelism unnecessarily.

## Operate and evolve

Measure oldest pending-event age, completion latency, provider rejection/unknown rates, retry count, and dead-letter backlog. Avoid putting private message bodies in logs. Audit preferences/authorization, credentials, and unsubscribe behavior. Roll out template/schema changes with compatible replay. Broker “exactly once” features have documented scopes; the end-to-end effect boundary must still be explained.

## Retrieve before practicing

Trace a commit/publish crash and a provider timeout. Explain which duplicates you can prevent locally and which require remote cooperation.
