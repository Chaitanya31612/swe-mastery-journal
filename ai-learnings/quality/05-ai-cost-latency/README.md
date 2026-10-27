# 5. Cost, latency, capacity, and useful fallbacks

**Intermediate · about 2 hours including practice**

Budget accepted tasks rather than isolated token calls and protect shared capacity.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Whole-run usage"]
 N1["Quality and acceptance definition"]
 N2["Latency and capacity limits"]
 N3["One measured optimization"]
 N4["Fallback and fairness checks"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
