## Understand

Keep domain work in an ordinary service that can be tested without MCP. The MCP tool validates its contract, obtains trusted actor context, calls that service, and serializes a small result.

This avoids duplicating business rules across protocol adapters.

Use the pinned official mcp gem in a separate modern training app. SDK APIs and supported Ruby/protocol versions change; the lab lockfile and tests identify the executable baseline.

A code fragment against a newer SDK should not be assumed to work in a legacy Rails runtime.

Return meaningful bounded errors without exposing internal exception messages or forbidden record existence. Tool descriptions help the model select a capability; they should not contain secrets or imply powers beyond the implementation.