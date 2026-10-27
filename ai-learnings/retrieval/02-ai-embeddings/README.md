# 2. Embeddings: useful geometry, limited meaning

**Beginner · about 1.5 hours including practice**

Interpret vector similarity without treating it as truth, identity, or permission.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Input and preprocessing"]
 N1["Versioned embedding"]
 N2["Chosen distance"]
 N3["Candidate ranking"]
 N4["Relevance and access checks"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [pgvector reference](https://github.com/pgvector/pgvector)
