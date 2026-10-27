# 11. SQL plans, connection pools, and transaction size

**Intermediate · about 2 hours with practice**

Investigate a slow service without assuming more threads or caching is the first fix.

## Use it

Slow list endpoints and connection exhaustion incidents.

**Benefit:** Repairs the bottleneck rather than hiding it.

**Cost or limit:** Representative measurement and safe database change plans take effort.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Spring JDBC transactions](https://docs.spring.io/spring-framework/reference/data-access/transaction.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
