# 2. Durable agents: resume without repeating effects

**Advanced · about 2.5 hours including practice**

Design run checkpoints, claims, leases, approval freshness, and uncertain-effect recovery.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Durable step identity"]
 N1["Claim and intent"]
 N2["Idempotent or uncertain effect"]
 N3["Observed outcome checkpoint"]
 N4["Current-policy resume"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Composable agent patterns](https://www.anthropic.com/research/building-effective-agents)
- [MCP security boundaries](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)
