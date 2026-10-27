# 4. Comparisons and briefings: code aligns, AI explains

**Intermediate · about 2.5 hours including practice**

Build exact comparison and grouping inputs before asking for a useful narrative.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Permitted bounded selection"]
 N1["Aligned facts or scoped aggregates"]
 N2["Explicit missing states"]
 N3["Optional narrative"]
 N4["Inspectable exact view"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
