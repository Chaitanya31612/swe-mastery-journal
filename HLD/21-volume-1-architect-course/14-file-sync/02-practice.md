# File sync: versioned metadata and recoverable conflicts — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Offline file sync

One million users, three devices/user, 100,000 changed files/day, 5 MB average new content. Two offline devices can edit the same binary file. Require no silent overwrites, resumable upload, 30-day version retention, and owner sharing controls. Define file/version identities, conditional publication, change cursors, conflicts, and safe cleanup.

## P2 — Delete versus stale editor

Device A deletes a file while offline device B edits an old version and reconnects a week later. A third device renamed the parent folder. Specify the chosen semantics and the metadata/log checks needed; do not conflate rename, identity, and content.

## P3 — Fix bad pseudocode

```text
upload(path, bytes)
metadata[path] = new_blob
notify_devices(path)
```

There is no base version, durable change record, or retry identity. Repair this protocol and explain a crash after byte upload but before metadata publication.

## Delayed gate

Trace concurrent binary edits and a delete/offline-edit conflict. Locate byte completion versus metadata visibility.
