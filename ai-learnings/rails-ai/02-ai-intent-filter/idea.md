## Understand

Natural language can be ambiguous. A model can propose status and depot_name; application code decides whether those fields are supported and resolves names within the actor's scope. Never let the model choose tenant identity, arbitrary column names, joins or SQL.

Use explicit result states: accepted filter, needs clarification, unsupported request, or unavailable model. Show the applied fields in human-readable chips. If there are two permitted depots called East, ask which one. Do not resolve ambiguity by searching all tenants.

The filter object should define its own validation and query conversion. That keeps model output away from ActiveRecord internals and makes the same filter usable through a manual form. Test language interpretation separately from deterministic filtering.
