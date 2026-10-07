# Autocomplete: derived indexes, top-K, and fresh snapshots

Learning outcome: Separate ingestion from serving, choose a prefix access structure, and evolve versioned results with privacy/freshness controls.

## Define matching and freshness

Autocomplete might return popular prefix completions, fuzzy matches, personalized results, or tenant-private names. These are different access/ranking contracts. Specify prefix length, top-K, language/normalization, latency measurement, freshness, removal, and authorization. Returning five global popular terms is simpler than per-user fuzzy ranking.

## Two planes: build and serve

Ingestion records eligible query/content events, normalizes strings, aggregates scores/windows, applies policy, and builds a serving index. Serving resolves a prefix and returns ranked allowed results with minimal request-time work. Do not update every serving replica synchronously for every keystroke unless the freshness contract requires and capacity supports it.

A trie expresses shared prefixes; caching top-K at nodes avoids scanning the entire matching subtree at read time. It costs index memory and update/rebuild work. Sorted ranges/FST-like compact indexes or appropriate database/search indexes are alternatives. A relational prefix query can be viable at smaller scale; “never use SQL” is not a reasoning rule. Fuzzy matching is additional scope, not automatically solved by a basic trie.

## Versioned publication and hot prefixes

Build immutable index versions, verify them, then atomically switch serving to a version and keep a rollback copy. Readers should not observe half-built state. Hot short prefixes benefit from replicated/cacheable result serving when the policy allows it. Estimate memory from strings/nodes/top-K payload and actual sharing, not from query count alone.

Freshness creates a batch/stream trade-off. Hourly rebuilds can satisfy an hourly popularity goal but not urgent removal of private/unsafe results; a fast deny/filter path can override the snapshot. Different tenants/users require isolation-aware keys and authorization, not one public cache entry per prefix.

## Client races and observability

The user types `ca`, then `cat`; a slower response for `ca` may arrive later and replace the current suggestions. Tag requests with sequence/input identity and discard obsolete responses. Server index consistency does not prevent this UI race.

Measure p95/p99 serving latency, index age, build/publish failures, hot-prefix load, blocked-result leakage, and relevant quality metrics. Minimize/private-query retention and avoid publishing individual sensitive searches as globally popular suggestions. Roll out normalization/ranking changes with controlled evaluation and compatible clients.

## Retrieve before practicing

Compare batch freshness with emergency removal. Explain why client response order and server index publication are separate mechanisms.
