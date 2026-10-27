## Understand the idea

A feature flag changes which behavior is active for a context. It can separate deployment from exposure and help a controlled rollout. It does not undo data already written or remove the need to test both paths.

Define the flag owner, intended lifetime, targeting inputs, safe default, and removal plan. Evaluate permissions on the server regardless of a client flag. A client-visible flag is not a secret access gate.

A flag provider is another dependency. Decide whether evaluation is local/cached/remote and what happens when it is unavailable. Keep the old/new schema compatible during overlap. Avoid combining many flags into untested state combinations.
