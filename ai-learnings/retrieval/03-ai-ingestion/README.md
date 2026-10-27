# Ingestion is a versioned data pipeline

Parse documents with provenance, access metadata, and a recoverable publication step.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
flowchart TD
 S[Approved source and access policy] --> E[Extract and normalize]
 E --> C[Split with headings and source IDs]
 C --> B[Embed a complete new source version]
 B --> T[Validate count, errors and permissions]
 T --> P[Publish version atomically]
 P --> R[Retrieve active permitted chunks]
 D[Source deleted or access revoked] --> I[Invalidate chunks, vectors and cached answers]
 I --> R
 T -->|Failure| Q[Keep old valid version or mark unavailable]
```

Remember: **Bad extraction becomes bad evidence. Inspect upstream first.**
