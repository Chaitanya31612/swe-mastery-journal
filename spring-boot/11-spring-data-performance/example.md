## Follow a concrete example

```sql
-- A common bounded work queue query:
SELECT id, title FROM tickets
WHERE workspace_id = 7 AND status = 'open'
ORDER BY created_at, id LIMIT 50;
-- Investigate a matching composite index and EXPLAIN on training data.
```
Use PostgreSQL for PostgreSQL plan/lock claims. The existing H2 lab proves smaller contracts, not the production engine’s plan or concurrency behavior.