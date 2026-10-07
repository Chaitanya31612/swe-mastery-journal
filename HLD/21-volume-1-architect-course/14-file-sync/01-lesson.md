# File sync: versioned metadata and recoverable conflicts

Learning outcome: Separate blob upload from metadata commit, handle concurrent edits/deletes, and synchronize devices with replayable cursors.

## File identity is not a path string

Clarify upload/download, folders, rename/move, offline edits, sharing, conflict behavior, history retention, and deletion. A stable file ID avoids treating a rename as an entirely unrelated blob. Metadata owns name/parent, owner/access, current version, and references to immutable content; object storage owns bytes.

## Bytes first, atomic version publication second

Create a scoped upload session, transfer/verify chunks or the whole object, then conditionally commit metadata against the expected base version. This is an optimistic compare-and-set: update only if the stored version still matches the client’s base. A losing editor gets a conflict, preserves a conflict copy, or merges under domain semantics. Binary files cannot be arbitrarily text-merged safely.

Retry a commit with a stable operation identity so a lost response does not create a second version. Incomplete/unreferenced blobs can be collected only after a safety window and reference verification; never delete objects still used by retained versions or in-flight publication.

## Chunking has trade-offs

Fixed-size chunks simplify implementation but an insertion near the beginning can shift many boundaries. Content-defined chunks can improve reuse under edits but add complexity. Hash fingerprints identify candidate equality; verify integrity and avoid cross-tenant deduplication leaking possession/existence of private content. Chunk references and checksums must be durable enough for version reconstruction. Resumable uploads require a session/part identity and a completion protocol, not just retrying the whole file blindly.

## Change log and device catch-up

Record versioned changes/tombstones in a durable ordered change log scoped to the relevant tenant/user. Devices request changes after a cursor; notifications only indicate that changes may exist. If a cursor predates retained history, require a snapshot/resync. Replayed changes must apply idempotently. Deletes must not be silently undone by an offline stale writer; its base version/deletion state must be checked.

Rename/move conflicts concern metadata relationships and authorization, not only byte hashes. Parent-folder moves can affect paths and sharing; define whether access inherits and how cycles are prevented. Concurrent operations need a chosen transaction/ordering boundary.

## Operate and evolve

Measure sync lag, conflict rate, cursor resets, upload failures, missing chunk references, and restore success. Test offline-to-online recovery, lost commit responses, concurrent delete/edit, and garbage collection. A retention policy is part of the product contract. Encrypt/protect content and scope permissions at upload, commit, and download. Roll out metadata/log schema versions with compatible clients.

## Retrieve before practicing

Trace concurrent binary edits and a delete/offline-edit conflict. Locate byte completion versus metadata visibility.
