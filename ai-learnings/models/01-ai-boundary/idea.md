## Understand

Start with a normal software boundary: input, output, failures, and an owner. An LLM predicts a useful continuation from the context it receives. It can turn a vague request into a proposed intent or explain supplied facts. It does not automatically know your database, current user, permissions, or whether a rule is true.

Keep exact work in code. A warehouse report can let a model interpret “late parcels at the east depot.” Code resolves the depot, validates the filter, scopes the query, and counts the rows. The model can describe those results. It does not need permission to write SQL or change a shipment.

Think in three boxes: **model proposes → code checks → application decides**. Some features need only deterministic code. Use the model where varied language or unstructured material makes it useful. Define a no-model path at the same time.
