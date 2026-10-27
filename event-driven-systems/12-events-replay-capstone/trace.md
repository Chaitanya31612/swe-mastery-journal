## Trace the execution

Choose rebuild purpose → validate retained/backfill source → create isolated projection identity → replay → compare to authority/expected fixtures → switch reads → monitor → retire old state under retention policy.

For restore, draw the timeline of DB state, outbox marks, Kafka retained records, group commits, and inbox/projection state. Recovery is a reconciliation problem across those boundaries.