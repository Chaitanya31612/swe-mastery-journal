# MCP: host, client, server, and model

Draw the MCP boundary without confusing the protocol with the model or application policy.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
flowchart LR
 U[User] --> H[AI host application]
 H --> M[Model provider]
 H --> C1[MCP client connection A]
 H --> C2[MCP client connection B]
 C1 <-->|MCP messages| S1[Shipment MCP server]
 C2 <-->|MCP messages| S2[Document MCP server]
 S1 --> P1[Application policy and shipment tools]
 S2 --> P2[Permitted documents]
 P1 --> D1[(Shipment database)]
 P2 --> D2[(Document store)]
```

Remember: **MCP connects capabilities. Your application still owns the decisions.**
