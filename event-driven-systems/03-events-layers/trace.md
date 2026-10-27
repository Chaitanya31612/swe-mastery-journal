## Trace the execution

The producer discovers leader endpoints, sends a batch, and receives an acknowledgement under its configuration. A consumer fetches retained records from assigned partitions.

It does not require the producer process to remain alive after durable publication.

When a client cannot connect after initial discovery, inspect advertised listeners/DNS/network/auth for actual broker addresses. When append latency rises, inspect broker/storage/replica health rather than only Rails CPU.