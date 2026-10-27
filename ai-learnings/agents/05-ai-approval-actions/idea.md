## Understand

A user approving “update this note” should not approve a later, different payload. Bind approval to an exact operation: actor, target, normalized arguments, relevant record version, scope, and expiry. Make the preview readable in ordinary language.

At execution, reauthorize, compare the current record/version, check the approval identity, and apply a stable business idempotency key. If the operation changed or became stale, require a new preview. The model cannot approve its own proposal.

Separate proposal, approval and execution status. A UI confirmation is not a database lock. An approved write can still fail or have an unknown outcome. Keep an audit trail and reconciliation path. The main course example remains read-only; the action sandbox illustrates these boundaries using synthetic in-memory data.
