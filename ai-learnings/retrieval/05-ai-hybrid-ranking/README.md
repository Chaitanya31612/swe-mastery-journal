# Lexical, vector, hybrid, and reranking

Choose a search pipeline and measure which stage loses the answer.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
flowchart LR
 Q[Question] --> L[Lexical candidates]
 Q --> E[Embedding candidates]
 A[Authenticated scope] --> L
 A --> E
 L --> F[Merge candidates by rank]
 E --> F
 F --> R[Optional reranker]
 R --> P[Recheck access and current source version]
 P --> B[Select diverse evidence within budget]
 B --> G[Answer or missing evidence]
```
Remember: **Find candidates. Order candidates. Pack evidence. Debug each separately.**