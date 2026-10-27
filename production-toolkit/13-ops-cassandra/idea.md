## Understand the idea

Cassandra is a distributed wide-column database with a query-oriented data model. Start from the reads you need.

Partition keys distribute/group data; clustering columns order rows within a partition under the table definition.

Do not port a normalized relational schema and expect arbitrary joins. You may store multiple tables/projections for different reads.

That makes write/update coordination and repair part of the application design.

Keep partitions bounded. A workspace with years of events under one partition can become a hotspot or grow too large.

Time bucketing is one possible strategy, with its own query cost. Consistency levels and replication settings affect the read/write/failure contract; they do not make every cross-row invariant transactional.