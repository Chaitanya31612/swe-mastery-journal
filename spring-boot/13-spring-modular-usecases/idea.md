## Understand the idea

A use case names an action, such as AssignTicket. It receives validated intent and a trusted actor, checks the rule, coordinates persistence, and returns a result.

A controller translates HTTP into that action. A scheduled job can call the same use case through a different entry point.

Put rules near the data and behavior they govern. Do not let a REST controller become the only place ownership is checked if a job or another controller can bypass it.

Keep adapters small around SQL and remote services when those boundaries need independent tests.

More interfaces do not automatically mean better architecture. Use a seam when it reduces a real coupling or gives a useful test/failure boundary.

Start with a modular monolith when independent deployment is not needed; a network adds partial failure and operations work.