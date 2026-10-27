# 5. A Ruby MCP tool around a Rails use case

**Intermediate · about 2 hours including practice**

Expose a narrow Rails read without moving business policy into a model or SDK class.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Authenticated context"]
 N1["Typed tool arguments"]
 N2["Shared domain service"]
 N3["Scoped facts"]
 N4["Protocol response"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Official Ruby MCP SDK](https://ruby.sdk.modelcontextprotocol.io/server/)
- [MCP security boundaries](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)
