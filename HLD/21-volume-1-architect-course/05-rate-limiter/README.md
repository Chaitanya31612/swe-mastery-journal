# 05 — Distributed rate limiting and overload control

Budget: **4 hours** including local feedback/retrieval. Prerequisites: modules 00–02; 04 useful. Book connection: Chapter 4; PDF pages 51–70.

Outcome: Choose an algorithm from the exact admission contract, enforce an atomic decision, and handle store/region failure.

## Local study order

1. Read [the lesson](01-lesson.md). Explain each decision before moving on.
2. Save an unaided attempt at [practice](02-practice.md); complete the transfer and repair exercises.
3. Answer [the checkpoint](03-checkpoint.md) with reasons, including why a tempting option fails.
4. Only after submitting your attempt, open [solutions](answers/01-solutions.md). Compare consequences, not diagram appearance.
5. Schedule delayed recall: Compare exact rolling limits with bursty token refill. Trace a last-token race and global-budget isolation.

Use [the rubric](../assessment-rubric.md) and [the learning protocol](../learning-protocol.md). A focused local exercise may leave rubric dimensions unassessed; use full designs to establish overall independence. Sources are optional verification in [the source map](../sources.md). The lesson includes the mechanisms needed for these exercises.
