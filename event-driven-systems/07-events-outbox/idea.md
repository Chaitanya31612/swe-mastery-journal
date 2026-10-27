## Understand the idea

A direct DB write followed by a Kafka send is a dual write. Crash after DB commit but before send loses the event. Send first and a later DB rollback can publish a fact that never committed. Neither ordering solves both cases.

An outbox stores the business change and event intent in one PostgreSQL transaction. A separate dispatcher publishes committed rows. If it crashes after Kafka acknowledgement but before marking the row published, it may resend the same event. The outbox trades lost intent for a repeatable delivery path; it does not create universal exactly-once effects.

Keep a stable event ID and a unique business rule for creating the completion fact. Define dispatcher concurrency and ordering. The lab starts with one serial dispatcher for clarity; a production multi-worker design needs claim leases/locking, throughput, ordering, and stuck-work recovery.
