# Consistent hashing, placement, and migration — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Compute and explain placement

Ring 0–99 has A=15, B=45, C=75. Keys are 5, 20, 40, 60, 90. Add D=30. Compute before/after owners and changed interval. Explain a cache rollout when old/new clients coexist.

## P2 — Durable-store migration

Move an ownership interval while writes continue. Provide a versioned routing/copy/catch-up/cutover/rollback plan. Then change the workload so one key accounts for 40% of requests: identify why additional virtual nodes may not fix it.

## P3 — Repair the proposal

“Hashing guarantees balanced traffic and replication. We select the next three virtual nodes as replicas and delete the old shard as soon as clients learn the new ring.” Identify missing physical/failure-domain and migration safeguards.

## Delayed gate

Place five keys on paper after adding/removing a node, then explain what the hashing function leaves unsolved during live writes.
