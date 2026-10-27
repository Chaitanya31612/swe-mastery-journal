# 7. Lambda event functions: small work with explicit retry boundaries

**Beginner · about 2 hours with practice**

Choose an event-function boundary and handle retry, concurrency, and database pressure.

## Use it

Queue/S3-triggered small processing steps.

**Benefit:** Managed event-driven compute without operating a VM per handler.

**Cost or limit:** Trigger semantics, cold starts, concurrency, and downstream limits remain.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Lambda overview](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
