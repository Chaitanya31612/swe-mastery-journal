# 3. Prompt injection is an application trust problem

**Intermediate · about 2 hours including practice**

Keep outside instructions from acquiring tools, data, or execution authority.

Read idea → example → trace → failure. Then attempt practice/repair.md and practice/transfer.md. Answers are separate in answers/. The app also provides prediction, quiz, recall, and optional AI review.

```mermaid
flowchart TD
 N0["Context origins"]
 N1["Minimal data and capabilities"]
 N2["Untrusted instruction attempt"]
 N3["Host/server policy gates"]
 N4["Bounded safe result or refusal"]
 N0 --> N1
 N1 --> N2
 N2 --> N3
 N3 --> N4
 N4 --> C{"Can you trust the result?"}
 C --> V["Check evidence, permissions, and the failure case"]
 V -. "repeat with a changed input" .-> N0
```

- [OWASP prompt injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [MCP security boundaries](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)
