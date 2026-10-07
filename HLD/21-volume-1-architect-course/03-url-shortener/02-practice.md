# URL shortener: serving and mutable mappings — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Editable short links

Two million links/day, 400 million redirects/day, 5× peaks, 18-month retention, and 600 bytes/mapping before overhead. Owners may change targets; edits/deletions must be visible within ten seconds. Design creation, resolution, and update flows including collisions, cache failure, HTTP cache policy, and analytics whose loss is acceptable.

## P2 — Private expiring document links

Transfer the mapping design to document-download links with one-hour expiry and owner revocation within two seconds. Explain what must change if you previously allowed shared/public caches. Clients must not receive another owner’s object.

## P3 — Bad design review

“Take the first six characters of a target hash, check the cache for absence, insert, then permanently cache redirects. Later we can support edits by deleting Redis.” Identify distinct errors and repair the mechanisms.

## Delayed gate

Redesign for immediate revocation and state which cache or availability assumptions must be surrendered.
