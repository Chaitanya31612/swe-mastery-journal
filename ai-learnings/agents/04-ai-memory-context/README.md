# 4. Memory is application data with a lifetime

**Intermediate · about 2 hours including practice**

Choose what to retain, revalidate, summarize, and delete between agent steps and sessions.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md.

Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Current intent"]
 N1["Permitted durable state"]
 N2["Provenance-preserving context"]
 N3["Revalidation and conflict handling"]
 N4["Explicit retention and deletion"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state)
- [OWASP prompt injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
