## Trace the execution

Producer chooses key → partitioner selects partition → leader appends record → offset identifies its position → assigned consumer processes that partition. Two partitions can advance at different speeds.

Draw A1/A2 in one partition and B1/B2 in another. There is no single cross-partition order you can infer merely from their offsets.