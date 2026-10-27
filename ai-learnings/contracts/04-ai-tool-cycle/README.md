# Tool calling is a proposal–execution loop

Follow tool arguments, host execution, call IDs, and results without giving the model unrestricted access.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
sequenceDiagram
 participant H as Application host
 participant M as Model
 participant P as Policy and validator
 participant T as Domain tool
 H->>M: Task plus allowed tool schemas
 M-->>H: Proposed tool name and arguments
 H->>P: Validate arguments and current actor
 alt Denied or invalid
 P-->>H: Safe error without hidden data
 else Permitted
 H->>T: Execute bounded operation
 T-->>H: Typed result with source version
 end
 H->>M: Tool result correlated to call ID
 M-->>H: Draft or next proposed call
 H->>H: Enforce total steps, time and spend
```
Remember: **The model asks. The host validates and runs.**