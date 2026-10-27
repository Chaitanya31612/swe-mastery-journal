## Understand the idea

A service object is ordinary Ruby. It earns its place by naming one use case and making its boundary clear. It does not automatically supply permissions, a transaction, retries, or thread safety.

Choose a result contract. A business rejection such as “already closed” can be an expected result. An unexpected database or programmer error should remain visible to monitoring. Do not rescue everything into nil; callers then cannot tell rejection from failure.

State who owns the transaction and which side effects happen later. Keep request-specific data in arguments and local values. Class-level mutable state can leak across calls or threads.
