# 6. Regression gates, shadow mode, and incident response

**Intermediate · about 2 hours including practice**

Release model, prompt, tool, and index changes as versioned application changes.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Versioned change"]
 N1["Runtime and held-out checks"]
 N2["Bounded shadow or cohort"]
 N3["Monitor product outcomes"]
 N4["Rollback and regression fixture"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Composable agent patterns](https://www.anthropic.com/research/building-effective-agents)
