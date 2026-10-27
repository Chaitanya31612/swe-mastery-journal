# 3. Build a fact bundle before explaining a cause

**Intermediate · about 2.5 hours including practice**

Create a minimal versioned fact set and keep verified rules separate from generated interpretation.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Authorized source"]
 N1["Reviewed rule"]
 N2["Versioned minimal facts"]
 N3["Generated draft"]
 N4["Checked facts and coverage labels"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
