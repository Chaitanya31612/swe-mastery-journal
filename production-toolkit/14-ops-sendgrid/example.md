## Follow a concrete example

```text
Ticket completed → notification intent in DB
Worker → provider request → accepted/provider message identity
Signed webhook → delivery/bounce/suppression event
DB status update keyed by provider event identity
```

Do not put free-text private ticket content into a demo template or telemetry. A fake adapter should simulate acceptance followed by timeout.
