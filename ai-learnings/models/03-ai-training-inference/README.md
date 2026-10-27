# Training, inference, and where knowledge lives

Distinguish learned weights, request context, retrieved knowledge, and application memory.

Start with idea.md, then example.md, trace.md and failure.md. Try practice before answers.

```mermaid
flowchart TD
 D[Training examples] --> T[Training computes weight updates]
 T --> W[Saved model weights]
 W --> I[Inference uses these weights]
 P[Prompt and selected context] --> I
 I --> O[Generated output]
 N[New company fact] --> C[Database or retrieved context]
 C --> P
 O -. Not normally a weight update .-> W
```

Remember: **Weights learn patterns. Context carries this task. Your system owns current facts.**
