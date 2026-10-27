# 12. Replay, rebuild, and explain the complete event system

**Intermediate · about 2 hours with practice**

Design a safe projection rebuild and explain which effects may and may not be replayed.

## Use it

Projection evolution and disaster-recovery reasoning.

**Benefit:** Makes replay a controlled engineering operation.

**Cost or limit:** Missing history, privacy, and irreversible effects can limit recovery.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Kafka design](https://kafka.apache.org/41/design/design/)
- [Kafka group operations](https://kafka.apache.org/41/operations/)
