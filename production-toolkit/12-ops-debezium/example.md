## Follow a concrete example

```text
Rails transaction: ticket update + outbox row
PostgreSQL committed log → Debezium connector
Outbox routing → ticket-events keyed by aggregate identity
Reporting consumer → inbox + projection transaction
```
The course’s runnable lab uses a polling outbox dispatcher first so you can see the dual-write boundary.

Debezium is an alternative publisher path, not an extra publisher that should also emit the same rows.