# 6. Multimodal integration: documents, images, and audio

**Advanced · about 2.5 hours including practice**

Extend the same evidence and validation boundaries to non-text inputs.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Permitted bounded source"]
 N1["Extraction and provenance"]
 N2["Interpretation"]
 N3["Domain and access checks"]
 N4["Uncertainty or reviewed result"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [OWASP prompt injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
