# 8. From local Rails lab to a production boundary

**Intermediate · about 2.5 hours including practice**

Plan deployment, runtime compatibility, credentials, egress, and feature rollout without copying a demo into production.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Current actor and minimized facts"]
 N1["Supported runtime or gateway"]
 N2["Approved provider and budgets"]
 N3["Durable runs and observability"]
 N4["Gated rollout and rollback"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Amazon Bedrock tool use](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html)
- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
