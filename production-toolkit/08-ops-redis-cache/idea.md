## Understand the idea

Cache-aside reads a copy if present, otherwise loads from the authority and stores a copy. The hard questions are which values may be stale, for how long, and how a write changes the cached answer.

Include tenant, query, and relevant version dimensions in keys. A TTL limits some stale lifetimes but does not prove immediate revocation or prevent old data being refilled after a race. Permission-sensitive checks may need a fresh authority boundary separate from cached content.

When many keys expire together, requests can stampede the database. Use bounded rebuilds, jittered expiries, request coalescing, and stale-serving policies only where the product allows them. A cache outage should not create unlimited fallback work.
