## Understand the idea

A request can wait for a connection, a row lock, a slow query, or an external service. Low CPU does not prove spare useful capacity.

Trace waiting time separately from execution time.

An index should serve a query shape: filter, ordering, and selected data. Check the plan with representative synthetic data and actual predicates.

An index adds write/storage cost and may not help a very broad query. Avoid loading full entities when a screen needs a few fields.

A connection pool is a limit, not free throughput. Long transactions hold connections and sometimes locks.

Increasing web threads beyond database capacity can grow queues and latency. Keep network calls out of database lock windows when possible.