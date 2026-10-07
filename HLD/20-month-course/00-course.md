# HLD: one-month course with an assessed finish

Prepared on 1 October 2026. Study window: **2–29 October 2026**. Completion deadline: **1 November 2026**, India time. Budget: **7 hours/week × 4 weeks = 28 hours**. 30 October–1 November is calendar buffer for moving missed sessions, not additional required study time.

## What completing this course means

You can take a bounded backend problem, clarify its requirements, propose a workable design, explain its data flows, defend important choices, and respond to a changed requirement in 45 minutes. You have four practiced designs, three unfamiliar timed attempts, three practical exercises (one may be a labeled paper simulation), and one architecture review of a real codebase.

This is an **assessed foundation in practical HLD**. It is not mastery of both books, a guarantee of interview success, or evidence of senior/staff readiness. Your target role was not specified; this course uses a general backend interview scope. Senior preparation would require more depth in migrations, operations, cross-team constraints, and designs you have owned.

Confidence here means: “I can start, make progress, explain my assumptions, and identify what I need to verify.” It does not require knowing every system or recalling every detail.

## What your existing work contributes

- Your HLD folder already contains 19 modules, exercises, solutions, practical designs, revision material, and an assessment. Use it as the reference library. The README’s original “Complete” statuses describe authored material, not demonstrated personal proficiency.
- Your estimation notes contain examples and screenshots. Convert selected examples into fresh calculations and decisions; collecting more screenshots is not the required output.
- Your LLD folder contains personal designs, code, a second Splitwise attempt, and reviews such as the LRU cache review. Reuse that attempt → feedback → repair → later attempt habit.
- Your app has an LLD catalog, timed phases, notes, and reports. Its HLD view is currently a placeholder. Its LLD score uses note length, keyword matches, code-line counts, and checkpoints; use it as practice scaffolding, not independent proof of competence. The DSA review logic uses confidence-based 1/3/7-day intervals, not a full HLD mastery tracker.
- The two attached images provide the books’ chapter lists. This plan maps those chapters; it does not claim to have audited the books’ full solutions.

You do not need a new resource collection or an HLD app implementation to begin. The journal is the course record; the books provide worked examples; the app supports existing DSA/LLD practice.

## The learning loop

For each design, save your unaided attempt before opening a solution. Then read to answer specific gaps, compare reasoning, repair the design, and retrieve it later under a different constraint.

1. **Attempt:** Use the statement and your own assumptions. Draw the design and trace a request. Put a question mark where you are uncertain.
2. **Study:** Open only the relevant journal sections and chapter. Ask: what constraint led to this component? Which alternative did the author reject? What fails?
3. **Compare:** Write three consequential differences. A different database or diagram is not automatically wrong; a missing invariant or unsupported guarantee is consequential.
4. **Repair:** Update the weakest flow. Preserve the original attempt so progress remains visible.
5. **Retrieve:** Close everything. Explain the flow aloud, then change a requirement and revise the design.

