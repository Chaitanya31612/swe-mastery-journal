## Trace the execution

Trace request arrival → pool wait → SQL/lock wait → row fetch → DTO mapping → response. Measure each boundary before changing a limit.

For a transaction that calls a slow provider between writes, show how many requests can hold connections while waiting. Move delivery intent into an outbox when a later external effect is acceptable.