# System Design / HLD Foundation Program

A rigorous, engineering-first High-Level Design (HLD) foundation curriculum designed to bridge the gap between fragmented distributed systems knowledge and intuitive architectural mastery.

> **Target Profile:** Software engineers with 3+ years of experience looking to build an unshakeable mental model of system design before diving into interview problem patterns (e.g., Alex Xu's System Design Interview volumes).

---

## 🎯 Core Philosophy

Architecture is not about memorizing diagrams or stringing together buzzwords. Architecture is the discipline of **making deliberate trade-offs under hard constraints**.

Every component in a system exists to solve a specific physical or computational constraint:
$$\text{Problem} \longrightarrow \text{Constraint} \longrightarrow \text{Architectural Decision} \longrightarrow \text{Consequence} \longrightarrow \text{Trade-off}$$

### The Universal Engineering Questions
For every concept in this curriculum, we obsessively answer:
1. **WHY** does this exist?
2. **WHAT** problem does it actually solve?
3. **WHEN** do we need it?
4. **WHEN** do we NOT need it? (Avoiding premature complexity)
5. **WHAT** are the viable alternatives?
6. **WHAT** does it cost? (Latency, operational overhead, dollars, cognitive load)
7. **WHAT** breaks first as the system scales 10x or 100x?
8. **WHAT** happens when it fails? (Blast radius and graceful degradation)
9. **HOW** do we articulate this in a high-stakes engineering or interview discussion?

---

## 🗺️ Master Curriculum Roadmap & Module Navigator

All 19 phases have been authored with rigorous engineering depth, following the 16-point standard topic blueprint:

| Phase | Directory & Primary Module | Core Focus Area | Status |
|---|---|---|---|
| **Phase 0** | [`01-baseline/01-diagnostic-assessment.md`](./01-baseline/01-diagnostic-assessment.md) | Diagnostic Baseline (23 Calibration Questions) | 🟢 Complete |
| **Phase 1** | [`02-system-design-thinking/01-system-design-mental-model.md`](./02-system-design-thinking/01-system-design-mental-model.md) | System Design Mental Model & 11 NFR Tensions | 🟢 Complete |
| **Phase 2** | [`03-estimation/01-back-of-the-envelope-estimation.md`](./03-estimation/01-back-of-the-envelope-estimation.md) | Back-of-the-Envelope Estimation Toolkit & Exercises | 🟢 Complete |
| **Phase 3** | [`04-networking/01-request-lifecycle-and-networking.md`](./04-networking/01-request-lifecycle-and-networking.md) | Request Lifecycle, Anycast, DNS, TCP/TLS & L4/L7 LBs | 🟢 Complete |
| **Phase 4** | [`05-compute-and-scaling/01-compute-statelessness-and-scaling.md`](./05-compute-and-scaling/01-compute-statelessness-and-scaling.md) | Compute, Statelessness, Scaling & 9 Bottlenecks | 🟢 Complete |
| **Phase 5** | [`06-databases/01-data-modeling-relational-and-nosql.md`](./06-databases/01-data-modeling-relational-and-nosql.md) | Relational vs NoSQL, B-Trees vs LSM-Trees, Sharding | 🟢 Complete |
| **Phase 6** | [`07-caching/01-caching-strategies-and-invalidation.md`](./07-caching/01-caching-strategies-and-invalidation.md) | Cache Patterns, Stampede/Penetration & Invalidation | 🟢 Complete |
| **Phase 7** | [`08-async-systems/01-queues-pubsub-and-event-driven.md`](./08-async-systems/01-queues-pubsub-and-event-driven.md) | Queues, Pub/Sub, Streams, Idempotency & Backpressure | 🟢 Complete |
| **Phase 8** | [`09-distributed-systems/01-distributed-fundamentals-and-consensus.md`](./09-distributed-systems/01-distributed-fundamentals-and-consensus.md) | Consensus (Raft), Quorums, CAP/PACELC & Resiliency | 🟢 Complete |
| **Phase 9** | [`10-storage/01-storage-paradigms-and-object-stores.md`](./10-storage/01-storage-paradigms-and-object-stores.md) | Block, File, Object Storage & Pre-Signed Direct Uploads | 🟢 Complete |
| **Phase 10** | [`11-search/01-search-systems-and-indexing-pipelines.md`](./11-search/01-search-systems-and-indexing-pipelines.md) | Inverted Indexes, Lexical Analysis, BM25 & CDC Sync | 🟢 Complete |
| **Phase 11** | [`12-reliability/01-reliability-fault-tolerance-and-slas.md`](./12-reliability/01-reliability-fault-tolerance-and-slas.md) | Bulkheads, Circuit Breakers, Failover & SLA/SLO/SLI | 🟢 Complete |
| **Phase 12** | [`13-observability/01-observability-telemetry-and-debugging.md`](./13-observability/01-observability-telemetry-and-debugging.md) | Metrics, Distributed Tracing (OTel), Logs & p99 Tails | 🟢 Complete |
| **Phase 13** | [`14-security/01-practical-architectural-security.md`](./14-security/01-practical-architectural-security.md) | Zero Trust, mTLS, Token Bucket Rate Limiting & BOLA | 🟢 Complete |
| **Phase 14** | [`15-architecture-patterns/01-core-architectural-patterns.md`](./15-architecture-patterns/01-core-architectural-patterns.md) | 16 Core Blueprints (CQRS, Sagas, Fan-out, Gateway) | 🟢 Complete |
| **Phase 15** | [`16-practical-designs/01-level-1-foundational-designs.md`](./16-practical-designs/01-level-1-foundational-designs.md)<br>[`16-practical-designs/02-level-2-distributed-designs.md`](./16-practical-designs/02-level-2-distributed-designs.md) | 10 Hands-on Designs with 13-Step Sequence | 🟢 Complete |
| **Phase 16** | [`17-industry-vocabulary/01-staff-engineer-dialect-guide.md`](./17-industry-vocabulary/01-staff-engineer-dialect-guide.md) | Staff Engineer Dialect (25 Essential System Terms) | 🟢 Complete |
| **Phase 17** | [`18-revision/01-spaced-repetition-and-decision-cheatsheet.md`](./18-revision/01-spaced-repetition-and-decision-cheatsheet.md) | Spaced Repetition, Anti-patterns & Decision Rules | 🟢 Complete |
| **Phase 18** | [`19-final-assessment/01-comprehensive-readiness-exam.md`](./19-final-assessment/01-comprehensive-readiness-exam.md) | Capstone Exam (Parts A–F) for Alex Xu Readiness | 🟢 Complete |

---

## 📁 Standard Topic Blueprint

Each core concept document strictly adheres to a battle-tested structure designed for deep retention and zero fluff:

1. **Mental Model** — The intuitive analogy and foundational principle
2. **Why It Exists** — The physical/architectural bottleneck that forced its invention
3. **How It Works** — Technical mechanics without unnecessary trivia
4. **When To Use It** — Clear triggers and operational thresholds
5. **When Not To Use It** — Anti-patterns and simpler alternatives
6. **Alternatives** — Trade-off comparisons across competing options
7. **Trade-offs** — What you gain vs. what you sacrifice
8. **Failure Modes** — How it misbehaves, cascades, or crashes in production
9. **Scaling** — What breaks first as load grows 10x–100x
10. **Production Example** — How top-tier engineering organizations deploy it
11. **Interview Perspective** — How to proactively bring it up in a 45-minute interview
12. **Industry Vocabulary** — Natural phrasing used by Staff+ engineers
13. **Common Mistakes** — Frequent traps candidates and junior engineers fall into
14. **Questions I Should Be Able To Answer** — Rapid diagnostic self-test
15. **Practice** — Active problem-solving without spoiled answers
16. **60-Second Explanation** — Concise, crisp executive summary

---

## 🚀 How to Study This Curriculum

1. **Start with the Diagnostic:** Evaluate your baseline via [`01-baseline/01-diagnostic-assessment.md`](./01-baseline/01-diagnostic-assessment.md) to discover your knowledge gaps.
2. **Master the Primitives (Phases 1–13):** Build your mental model of computing, networking, storage, databases, and resiliency.
3. **Study the Blueprints (Phase 14):** Learn how Staff engineers combine primitives to solve distributed constraints.
4. **Solve the 10 Practical Designs (Phase 15):** Work through Level 1 and Level 2 designs using the **Mandatory 13-Step Sequence**.
5. **Adopt the Staff Dialect (Phase 16):** Internalize the 25 core terms so you can communicate trade-offs crisply in reviews and interviews.
6. **Execute Spaced Recall (Phase 17):** Test yourself regularly against the decision matrix and anti-pattern checklists.
7. **Take the Final Exam (Phase 18):** Pass the capstone exam before diving into Alex Xu's advanced case studies!
