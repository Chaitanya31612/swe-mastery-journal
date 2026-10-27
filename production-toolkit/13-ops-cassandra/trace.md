## Trace the execution

Query need → partition key scope → bounded partition → within-partition order → replicas/consistency → result. Then trace the writes needed for a second access pattern and how projections are repaired.

Measure partition size/skew and the cost of fetching a range across buckets. A query that requires broad filtering may signal a mismatched model.