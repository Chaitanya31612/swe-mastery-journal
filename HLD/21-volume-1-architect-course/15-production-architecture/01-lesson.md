# Production practice: service objectives, security, and safe evolution

Learning outcome: Turn a diagram into measurable service behavior, bounded failure recovery, threat boundaries, and a reversible migration plan.

## Objectives describe useful service

An SLI measures service behavior, such as successful authorized redirects, durable message acceptance latency, or timely completed jobs. An SLO sets a target over a window. A raw uptime number can miss incorrect results and delayed async work. Separate internal diagnostic metrics from user-visible indicators. An error budget is the allowed shortfall implied by the objective and measurement policy; it informs reliability/product trade-offs, not an automatic punishment rule.

## Bound failure rather than multiplying it

For example, a 99.9% successful-request SLO over one million eligible requests allows 1,000 unsuccessful requests under that measurement definition. A time-based 99.9% availability target over 30 days allows about 43.2 minutes; do not interchange time and request ratios without defining the SLI. Burn rate describes how quickly the permitted shortfall is being consumed, and useful alerts distinguish urgent sustained impact from noise.

Give downstream calls deadlines within an end-to-end budget. Retries consume remaining time/capacity; retry only eligible operations with stable identity and a bounded budget, using jitter where synchronized attempts could overload a dependency. A circuit breaker can temporarily avoid an unhealthy dependency, with recovery probes; it does not repair it or prevent every cascade. Bulkheads/concurrency limits isolate scarce resources. Shed/defer work when the product contract permits, and define what the user sees.

For recovery, RPO is tolerated data loss measured in time/operations as defined; RTO is tolerated restoration time. Replication, backups, restoration tests, failover, and regional disaster procedures address different failure modes. Multi-region active-active adds ownership/conflict/latency/operational cost; do not add it without a contract requiring it.

## Threat model from flows

List assets and trust boundaries: public client, authenticated user, service credential, tenant data, untrusted URL/file, provider. Authentication identifies a principal; authorization checks an operation against resource policy. Enforce tenant/resource scope on all relevant reads/writes, not only login. Protect secrets, validate untrusted input at the actual execution boundary, limit abuse, and choose sensitive-data retention/logging policy. A queue/CDN can carry data across boundaries and needs compatible policy.

## Schema and architecture evolution

An expand/migrate/contract rollout first adds a compatible representation, deploys readers/writers that tolerate both, backfills with checkpoints/idempotency, validates, cuts over gradually, and only later removes the old form. Blind dual writes can diverge; choose one authoritative source and track reconciliation/progress. A rollback must be meaningful after the change, including old-reader compatibility and data written during the new version.

Use canaries/shadow comparisons with observable success criteria. Performance tests include realistic data/skew, cold caches, failure, and tail behavior, not just happy-path requests. Capacity/cost estimates identify dominant bytes, replicas, storage retention, compute jobs, or third-party quotas. Compare build-versus-managed choices against requirements and operational expertise.

## Architecture review artifact

Write context/contract → evidence → two alternatives → decision/consequences → failure/operation → rollout/verification. A senior-quality review acknowledges uncertainty and seeks measurements rather than declaring a diagram perfect. During an incident, stabilize user impact first, preserve evidence, and separate mitigation from root-cause analysis.

## Retrieve before practicing

Explain RPO/RTO with an actual restore scenario. Write an expand/migrate/contract plan and identify when rollback ceases to be safe.
