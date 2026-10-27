## Understand the idea

A composable is a function that packages reusable stateful logic. It is not simply any helper with use in its name.

A pure formatter is often just a function.

Choose where state is created. A ref inside useSelection gives each call its own selection.

A ref at module scope is shared by every caller in that JavaScript runtime. That can be deliberate for a store, but dangerous for per-request state in server rendering.

Return refs when callers need to destructure reactive values. Accept a getter/ref when the input should remain live, and watch that input explicitly.

Register lifecycle cleanup while the component context is available. Detached listeners, intervals, and subscriptions must have a lifetime owner.