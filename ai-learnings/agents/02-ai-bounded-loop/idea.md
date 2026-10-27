## Understand

Treat an agent run as a state machine.

It receives a task and context, asks a model for a proposal, validates a tool call or final answer, executes approved work, records the observation, and either continues or stops.

Every transition needs an owner.

Bound steps, elapsed time, tokens/cost, tool outputs, and simultaneous work. Decide what happens when the limit is reached: partial result with evidence, clarification, fallback, or failure.

Do not let “keep trying until solved” become an unbounded production loop.

Store useful observations, not unrestricted hidden reasoning. A short user-facing explanation of decisions is different from exposing a model's internal chain of thought.

Debug by tool proposals, policy decisions, supplied evidence and outcomes.