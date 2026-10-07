# Distributed rate limiting and overload control — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Exact rolling quota

Across eight API instances enforce at most 120 accepted writes per account in any rolling 60-second period. Peak checks are 15,000/s. Read endpoints may use an approximate limit. Design the write limit, storage/memory estimate method, boundary concurrency, and degraded behavior when the shared store is unavailable.

## P2 — Global and regional budgets

Two regions must share a 10,000 requests/s provider quota; isolated regions can continue only within assigned emergency budgets. Design allocation and explain precision, lease/fencing, and unused-capacity trade-offs.

## P3 — Fix bad pseudocode

```text
count = shared.get(account)
if count < limit:
    shared.set(account, count + 1)
    allow()
else:
    deny()
```

It has no window handling. Fix the race and identify what further mechanism the rolling-window contract requires.

## Delayed gate

Compare exact rolling limits with bursty token refill. Trace a last-token race and global-budget isolation.
