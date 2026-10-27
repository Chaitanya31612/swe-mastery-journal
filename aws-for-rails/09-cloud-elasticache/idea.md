## Understand the idea

ElastiCache supplies managed in-memory engines/options. Identify the selected engine and mode rather than assuming every Redis-compatible feature and durability behavior is identical.

Client compatibility, topology, authentication, TLS, and failover matter.

A disposable cache can evict/rebuild data. A background queue’s work may not be safely disposable.

Mixing both under one eviction and memory policy can turn a cache-pressure event into lost jobs. Isolate roles according to their correctness needs.

Setup: choose engine/mode, private connectivity, access/TLS settings, memory/eviction policy, client timeout/pool behavior, and monitoring. Test a cold cache, memory pressure, and endpoint/failover changes with synthetic data.

Do not expose a cache endpoint publicly to avoid a VPC configuration problem.