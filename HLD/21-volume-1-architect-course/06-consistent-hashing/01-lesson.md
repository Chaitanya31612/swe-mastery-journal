# Consistent hashing, placement, and migration

Learning outcome: Compute ownership and changed placement, distinguish distribution from replication, and preserve reads during migration.

## Placement is a mapping, not a database

Naive `hash(key) mod server_count` can remap many keys when the count changes. A consistent-hash ring puts node positions and key hashes in a shared circular space; each key belongs to the next node clockwise. Adding a node changes ownership of one interval rather than recomputing all modulo assignments. Expected movement depends on placement/distribution assumptions, not an absolute guarantee for every dataset.

On a ring 0–99 with nodes A=10, B=40, C=80, key 5 belongs to A, 20 to B, 60 to C, and 90 wraps to A. Add D=30: keys in the interval (10,30] move from B to D; the rest retain owners. All clients must agree on a versioned membership view or route through a coordinator with that responsibility.

## Virtual nodes and physical independence

Give each physical server multiple ring positions to average uneven intervals or weight capacity. Choose replicas on distinct physical/failure-domain owners, not merely the next three virtual positions that could belong to one box. Virtual nodes do not eliminate skewed access: one extremely hot key still maps to a bounded set of owners.

Alternative placement schemes include rendezvous hashing and fixed logical partitions assigned to physical servers. Fixed partitions can make migration units explicit. Select from movement cost, operational visibility, heterogeneous capacity, and consistency requirements.

## Membership changes require a data protocol

For a cache, changed ownership produces misses and rewarming. For a durable store, it requires migration, reads during movement, writes/routing version handling, and safe cutover. A ring algorithm by itself neither copies data nor prevents lost updates. Introduce a migration epoch, transfer snapshot plus concurrent changes or another suitable mechanism, reconcile, and switch ownership only after verification. Rollback needs compatible routes and retained source data.

Health detection has uncertainty: a timeout does not prove a node is permanently dead. Removing ownership aggressively can cause churn or double writers. Coordinate membership/fencing according to the store’s correctness contract.

## Hot keys and observability

Measure per-owner load, bytes moved, cache miss spikes, migration backlog, and routing-version errors. A hot key might need replicated read serving, request coalescing, a special partition strategy, or rate limits. Adding more owners helps a distribution of keys; it does not automatically divide a single key’s serialized writes. Explain the physical bottleneck separately from hash-space balance.

## Retrieve before practicing

Place five keys on paper after adding/removing a node, then explain what the hashing function leaves unsolved during live writes.
