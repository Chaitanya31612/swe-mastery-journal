## Understand

A deadline should cover the user-visible operation, not only one network call. A run may include retrieval, multiple model calls, tool work, validation, and retries. Layering SDK retries inside job retries inside agent retries can multiply cost and delay.

Classify failures. Authentication and invalid-schema errors usually need a configuration/code repair. Rate limits and transient connectivity may justify bounded backoff with jitter. A timeout after a side-effect request can mean the effect happened but its acknowledgment was lost. Do not blindly repeat it.

Set attempt limits and a remaining time/cost budget. Honor provider retry guidance when applicable. Protect shared capacity with concurrency limits and a circuit breaker or fallback policy. Cancellation of a browser request does not prove that provider work or an external write stopped.
