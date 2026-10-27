## Understand the idea

Lag is a progress difference, not a complete user-impact measure. A small lag can contain very old important work; a large lag can drain quickly.

Observe oldest unprocessed age, processing rate, errors/retries, and backlog growth as well.

Group membership changes and poll/processing behavior can trigger rebalances. An assignment change means a new process may own a partition and replay uncommitted work.

Long processing, insufficient polling, and uncontrolled parallelism can interact with the client’s liveness contract.

Retention limits available history. A consumer offline beyond it needs a rebuild/backfill source.

Compaction is a different policy from keeping every event forever: key/tombstone/latest-value behavior must fit the topic’s purpose. The lab uses delete-retained event history for clarity.