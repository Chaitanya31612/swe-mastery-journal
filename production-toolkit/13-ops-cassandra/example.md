## Follow a concrete example

```sql
CREATE TABLE ticket_events_by_day (
  workspace_id text, event_day date, occurred_at timestamp,
  event_id uuid, ticket_id text, kind text,
  PRIMARY KEY ((workspace_id, event_day), occurred_at, event_id)
) WITH CLUSTERING ORDER BY (occurred_at DESC, event_id ASC);
```

This example serves one day-scoped event query. It is not a universal ticket schema or a replacement for relational ownership/transaction rules.
