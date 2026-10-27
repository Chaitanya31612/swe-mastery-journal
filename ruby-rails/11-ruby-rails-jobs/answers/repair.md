# One valid repair

Use a unique logical event key and durable job/outbox state. Claim local work with a database-safe operation.

Send with a stable remote idempotency key if supported. A crash after provider acceptance but before local acknowledgement can still duplicate without that support; reconcile or tolerate duplicates explicitly.

**How to check:** Jobs cross a time/process boundary. Simple serialized arguments and deliberate reload behavior make that boundary clearer.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test.

Code length and matching keywords are not evidence.