## Understand the idea

A Kafka topic is split into partitions. Each partition is an ordered append log with offsets. Offset 10 in partition 0 is unrelated to offset 10 in partition 1; it is not a global event number.

A record key helps the partitioner place related records together under a stable configuration. Using ticket identity as the key can keep that ticket’s records on one partition. It does not order all tickets globally. A single very hot key can limit useful parallelism.

Adding partitions can change key-to-partition mapping. If per-entity ordering matters across such a change, plan migration/transition semantics rather than assuming the old placement stays unchanged. Also keep application version/sequence checks when events can be retried or produced through several paths.
