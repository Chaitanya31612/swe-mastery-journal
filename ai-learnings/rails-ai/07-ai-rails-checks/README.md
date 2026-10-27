# 7. Test the Rails feature at three different layers

**Intermediate · about 2.5 hours including practice**

Separate deterministic application checks, adapter contract checks, and live model evaluations.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Deterministic service fixtures"]
 N1["Provider contract stubs"]
 N2["API and MCP smoke"]
 N3["Separate live model evaluation"]
 N4["Honest report and fallback checks"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [Rails Active Job](https://guides.rubyonrails.org/v7.2/active_job_basics.html)
