## Trace the execution

Submit desired state → controller creates/adjusts ReplicaSet → scheduler chooses capacity → kubelet/runtime starts containers → readiness decides traffic eligibility.

Remove one lab pod and observe reconciliation, not manual resurrection of the same identity.

Inspect events when a pod is Pending or repeatedly restarting. Image pull, scheduling, process failure, and readiness failure are different states.