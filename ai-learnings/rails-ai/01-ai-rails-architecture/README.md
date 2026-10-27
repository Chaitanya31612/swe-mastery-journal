# Dispatch Desk: the whole Rails architecture

Map a useful AI feature onto ordinary Rails boundaries and separate its four user tasks.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
flowchart TD
 U[Operator] --> C[Training assistant controller]
 C --> A[Current actor from identity boundary]
 A --> F[Intent service validates filter proposal]
 F --> DB[(Scoped shipment relation)]
 A --> R[Rules fact builder]
 R --> DB
 R --> V[Minimal verified fact snapshot]
 V --> J[Owned explanation run and job]
 J --> P[Provider adapter]
 P --> E[Explanation result checks]
 E -->|Invalid or unavailable| G[Reviewed rule guidance]
 E -->|Accepted| D[Labelled AI draft]
 G --> UI[Presenter with source version]
 D --> UI
 UI --> U
```
Remember: **A useful AI feature still looks like a well-structured application.**