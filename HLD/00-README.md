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

| Phase | Primary Learning Module | Detailed Solutions | Status |
|---|---|---|---|
| **Phase 0** | [`01-baseline/01-diagnostic-assessment.md`](./01-baseline/01-diagnostic-assessment.md) | [`01-baseline/solutions.md`](./01-baseline/solutions.md) | 🟢 Complete |
| **Phase 1** | [`02-system-design-thinking/01-system-design-mental-model.md`](./02-system-design-thinking/01-system-design-mental-model.md) | [`02-system-design-thinking/solutions.md`](./02-system-design-thinking/solutions.md) | 🟢 Complete |
| **Phase 2** | [`03-estimation/01-back-of-the-envelope-estimation.md`](./03-estimation/01-back-of-the-envelope-estimation.md) | [`03-estimation/solutions.md`](./03-estimation/solutions.md) | 🟢 Complete |
| **Phase 3** | [`04-networking/01-request-lifecycle-and-networking.md`](./04-networking/01-request-lifecycle-and-networking.md) | [`04-networking/solutions.md`](./04-networking/solutions.md) | 🟢 Complete |
| **Phase 4** | [`05-compute-and-scaling/01-compute-statelessness-and-scaling.md`](./05-compute-and-scaling/01-compute-statelessness-and-scaling.md) | [`05-compute-and-scaling/solutions.md`](./05-compute-and-scaling/solutions.md) | 🟢 Complete |
| **Phase 5** | [`06-databases/01-data-modeling-relational-and-nosql.md`](./06-databases/01-data-modeling-relational-and-nosql.md) | [`06-databases/solutions.md`](./06-databases/solutions.md) | 🟢 Complete |
| **Phase 6** | [`07-caching/01-caching-strategies-and-invalidation.md`](./07-caching/01-caching-strategies-and-invalidation.md) | [`07-caching/solutions.md`](./07-caching/solutions.md) | 🟢 Complete |
| **Phase 7** | [`08-async-systems/01-queues-pubsub-and-event-driven.md`](./08-async-systems/01-queues-pubsub-and-event-driven.md) | [`08-async-systems/solutions.md`](./08-async-systems/solutions.md) | 🟢 Complete |
| **Phase 8** | [`09-distributed-systems/01-distributed-fundamentals-and-consensus.md`](./09-distributed-systems/01-distributed-fundamentals-and-consensus.md) | [`09-distributed-systems/solutions.md`](./09-distributed-systems/solutions.md) | 🟢 Complete |
| **Phase 9** | [`10-storage/01-storage-paradigms-and-object-stores.md`](./10-storage/01-storage-paradigms-and-object-stores.md) | [`10-storage/solutions.md`](./10-storage/solutions.md) | 🟢 Complete |
| **Phase 10** | [`11-search/01-search-systems-and-indexing-pipelines.md`](./11-search/01-search-systems-and-indexing-pipelines.md) | [`11-search/solutions.md`](./11-search/solutions.md) | 🟢 Complete |
| **Phase 11** | [`12-reliability/01-reliability-fault-tolerance-and-slas.md`](./12-reliability/01-reliability-fault-tolerance-and-slas.md) | [`12-reliability/solutions.md`](./12-reliability/solutions.md) | 🟢 Complete |
| **Phase 12** | [`13-observability/01-observability-telemetry-and-debugging.md`](./13-observability/01-observability-telemetry-and-debugging.md) | [`13-observability/solutions.md`](./13-observability/solutions.md) | 🟢 Complete |
| **Phase 13** | [`14-security/01-practical-architectural-security.md`](./14-security/01-practical-architectural-security.md) | [`14-security/solutions.md`](./14-security/solutions.md) | 🟢 Complete |
| **Phase 14** | [`15-architecture-patterns/01-core-architectural-patterns.md`](./15-architecture-patterns/01-core-architectural-patterns.md) | [`15-architecture-patterns/solutions.md`](./15-architecture-patterns/solutions.md) | 🟢 Complete |
| **Phase 15** | [`16-practical-designs/01-level-1-foundational-designs.md`](./16-practical-designs/01-level-1-foundational-designs.md)<br>[`16-practical-designs/02-level-2-distributed-designs.md`](./16-practical-designs/02-level-2-distributed-designs.md) | [`16-practical-designs/solutions.md`](./16-practical-designs/solutions.md) | 🟢 Complete |
| **Phase 16** | [`17-industry-vocabulary/01-staff-engineer-dialect-guide.md`](./17-industry-vocabulary/01-staff-engineer-dialect-guide.md) | [`17-industry-vocabulary/solutions.md`](./17-industry-vocabulary/solutions.md) | 🟢 Complete |
| **Phase 17** | [`18-revision/01-spaced-repetition-and-decision-cheatsheet.md`](./18-revision/01-spaced-repetition-and-decision-cheatsheet.md) | [`18-revision/solutions.md`](./18-revision/solutions.md) | 🟢 Complete |
| **Phase 18** | [`19-final-assessment/01-comprehensive-readiness-exam.md`](./19-final-assessment/01-comprehensive-readiness-exam.md) | [`19-final-assessment/solutions.md`](./19-final-assessment/solutions.md) | 🟢 Complete |

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
