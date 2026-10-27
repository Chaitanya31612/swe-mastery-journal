## Follow a concrete example

```text
DB transaction:
  INSERT inbox (consumer_name, event_id) under unique constraint
  if new: update reporting projection
  commit
After DB transaction: commit Kafka message progress

On duplicate: skip the already committed local effect,
then allow progress acknowledgement.
```

For PostgreSQL, catch a uniqueness exception outside the failed transaction before starting further SQL; a statement error can leave that transaction aborted.
