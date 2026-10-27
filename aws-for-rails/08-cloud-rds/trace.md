## Trace the execution

Rails checks out a connection → network/TLS/authentication → SQL/locks → commit → connection returns to pool. Multiply pool size by web/worker process count before comparing with DB limits.

During failover, existing connections can break. The app needs bounded retry/reconnect behavior and must not retry a non-idempotent transaction blindly after an unknown commit outcome.