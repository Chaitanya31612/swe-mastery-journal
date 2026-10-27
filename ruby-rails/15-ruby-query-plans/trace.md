## Trace the execution

Request scope → SQL predicate/order → database plan → limited rows/batches → Ruby transformation → output. Measure rows, query count, and memory at separate points.

For an export, decide what happens when tickets change while it runs.

A transaction snapshot may give stability but can be expensive over a long job; a materialized export scope is another tradeoff.