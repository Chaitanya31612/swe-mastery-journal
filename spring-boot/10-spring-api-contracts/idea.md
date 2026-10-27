## Understand the idea

An endpoint contract includes more than a URL. Define allowed input, authorization, response shape, errors, ordering, page limits, and retry semantics.

A list without a bound can turn an ordinary screen into an accidental bulk export.

Use stable ordering for pagination. Offset pages can shift when rows are inserted; a cursor can be more stable for an append-heavy feed.

A cursor must still be scoped to the caller and filter contract.

A retried create can duplicate a ticket. An idempotency key identifies one logical command.

Store the key with a request fingerprint and result under a database uniqueness rule. The same key with a different request should conflict.

A pre-check in a local map does not protect multiple service instances.