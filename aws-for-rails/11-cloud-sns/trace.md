## Trace the execution

Publisher sends one fact → SNS evaluates subscriptions/filters → each destination receives according to its delivery contract → each queue/consumer manages its own completion.

One slow subscriber should not dictate another’s progress when their buffers are separate.

Carry an event ID for duplicate handling and traceability. A publish acknowledgement does not prove every subscriber’s business effect completed.