# Video delivery: control plane, data plane, and processing — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Capacity and publication

Sources grow about 2 TB/day decimal, or 60 TB over 30 days; if renditions have the same retention, their threefold bytes add 180 TB, for 240 TB total before copies/metadata/temporary files. If rendition retention differs, recompute it explicitly. Playback is about 150 Gb/s raw before protocol overhead.

Use authenticated tenant upload sessions, constrained multipart/direct object transfer where appropriate, verification, and durable processing intent. Workers generate immutable versioned outputs; readiness publishes a verified manifest/metadata transition. Playback authorizes tenant/video access and uses private-serving/CDN policies consistent with revocation/deletion. A long-lived signed URL or public cache can conflict with prompt removal; define the actual bound. Measure processing age and user playback indicators. Queue retries reuse job/output identity; garbage collection respects active jobs/references.

## P2 — New workload

Live capture/transcode/packaging runs continuously, with much smaller latency budgets, shorter segments/buffering, and a delivery topology/protocol suited to the target. Source replay/history and viewer synchronization differ. Two-second end-to-end latency needs measurements across capture, encoding, network, and playback; it is not proved by an API p95 or a shorter cron interval. Treat this as expanded scope and compare trade-offs in stability, quality, latency, and egress.

## P3 — Repair

One API byte proxy may become a bandwidth/resource choke point absent a reason for it. Premature ready exposes incomplete objects. Public private-manifest caching violates isolation/revocation. Overwriting served outputs makes retries observable and can corrupt versions. Use controlled transfer, verified readiness, isolated access-aware caches, immutable outputs, and atomic manifest publication. A proxy remains a valid alternative when required, provided capacity/security costs are acknowledged.

## Checkpoint explanations

1. **C.** C measures delivered bits. A/B are not load; D affects processing/storage but does not alone specify playback traffic.

2. **D.** D preserves ready semantics. A/B/C can expose incomplete output.

3. **A.** Possession conveys the authorized operation under policy. B/C overstate ownership/lifetime; D is a different boundary.

4. **B.** B separates construction from visible publication. A/C/D are not guaranteed.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
