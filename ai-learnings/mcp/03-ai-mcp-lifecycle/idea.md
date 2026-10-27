## Understand

MCP uses JSON-RPC 2.0 messages under a versioned lifecycle. Initialization exchanges protocol/version and capability information. The client then signals readiness. Normal operations follow the negotiated rules. The course pins the 2025-11-25 specification as a reference; check a peer's supported revision rather than treating it as permanently latest.

Requests have IDs so responses can be correlated. Notifications do not request a response. A protocol error and a tool execution failure are different outcomes. Keep request IDs, model tool call IDs, application run IDs, and business idempotency keys distinct.

Use an SDK for supported protocol behavior, but understand the messages well enough to debug a connection. Do not build a partial imitation and label it fully compliant. The lab includes a small local client trace against the pinned Ruby SDK, plus separate tests for the domain service.
