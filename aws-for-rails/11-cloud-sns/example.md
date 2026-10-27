## Follow a concrete example

```text
TicketCompleted topic
  → reporting queue → reporting workers
  → notification queue → notification workers
```

Three reporting workers on the reporting queue share reporting work. They are not three separate business subscriptions.
