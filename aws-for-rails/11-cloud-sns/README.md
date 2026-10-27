# 6. SNS: fan out one fact to independent subscribers

**Beginner · about 2 hours with practice**

Distinguish publish/subscribe fan-out from competing workers on a queue.

## Use it

A ticket event consumed by reporting and notifications.

**Benefit:** Simple fan-out with independently buffered subscribers.

**Cost or limit:** Schema, delivery type, policies, and history/backfill remain explicit choices.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [SNS overview](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
