## Follow a concrete example

```text
Failure categories
temporary DB outage → bounded retry/backoff, retain position
invalid event schema → visible stop/quarantine under policy
business stale version → deliberate ignore/reconcile rule
unknown remote side effect → reconcile, not blind resend
```
The lab deliberately stops on invalid input and leaves the offset uncommitted. Retry/DLQ routing is a follow-up design exercise, not silently implemented magic.