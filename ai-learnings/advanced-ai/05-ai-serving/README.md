# 5. Managed APIs, self-hosting, quantization, and serving budgets

**Advanced · about 2.5 hours including practice**

Explain deployment tradeoffs and the memory/latency costs application developers need to understand.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Deployment constraints"]
 N1["Weights and runtime memory"]
 N2["Prefill decode and concurrency"]
 N3["Task-level load and quality test"]
 N4["Operated service and fallback"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [PagedAttention / vLLM research](https://arxiv.org/abs/2309.06180)
- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
