# Video delivery: control plane, data plane, and processing

Learning outcome: Separate media bytes from metadata, publish only ready renditions, and reason about bandwidth, retries, CDN policy, and cost.

## Narrow “video platform”

Begin with upload, processing, and on-demand playback. Comments, recommendations, live broadcast, DRM, and advertising are separate scope choices. Specify upload sizes, resumability, time-to-ready, playback startup/rebuffering, visibility, and deletion. A low-latency metadata API does not establish smooth playback.

Separate the control plane (identity, authorization, metadata, job status, manifests) from the data plane (large object upload/download). Authorize an upload session and issue a bounded object-transfer capability, or proxy bytes if a requirement warrants it. Presigned URLs allow specific authorized operations within their policy/lifetime; they are bearer capabilities, not perpetual public links.

## Upload → process → publish

Create an upload session with owner, expected identity/size/type constraints. Upload chunks/parts to object storage, resume/retry, verify completion/checksum, then mark source ready and enqueue durable processing intent. Jobs may probe, transcode renditions, extract thumbnails, and package segments. Model dependencies as a DAG: later publication depends on successful verified outputs, not merely task scheduling.

Use job/output version identities so retries do not publish competing partial media. Workers can write immutable outputs, then atomically publish metadata/manifest references once the chosen rendition set is ready. Failed jobs leave visible processing/failure state, not a broken “ready” URL. Retain replay inputs within a defined policy; clean abandoned uploads and partial outputs safely.

## Playback and bandwidth

Player obtains an authorized manifest and retrieves selected segments through an appropriate CDN/object path. Adaptive bitrate selects renditions from network/player behavior; codec, container, and transport packaging are different concepts. A cached manifest must not outlive private-access/deletion guarantees accidentally.

`egress bits/s ≈ concurrent viewers × chosen mean bitrate`. At 50,000 viewers averaging 3 Mb/s, delivery is about 150 Gb/s before overhead. Transcoding/storage cost depends on uploaded duration, rendition multiplication, codecs, and retention. QPS at the metadata API cannot size media delivery.

## Failure, privacy, and evolution

CDN misses can load origin; signed/private content requires cache-key/access policy that does not leak between users. Track startup delay, rebuffering, processing age/failure, rendition availability, and origin/CDN bytes. Rate-limit upload and isolate parsers/transcoders from untrusted files. Roll out new rendition/manifest versions with old player compatibility and rollback. Resilient playback may use degraded available renditions only when the contract permits it.

## Retrieve before practicing

Trace upload-to-ready and identify the durable intent and publication boundary. Recompute egress when bitrate doubles.
