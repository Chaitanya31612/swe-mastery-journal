# 14. DOM events, cleanup, and resource ownership

**Intermediate · about 2 hours with practice**

Trace event propagation and release listeners, timers, observers, and subscriptions with their owner.

## Use it

Route transitions, realtime UI, resize handling, and forms.

**Benefit:** Fewer duplicate actions and retained screens.

**Cost or limit:** Resource ownership is separate from rendering correctness.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [MDN event bubbling](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Event_bubbling)
- [Vue lifecycle](https://vuejs.org/guide/essentials/lifecycle.html)