Practice testing and distributing study over time have stronger evidence than relying on repeated rereading. This course applies those principles to design practice; it is not a research-validated HLD curriculum. See [Dunlosky et al., learning-techniques review](https://www.psychologicalscience.org/publications/journals/pspi/learning-techniques.html).

### How to read a chapter alongside practice

- For Volume 1 chapters 1–3, read selectively during foundation sessions, then answer a question without looking.
- For case studies, read **after** your attempt. Start with requirements and the main flow, then inspect the deep dive that addresses your biggest gap.
- The reading budget is deliberately limited. A long chapter may need a later pass; mark sections “not yet studied” instead of pretending the whole chapter is completed.
- After closing the chapter, write one decision card: **constraint → choice → alternative → downside → failure response → condition that would change my choice**.
- Use a video only for a precise unresolved question, within the allocated study time. Finish it by answering that question from memory. Do not add a parallel video syllabus this month.
- Separate “I recognize this solution” from “I can derive and adapt a solution.” Only the latter counts at a gate.

## Weekly rhythm

Use Friday 60 minutes, Saturday 120 minutes, Sunday 60 minutes, Tuesday 60 minutes, Wednesday 60 minutes, and Thursday 60 minutes. Monday is free. Shift the days if needed while preserving **420 minutes per week** and spacing later reviews away from the initial attempt.

The dated sessions below include reading, review, and assessment. They are not extra homework on top of seven hours. DSA and LLD maintenance are outside this HLD budget; if your seven hours is the total budget for all preparation, replace one HLD hour explicitly and reduce scope.

## Week 1 · 2–8 October · build a coherent first design

**Anchor:** URL shortener. **Outcome:** explain a read-heavy service from API to storage, with estimates that influence choices.

Journal: [baseline](../01-baseline/01-diagnostic-assessment.md), [mental model](../02-system-design-thinking/01-system-design-mental-model.md), [estimation](../03-estimation/01-back-of-the-envelope-estimation.md), [networking](../04-networking/01-request-lifecycle-and-networking.md), [compute](../05-compute-and-scaling/01-compute-statelessness-and-scaling.md), and the data-modeling sections of [databases](../06-databases/01-data-modeling-relational-and-nosql.md). Skim what you can already explain; do not read every file end to end.

Book: Volume 1 chapters 1–3 selectively; chapter 8 after the attempt; the ID-generation section of chapter 7 when comparing approaches.

- **2 Oct · 60 min:** Answer the existing 22-question baseline closed-book for 40 minutes. Spend 20 minutes identifying your three weakest areas. Save your answers; no current level is assumed in this plan.
- **3 Oct · 120 min:** Spend 60 minutes repairing the most relevant foundations. Attempt URL shortener for 45 minutes; spend 15 minutes recording gaps before reading a solution.
- **4 Oct · 60 min:** Read relevant chapter 8 sections for 30 minutes. Compare for 20 minutes; write one decision card for 10 minutes.
- **6 Oct · 60 min:** Study request flow/data modeling for 30 minutes. Start the estimation experiment for 30 minutes.
- **7 Oct · 60 min:** Finish the estimation experiment for 30 minutes. Spend 30 minutes retrieving baseline concepts and the shortener without notes.
- **8 Oct · 60 min:** Gate for 45 minutes; schedule later recall and record feedback for 15 minutes.

**Practice statement:** Assume 10 million active users/day, 0.1 new links/user/day, 20 redirects/user/day, a peak factor of 5, and five-year retention. Support creation and redirects; decide whether links can expire or change. Choose a latency target and specify where it is measured. Explain ID collisions, ownership, hot links, and cache failure.

**Estimation experiment:** Compute create/redirect QPS and raw mapping storage using an assumed 500 bytes/mapping. State decimal/binary units and what indexes/replication add. Then recompute database reads at 0%, 80%, and 95% cache hit rates. Change the traffic mix: what architectural decision changes? QPS is used for both request and query rates in practice; label the operation and layer instead of depending on the acronym.

**Gate 1:** In 20 minutes redraw the shortener and narrate create/redirect paths without notes. In 10 minutes explain the estimates and the assumption most likely to be wrong. In 10 minutes handle “links are editable” or “one link receives half the traffic.” In 5 minutes record the rubric. Target at least 14/24 with no zero in requirements, flows, or correctness. This is a progress gate, not interview certification.

## Week 2 · 9–15 October · control load and make background work reliable

**Anchors:** rate limiter and notification system. **Outcome:** connect your LLD logic to multi-instance behavior, retries, and operational limits.

Journal: [caching](../07-caching/01-caching-strategies-and-invalidation.md), [async systems](../08-async-systems/01-queues-pubsub-and-event-driven.md), relevant consistency/partition sections of [distributed fundamentals](../09-distributed-systems/01-distributed-fundamentals-and-consensus.md), and [reliability](../12-reliability/01-reliability-fault-tolerance-and-slas.md).

Book: Volume 1 chapter 4 and selected chapter 10 sections after attempts. Do not add the entire key-value-store chapter this week.

- **9 Oct · 60 min:** Study caching, queue delivery, retries, and idempotency through concrete flows. Start with a five-minute closed-book shortener explanation inside this block.
- **10 Oct · 120 min:** Rate-limiter cycle: 35-minute attempt, 25-minute targeted read, 20-minute comparison, 10-minute decision card. Use the remaining 30 minutes on atomicity/partial failure.
- **11 Oct · 60 min:** Notification attempt for 45 minutes; record gaps for 15 minutes.
- **13 Oct · 60 min:** Notification reading for 30 minutes, comparison for 20, decision card for 10.
- **14 Oct · 60 min:** Run the retry/idempotency experiment below.
- **15 Oct · 60 min:** Closed-book review for 30 minutes; Gate 2 for 30 minutes.

**Rate-limiter statement:** Limit each account to 100 requests/minute, allow a defined burst, and enforce limits across four API instances. Explain the identity key, algorithm, atomic state update, time source assumptions, and response when the shared store is unavailable. Compare global precision with availability and latency. Connect this to your LLD rate-limiter attempt: thread safety inside one process does not enforce a global limit.

**Notification statement:** Send email/push for order events. Assume one million events/day, bursts 10× the average, and a provider quota of 200 sends/second. Define what “accepted” and “sent” mean; handle duplicates, provider timeout, retries, quotas, preferences, and dead-letter handling. Estimate backlog drain time and say which metric will expose delay.

**Retry experiment:** In a small local program in a language you already know, process the same event twice. First observe duplicate local effects, then use a durable unique event ID/transaction to produce one local effect. Simulate a crash after the effect but before acknowledgment and replay. Explain why this local deduplication does not itself guarantee a single external email when a provider response is lost. A file-backed SQLite experiment is enough; no Kafka cluster or cloud setup is required.

**Gate 2:** Spend 10 minutes explaining a distributed limiter under store failure, 15 minutes tracing duplicate notifications and a provider timeout, and 5 minutes scoring. Target at least 16/24, with correctness and failure handling at least 2/3. You must identify the external-side-effect guarantee boundary. Kafka’s transactional/exactly-once guarantees have specific scope; external destinations require additional cooperation. See [Apache Kafka design](https://kafka.apache.org/41/design/design/).

## Week 3 · 16–22 October · preserve correctness and operate the design

**Anchor:** hotel reservation system. **Outcome:** explain concurrent claims on finite inventory, then connect architecture to measurements and recovery.

Journal: transaction/isolation sections of [databases](../06-databases/01-data-modeling-relational-and-nosql.md), [reliability](../12-reliability/01-reliability-fault-tolerance-and-slas.md), [observability](../13-observability/01-observability-telemetry-and-debugging.md), [security](../14-security/01-practical-architectural-security.md), and targeted [architecture patterns](../15-architecture-patterns/01-core-architectural-patterns.md).

Book: Volume 2 chapter 7 after the attempt. Use it to compare inventory models and concurrent booking, not to memorize every component.

- **16 Oct · 60 min:** Study transactions, isolation, locking/conditional updates, and idempotency. Retrieve one Week 2 decision before opening notes.
- **17 Oct · 120 min:** Reservation attempt for 45 minutes, targeted reading for 45, comparison/repair for 30.
- **18 Oct · 60 min:** Finish the reservation decision card for 15 minutes. Study reliability/security for 30; retrieve an earlier design for 15.
- **20 Oct · 60 min:** Transfer exercise and concurrent-inventory experiment below.
- **21 Oct · 60 min:** Give the reservation design an operations plan: user-facing SLI/SLO, latency percentiles, availability, structured logs, alert, backup/restore assumptions, RPO/RTO, authorization, and one main cost driver.
- **22 Oct · 60 min:** Mixed review for 30 minutes; Gate 3 for 30 minutes.

**Reservation statement:** Search hotels by city/date and reserve one of a finite number of rooms for a date range. Assume 100,000 properties, one million searches/day, and 50,000 bookings/day. Explicitly choose room-type inventory or individually identified rooms. Prevent overselling across concurrent clients. Add a five-minute hold, expiration, retries, and uncertain payment outcome. An external payment provider is assumed; designing a complete payment network is out of scope.

**Transfer exercise:** Use your LLD booking-system or Splitwise work. Ask what changes when two service instances process the same request and state moves into a database. Keep class design separate from deployment, ownership, transaction boundaries, and asynchronous work.

**Concurrent-inventory experiment:** Spend 30 minutes demonstrating two clients competing for one unit, using a database you already have. Compare unsafe read-then-write with a conditional update such as `UPDATE inventory SET available = available - 1 WHERE id = ? AND available > 0`, checking affected rows. This demonstrates one-unit allocation only; multi-night hotel inventory requires an appropriate transaction across affected dates and contention/deadlock handling. If no database is available, trace the two interleavings on paper within the same budget; mark it “reasoned, not executed.” Use the other 30 minutes for the transfer exercise.

**Gate 3:** Spend 15 minutes walking two concurrent reservations, 10 minutes handling hold expiration during uncertain payment, and 5 minutes scoring. Target at least 18/24 with correctness at least 2/3. Explicitly name the invariant, atomic boundary, and recovery path. Transactions need the right isolation/locking and retry strategy; transaction syntax alone is not enough. See [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html).

## Week 4 · 23–29 October · demonstrate transfer and finish

**Outcome:** attempt unfamiliar prompts under time pressure and use the same reasoning on a real system. Do not start a new book chapter this week.

Use [coach prompts](03-coach-prompts.md) to obtain three previously unpracticed problems. Ask for one read-heavy, one asynchronous, and one correctness-sensitive system. The coach should generate the statement and reveal it only at the beginning of each round. Your earlier reading means some standard prompts may feel familiar; disclose that and request a different one. The purpose is transfer, not secrecy for its own sake.

- **23 Oct · 60 min:** Mock 1: 45-minute unaided design + 15-minute rubric feedback.
- **24 Oct · 120 min:** Mock 2: 45-minute design + 15-minute feedback. Start a real-codebase architecture review for 60 minutes.
- **25 Oct · 60 min:** Closed-book mixed retrieval and changed-constraint drills across the four anchors. Include early decision cards reaching their later recall date.
- **27 Oct · 60 min:** Mock 3: 45-minute design + 15-minute feedback.
- **28 Oct · 60 min:** Finish the real-codebase review for 30 minutes. Repair the most repeated mock weakness for 30 minutes.
- **29 Oct · 60 min:** Spend 30 minutes reattempting that weakness without help. Spend 30 minutes assembling the evidence and assigning an honest completion level.

**Real-codebase review:** Prefer one service you actually work on if you can inspect it appropriately. Otherwise use `DSAPatternLearnApp`: trace frontend data loading, local progress persistence, and optional backend AI/mock endpoints. Distinguish what the code demonstrates from hypothetical production requirements. Draw the actual architecture; identify the source of truth, one failure mode, a measurement, and one justified improvement. Then propose a separate design for a clearly stated scenario such as 10,000 users needing cross-device progress. That is an architecture exercise, not a requirement to modify the app.

**Submission bundle:** baseline answers; four first attempts and repairs; four decision cards; estimation experiment; retry experiment; concurrent-inventory result or paper trace; three mock scores with evidence; one real-system review; and a list of unresolved gaps. Later recall records live in the tracker. Save lab outputs with attempts; code size is not a completion metric.

## The 45-minute design structure

Use this until it becomes familiar, then adapt it to the interviewer and problem:

1. **0–5 min:** clarify the user, two or three core features, scope, and the most important NFR/invariant.
2. **5–9 min:** estimate only quantities that affect decisions. State assumptions and peak load.
3. **9–15 min:** outline API contracts, important entities, access patterns, and source of truth.
4. **15–25 min:** draw a simple end-to-end architecture; trace one write and one read/background flow.
5. **25–37 min:** deep-dive the main risk: contention, hot keys, delivery, fan-out, storage, or another problem-specific constraint.
6. **37–42 min:** failures, recovery, security, monitoring, and likely scale/cost limit.
7. **42–45 min:** summarize choices, accepted downsides, and what must be verified next.

Do not mechanically spend ten minutes calculating every capacity number. In a booking problem, the inventory invariant deserves more time than bandwidth arithmetic. Use the existing 13-step recipe as a coverage checklist after practice, not a script that prevents discussion.

## Assessment rubric and completion levels

Score eight dimensions **0–3 each, total 24**:

- **Requirements:** bounded functionality, justified NFRs, explicit assumptions.
- **Scale:** correct units/order of magnitude; estimates change a decision.
- **Data and interfaces:** access patterns, ownership/source of truth, plausible API/schema.
- **Flows:** coherent end-to-end read/write/background paths.
- **Correctness:** domain invariant, races, consistency, duplicate/uncertain outcomes where relevant.
- **Failure and operations:** partial failure, recovery, useful metrics, and relevant security/cost.
- **Trade-offs:** credible alternative and downside; complexity justified by a constraint.
- **Communication and adaptation:** understandable narrative, time control, and response to one changed requirement.

For each dimension: **0** = missing or fundamentally wrong; **1** = recognizable terms but needs substantial prompting; **2** = workable and justified without help; **3** = also handles a changed constraint or counterexample. Attach a sentence from the attempt as evidence. A score without evidence is provisional.

These thresholds are course criteria, not a standardized industry hiring score. Have a peer/experienced engineer review at least one final round if available. An AI review is useful feedback but can miss errors; ask it for concrete counterexamples and verify disputed technical claims.

By 1 November, assign one level:

- **Course work completed:** the submission bundle exists. This says you practiced seriously; it does not by itself prove independent skill.
- **Foundation demonstrated:** an unaided anchor redesign passes 18/24, correctness and flows are at least 2/3, and you can explain major decisions after a delay.
- **Independent problem solving demonstrated:** at least two of the three unfamiliar 45-minute rounds score 18/24 or higher; every dimension is at least 2/3 in those rounds; you handle the changed requirement; and the real-system review distinguishes observed behavior from proposals.

If prompts/hints were used, mark the attempt **assisted**; it cannot establish independence. If a round leaves the core invariant broken, it does not pass regardless of the total. For an asynchronous problem, identify whether a guarantee applies to broker delivery, local database effects, or external provider effects.

The honest final statement is: “I completed 28 hours of structured HLD practice and demonstrated [level] on [evidence]. My remaining gaps are [specific gaps].” You no longer need the broad claim “I have never studied HLD seriously.”

If a gate fails, replace the next study block with a focused repair and later unaided reattempt. Keep the calendar deadline; reduce reading breadth first. Preserve a final unfamiliar round and record incomplete deliverables. Missed work moves into the buffer only if you have the time. If the final standard is unmet, label the result accurately and prescribe the next two practice sessions; do not restart the whole book.

## Retention after the initial attempt

Use approximately **+1, +3, +7, +14, +30, and +60 days**, adjusted to your sessions. These are practical defaults, not uniquely optimal scientific intervals. Within the month, review comes from the explicit review blocks and short retrieval starts. Later reviews are part of maintenance.

- **+1:** a five-minute explanation of the central choice without notes.
- **+3:** a five-minute failure or changed-constraint question.
- **+7:** a ten-minute redraw of the main flow.
- **+14:** a five-minute comparison with a different system.
- **+30:** a ten-minute transfer problem.
- **+60:** a short mixed mock or redesign under changed assumptions.

Review the most consequential weak decisions first. Keep about 20–30 decision cards, not hundreds of fact cards. A good prompt is “A provider times out after accepting a request: what can I guarantee and how do I recover?” rather than “What is a queue?”

If recall fails, attempt it first, check only the missing mechanism, and retry tomorrow. If recall is easy, lengthen the gap or change the problem. The goal is durable retrieval and reasoning, not permanent verbatim memory.

After the deadline, reserve **90 minutes/week** if you are maintaining rather than extending: 20 minutes due recall, 45 minutes a changed/unfamiliar design, 25 minutes feedback. Once a month, replace that round with a real-system review or a peer mock.

## Continue through both books after the one-month finish

The following is an optional **12-week extension**, not work required before 1 November. Continue at seven hours/week. For most weeks: two 90-minute attempt/read/compare cycles, 60 minutes targeted foundations, 60 minutes due review, a 60-minute mock/feedback block, and 60 minutes practical application. For a difficult chapter, use both cycles on the same design. Completion still depends on delayed recall and unfamiliar transfer.

- **Week 5:** Volume 1 chapters 5–6, consistent hashing and key-value store. Focus on partitioning, replicas, consistency assumptions, and hot keys. Deepen journal module 09.
- **Week 6:** Volume 1 chapters 11–12, news feed and chat. Focus on fan-out, ordering, presence, pagination, and reconnects.
- **Week 7:** Volume 1 chapters 9 and 13, crawler and autocomplete. Focus on scheduling, deduplication, indexing pipelines, and fresh versus precomputed results. Deepen modules 08 and 11.
- **Week 8:** Volume 1 chapters 14–15, video delivery and file synchronization. Focus on object storage, CDN, upload workflows, metadata, sync conflicts. Deepen module 10. Use chapter 16 for follow-up reading only when it answers a gap.
- **Week 9:** Volume 2 chapters 1–2, proximity and nearby friends. Focus on geographic indexes, freshness, location privacy, and connection load.
- **Week 10:** Volume 2 chapter 3, maps. Use two passes: spatial/routing data first, then live updates and serving. Keep the scope of navigation explicit.
- **Week 11:** Volume 2 chapters 4–5, distributed queue and monitoring. Focus on partition ownership, durability, acknowledgment, cardinality, retention, and operational limits.
- **Week 12:** Volume 2 chapters 6 and 10, event aggregation and leaderboard. Focus on windows, late/duplicate events, top-K/ranking, freshness, and materialized results.
- **Week 13:** Revisit Volume 2 chapter 7 at greater depth; then chapter 8, distributed email. Add multi-night contention, uncertain outcomes, mail ingest/search, and failure recovery.
- **Week 14:** Volume 2 chapter 9, object storage. Spend one cycle on metadata and another on data durability, repair, and placement.
- **Week 15:** Volume 2 chapters 11–12, payments and wallet. Focus on business invariants, idempotency, ledger effects, reconciliation, and explicit external-system assumptions. These are design exercises, not operational financial guidance.
- **Week 16:** Volume 2 chapter 13, stock exchange, with a narrow matching/ordering scope; use the second cycle for a final unfamiliar mock and accumulated-gap review.

Use the existing final assessment as an additional question bank after corrections, not as an automatic “85% means senior interview ready” certificate. Add one migration/incident/rollout exercise per extended phase if you are targeting senior roles. You can stop at the assessed month-one finish, maintain it, and resume the extension later without invalidating that finish.

## Reading notes need conditions, not automatic answers

Some existing journal summaries contain strong heuristics. Treat them as prompts to investigate. For example:

- There is no universal “5,000–10,000 writes/sec means choose NoSQL” threshold. Data model, hardware, transaction shape, indexes, latency targets, and measurements determine capacity.
- Daily query volume does not determine cache working-set RAM. Estimate distinct cached objects and sizes, reuse/locality, TTL, metadata, and a desired hit rate.
- Invalidation can be useful, but “always delete the cache key” is not a universal consistency solution; analyze concurrent readers/writers and the actual freshness contract.
- A queue buffers a temporary mismatch. A persistent input rate greater than processing capacity still creates unbounded lag until capacity, admission control, retention, or work changes.
- A fixed five-second primary-routing window does not prove read-your-writes under every replication delay. State the assumption or use a mechanism tied to observed progress.
- High recall scores and vocabulary fluency do not establish design skill. “LSM is always faster,” “SQL search is never valid,” and “p99 is always the only target” need workload and implementation conditions.

Do not rewrite the entire reference library this month. Correct claims that affect your current decision cards and cite the relevant implementation documentation.

Use only a small supplemental set when it addresses a current question: [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html), [Apache Kafka design](https://kafka.apache.org/41/design/design/), and [Google SRE service-level objectives](https://sre.google/sre-book/service-level-objectives/). SLOs should reflect the user-visible service; picking an availability number alone does not define useful service behavior.

## Start here

On 2 October, create `baseline-2026-10-02.md` beside this course, answer the existing diagnostic without looking at solutions, and record three gaps in [the tracker](02-progress-tracker.md). Your first deliverable is your own baseline, not another rewritten set of notes.
