## Understand the idea

OpenTelemetry supplies standards, APIs/SDKs, instrumentation, and collection/export tools. It is not by itself the long-term observability database or dashboard.

You still choose where telemetry is stored and how it is queried/retained.

A trace has spans describing work and relationships. Propagated context connects work across HTTP boundaries.

An asynchronous event may carry context or link separate work under an explicit policy. Avoid putting sensitive business data into baggage that travels broadly.

Setup: select compatible instrumentation, stable resource attributes, a collector/exporter path, sampling/retention policy, and a test trace. Verify every hop and failure behavior.

Telemetry failure should not accidentally block the main business operation without a deliberate reason.