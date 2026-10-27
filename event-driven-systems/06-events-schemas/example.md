## Follow a concrete example

```json
{
  "event_id":"synthetic-e1","event_type":"TicketCompleted",
  "schema_version":1,"aggregate_id":"42","aggregate_version":3,
  "workspace_id":"7","occurred_at":"2026-10-21T09:00:00Z",
  "data":{"title":"Synthetic ticket"}
}
```

This is teaching data. The lab validates required fields and refuses unsupported schema versions. It does not serialize the work project’s models.
