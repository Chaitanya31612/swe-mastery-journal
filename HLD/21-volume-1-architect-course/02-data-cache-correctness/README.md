# 02 — Data access, caches, and atomic boundaries

Budget: **4 hours** including local feedback/retrieval. Prerequisites: modules 01. Book connection: Chapter 1 data/cache foundations; supplemented by database semantics.

Outcome: Choose keys/indexes from access patterns, preserve a concurrent invariant, and specify cache freshness/failure behavior.

## Local study order

1. Read [the lesson](01-lesson.md). Explain each decision before moving on.
2. Save an unaided attempt at [practice](02-practice.md); complete the transfer and repair exercises.
3. Answer [the checkpoint](03-checkpoint.md) with reasons, including why a tempting option fails.
4. Only after submitting your attempt, open [solutions](answers/01-solutions.md). Compare consequences, not diagram appearance.
5. Schedule delayed recall: Trace a stale-cache repopulation after invalidation; then explain the single-unit claim boundary and why an external timeout differs.

Use [the rubric](../assessment-rubric.md) and [the learning protocol](../learning-protocol.md). A focused local exercise may leave rubric dimensions unassessed; use full designs to establish overall independence. Sources are optional verification in [the source map](../sources.md). The lesson includes the mechanisms needed for these exercises.
