## Trace the execution

Source event → invocation/batch → validate record → durable effect → source-specific acknowledgement/failure handling. A retry may invoke the handler again with the same logical item.

Measure cold-start and dependency latency for the actual interaction. Bound concurrency so a surge does not create more database connections than RDS can support.
