# Rails jobs, run state, and result ownership

Build a durable result contract and prevent cross-user or stale background answers.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
stateDiagram-v2
 [*] --> queued: persist owned run
 queued --> running: atomic claim
 running --> completed: valid draft
 running --> fallback: provider or validation failure
 running --> unavailable: access or source missing
 completed --> stale: source version changed on read
 fallback --> stale: source version changed on read
 completed --> completed: duplicate completed delivery does nothing
 note right of running
 Local lab has no crash lease recovery.
 Design it before using a durable worker.
 end note
```
Remember: **A run has an owner, a snapshot, and an honest state.**