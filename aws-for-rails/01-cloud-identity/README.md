# 1. AWS identity: accounts, roles, and the caller you actually are

**Beginner · about 2 hours with practice**

Set up a training identity and distinguish human sign-in, workload roles, trust, and permissions.

## Use it

Every Rails-to-AWS integration.

**Benefit:** Explicit identity and smaller permission scope.

**Cost or limit:** Several policy layers can affect the final decision.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [IAM practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Ruby credential chain](https://docs.aws.amazon.com/sdk-for-ruby/v3/developer-guide/credential-providers.html)
