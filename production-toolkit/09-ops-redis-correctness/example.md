## Follow a concrete example

```text
Bad release: DEL lock:key, regardless of owner
Better ownership release: compare stored token, then delete atomically

Still possible:
A lease expires → B owns lease → A resumes → stale A writes elsewhere
```
For inventory or money, prefer a rule enforced at the authoritative database boundary where feasible. Do not use a short Redis TTL as proof of global mutual exclusion.