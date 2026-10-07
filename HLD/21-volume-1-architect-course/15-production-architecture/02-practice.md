# Production practice: service objectives, security, and safe evolution — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Review one actual service

Choose a work service you may inspect or the learning app. Trace one write/read/background path from actual code/config. Record facts, inferences, and proposed changes separately. Define one user SLI/SLO, dominant cost/bottleneck hypothesis, two failure scenarios, authorization boundary, and one improvement with rollout/rollback. Do not invent production usage.

## P2 — Online schema migration

A shortener needs mutable destinations and a new version field while old instances keep serving. Design expand/backfill/cutover/rollback. New writes may occur during backfill. Explain verification and how the old code behaves after rollback.

## P3 — Repair an incident plan

“Provider timeout is 30 seconds, so retry every second forever. If the queue grows, double every worker fleet. Backups exist, so recovery is guaranteed. Ship all new readers and delete the old schema tonight.” Replace this with a bounded incident/evolution plan.

## Delayed gate

Explain RPO/RTO with an actual restore scenario. Write an expand/migrate/contract plan and identify when rollback ceases to be safe.
