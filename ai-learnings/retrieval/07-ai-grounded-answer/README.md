# 7. Grounding, citations, and the support gap

**Intermediate · about 2 hours including practice**

Distinguish source membership, claim support, freshness, and authority.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Claim and source ID"]
 N1["Source membership"]
 N2["Exact fact checks"]
 N3["Semantic support and freshness"]
 N4["Honest result labels"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
