# 8. Evaluate retrieval before polishing answers

**Intermediate · about 2 hours including practice**

Build a query–evidence dataset and diagnose ingestion, retrieval, ranking, or generation failures.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Label queries and supporting spans"]
 N1["Freeze holdout"]
 N2["Measure candidate and ranking quality"]
 N3["Check access and answerability"]
 N4["Tune one stage and compare"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
