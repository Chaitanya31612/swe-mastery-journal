## Understand

A durable agent stores enough explicit state to survive process loss. Model proposals, tool identities, effect status, evidence versions, budgets, approvals and stopping reason need deliberate persistence.

Replaying a run is not the same as repeating every external operation.

Use step identities and state transitions. A worker can claim a step under a lease, but a paused worker may resume after another worker takes over.

Protect state changes with versions/fencing as appropriate. Business effects require stable idempotency and reconciliation; a lease alone does not make an external action exactly once.

On resume, recheck current access, evidence and approval. A checkpoint from last week cannot authorize today's changed record.

Separate pure computation/read replay from irreversible effects. Store minimal useful observations rather than unrestricted reasoning or private documents forever.