## Understand the idea

Startup, readiness, and liveness ask different questions. Startup protects a slow initialization phase. Readiness controls traffic eligibility. Liveness can trigger a restart when the process is stuck under the chosen health contract.

Do not make liveness depend on every remote service; an outage can cause a restart storm. A worker also needs a progress/processing health model, not necessarily the web app’s HTTP probe.

Resource requests affect scheduling; limits affect runtime behavior under the selected resource type. CPU throttling and memory termination can look like app bugs. A rollout needs compatible schema, ready new pods, graceful old-pod shutdown, and an explicit rollback/data plan.
