# File sync: versioned metadata and recoverable conflicts — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Versioned publication

Raw new bytes are about 500 GB/day decimal; 30 days of fully retained changed versions would be 15 TB before deduplication/copies/metadata. Use stable file IDs, immutable content/version records, expected base version, and scoped operation identities. Resumable sessions record verified parts/complete objects. Conditionally commit metadata plus durable change intent; the losing concurrent binary editor keeps a conflict copy or receives an explicit conflict. Do not silently select a winner while claiming no overwrite.

Devices consume ordered changes after durable cursors and can resync from snapshots if history expired. Authorization is checked across tenant/owner/share boundaries. Orphan cleanup waits for active sessions and version references; byte upload alone does not make the new file visible. Deduplication is optional and needs a privacy/integrity policy.

## P2 — Explicit conflicts

Represent deletion/tombstone as a versioned state. B’s stale base no longer matches, so its commit conflicts; preserve user data as a conflict copy or require an explicit restore action. A rename changes parent/path metadata for the stable file identity, not the content identity itself. Apply the parent relationship/access rule under an atomic boundary; replay changes consistently. Your exact restore/conflict UX can vary, but stale edits must not silently resurrect a deleted file under the stated contract.

## P3 — Repair and recovery

Upload immutable bytes under a session/version identity and verify. In a local atomic metadata transition, verify authorization/base version, install references, and record a replayable change. Lost response retries return the recorded result. A crash before publication leaves an orphan/in-progress object recoverable by session retry or later safe collection; notifications may repeat or be lost because durable changes/cursors are the catch-up authority. A path-only blind assignment cannot detect concurrent edits or renames.

## Checkpoint explanations

1. **D.** D detects a changed base. A/B/C do not arbitrate metadata versions.

2. **A.** A persists observable changes. B/C/D do not reconstruct missed updates.

3. **B.** B protects active/retained content. A/C/D can delete bytes needed by current or future publication.

4. **C.** Hashes are not version arbitration or permissions. A/B/D require other policies/mechanisms.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
