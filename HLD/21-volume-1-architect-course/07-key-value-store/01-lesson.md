# Distributed key-value stores and honest consistency claims

Learning outcome: Trace durable read/write paths, explain replicas and quorum assumptions, and reason about partitions, conflicts, and repair.

## State the API and consistency contract

A key-value service exposes `put(key,value)` and `get(key)`, perhaps delete and conditional compare-and-set. Value size, retention, workload skew, and expected read freshness matter. A profile store tolerating stale reads differs from an inventory authority requiring serialized conditional changes. Do not promise the latter merely because the service has three replicas.

## Local durability and serving mechanics

A storage engine can append a write-ahead log before acknowledgment, buffer state in memory, and flush indexed sorted files/pages later. Recovery replays durable state; compaction controls storage/read amplification for suitable engines. The acknowledgment’s durability depends on flush/replication policy. “Written in RAM” is not durable under power loss. LSM/B-tree choices trade write/read/space costs; they are not universal winners independent of workload.

Partitioning places keys; replication keeps copies. A coordinator sends operations to the chosen owners. Leader-based replication can serialize operations through a fenced authoritative leader and replicate to followers; read routing determines freshness. An availability-oriented multi-writer model can accept divergent versions during partition and needs reconciliation.

## Quorum overlap is a useful condition, not a full proof

**Eventual consistency** permits temporary disagreement and aims for convergence when updates stop and repair succeeds. **Read-your-writes** is a session guarantee: later reads by that client include its acknowledged update, under the chosen session/routing model. **Linearizability** makes each operation appear atomic at a point between its invocation and response, respecting real-time order. **Serializability** makes committed transactions equivalent to some serial execution; it does not by itself assert that serial order follows real time. Name the guarantee you actually need.

During a network partition, a service cannot simply promise both always-successful responses on all sides and one linearizable shared state for conflicting operations. Choosing to reject some operations can preserve safety. Choosing available multi-writer updates requires a conflict/convergence policy. This is a statement about behavior under partitions, not an instruction to label every database permanently “CP” or “AP.”

With N designated replicas, requiring W write acknowledgments and R read responses such that R+W>N makes those designated sets intersect. The intersection alone does not define version selection, concurrent-write ordering, durable acknowledgments, membership changes, sloppy quorums, or a linearizable read/write protocol. A complete guarantee requires those mechanics. State precisely whether the proposed service offers eventual consistency, session guarantees, or stronger ordering.

For N=3, W=2, R=2, loss of one replica can still permit these operations if the remaining replicas and protocol satisfy the contract. A two-versus-one network partition changes which operations can proceed under different consistency choices. Refusing a write to preserve a strong invariant is different from accepting writes everywhere and later merging.

## Divergence and repair

Version metadata can detect ordering/concurrency according to its model. Vector-like version information can identify concurrent branches, but the application must define a merge or conflict response. Last-write-wins based on physical clocks can discard concurrent effects. Hinted handoff, read repair, or background anti-entropy reduce divergence; each depends on retention, membership, and repair completion.

Monitor replication/repair lag, unavailable operations, stale reads, tombstone/compaction pressure, and hot partitions. Backups protect deletion/corruption scenarios replication can propagate. Explain what success means after a node failure and how the system restores its intended replica count.

## Retrieve before practicing

State what quorum overlap proves and what it does not. Trace stock decrement under a two-versus-one partition.
