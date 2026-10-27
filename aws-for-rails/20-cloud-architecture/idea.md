## Understand the idea

Use a modular Rails app with web and workers, PostgreSQL as the business source, private attachments, a cache, and deliberate event delivery. Choose ECS/Fargate as one baseline; EKS is an alternative when Kubernetes benefits justify it. They are not two layers every app must run together.

Trace four journeys: a user opens a ticket, uploads an attachment, requests a report, and completes a ticket that updates reporting. For each, name identity, network, authoritative write, asynchronous boundary, user-visible state, and recovery path.

Then stress the design: one zone fails, the provider slows, a worker repeats, the DB pool fills, a secret rotates, or a user loses access. Cost reasoning includes always-on capacity, storage/retention, data transfer, NAT/endpoints, logs, and managed service overhead. Use current regional pricing when actually provisioning; this course does not promise a free deployment.
