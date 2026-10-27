## Follow a concrete example

```json
{"event":"receipt_attempt","event_id":"synthetic-e1","attempt":2,
 "outcome":"timeout","duration_ms":850,"request_id":"synthetic-r1"}
```
Use event/request IDs in controlled logs/traces for correlation. Metrics might use bounded service, environment, and outcome categories.

Avoid logging payloads or secrets.