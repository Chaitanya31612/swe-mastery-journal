# 2. Structured output: syntax is the first gate

**Beginner · about 2 hours including practice**

Validate shape and business meaning before using a model result.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Raw response or refusal"]
 N1["Parse and schema"]
 N2["Resolve business meaning"]
 N3["Check permission"]
 N4["Accepted result or fallback"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
