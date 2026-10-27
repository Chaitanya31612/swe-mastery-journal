## Follow a concrete example

```text
Topic ticket-events
Partition 0: offset 0 [ticket A v1], offset 1 [ticket A v2]
Partition 1: offset 0 [ticket B v1]

Key = workspace_id + ticket_id under a deliberate stable contract.
Value = versioned event envelope.
```
Consumer parallelism is constrained by partition assignment within a group. Adding more consumers than active partitions does not give every member a partition.