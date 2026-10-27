# 11. Docker builds: layers, identity, and a smaller runtime

**Intermediate · about 2 hours with practice**

Build a Rails artifact without embedding secrets or relying on mutable tags.

## Use it

Rails image delivery and predictable rebuilds.

**Benefit:** Faster repeat builds and clearer runtime boundaries.

**Cost or limit:** Native dependencies, patching, and reproducibility need maintenance.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Docker build practices](https://docs.docker.com/build/building/best-practices/)
