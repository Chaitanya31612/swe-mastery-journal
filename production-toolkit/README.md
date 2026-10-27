# Production toolkit · Build and operate

Beginner builds the model. Intermediate adds real constraints, failure cases, and tradeoffs. Follow the sequence below. Folder names and module IDs stay stable for saved progress.

## Beginner

- 01. [Docker: image, container, process, and volume](01-ops-docker-model/README.md): Reconstruct what survives stop, restart, replacement, and image rebuild.
- 02. [Compose: connect web, database, broker, and workers](03-ops-compose/README.md): Explain service DNS, ports, volumes, health, and startup versus readiness in a local application.
- 03. [Kubernetes: desired state, pods, and controllers](04-ops-kubernetes-model/README.md): Explain how a Deployment leads to running pods and what happens when one disappears.
- 04. [Redis foundations: pick a data structure for the question](07-ops-redis-types/README.md): Choose strings, hashes, sets, sorted sets, lists, and streams from access patterns.
- 05. [Datadog: turn traces and monitors into an investigation](10-ops-datadog/README.md): Connect Rails requests, jobs, SQL, and provider calls with useful service identity and bounded telemetry.
- 06. [OpenTelemetry: instrumentation is not the storage backend](11-ops-opentelemetry/README.md): Explain traces, metrics, logs, context propagation, and collector/exporter roles.
- 07. [SendGrid: accepted email is not delivered email](14-ops-sendgrid/README.md): Trace message intent, provider acceptance, delivery events, suppression, and retry uncertainty.
- 08. [cron and scheduled work: a trigger is not a transaction](15-ops-cron/README.md): Read a schedule and design missed-run, overlap, timezone, and deduplication behavior.
- 09. [Pendo: measure meaningful product behavior](16-ops-pendo/README.md): Define a product event and separate analytics identity, consent/data policy, and business success.
- 10. [Prometheus and Grafana: collect a signal, then ask a question](20-ops-metrics-stack/README.md): Explain metric collection, labels, rates, dashboards, and alert ownership without treating a graph as evidence by itself.

## Intermediate

- 11. [Docker builds: layers, identity, and a smaller runtime](02-ops-docker-build/README.md): Build a Rails artifact without embedding secrets or relying on mutable tags.
- 12. [Kubernetes networking: Services, selectors, ingress, and names](05-ops-kubernetes-network/README.md): Trace a request from edge to a ready pod and debug an empty Service endpoint set.
- 13. [Kubernetes probes, resources, rollout, and graceful work](06-ops-kubernetes-release/README.md): Choose startup/readiness/liveness signals and release web/worker code without confusing restart with recovery.
- 14. [Redis caching: freshness, invalidation, and stampedes](08-ops-redis-cache/README.md): Design cache-aside with scoped keys and bounded rebuild behavior.
- 15. [Redis correctness: persistence, atomic work, and lock expiry](09-ops-redis-correctness/README.md): Explain pipeline versus transaction/script, persistence loss windows, and why a lease needs stale-writer protection.
- 16. [Debezium: capture committed changes without inventing business meaning](12-ops-debezium/README.md): Explain CDC, snapshots, log positions, outbox routing, and duplicate-safe downstream processing.
- 17. [Cassandra: design the query before the table](13-ops-cassandra/README.md): Explain partition/clustering keys, bounded partitions, denormalization, and the tradeoff versus PostgreSQL.
- 18. [Terraform: desired infrastructure with state and review](17-ops-terraform/README.md): Explain configuration, plan, state, drift, and the effect of apply without treating a plan as a harmless toy.
- 19. [GitHub Actions: test, build once, and promote an artifact](18-ops-github-actions/README.md): Design a CI/CD path with explicit permissions, artifact identity, and release gates.
- 20. [Nginx and PgBouncer: two different kinds of front door](19-ops-proxy-pools/README.md): Distinguish HTTP reverse proxying from database connection pooling and test their compatibility limits.
- 21. [Feature flags: release control without permanent branching](21-ops-feature-flags/README.md): Use a flag to limit exposure and define defaults, ownership, removal, and data compatibility.
- 22. [Choose the tools, then debug the whole application](22-ops-toolkit-capstone/README.md): Explain a production tool map and recover a synthetic incident without adding every tool by default.
