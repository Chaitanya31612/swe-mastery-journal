# 5. Timeouts, retries, and whole-run budgets

**Intermediate · about 2 hours including practice**

Distinguish failed requests from unknown outcomes and bound the entire integration.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Whole-run deadline"]
 N1["Failure classification"]
 N2["One retry owner"]
 N3["Bounded attempts and concurrency"]
 N4["Fallback or reconciliation"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
