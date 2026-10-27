# 1. Advanced retrieval: hierarchy, graphs, and query planning

**Advanced · about 2.5 hours including practice**

Choose advanced retrieval from a query failure pattern rather than a trend.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Query category and failure"]
 N1["Simple measured baseline"]
 N2["One advanced strategy"]
 N3["Bounded permitted evidence"]
 N4["Support cost and freshness comparison"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [GraphRAG research](https://arxiv.org/abs/2404.16130)
- [PageIndex implementation](https://github.com/VectifyAI/PageIndex)
- [Your AI journal](https://github.com/Chaitanya31612/ai-mastery-journal)
