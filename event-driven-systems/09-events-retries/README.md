# 9. Retries, poison events, and the ordering tradeoff

**Intermediate · about 2 hours with practice**

Choose blocking retry, retry topics, or quarantine from the required per-entity behavior.

## Use it

A consumer that must remain correct during outages and bad input.

**Benefit:** Explicit recovery instead of infinite or silent failure.

**Cost or limit:** Progress, ordering, and completeness can trade off.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Kafka operations](https://kafka.apache.org/41/operations/)
