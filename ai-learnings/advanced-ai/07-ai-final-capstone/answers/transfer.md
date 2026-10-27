## Add a write only after you can describe its exact effect

Suppose the support team now asks the assistant to close a ticket. Do not turn the read tool into a general update method.

1. Generate a bounded proposal such as ticket ID, action, reason and expected record version. The proposal has no effect.
2. Code checks current permission and builds a human-readable preview from trusted data. Show the exact record and fields that would change.
3. Bind approval to actor, operation digest, target, record version and expiry. A changed target or payload needs new approval. Keep approval outside text the model can rewrite.
4. At execution, recheck current policy and version. Use a stable business idempotency key and record durable effect status. A queue retry must not close or notify twice.
5. Handle a timeout after a possible remote effect as uncertain. Query/reconcile using the operation ID before retrying. “We did not receive a response” does not mean “nothing happened.”
6. Audit who approved and what actually happened. Define cancellation, compensation and rollback limits. Reopening a ticket may not undo an email that was already sent.
7. Add denied, changed, expired, duplicate and uncertain-outcome evaluation cases before enabling the write. Keep the first release read-only until these checks and recovery paths are reviewed.

A workflow with explicit approval may meet the need more simply than an autonomous agent. State what extra benefit autonomy would provide before accepting its added failure paths.
