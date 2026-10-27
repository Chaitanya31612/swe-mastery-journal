# 4. Stdio and Streamable HTTP are different deployments

**Intermediate · about 2 hours including practice**

Choose a transport and locate its process, network, identity, and streaming boundaries.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Local process or remote HTTP"]
 N1["Transport lifecycle"]
 N2["Request-local identity"]
 N3["SDK protocol handling"]
 N4["Scoped tool and bounded result"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [MCP transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- [MCP security boundaries](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)
