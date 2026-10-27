## Trace the execution

Follow HTTP headers/body/timeouts through the proxy, then follow one database transaction through both client and server pools. Count application processes/pools and observe queued versus active DB work.

Test a feature relying on connection/session state before selecting transaction pooling. Do not infer compatibility from one simple SELECT.