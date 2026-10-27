# 14. Multi-tenant scopes and object-level permission

**Intermediate · about 2 hours with practice**

Keep workspace identity in reads, writes, caches, jobs, and tests.

## Use it

B2B workspaces and delayed background actions.

**Benefit:** Protects cross-tenant data and makes scope testable.

**Cost or limit:** Implicit context is convenient but easy to lose across jobs and caches.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Rails controller scopes](https://guides.rubyonrails.org/v4.2/action_controller_overview.html)
- [Rails security](https://guides.rubyonrails.org/v4.2/security.html)
