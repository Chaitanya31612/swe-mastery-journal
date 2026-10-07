# Unique IDs: clocks, coordination, and order

Learning outcome: Separate uniqueness from ordering and explain allocation, worker identity, clock rollback, and sequence exhaustion.

## Ask what “unique and sorted” means

An ID may need probabilistic collision resistance, centrally enforced uniqueness, approximate time sorting, or strict ordered allocation. These are different contracts. A globally monotonic order across all nodes requires stronger coordination than independent time-based generators. IDs are not access-control tokens merely because their values look random.

Three useful designs are random identifiers with an authoritative collision policy; a centralized or range-leased allocator; and time/worker/sequence identifiers. A central allocator makes uniqueness/order easier to reason about but becomes an availability/throughput dependency. Leasing disjoint ranges reduces per-ID coordination but needs durable allocation and safe reuse rules. Random IDs reduce coordination but size/index locality and exposure have consequences.

## Derive a time-based bit layout

For an illustrative unsigned 64-bit scheme, reserve one bit, use 41 bits of elapsed milliseconds, 10 bits of worker identity, and 12 bits of sequence. This supports 1,024 worker identities and 4,096 IDs per worker per millisecond under the scheme’s assumptions; the time range is about 69.7 years from its chosen epoch. It does not mean the implementation can sustain its bit-space limit.

Compose the fields only after validating time and worker identity. Workers must not share the same identity while active, and restarted workers must not reuse a timestamp/sequence combination already emitted. When the sequence is exhausted in one millisecond, wait for a later safe timestamp, reject/backpressure, or use a different allocation scheme. Masking and wrapping to zero silently creates duplicates.

## Wall clocks can move backwards

NTP synchronization does not prove clocks never regress. A restart, clock adjustment, or VM behavior can make the observed timestamp less than a previous emitted value. Choose fail-stop/wait, persisted monotonic last state with safe restart, or a coordinated alternative. Each changes availability/latency. Fencing and durable worker allocation matter when ownership changes.

Timestamps sort approximately by physical time, not necessarily causality across machines. A per-conversation sequence, log offset, or coordination protocol may be needed for actual application order. Do not use a snowflake-like ID as evidence that all concurrent operations have a globally meaningful sequence.

## Production decision

Measure allocator errors, rollback events, exhausted capacity, duplicate-key rejection, and identity lease health. Evolving epochs/layouts needs a version/compatibility strategy. Choose the smallest guarantee the business requires, and expose assumptions explicitly.

## Retrieve before practicing

Explain a duplicate after restart and distinguish roughly sorted IDs from a strict global ticket sequence.
