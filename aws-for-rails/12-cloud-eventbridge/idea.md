## Understand the idea

EventBridge connects event sources and targets with routing/filtering features. It is useful when you integrate AWS/service events or route application facts by a structured envelope. Choose the actual bus/pipe offering and its documented retention/ordering/replay behavior; newer offerings can differ from classic rule-based examples.

This chapter’s setup uses a deliberate classic-style custom bus, event pattern, and target such as SQS. An event pattern selects meaning from fields such as source and detail-type. It does not validate every business rule inside detail.

Setup: choose the supported bus type, define a small event schema, create a matching rule and target permission, configure delivery failure handling, and send one matching and one non-matching event. Inspect the producer response for per-entry failure rather than treating the HTTP request alone as success.
