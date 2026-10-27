## Follow a concrete example

```text
POST /tickets/:id/complete
  → CompleteTicket.call
  → transaction(ticket + outbox)
  → OutboxDispatcher
  → KafkaPublisher delivery acknowledgement
  → ReportingConsumer
  → transaction(inbox + projection)
  → commit message offset
```
Open the app’s Hands-on lab tab for the complete file tree and commands. The README includes expected observations, repeat-event checks, and safe cleanup limited to this Compose project.