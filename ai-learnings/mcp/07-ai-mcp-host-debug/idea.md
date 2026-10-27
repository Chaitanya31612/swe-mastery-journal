## Understand

A Rails application can act as a host as well as a capability server. Its client initializes a connection, inspects capabilities/tools, and calls permitted operations.

A model is optional for testing that connection. Start with a known synthetic request and prove the protocol path before adding generated tool choice.

Map only reviewed tool definitions into the model's visible tool set. Bound tool descriptions and results.

Preserve both provider call IDs and protocol request IDs in the run trace without treating either as business approval. Close connections/processes under the chosen transport lifecycle.

Debug by boundary: DNS/TLS/network, HTTP identity, protocol negotiation, tool schema, domain permission, tool execution, then final model interpretation. A failure in one layer should not be reported as a generic hallucination.