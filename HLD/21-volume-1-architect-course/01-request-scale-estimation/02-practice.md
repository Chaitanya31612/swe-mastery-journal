# Requests, scale, and useful estimates — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Product page capacity

Ten million active users/day view 30 product pages each and create 0.05 reviews each. A page view makes four database reads; average returned data is 20 KB. Use 5× peaks. Reviews average 1 KB and are retained for three years. Calculate operation rates, database rates without caching, outbound bandwidth, and raw review storage. Identify two important unknowns and propose a simple initial design.

## P2 — Waiting, not computing

An API receives 400 requests/s; mean latency is 0.5 seconds, p99 is 4 seconds, CPU is 15%, and the DB pool is full. A proposal increases instances from 10 to 50, each with a 100-connection pool. Diagnose possible causes and propose measurements before scaling. Explain stable mean in-flight work versus worker/database limits.

## P3 — Repair the capacity argument

“The average rate is 400/s. Each server handles 400/s in a local benchmark. One server is therefore sufficient and there is no need for peak allowance or failure capacity.” Identify the assumptions and write a better argument.

Save calculations and the architectural consequence, not just final numbers.

## Delayed gate

Explain why scaling an API can harm a shared database. Recompute P1 when each view makes only one DB read and page bytes triple.
