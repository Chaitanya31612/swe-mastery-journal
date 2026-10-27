# 3. Frameworks and multiple agents: earn the complexity

**Advanced · about 2.5 hours including practice**

Compare explicit orchestration, framework runtimes, and specialized agents using task evidence.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Simple orchestration baseline"]
 N1["Needed runtime capability"]
 N2["Restricted specialist handoff"]
 N3["Validated synthesis and review"]
 N4["Measured benefit and cost"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Composable agent patterns](https://www.anthropic.com/research/building-effective-agents)
- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
