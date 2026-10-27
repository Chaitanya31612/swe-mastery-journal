## Understand

pgvector adds vector types and distance operations to PostgreSQL. By default, nearest-neighbor search can be exact.

Approximate indexes such as HNSW trade some recall for speed. Choose that tradeoff after measuring the data and query pattern.

Use tenant/publication/access conditions in the query. With approximate indexes, filtering can leave fewer results because candidate search and filtering interact.

Iterative scans in supported versions can improve filtered search, but do not replace authorization. Validate dimensions, numeric values, model version, and query size before executing SQL.

A Rails relation should own the actor scope. Bind outside values and build only deliberate SQL fragments.

Never interpolate model-generated SQL, column names, or vector strings directly.

The local lab uses PostgreSQL with pgvector and tiny hand-made vectors to test storage, ordering, and access boundaries; it does not benchmark real embedding quality.