# 14. Integration tests, migrations, and a release rehearsal

**Intermediate · about 2 hours with practice**

Prove the deployed configuration, database changes, and failure recovery beyond mock tests.

## Use it

A service release with a schema change and background delivery.

**Benefit:** Makes deployment assumptions testable.

**Cost or limit:** Integration environments cost time and still do not cover every production condition.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Spring testing](https://docs.spring.io/spring-boot/reference/testing/index.html)
- [Testcontainers PostgreSQL](https://java.testcontainers.org/modules/databases/postgres/)
