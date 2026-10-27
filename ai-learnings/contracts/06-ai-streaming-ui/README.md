# 6. Streaming with honest UI states

**Intermediate · about 2 hours including practice**

Render partial output without treating it as a validated final answer.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Run identity"]
 N1["Typed stream events"]
 N2["Partial presentation"]
 N3["Final validation"]
 N4["Completed or honest fallback"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Response streaming](https://developers.openai.com/api/docs/guides/streaming-responses)
