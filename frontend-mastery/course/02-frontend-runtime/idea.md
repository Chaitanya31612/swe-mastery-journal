# The idea

JavaScript code runs on a call stack. Browser events and timers schedule later tasks. Promise callbacks use a microtask queue, which is drained after the current stack before the next task. A zero-delay timer means “eligible later,” not “run now.”

Closures retain access to lexical bindings. const prevents rebinding the name; it does not freeze the object. let in a loop creates useful per-iteration bindings. Prototype lookup chooses inherited properties when an own property is absent.

Async requests can finish out of order. If a search for “ca” finishes after “cat,” blindly applying both results makes the screen go backward. Cancellation can save work, but a latest-request check makes the UI’s acceptance rule explicit.
