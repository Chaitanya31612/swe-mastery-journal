## Walk through an example

```sql
SELECT id, source_version, body
FROM policy_documents
WHERE tenant_id = $1 AND published = true
ORDER BY embedding <=> $2::vector
LIMIT 5;
```
Here $1 comes from the authenticated actor and $2 from a validated vector. The operator is cosine distance.

Lower distance ranks earlier. The exact query plan and model/distance compatibility still need measurement.