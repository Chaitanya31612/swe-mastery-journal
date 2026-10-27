## Break it and reason about the repair

A pod is disposable identity, not your only copy of data. Increasing replicas does not make a database transaction safe or a queue effect unique.

**Remember:** Declare the state. Observe reconciliation.

Keep data responsibility explicit.