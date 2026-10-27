## Follow the execution

Trace job status separately from transport connection. Simulate disconnect, reconnect, out-of-order status reads, malformed final output, and a newer request finishing first.

Protect every visible state update with the current run identity.