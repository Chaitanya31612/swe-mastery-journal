# Volume 1: practical system architecture course

Start with [the design framework](00-design-framework/01-lesson.md), then [three worked teaching examples](00-design-framework/worked-examples.md). This course is written in a senior architect’s teaching style: constraints, invariants, trade-offs, failure recovery, measurements, and evolution. Completing it does not by itself confer senior architect competence.

The backbone is Alex Xu’s *System Design Interview*, second edition, Volume 1, supplied by you. The lessons and exercises are original explanations with different assumptions and transfer problems. Primary technical documentation adds important conditions to simplified interview models. Volume 2 is outside this course.

## Files and spoiler boundary

Every module has a local README, `01-lesson.md`, `02-practice.md`, `03-checkpoint.md`, and `answers/01-solutions.md`. Lessons teach mechanisms; practice and checkpoint files contain no answer keys. Open the answer folder only after saving an attempt. Worked **teaching** examples are intentionally solved and labeled separately from assessment problems. This separation is a study convention, not access control.

The module lessons contain the mechanisms required for the local exercises. External sources and old journal notes are optional checks/deeper reading, not prerequisites for understanding the lesson. Exercises may require you to choose assumptions; defensible alternatives are expected. Solutions show one defensible design, assumptions, calculations, alternatives, and failure cases rather than declaring a unique answer.

## Course order

1. [00 — Design framework](00-design-framework/README.md): narrow ambiguity and present a coherent solution. 4 hours.
2. [01 — Requests, scale, and estimation](01-request-scale-estimation/README.md): derive useful numbers and identify bottlenecks. 4 hours.
3. [02 — Data, caching, and correctness](02-data-cache-correctness/README.md): design access patterns and atomic boundaries. 4 hours.
4. [03 — URL shortener](03-url-shortener/README.md): read-heavy systems, identifiers, redirects, and invalidation. 4 hours.
5. [04 — Unique IDs](04-unique-ids/README.md): uniqueness, clocks, coordination, and ordering. 3 hours.
6. [05 — Rate limiter](05-rate-limiter/README.md): admission control, atomic decisions, and multi-instance limits. 4 hours.
7. [06 — Consistent hashing](06-consistent-hashing/README.md): placement, rebalancing, and hot keys. 3 hours.
8. [07 — Distributed key-value store](07-key-value-store/README.md): durability, replicas, consistency, and repair. 5 hours.
9. [08 — Async work and notifications](08-notifications/README.md): delivery semantics, retries, outbox, and quotas. 5 hours.
10. [09 — Crawler](09-web-crawler/README.md): scheduling, politeness, deduplication, and bounded work. 4 hours.
11. [10 — News feed](10-news-feed/README.md): materialized views, fan-out, pagination, and privacy. 4 hours.
12. [11 — Chat](11-chat/README.md): persistent connections, durable messages, cursors, and presence. 5 hours.
13. [12 — Autocomplete](12-autocomplete/README.md): indexing, top-K, snapshots, and freshness. 4 hours.
14. [13 — Video platform](13-video-platform/README.md): object storage, processing DAGs, CDN, and media delivery. 5 hours.
15. [14 — File synchronization](14-file-sync/README.md): versioning, resumable uploads, conflicts, and garbage collection. 5 hours.
16. [15 — Production architecture](15-production-architecture/README.md): SLOs, security, migrations, incidents, and cost. 5 hours.
17. [16 — Transfer and final assessment](16-final-assessment/README.md): unseen systems and evidence-based completion. 4 hours.

Total: **72 hours of planned module work**, including local feedback and retrieval. Reserve another **one hour/week for cross-module spaced review**. At your earlier seven hours/week, use six hours for module work and one for mixed review: **12 study weeks**, with a thirteenth week reserved for repair if needed. These are planning estimates, not time limits on learning.

Keep **1 November 2026** as the earlier requested foundation checkpoint, not a deadline for all Volume 1. From 6 October, target modules 00/01/02/03/05 (20 hours), about four hours of spaced review, and two hours of unfamiliar practice/feedback: approximately 26 hours. If already completed, assess and skip mastered sections rather than repeat them mechanically. Actual passing evidence determines the result; do not mark modules complete because their files exist.

## How to use a module

For a four-hour module: 45 minutes lesson/self-explanation; 45 minutes practice P1; 30 minutes solution comparison; 40 minutes P2/repair work; 20 minutes checkpoint; 30 minutes delayed redraw or transfer; 30 minutes repair and evidence. Move the delayed block to a later day. Three-hour modules narrow the practice/reading blocks; five-hour modules add a deeper failure experiment and later transfer. Do not force every chapter into one sitting.

Early in learning, study a worked example and explain why each decision exists. Next, complete a partially guided problem. Finally, attempt a transfer problem from a blank page. After you can explain a mechanism, spend less time rereading it and more time applying it. MCQs diagnose misconceptions; they cannot certify design skill. Repair exercises use code only where code reveals an architectural race or guarantee boundary; elsewhere they critique a design proposal or incident response.

Use the [attempt template](attempt-template.md), [progress tracker](progress.md), [learning protocol](learning-protocol.md), and [assessment rubric](assessment-rubric.md). Evidence should be saved in your own attempt files. Read [sources and book mapping](sources.md) when verifying a claim.

## Completion standard

Finish the practices and checkpoints, pass delayed transfer gates, and complete the three unfamiliar final designs plus one real-system review. A pass requires a coherent design, an intact central invariant, justified trade-offs, and unaided adaptation. The standard is specified in the rubric; it is a course criterion, not a hiring prediction.

No program can guarantee permanent retention. This course gives you repeated retrieval, corrective feedback, gradually reduced guidance, and transfer checks. The useful goal is that you can recover and apply the reasoning, even when you forget a product-specific detail.
