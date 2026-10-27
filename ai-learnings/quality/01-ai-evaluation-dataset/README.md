# Build an evaluation dataset before a success story

Define task outcomes, labelled cases, holdouts, and hard failure gates.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
flowchart TD
 T[Task and acceptance criteria] --> D[Labelled synthetic cases]
 D --> S[Split development from held-out evaluation]
 S --> R[Run versioned prompt, model and retrieval]
 R --> C[Deterministic contract and access checks]
 R --> H[Human-reviewed task quality]
 C --> G[Slice metrics and inspect failures]
 H --> G
 G --> P{Meets release gate?}
 P -->|No| F[Repair one failure category]
 F --> R
 P -->|Yes| L[Limited release with monitoring and rollback]
```

Remember: **Define success before looking at the answer.**
