## Trace the execution

New specification → new pods start → startup check → readiness allows traffic → old pods drain → process receives termination signal → unfinished work completes or becomes safely retryable.

Observe rollout and user-level error/latency.

If a worker is terminated after DB commit but before offset/queue acknowledgement, its replacement may repeat the item. Infrastructure shutdown and business idempotence must cooperate.