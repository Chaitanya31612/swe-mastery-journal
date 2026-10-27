## Trace the execution

Follow one notification ID through retries and provider events. A webhook can be repeated or arrive after another event.

Define allowed state transitions from observed facts rather than assuming arrival order is perfect.

For a timeout, check provider-supported status/idempotency behavior before resending. If acceptance is unknown, record uncertainty and reconcile rather than asserting success or failure without evidence.