## Trace the execution

Read query inside computed → Vue records that dependency. Change query → computed becomes stale → a dependent render asks for the new value.

Several synchronous writes can lead to one DOM update batch.

Use shallowRef when you intentionally treat a large outside object as one replaceable value. Deep mutation will not behave like an ordinary deep reactive ref.

Choose it for a reason, such as an external editor instance, not as a universal speed switch.