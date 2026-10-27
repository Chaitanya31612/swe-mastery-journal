# 7. Rails as an MCP host: inspect, call, and debug

**Intermediate · about 2 hours including practice**

Connect a host to a server and distinguish transport, protocol, policy, tool, and model failures.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Initialized client"]
 N1["Reviewed discovered tools"]
 N2["Host translation and policy"]
 N3["Server/domain result"]
 N4["Classified trace and model continuation"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [MCP specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- [Official Ruby MCP SDK](https://ruby.sdk.modelcontextprotocol.io/server/)
