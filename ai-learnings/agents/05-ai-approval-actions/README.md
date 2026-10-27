# 5. Write actions: preview, approval, and stale state

**Intermediate · about 2 hours including practice**

Bind approval to an exact operation and recheck it before an effect.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Exact proposed action"]
 N1["Readable preview"]
 N2["Scoped approval"]
 N3["Current policy and version"]
 N4["Idempotent effect and outcome"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [MCP security boundaries](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)
- [Composable agent patterns](https://www.anthropic.com/research/building-effective-agents)
