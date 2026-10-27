# 17. Refactor callback-heavy Rails without changing behavior accidentally

**Intermediate · about 2 hours with practice**

Map hidden effects, move orchestration carefully, and keep a regression timeline.

## Use it

Legacy concerns and duplicate background effects.

**Benefit:** Makes hidden behavior explainable and refactoring safer.

**Cost or limit:** A complete caller map and version-aware tests are necessary.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Rails 4.2 callbacks](https://guides.rubyonrails.org/v4.2/active_record_callbacks.html)
