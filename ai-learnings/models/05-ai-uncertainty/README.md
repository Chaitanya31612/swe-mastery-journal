# 5. Fluency, hallucination, and honest uncertainty

**Beginner · about 1.5 hours including practice**

Design answers that distinguish supplied facts, interpretation, and missing information.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Claim"]
 N1["Available evidence"]
 N2["Exact checks"]
 N3["Interpretation or uncertainty"]
 N4["Clear answer or clarification"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Calibration of modern neural networks](https://arxiv.org/abs/1706.04599)
