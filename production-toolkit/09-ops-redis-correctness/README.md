# 15. Redis correctness: persistence, atomic work, and lock expiry

**Intermediate · about 2 hours with practice**

Explain pipeline versus transaction/script, persistence loss windows, and why a lease needs stale-writer protection.

## Use it

Distributed workers, counters, and critical lock-based coordination.

**Benefit:** Prevents overclaiming what a fast coordination tool guarantees.

**Cost or limit:** Strong correctness can require authority-side mechanisms beyond Redis.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Redis transactions](https://redis.io/docs/latest/develop/interact/transactions/)
- [Redis persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)
- [Redis locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/)
