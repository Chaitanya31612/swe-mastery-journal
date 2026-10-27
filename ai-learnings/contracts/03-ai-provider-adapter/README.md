# 3. A Rails provider adapter you can replace

**Intermediate · about 2 hours including practice**

Keep provider request formats outside the business use case and normalize failures.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Rails use case"]
 N1["Application adapter interface"]
 N2["Provider-specific request"]
 N3["Normalized result"]
 N4["Business validation and UI"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Amazon Bedrock tool use](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html)
