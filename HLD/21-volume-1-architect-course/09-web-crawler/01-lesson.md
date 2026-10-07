# Crawler scheduling, bounded exploration, and safe fetching

Learning outcome: Design a restartable frontier with per-host policy, explain deduplication limits, and protect the fetch boundary.

## Crawling is scheduling under constraints

Clarify discovery versus recurring refresh, allowed destinations, content types, depth, storage, freshness, and per-host policy. A crawler cannot safely “follow every link forever”: calendars, session URLs, redirects, huge bodies, and duplicate content create unbounded work. Define budgets for domains, paths, depth, redirects, bytes, and retries.

Maintain a durable frontier of discovered URLs and scheduling metadata. Separate selecting eligible work from downloading, parsing, deduplicating, storing, and rediscovering links. Assign host ownership or coordinate per-host schedules so distributed workers do not independently violate a host limit. Priorities can consider freshness/value, but starvation and fairness need a policy.

## Two different duplicate problems

URL normalization decides whether two strings refer to the same crawl target under chosen rules. Dropping arbitrary query parameters can incorrectly merge distinct resources. Content fingerprints detect equal or similar retrieved content, a separate question. A probabilistic Bloom filter can reject some unseen URLs as duplicates; use it only if the loss is acceptable or verify positives in exact state. A visited check then insert must be atomic enough for the chosen duplicate-work contract.

## Trace the restartable flow

Scheduler claims a URL with a lease → downloader checks destination/host policy → fetch with deadlines/size/redirect limits → persist content and fetch metadata → parse links → publish new frontier entries → mark completion. Crashes can repeat work; use stable fetch/task identities and replay-safe storage. Lease expiry can overlap slow old workers; fencing/versioned completion prevents stale workers overwriting newer results.

Respect robots exclusion for the crawler agent and handle retrieval/cache/error behavior explicitly. It is a protocol for crawler behavior, not permission to bypass authentication or a legal authorization mechanism. Scope this course to permitted public sources or your own controlled test pages.

## User-controlled destinations are a trust boundary

A server fetching arbitrary URLs can reach internal services or cloud metadata unless protected. Validate destinations after DNS resolution and across redirects, reject disallowed schemes/networks, and enforce egress policy. DNS rebinding/redirect changes mean checking only the original string is insufficient. Sandbox parsing and cap decompression/body sizes.

## Capacity and operation

Estimate fetches/s, mean bytes, concurrency from service time, and host-specific limits. A queue can contain vast work while individual hosts remain intentionally slow. Measure frontier age by priority, per-host rejection/rate, fetch latency/error, unique-content ratio, and bytes. Scale download/parse/store separately only when the measured limit justifies it.

## Retrieve before practicing

Explain why per-host scheduling, duplicate content detection, and URL identity are three different problems.
