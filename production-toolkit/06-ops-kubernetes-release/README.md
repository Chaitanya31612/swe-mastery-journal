# 13. Kubernetes probes, resources, rollout, and graceful work

**Intermediate · about 2 hours with practice**

Choose startup/readiness/liveness signals and release web/worker code without confusing restart with recovery.

## Use it

Rails web/worker deployment and incident diagnosis.

**Benefit:** Controlled traffic and process lifecycle.

**Cost or limit:** Poor probes/limits can create outages themselves.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Kubernetes probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
