## Understand

A production deployment needs an explicit data boundary, identity flow, durable queue/run store, provider configuration, budgets, observability and rollback. The model call is one dependency inside that system.

Keep secrets in approved runtime configuration; never expose provider keys to the browser or MCP tool arguments.

For a legacy Rails runtime, a separate modern AI gateway can isolate newer SDKs.

The application authenticates the user, sends a minimal permitted request to the gateway, and validates the returned domain result. A gateway should not become an unscoped database administrator.

Decide which service owns record access and keep that policy enforceable.

Bedrock, direct APIs and self-hosted models differ in operations, capabilities, region and data-handling settings. Use current provider documentation and your actual organizational policy.

The course does not claim a particular provider/configuration is universally compliant or safe for private work data.