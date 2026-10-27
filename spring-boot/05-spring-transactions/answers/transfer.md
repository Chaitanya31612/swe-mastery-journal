# One valid adaptation

Write an outbox row with the business change in one DB transaction. A worker retries sending it. The provider may accept a message before a timeout, so retries still need an idempotency strategy or duplicate tolerance. Outbox guarantees saved intent, not universal exactly-once delivery.

**Explain back:** The wrapper must see the call. What changed in the new condition? What would make your answer fail?
