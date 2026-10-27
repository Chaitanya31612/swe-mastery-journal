## Follow a concrete example

```json
{"source":["learning.tickets"],"detail-type":["TicketCompleted"]}
```
The rule targets a reporting queue under an explicit policy. Include event_id, workspace_id, ticket_id, schema_version, and occurred_at in a minimal detail envelope.

Do not publish whole private model snapshots.