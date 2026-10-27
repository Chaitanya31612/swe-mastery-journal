## Follow a concrete example

```text
Rails outbox → producer adapter → reachable MSK brokers
Topic key = ticket identity
Reporting group → repeat-safe PostgreSQL projection
Metrics = producer errors, consumer lag/age, processing errors, retention headroom
```

The local PLAINTEXT development listener is not the cloud security configuration. Choose authentication and client settings from the selected MSK mode’s docs.
