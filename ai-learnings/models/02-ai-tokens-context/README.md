# Tokens, context, and the request budget

Explain tokens and build an input budget that leaves room for the answer.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
flowchart LR
 I[Instructions] --> B[Finite context budget]
 T[Tool definitions] --> B
 H[Selected conversation history] --> B
 E[Retrieved evidence] --> B
 Q[Current question] --> B
 B --> R[Reserve space for output and provider needs]
 R --> F{Fits?}
 F -->|No| S[Select or shorten evidence and history]
 S --> B
 F -->|Yes| M[Model request]
```

Remember: **Count the whole suitcase, not just the question.**
