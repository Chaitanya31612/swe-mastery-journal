# 13. ElastiCache: choose managed cache and queue roles deliberately

**Intermediate · about 2 hours with practice**

Separate cache data from durable work and plan client behavior during eviction or failover.

## Use it

Rails caches, sessions, and queue infrastructure.

**Benefit:** Managed in-memory service operations.

**Cost or limit:** Role mixing and fallback behavior can threaten correctness or the DB.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [ElastiCache overview](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html)
- [Redis eviction](https://redis.io/docs/latest/develop/reference/eviction/)
