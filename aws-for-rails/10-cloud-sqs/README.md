# 14. SQS: work delivery, visibility, and deletion

**Intermediate · about 2 hours with practice**

Set up a queue and dead-letter path and implement repeat-safe processing.

## Use it

Exports and independent background tasks.

**Benefit:** Managed work delivery and buffering.

**Cost or limit:** Visibility, duplicate effects, and DLQ recovery still need design.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [SQS visibility](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)
