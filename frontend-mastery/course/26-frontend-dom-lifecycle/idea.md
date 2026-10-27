## Understand the idea

An event travels through capture, target, and bubble phases when the event supports propagation. target is where it originated; currentTarget is the element whose handler is running.

Event delegation puts a handler on a stable ancestor and checks the relevant descendant. It is useful for dynamic lists, but needs a precise match and containment check.

preventDefault cancels a supported default action. stopPropagation changes event propagation. They solve different problems.

A button inside a form defaults to submit unless its type says otherwise. Correct HTML often avoids a JavaScript workaround.

Every long-lived resource needs an owner: window listener, timer, ResizeObserver, WebSocket, and subscription. Vue watchers created synchronously in setup are linked to the component; manually created resources still need cleanup.

A watcher created later outside that scope may need explicit disposal.