# 8. Consumer inbox: one local effect for a repeated event

**Intermediate · about 2 hours with practice**

Commit deduplication and projection changes together, then acknowledge Kafka progress.

## Use it

Reporting/search/materialized projections.

**Benefit:** Repeat-safe local effects across process crashes.

**Cost or limit:** External side effects need additional boundaries.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Kafka consumer contract](https://kafka.apache.org/41/configuration/consumer-configs/)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
