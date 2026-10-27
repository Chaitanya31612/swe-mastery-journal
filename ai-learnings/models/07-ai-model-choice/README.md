# 7. Choose a model for a task, not a leaderboard

**Intermediate · about 2 hours including practice**

Choose capabilities, latency, cost, and deployment constraints from a measured task.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Task and constraints"]
 N1["Capability shortlist"]
 N2["Representative evaluation"]
 N3["Whole-run cost and latency"]
 N4["Versioned selection and fallback"]
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
