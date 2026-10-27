# 2. A bounded agent loop you can trace

**Intermediate · about 2 hours including practice**

Implement proposal, policy, execution, observation, and stopping as explicit states.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Task and run state"]
 N1["Model proposal"]
 N2["Policy and schema gate"]
 N3["Bounded tool observation"]
 N4["Final check or explicit stop"]
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
