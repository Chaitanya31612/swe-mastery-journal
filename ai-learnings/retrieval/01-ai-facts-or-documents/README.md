# Choose SQL facts, search, or RAG

Choose the right source before choosing a vector database.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
flowchart TD
 Q[User question] --> D{What truth does it require?}
 D -->|Current count or state| S[Scoped SQL and reviewed rules]
 D -->|Policy explanation| R[Permitted versioned document evidence]
 D -->|Both| B[Join facts and evidence with provenance]
 S --> C[Typed current facts]
 R --> E[Retrieved source excerpts]
 C --> G[Optional generated explanation]
 E --> G
 B --> G
 G --> V[Check supported claims or abstain]
```
Remember: **Find the authority first. Retrieve second. Generate only if useful.**