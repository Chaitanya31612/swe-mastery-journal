# Inside the black box: attention, prefill, and decode

Follow a text request through tokenization, contextual representations, and generated output.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
flowchart TD
 T[Input text] --> K[Token IDs]
 K --> E[Numeric token and position representations]
 E --> A[Repeated attention and feed-forward layers]
 A --> L[Scores for possible next tokens]
 L --> S[Decode one token]
 S --> U[Append token to context]
 U --> A
 S --> X{Stop condition?}
 X -->|Yes| R[Return output]
 X -->|No| U
```
Remember: **It continues a context. It does not inspect your world by itself.**