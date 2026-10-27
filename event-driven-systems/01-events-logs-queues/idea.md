## Understand the idea

A command asks someone to do something: GenerateReport. An event states a fact: TicketCompleted. Naming the difference helps decide who owns rejection, completion, and follow-up work.

A work queue commonly distributes work among competing workers. A retained log keeps ordered records under a retention policy while each consumer group tracks its own progress. Kafka is useful for independent subscribers and replay, not merely because a system has background jobs.

Asynchronous communication moves a boundary in time. It can buffer work and decouple processing, but users need an honest pending/result model. It also adds duplicates, schema evolution, delayed access/context, and operational recovery questions. A direct call or existing job queue can be simpler when those benefits are not needed.
