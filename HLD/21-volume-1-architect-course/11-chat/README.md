# 11 — Chat: durable acceptance, live delivery, and reconnects

Budget: **5 hours** including local feedback/retrieval. Prerequisites: modules 04/08; 07 useful. Book connection: Chapter 12; PDF pages 178–199.

Outcome: Separate transport from durability, implement retry-safe messages and catch-up cursors, and state presence/order limits.

## Local study order

1. Read [the lesson](01-lesson.md). Explain each decision before moving on.
2. Save an unaided attempt at [practice](02-practice.md); complete the transfer and repair exercises.
3. Answer [the checkpoint](03-checkpoint.md) with reasons, including why a tempting option fails.
4. Only after submitting your attempt, open [solutions](answers/01-solutions.md). Compare consequences, not diagram appearance.
5. Schedule delayed recall: Explain accepted versus delivered versus read. Trace a retry after commit and a reconnect after a missed live message.

Use [the rubric](../assessment-rubric.md) and [the learning protocol](../learning-protocol.md). A focused local exercise may leave rubric dimensions unassessed; use full designs to establish overall independence. Sources are optional verification in [the source map](../sources.md). The lesson includes the mechanisms needed for these exercises.
