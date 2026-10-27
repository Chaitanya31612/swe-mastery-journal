## Trace the execution

Cache miss → authoritative DB read → cached copy → later hit → expiry/eviction → rebuild. Then trace failover: client connection breaks, DNS/topology changes, operations retry under the selected contract.

Monitor memory, eviction, latency, connection count, and application fallback load. A cache outage can overload PostgreSQL if every request immediately falls back.