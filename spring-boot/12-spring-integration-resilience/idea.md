## Understand the idea

A remote call crosses a failure boundary. The provider can reject, respond slowly, complete and lose the response, or return malformed data.

A timeout says you did not get an answer in time; it does not prove no side effect occurred.

Choose connection/response timeouts and an overall request budget. Limit attempts and use backoff with jitter where appropriate.

Retry only failures and operations whose semantics allow it. A circuit breaker can stop repeated pressure on a failing dependency; it does not repair correctness or replace a timeout.

Keep an adapter around the provider so your use case works with a small result contract.

Record correlation ID, logical command key, attempt number, duration, and outcome category without logging secrets or whole payloads.