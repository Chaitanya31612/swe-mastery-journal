## Follow a concrete example

```text
Partition records: 0, 1, 2, 3
Completed durable effects: 0 and 1
Safe resume offset: 2

Crash after effect for 2, before commit:
resume at 2 → effect must tolerate repetition.
```

The lab uses a synchronous rdkafka message commit after its DB transaction and disables automatic commit/store behavior explicitly.
