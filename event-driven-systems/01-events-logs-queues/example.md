## Follow a concrete example

```text
Command: GenerateReport(report_run_id)
Owner: reporting worker; outcome ready/failed.

Event: TicketCompleted(event_id, ticket_id, workspace_id, version)
Subscribers: reporting projection and notification intent.
Each subscriber has independent progress and failure handling.
```
Do not use an event name to hide a synchronous business requirement. If completing the ticket requires another decision now, model that dependency explicitly.