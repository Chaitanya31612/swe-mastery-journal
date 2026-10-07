# Framework answers — open after attempting

## P1 — One defensible notes design

Assume authenticated owners can share by an unguessable token; notes are editable; deleted notes must stop resolving within five seconds. Creating/updating requires owner authorization. Reads may briefly lag; storing an update must not overwrite a newer version silently. One region is sufficient for the initial contract.

100,000 creates/day ≈ 1.16/s; two million reads/day ≈ 23.1/s. At 5× peaks, approximately 6 writes/s and 116 reads/s. Raw note bodies grow 200 MB/day before metadata/index/replication. A simple application and relational store with suitable keys/indexes is a reasonable start; numbers do not justify compulsory sharding.

Define `POST /notes`, `GET /shared/{token}`, and owner-only versioned updates/deletes. Store note ID, owner, version, text, share token, and deletion state. Write flow authenticates and conditionally changes the expected version; read flow checks sharing and deletion. A cache is optional at this scale. Under viral traffic, a bounded cache/CDN policy can help, but revocation freshness must survive it. Protect service capacity when a cache is cold. A durable store, backups, and useful note-read/update metrics are more valuable initially than an unmotivated event network.

A different sharing model or eventual deletion contract can justify a different design. What fails is assuming public sharing and immediate deletion while placing bodies in indefinitely cached public URLs.

## P2 — Export service

The average arrival rate is about 0.116/s, implying about 2.32 concurrent jobs at 20 seconds/job in steady state, assuming the stated mean service time. A sustained 30/s spike needs about 600 concurrent workers merely to keep up; a five-minute delay allowance can buffer a short burst but does not eliminate the deficit.

Accept by recording a job/request identity durably. Use a durable outbox/dispatcher or job table to avoid losing work between recording and queueing. A worker claims a job with a lease, writes output under a deterministic job/version identity, records completion, and exposes status plus an authorized download. Retries return the same job for the same scoped request identity. A crash after output creation but before completion can be reconciled safely with the job record. Set concurrency limits for CPU/memory/external dependencies and admission control when the completion-time promise cannot be met.

Main metrics are oldest queued-job age, completion latency, failure rate, and worker resource saturation. The exact worker count needs measured job durations/distribution and burst duration, not only averages.

## P3 — Proposal critique

The proposal has no feature contract, invariant, traffic evidence, source of truth, request flow, failure recovery, cost model, or migration plan. Sharding does not guarantee availability; a queue does not automatically solve retries; two regions introduce conflict/routing/operational choices. Start with the notes contract and a durable application/store. Add a cache for measured read load, background processing for a concrete async task, and replicas/regions only when latency/availability requirements justify their consequences.

## Checkpoint answers

1. **B.** Scope and conflict semantics determine what to design. A selects technology before needs; C computes irrelevant detail prematurely; D duplicates a product without its contract.
2. **C.** Traced state transitions establish the mechanism. A and D are authority/recognition cues, and B incorrectly converts buffering into universal reliability.
3. **A.** Delivered bytes often dominate capacity/cost. B and C are not serving-load drivers; D is a minor data detail unless a stated constraint makes it relevant.
4. **D.** Architecture is constrained choice. A adds complexity automatically; B confuses a reference with correctness; C substitutes familiarity for an access-pattern/guarantee analysis.
