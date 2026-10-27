## Follow a concrete example

```text
HTTP: browser → Nginx/ALB → Puma → Rails
SQL: Rails pool → PgBouncer (chosen mode) → PostgreSQL
```
For debugging, record which layer generated an error and whether a request/connection reached the next hop. A 504 and a DB pool checkout timeout are not the same symptom.