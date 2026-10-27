# AI is a component, not the whole application

Separate interpretation and generation from exact rules, permissions, and actions.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
flowchart TD
 U[Operator asks: show held parcels] --> I[Model proposes status: held]
 I --> V{Allowed fields and values?}
 V -->|No| F[Keep manual filters available]
 V -->|Yes| S[Actor-scoped Rails query]
 S --> C[Database computes count]
 C --> P[Show facts and labelled interpretation]
 I -. No direct SQL or writes .-> X[Application owns authority]
```

Remember: **Model proposes. Code checks. The application decides.**
