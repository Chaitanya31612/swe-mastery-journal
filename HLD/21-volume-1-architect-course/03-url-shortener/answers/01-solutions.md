# URL shortener: serving and mutable mappings — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — One defensible design

Creation averages about 23.1/s; redirects 4,630/s. Peaks are about 116 creates/s and 23,150 redirects/s. Using an explicit 30-day month assumption, raw retention is `2e6 × 540 × 600` = 648 GB before indexes/copies. Different calendar-month modeling changes this slightly; state it.

Use an owner-authorized mapping API and durable unique code key, with random candidate generation and insert/retry or a correct allocated-ID scheme. Store version/expiry/deletion state. Serve from bounded caches only under the ten-second freshness contract; propagate invalidations or use version/freshness checks and TTLs whose worst-case behavior is explained. Client/edge policies must not bypass revocation. Best-effort analytics can drop during outage without blocking useful resolution. Plan DB fallback admission and popular-key coalescing. No estimate proves compulsory sharding; validate the selected store and cold-cache peak.

## P2 — Different contract

Authenticate/authorize the link issuer and object access, use an opaque token, enforce expiry/revocation at an authoritative policy boundary, and avoid caching private content across users without a valid isolation policy. A direct presigned object URL can remain usable for its authorized lifetime unless another mechanism revokes it; that may conflict with two-second revocation. A gated download/proxy or very short-lived object token has different latency/cost consequences. Never claim secrecy solely from Base62.

## P3 — Repair

Truncated hashes collide; cache absence is neither durable uniqueness nor safe under concurrency; permanent caching conflicts with prompt edits; deleting Redis does not purge all client/CDN caches and can race with stale fills. Enforce unique insertion in durable truth, choose adequate code space, record ownership/lifetime, and design freshness end to end. If immutable links are a deliberate alternative, remove edit promises instead of claiming both.

## Checkpoint explanations

1. **C.** Encoding expresses a value. A/D require other mechanisms; B depends on generation/storage constraints.

2. **D.** A shared unique constraint arbitrates concurrent insertion. A/B race; C reduces probability but does not arbitrate.

3. **A.** Stale resolution can bypass policy. B/C/D do not enforce revocation.

4. **B.** Miss load reaches the source. A ignores failure; C amplifies it; D may violate freshness and is not controlled capacity.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
