# 7. Trace the integration, not private conversations

**Intermediate · about 2 hours including practice**

Record the boundaries needed to debug quality, latency, and cost without dumping sensitive text.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Run and version IDs"]
 N1["Retrieval and tool spans"]
 N2["Validation decisions"]
 N3["User-visible outcome"]
 N4["Restricted feedback and evaluation"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
