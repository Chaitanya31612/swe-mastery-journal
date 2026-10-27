# The idea

A background job runs later and may run more than once. Pass small JSON-friendly arguments, usually IDs, rather than whole model objects.

The row may have changed or disappeared before the worker starts.

Sidekiq 5 uses include Sidekiq::Worker for a direct worker. Modern Sidekiq examples can use newer APIs; keep that version difference visible.

A successful enqueue is not proof that work completed. Monitor queue latency, retries, and terminal failures.

Idempotent means repeating the same logical command does not create another logical effect. A seen? pre-check can race.

Use a database uniqueness rule for local effects and a stable provider idempotency key when the remote API supports it. A cache stores a copy; define its key, expiry, and invalidation.

Tenant/user context may belong in the key.