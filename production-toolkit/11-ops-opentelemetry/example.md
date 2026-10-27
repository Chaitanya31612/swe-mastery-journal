## Follow a concrete example

```text
Rails instrumentation → OTLP exporter → Collector
Collector: receive → process/redact/batch → export
Backend: storage, queries, dashboards, alerts
```

Record service.name, deployment environment, and version deliberately. Keep event IDs in suitable spans/logs; do not make every event a metric label.
