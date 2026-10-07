# URL shortener: serving and mutable mappings

Learning outcome: Derive a read-heavy architecture, prevent code collisions, and revise caching when links become editable or revocable.

## Begin with the mapping contract

A shortener owns a mapping from code to target plus owner, lifetime, and policy. Ask whether repeated targets share a code, whether custom aliases exist, and whether targets can be edited/revoked. A public code is an identifier, not proof of authorization for editing. Link safety/abuse is a product concern separate from mapping lookup.

Creation and redirect are different flows. Creation must install an unambiguous mapping durably before returning success. Redirect must resolve a live authorized target within its serving/freshness goal. Expired, deleted, and unknown links have explicit behavior. Metrics collection should not silently change the redirect availability contract.

## IDs and redirects are mechanisms

Random codes require enough space and an authoritative unique-key insert/retry. A sequential allocator encoded in Base62 avoids collisions under its allocation assumptions but introduces coordination and enumeration. Hashing the target can collide and may wrongly merge different owners’ links. Base62 expresses an integer/string in a compact alphabet; it adds neither randomness nor secrecy by itself.

HTTP redirect choices and cache headers affect subsequent traffic and freshness. Do not assume all permanent responses are cached forever or all temporary responses are never cached; explicit response policy and clients/CDNs matter. Immutable mappings permit longer-lived caches; a prompt edit/revocation contract constrains every caching layer, including browser and edge.

## Read-heavy does not mean automatically sharded

Use estimates to identify likely limits. A mapping store indexed by code supports lookup; a cache reduces repeated source reads. Distinct working-set size, key skew, and measured source capacity determine whether caching/replicas/partitioning are needed. A single viral code can overload one key or server even if average traffic is modest.

On a miss, trace source lookup and cache publication. Bound cache-failure fallback. Coalesce misses for popular codes; allow stale serving only if expiry/revocation semantics permit it. If analytics must be exact/durable, define how its event participates in redirect handling and the accepted cost. Best-effort analytics can be decoupled but must be honestly described.

## Evolve without breaking old links

Changing code length/generator or shard placement needs compatible readers and stable existing mappings. Index backfills and additional routing are migration tasks, not just new boxes. Monitor useful redirects, stale/revoked resolutions, creation collisions, miss load, and lookup tail latency. Separate public resolution from owner management authorization.

## Retrieve before practicing

Redesign for immediate revocation and state which cache or availability assumptions must be surrendered.
