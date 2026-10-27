## Understand

An agent framework can provide tool registration, state graphs, retries, tracing or persistence. It can reduce wiring, but it can also hide control flow and defaults.

Start by drawing the underlying state machine and identifying which guarantees the framework actually supplies in the selected version.

Multiple agents can divide work by expertise, source or independent review. They also add context handoffs, correlated errors, coordination cost and a larger capability surface.

Two models agreeing is not independent proof if both saw the same bad evidence. A reviewer agent needs a rubric and authority limits too.

Keep shared state typed and provenance-aware. Do not pass every private context field to every agent.

Bound delegation depth, fan-out, time and cost. Compare a single-agent or deterministic workflow baseline on the same held-out tasks before adopting the extra machinery.