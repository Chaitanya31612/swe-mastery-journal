# 6. PostgreSQL and pgvector in a Rails data boundary

**Intermediate · about 2 hours including practice**

Store versioned vectors and run scoped retrieval without letting similarity bypass access.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Actor and vector validation"]
 N1["Authorized relation"]
 N2["Exact or measured approximate ranking"]
 N3["Versioned evidence"]
 N4["Access-safe result"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [pgvector reference](https://github.com/pgvector/pgvector)
