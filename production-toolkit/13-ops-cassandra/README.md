# 17. Cassandra: design the query before the table

**Intermediate · about 2 hours with practice**

Explain partition/clustering keys, bounded partitions, denormalization, and the tradeoff versus PostgreSQL.

## Use it

High-volume query-specific event projections.

**Benefit:** Distributed storage designed around known access patterns.

**Cost or limit:** Denormalization, skew, consistency choices, and operations add responsibility.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Cassandra data modeling](https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/intro.html)
