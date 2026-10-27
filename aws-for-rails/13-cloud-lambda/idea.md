## Understand the idea

This chapter focuses on Lambda event functions: a handler invoked under a configured event source. Other Lambda offerings have different contracts. A small S3 metadata check or queue-driven transformation can fit well; a large always-warm Rails web process is a different decision.

The trigger controls invocation and retry semantics. A queue event source is not identical to a synchronous API call. A batch can contain several records, and reporting failure incorrectly can repeat already completed items. Keep the logical effect idempotent.

Setup: choose the runtime and handler, attach a narrow execution role, configure environment/secret access, timeout/memory/concurrency, connect the event source, and test failure plus repeated delivery. If using private database access, plan network paths and connection multiplication.
