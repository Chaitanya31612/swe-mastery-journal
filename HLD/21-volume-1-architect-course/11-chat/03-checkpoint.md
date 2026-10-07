# Chat: durable acceptance, live delivery, and reconnects — checkpoint

Select one option, explain your choice, and reject one tempting alternative. No answer key is included here.

1. WebSocket success proves what?
   - A. Durable history
   - B. Recipient has read
   - C. Global order
   - D. A transport action, not all delivery/durability states

2. A lost acceptance response is safely retried using what?
   - A. A stable scoped request identity with durable deduplication
   - B. A new ID every retry
   - C. Only a sender-local lock
   - D. Presence TTL

3. Presence after abrupt power loss is usually what?
   - A. Instant perfect truth
   - B. An approximation inferred by heartbeat/expiry
   - C. A transaction receipt
   - D. Always permanently online

4. 500,000 connections with modest message QPS still require analysis of what?
   - A. Only database row count
   - B. Only ID characters
   - C. Connection memory/buffers and reconnect behavior
   - D. Only CPU average

