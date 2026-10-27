# 6. Sampling and reproducible experiments

**Intermediate · about 2 hours including practice**

Explain temperature and evaluate changes without mistaking one lucky output for reliability.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Versioned fixtures"]
 N1["Fixed baseline"]
 N2["One deliberate change"]
 N3["Category-level comparison"]
 N4["Held-out release check"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
