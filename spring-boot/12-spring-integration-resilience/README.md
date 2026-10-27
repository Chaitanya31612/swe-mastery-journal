# 12. Remote calls: timeouts, retries, and unknown outcomes

**Intermediate · about 2 hours with practice**

Bound dependency work and design retries around a logical command rather than an exception name.

## Use it

Email, payments, file conversion, and third-party APIs.

**Benefit:** Contained failure and explainable retry behavior.

**Cost or limit:** Some outcomes remain ambiguous without provider support.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Spring REST clients](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html)
