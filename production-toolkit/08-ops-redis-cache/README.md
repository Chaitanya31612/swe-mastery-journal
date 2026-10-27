# 14. Redis caching: freshness, invalidation, and stampedes

**Intermediate · about 2 hours with practice**

Design cache-aside with scoped keys and bounded rebuild behavior.

## Use it

Ticket summaries and expensive dashboard reads.

**Benefit:** Reduces repeated authority work.

**Cost or limit:** Freshness races and fallback pressure can be harder than the lookup itself.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Redis eviction](https://redis.io/docs/latest/develop/reference/eviction/)
- [Rails caching](https://guides.rubyonrails.org/v4.2/caching_with_rails.html)
