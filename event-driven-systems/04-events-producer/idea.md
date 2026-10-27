## Understand the idea

A producer serializes a record and asks a partition leader to append it. Its delivery handle/future reports the result under the client configuration.

Enqueueing into a client buffer is not the same as an acknowledged broker append.

acks, replica/min-ISR settings, retry limits, and delivery timeouts interact. Idempotent producer support prevents certain retry duplicates under the protocol/session contract.

It does not recognize that two separate application calls with different identities mean the same business completion.

Always carry a stable business event ID. In the outbox, retrying the same saved event preserves that ID.

A consumer can then deduplicate the business effect even when the application re-publishes after a crash.

Choose and verify settings for the actual client library; Ruby librdkafka options are not every Java default pasted unchanged.