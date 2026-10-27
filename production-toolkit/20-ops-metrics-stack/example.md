## Follow a concrete example

```text
completed_jobs_total{service="reporting", outcome="success"}
pending_jobs{service="reporting"}
oldest_pending_age_seconds{service="reporting"}
```

Use event IDs in appropriate logs/traces, not as a new time-series label for every event. Compare rate and age with failure/retry signals.
