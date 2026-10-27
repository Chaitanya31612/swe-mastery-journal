# 5. Consumers: groups, positions, stored offsets, and commits

**Beginner · about 2 hours with practice**

Predict replay from the committed next offset and avoid acknowledging unfinished work.

## Use it

A reporting group with controlled replay.

**Benefit:** Independent subscribers and explicit progress.

**Cost or limit:** Incorrect offset handling can lose or duplicate business work.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Kafka consumer config](https://kafka.apache.org/41/configuration/consumer-configs/)
