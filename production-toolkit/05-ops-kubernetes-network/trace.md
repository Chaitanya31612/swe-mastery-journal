## Trace the execution

Client/edge → controller route → Service port → selected ready Pod endpoint → app target port. A 503 can come from no eligible endpoints even when a pod process exists.

Test a selector mismatch, wrong targetPort, and readiness failure separately. Observe how each changes events/endpoints/response. Keep the app’s allowed-host/proxy/TLS configuration in the path.
