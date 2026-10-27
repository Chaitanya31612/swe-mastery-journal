## One valid approach

Track call identity and durable execution status. For reads, avoid ambiguous duplicated continuation items; for writes, require idempotent execution and reconcile uncertain outcomes.

A call ID is a correlation handle, not automatically an idempotency key enforced by the business system.

Other designs can work. Check the stated constraint, the trust boundary, and the changed condition.

Do not award yourself a passing check for naming a tool.