## Follow a concrete example

```text
Before: ticket.save → concern callback → enqueue receipt
Risk: importer + explicit enqueue path may duplicate the effect.

Target: CompleteTicket use case
  transaction: ticket state + one outbox event
  later: dispatcher publishes saved intent
```
Not every callback must disappear. Keep local model rules where their behavior and bypass paths are understood.