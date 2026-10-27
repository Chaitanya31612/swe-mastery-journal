# Final capstone: design, build, break, and explain

Demonstrate an AI-powered application boundary on an unfamiliar case with observable evidence.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
flowchart TD
 U[User task and success criteria] --> T[Truth owners and permitted evidence]
 T --> B[Input, output and tool contracts]
 B --> W{Simplest useful flow?}
 W --> C[Deterministic feature]
 W --> R[Retrieval plus model call]
 W --> A[Bounded agent only if justified]
 C --> V[Validation, failure path and honest UI]
 R --> V
 A --> V
 V --> E[Offline checks plus live model evaluation]
 E --> G[Cost, privacy, latency and release gates]
 G --> O[Limited rollout and rollback]
 O --> D[Delayed transfer problem in a new domain]
```
Remember: **Build one path. Break its boundaries. Explain what the evidence actually proves.**