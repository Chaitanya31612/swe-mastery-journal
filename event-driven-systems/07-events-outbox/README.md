# 7. Rails transactional outbox: save intent with the change

**Intermediate · about 2 hours with practice**

Close the DB/publish loss gap while accepting and handling duplicate publication.

## Use it

Reliable Rails facts consumed by other services.

**Benefit:** No lost publication intent after a committed business change.

**Cost or limit:** Dispatcher operations and duplicate handling remain.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Transactional outbox context](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)
