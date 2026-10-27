## Understand the idea

S3 stores objects addressed by bucket and key. A slash in a key is a naming convention, not a filesystem directory with ordinary POSIX behavior.

Keep application metadata and access rules in the database; the object is the bytes.

Use private defaults and a workload role scoped to the required bucket/prefix/actions. A presigned URL grants time-limited access using the signer’s permissions.

It can be reused while valid and may expire earlier when its credentials expire. It is not inherently a single-use ticket.

Setup: choose a unique training bucket/region, block unintended public access, choose encryption and lifecycle/versioning deliberately, scope the app role, configure CORS only for required browser direct-upload behavior, then test an allowed upload/read and denied outside key.

Plan cleanup of abandoned uploads and retained versions.