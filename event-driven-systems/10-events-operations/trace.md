## Trace the execution

Missing report → locate outbox event → publication result → topic/partition record → group committed progress → inbox row → projection. The first missing boundary narrows the investigation.

For slow work, compare producer rate, consumer processing time, DB wait, hot partitions, and rebalance frequency. Adding partitions/consumers changes contracts and is not always the smallest repair.