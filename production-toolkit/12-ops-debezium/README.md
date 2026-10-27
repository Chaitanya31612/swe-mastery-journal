# 16. Debezium: capture committed changes without inventing business meaning

**Intermediate · about 2 hours with practice**

Explain CDC, snapshots, log positions, outbox routing, and duplicate-safe downstream processing.

## Use it

Search/reporting projections and deliberate event publication.

**Benefit:** Captures committed changes without app-level network dual writes.

**Cost or limit:** Connector state, source logs, schema exposure, and cutover require operations.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Debezium outbox router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)
- [PostgreSQL connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)
