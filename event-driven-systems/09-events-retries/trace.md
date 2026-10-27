## Trace the execution

Receive A1 → fails → choose policy → observe whether A2/B1 may proceed → repair → redrive A1 → verify entity/projection version. Draw the order after every proposed retry design.

Use event_id, key, schema version, topic/partition/offset, attempt, and safe error category in diagnostics. Keep sensitive payloads out of logs.
