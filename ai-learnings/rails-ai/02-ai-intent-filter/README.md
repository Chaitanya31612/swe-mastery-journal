# 2. From user language to an allowlisted Rails query

**Intermediate · about 2.5 hours including practice**

Turn a proposed intent into previewed filters without executing generated SQL.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["User wording"]
 N1["Proposed small intent"]
 N2["Allowlist and name resolution"]
 N3["Previewed scoped query"]
 N4["Exact result and manual fallback"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Function calling](https://developers.openai.com/api/docs/guides/function-calling)
