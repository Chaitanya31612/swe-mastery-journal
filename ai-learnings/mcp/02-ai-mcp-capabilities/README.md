# 2. Tools, resources, prompts, and other capabilities

**Beginner · about 1.5 hours including practice**

Choose the correct MCP primitive and understand that descriptions are not enforcement.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Needed interaction"]
 N1["Tool resource or prompt"]
 N2["Negotiated capability"]
 N3["Scoped implementation"]
 N4["Reviewed host behavior"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [MCP specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- [MCP security boundaries](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)
