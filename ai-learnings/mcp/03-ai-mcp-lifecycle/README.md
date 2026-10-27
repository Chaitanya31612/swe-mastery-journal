# JSON-RPC and the MCP lifecycle

Trace initialization, capabilities, request IDs, tool calls, errors, and notifications.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
sequenceDiagram
 participant H as Host MCP client
 participant S as MCP server
 H->>S: initialize with version and capabilities
 S-->>H: Selected version and server capabilities
 H->>S: notifications/initialized
 H->>S: tools/list
 S-->>H: Tool names and input schemas
 H->>H: Choose whether to expose tools to model
 H->>S: tools/call with request ID and arguments
 S->>S: Validate current actor and object access
 S-->>H: Tool result or error
 H->>H: Correlate result and apply execution budget
```
Remember: **Negotiate first. Correlate carefully. Classify the failure.**