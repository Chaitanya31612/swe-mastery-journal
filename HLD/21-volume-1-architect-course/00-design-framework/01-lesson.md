# The bare bones of a defensible HLD

A system design is an argument: **given this contract and workload, these mechanisms preserve the required behavior at an acceptable cost**. A diagram is part of the argument, not its conclusion. Begin with the user action and the property that must remain true.

Remember seven verbs: **Contract → Size → Model → Flow → Stress → Operate → Explain**. These organize thinking; they do not prescribe components. They expand the book’s scope/proposal/deep-dive/wrap-up stages into concrete evidence you can produce.

## 1. Contract: what are we promising?

Ask who uses the service and which two or three actions matter. Define excluded scope. Clarify correctness, freshness, latency, availability, and durability only where they change choices. An invariant is a statement that must remain true across execution, such as “one short code does not refer to two live targets” or “retrying a send does not create a second logical message.”

For a latency goal, specify the operation and measurement boundary. “p95 redirect lookup below 100 ms inside our region” differs from a globally observed browser redirect time. For durability, distinguish accepted work from completed effects. For availability, define what useful success means instead of counting any HTTP 200.

If the interviewer provides no answer, choose and record an assumption. Do not silently invent a requirement. “I’ll assume one region and eventual feed freshness within 30 seconds; stronger freshness would change the projection design.”

## 2. Size: which quantity constrains us?

Estimate operation rates, peak factors, stored objects, retention, bandwidth, or live connections **only when they influence design**. Keep units on every intermediate value. Separate user actions from database operations: one page view can trigger many queries. State the uncertain input.

The useful conclusion is not “11,574 QPS.” It is “reads dominate; we need a serving path whose cache failure does not push the entire peak directly into a smaller database.” For chat, active sockets and per-connection memory may matter more than message QPS. For video, bytes delivered dominate API calls.

## 3. Model: what state and contracts exist?

Define the important API, entities, access patterns, identity/ownership, and source of truth. Identify the atomic boundary. Choose a storage model from the access pattern and required guarantees, not because the company uses a fashionable database.

List a few queries: lookup code; append message; fetch messages after cursor; resolve file version. A schema and key that cannot efficiently serve those operations need another index, projection, or different model. State which data can be rebuilt and which must not be lost.

## 4. Flow: does one real request work?

Start with the simplest viable deployment: client → application → durable store. Add a component only after naming the constraint it resolves. Draw both a state-changing flow and a read/background flow. Label requests, data, and success acknowledgment.

For a send operation: authenticate, validate, assign/deduplicate identity, persist, acknowledge, then deliver asynchronously if the contract permits. “Use Kafka” is not a flow; explain who produces, when, what happens after a crash, and where the durable state lives.

## 5. Stress: what is most likely to break the contract?

Choose at most two deep dives. Prioritize a problem-specific correctness risk and the dominant capacity/failure risk. Use small counterexamples before discussing a million nodes: two concurrent writers, a response lost after commit, a hot key, a stale replica, or a network partition.

For each: trace the race/failure → identify violated property → select a mechanism → state its assumptions → acknowledge its downside. A lock inside one application process cannot coordinate four instances. A database transaction does not automatically protect state held in another system. A retry without an identity can repeat effects.

## 6. Operate: how will we know and recover?

Choose a user-facing SLI, target, alert/response, and one component metric confirming a suspected bottleneck. Consider authorization, sensitive data, abuse, retention, and the main cost driver. Define degraded behavior and recovery. Add migration/rollout/rollback reasoning for senior-level depth.

For a notification system, oldest undelivered-event age can matter more than worker CPU. For sync, recent-version availability and conflict/error rates matter. An alert should lead to a specific action; “add monitoring” is incomplete.

## 7. Explain: what did we choose and leave unresolved?

Summarize the main choice, alternative, accepted downside, next limit, and verification required before production. “I chose async projection because 30-second freshness is acceptable; it lowers write-path coupling but needs replay and lag monitoring.” Be willing to change the choice when the contract changes.

## Time and thinking-space control

For a 45-minute round: Contract 0–6; Size 6–10; Model 10–16; Flow 16–26; Stress 26–37; Operate 37–42; Explain 42–45. Adapt these times to the discussion; keep enough time for flows and the main risk.

Before drawing, select a dominant family: **lookup/read-heavy; contention/correctness; async pipeline; live interaction; derived index/fan-out; large objects/synchronization**. Then shortlist questions appropriate to that family. A reservation deep dive is concurrency; an autocomplete deep dive is serving/index freshness; a crawler deep dive is bounded scheduling and destination safety. Do not design every family simultaneously.

Under uncertainty, say: “I don’t know the product limit; I would measure X. The required property is Y, so the mechanism must provide Z.” This keeps reasoning moving without invented guarantees.

## Self-explanation before proceeding

Cover this page. Name the seven verbs and explain the artifact produced by each. Then explain why a component list cannot show durable acceptance, correct concurrent behavior, or justified complexity. Continue to the teaching examples only after trying this retrieval.
