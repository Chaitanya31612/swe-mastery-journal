# 4. RAG, fine-tuning, LoRA, and distillation

**Advanced · about 2.5 hours including practice**

Choose an adaptation method from the failure type without turning the course into model training.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Observed failure category"]
 N1["Prompt data and retrieval baseline"]
 N2["Permitted adaptation data"]
 N3["Held-out quality and boundary checks"]
 N4["Versioned deployment choice"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [LoRA research](https://arxiv.org/abs/2106.09685)
- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
