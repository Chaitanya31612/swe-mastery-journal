# Software Learnings: a practical course, one boundary at a time

Use this as a reference library and a guided course. You do not need to learn every tool before doing useful work. Start with the frontend and UX path because those are central to your current work. Keep one main track at a time.

## Course map

- **Java · Spring Boot**: 14 chapters, 4 Beginner + 10 Intermediate. About 36 hours including practice.
- **Ruby · Rails at work**: 18 chapters, 8 Beginner + 10 Intermediate. About 48 hours including practice.
- **Git · Change with confidence**: 10 chapters, 5 Beginner + 5 Intermediate. About 20 hours including practice.
- **Frontend · JavaScript & Vue 3**: 27 chapters, 10 Beginner + 17 Intermediate. About 62 hours including practice.
- **UX · Design for understanding**: 9 chapters, 5 Beginner + 4 Intermediate. About 18 hours including practice.
- **AWS · Run a Rails application**: 20 chapters, 9 Beginner + 11 Intermediate. About 40 hours including practice.
- **Production toolkit · Build and operate**: 22 chapters, 10 Beginner + 12 Intermediate. About 44 hours including practice.
- **Event-driven systems · Kafka & Rails**: 12 chapters, 6 Beginner + 6 Intermediate. About 24 hours including practice.

The full library is about 292 hours with practice, before extra project work: roughly 42 weeks at seven hours/week. This is an estimate, not a promise of mastery. The earlier one-month HLD deadline does not fit this entire new library. Use a focused four-week block, demonstrate a specific skill, then choose the next block.

## Your first four-week block: frontend and UX

Spend about seven hours each week. Choose depth over checking every chapter.

1. **Week 1: explain what the UI is doing.** JavaScript values, functions/closures, async runtime, TypeScript states, and the UX task model. Predict a stale-response bug before running the small example.
2. **Week 2: make a component understandable.** CSS layout, Vue props/events, reactivity, hierarchy, and feedback. Draw query → request → current result → independent edit draft. Test a long label, narrow layout, and Cancel.
3. **Week 3: own asynchronous state.** Vue composables, async cleanup, forms, and useful errors. Run the Vue ticket lab. Reproduce stale success, stale error, and a failed save. Keep a bug diary with expected and actual results.
4. **Week 4: prove a small improvement.** Testing, browser performance, inclusive access, and the frontend/UX capstones. Improve one synthetic support workflow. Keep before/after evidence. Solve one changed requirement without opening the reference.

This block samples related chapters; finishing every exercise in those chapters can take longer. Continue unfinished practice before moving on. Familiar material may need only a cold prediction and a failed-case check.

## Later blocks

- **Rails and Git:** follow a request through scoped data access, transaction, job intent, retries, query plan, and tests. Use Git surgery/conflict/investigation cases in a disposable repository. Keep modern lab APIs distinct from the legacy work baseline.
- **Container foundation:** Docker image versus container, Compose service networking, then Kubernetes desired state, Service endpoints, readiness, and release behavior. Explain which system owns which decision before memorizing YAML.
- **AWS for Rails:** identity and networking first. Follow a web request, upload, DB connection, cache, job, and secret. Start with ECS; compare EKS when Kubernetes brings a real benefit. Use the setup worksheet and local SDK stubs before optional cloud work.
- **Event-driven systems:** log/queue → key/partition → broker layers → producer → consumer → schema → outbox/inbox → retries → operations → multi-file Rails lab → replay capstone. Keep one event ID in view at every boundary.
- **Production toolkit:** learn one tool when its problem appears. Each chapter covers its use, benefit, cost, example, failure, practice, and quiz. Finish with the cumulative check across the tools. Redis gets three chapters and a real local lab.

## A repeatable seven-hour week

Use two 90-minute lessons, two 75-minute practical sessions, and six 15-minute recall sessions. That is seven hours. If a lab takes longer, reduce new reading that week. Keep a small queue: at most two unfinished modules before consolidating them.

## One chapter, one routine

1. **See:** inspect the diagram. Say what goes in and what should come out.
2. **Trace:** follow one example through its real files or steps.
3. **Predict:** write an outcome before revealing or running it.
4. **Do:** attempt the repair with answers closed. Use a separate training sandbox.
5. **Compare:** submit a snapshot; open the reference or request AI feedback. Explain one difference.
6. **Transfer:** change a condition. Try again without the reference.
7. **Recall:** explain the rule, example, and failure later, before rereading.

The app has Learn, Predict, optional Code lab, Practice, Quiz, References, notes, and a recall queue. The Code lab shows read-only files; it does not execute commands. Reference solutions unlock after submitting practice. Quiz explanations appear after checking all answers. AI tutoring uses the selected step/file. Practice coaching gives a hint; snapshot review compares the submitted evidence with the reference. AI does not run tests.

## Beginner and Intermediate completion gates

**Beginner:** explain the key terms in ordinary words; draw the happy path; predict a small example; run or inspect a basic failure; answer why the wrong quiz options fail.

**Intermediate:** trace state across multiple files/services; reproduce a failure timeline; choose between two valid approaches using a constraint; add a regression check; explain an operating cost; solve a changed requirement without the answer.

For the toolkit/AWS/Kafka final chapters, do the cumulative quiz and the changed-case design. A good score alone is insufficient. Explain a failure and verify a recovery boundary. For frontend/UX, demonstrate task success, error recovery, keyboard use, readable small-screen content, and before/after evidence.

The app records lesson steps, both attempts, quiz accuracy, and delayed recall. Consolidated means all steps, both attempts, latest quiz at least 75%, and a successful recall at least seven days after the first practice. These are learning signals, not independently verified job readiness.

## Retention without endless rereading

First recall is due after one day. Successful recalls move to 3, 7, 14, 30, and 60-day gaps. Again returns in ten minutes; Hard in a day. These intervals are product defaults, not a universal optimal schedule. Reviews appear when you open the app; no background notifications are implied.

Use a three-line bug diary: symptom → mechanism → check that catches it. Connect the memory cue to a concrete failure. Each week, mix one older problem into the new topic. If you cannot explain it, take the small example again, then close it and retrieve. No course can guarantee permanent memory. Repeated retrieval, correction, spacing, and real use make forgetting easier to notice and repair.

Retrieval practice and spacing have research support: [Roediger and Karpicke](https://www.psychologicalscience.org/journals/psychological-science/j.1467-9280.2006.01693.x/) and [Cepeda and colleagues](https://doi.org/10.1111/j.1467-9280.2008.02209.x). The exact chapter format and fixed intervals here are design choices, not outcomes proven by those studies.

## Read books as a second pass

Try the example first. Use the mapped Ruby book chapter to fill a specific gap. Avoid restarting the whole book every time confidence drops. Use versioned official docs for runtime details. The UX guide builds on task models, feedback, accessibility, measurement, and carefully bounded laws; it does not reduce design to a magic number of choices.

## Sandboxes and work safety

The work repository remains read-only. Examples are fresh synthetic support-ticket code, not copied production code. Course runtime and AI do not read the work directory. Do not paste private data or code into AI chat.

The modern Rails/Kafka lab uses Ruby 3.3 / Rails 7.2; work uses Ruby 2.7 / Rails 4.2. Read the compatibility notes. Local Docker labs do not create cloud resources. AWS adapter tests use SDK stubs; they cannot prove real IAM or network setup. See [versions and sources](versions-and-sources.md) and the lab READMEs for exact commands and limits.

Export progress regularly from Backup. Your journal lessons are source files; learning attempts and recall history live in browser storage.
