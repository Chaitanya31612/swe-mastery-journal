# 2. Rubrics, judges, confidence, and calibration

**Intermediate · about 2 hours including practice**

Use automated judging carefully and choose decision thresholds from observed errors.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Explicit rubric"]
 N1["Reviewed labels"]
 N2["Judge agreement and disagreement"]
 N3["Measured threshold policy"]
 N4["Holdout quality and coverage"]
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
