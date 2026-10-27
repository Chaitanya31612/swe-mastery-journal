## Understand

RAG means retrieving relevant material and giving it to a generator. It is an application pattern, not a guarantee of correctness. The original research combines learned generation with retrieved information; modern products implement many variants.

A current delivery count belongs in a scoped database query. A policy explanation may need retrieved documents. A shipment's verified hold reason may come from a deterministic rule over current fields. These sources can appear together in one answer, but keep their authority and freshness visible.

Start with the smallest sufficient retrieval method. Exact IDs, filters, full-text search, and a document table may be enough. Add semantic search when wording varies in a way lexical search misses. Never move access control into similarity scoring or ask a model to infer the user's tenant.
