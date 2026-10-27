# 6. Evaluate the path, not only the final sentence

**Intermediate · about 2 hours including practice**

Judge task success, tool policy, efficiency, and recovery across agent trajectories.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Task fixtures"]
 N1["Model proposals and tool traces"]
 N2["Hard policy checks"]
 N3["Supported outcome and recovery"]
 N4["Whole-run quality cost and latency"]
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
