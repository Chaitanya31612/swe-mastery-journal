# 1. Workflow or agent: choose who controls the next step

**Beginner · about 1.5 hours including practice**

Choose fixed orchestration for known paths and model-directed steps only when they earn their cost.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Task variability"]
 N1["Known workflow baseline"]
 N2["Measured need for tool choice"]
 N3["Bounded agent option"]
 N4["Compare success and operating cost"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Composable agent patterns](https://www.anthropic.com/research/building-effective-agents)
- [ReAct research](https://arxiv.org/abs/2210.03629)
