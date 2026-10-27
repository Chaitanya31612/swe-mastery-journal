# Follow the execution

Trace enqueue → delayed start → load current row → attempt external effect → timeout → retry. The timeout does not say whether the provider accepted the action. Reusing the same logical key lets a supporting provider deduplicate it.

For a cache, trace miss → compute → store → hit → underlying update → expiry/invalidation. Record what maximum staleness the user can accept. A permission decision should not use an indefinitely stale shared cache.
