# 14 — File sync: versioned metadata and recoverable conflicts

Budget: **5 hours** including local feedback/retrieval. Prerequisites: modules 02/08/13. Book connection: Chapter 15; PDF pages 244–263.

Outcome: Separate blob upload from metadata commit, handle concurrent edits/deletes, and synchronize devices with replayable cursors.

## Local study order

1. Read [the lesson](01-lesson.md). Explain each decision before moving on.
2. Save an unaided attempt at [practice](02-practice.md); complete the transfer and repair exercises.
3. Answer [the checkpoint](03-checkpoint.md) with reasons, including why a tempting option fails.
4. Only after submitting your attempt, open [solutions](answers/01-solutions.md). Compare consequences, not diagram appearance.
5. Schedule delayed recall: Trace concurrent binary edits and a delete/offline-edit conflict. Locate byte completion versus metadata visibility.

Use [the rubric](../assessment-rubric.md) and [the learning protocol](../learning-protocol.md). A focused local exercise may leave rubric dimensions unassessed; use full designs to establish overall independence. Sources are optional verification in [the source map](../sources.md). The lesson includes the mechanisms needed for these exercises.
