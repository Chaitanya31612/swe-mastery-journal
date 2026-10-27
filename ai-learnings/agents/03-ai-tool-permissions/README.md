# 3. Tools are capabilities with a policy boundary

**Intermediate · about 2 hours including practice**

Design narrow tools and authorize every execution against current application state.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Narrow capability"]
 N1["Arguments as outside input"]
 N2["Current actor policy"]
 N3["Scoped minimal result"]
 N4["Output and egress limits"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [MCP security boundaries](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)
