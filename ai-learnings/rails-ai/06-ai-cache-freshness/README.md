# 6. Cache answers without caching the wrong authority

**Intermediate · about 2.5 hours including practice**

Separate prompt caching, retrieval caching, and answer caching with correct invalidation.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Cache type"]
 N1["Task and authority key"]
 N2["Version and expiry"]
 N3["Current access gate"]
 N4["Valid reused result or recompute"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- [MCP security boundaries](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)
