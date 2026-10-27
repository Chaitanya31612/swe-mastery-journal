## Understand the idea

A secret is a value the app needs, such as a database password. An encryption key protects cryptographic operations/data under a key policy.

Secrets Manager and KMS address related but different responsibilities.

Use workload identity to retrieve an allowed secret or use a key. Encryption at rest does not prove that the application is allowed to show a record to this user.

Secret rotation also needs client behavior: a long-lived connection/client may keep using an old value until refreshed or reconnected.

Setup: create a training secret, choose its key policy, grant narrow workload retrieval/decryption access as required, choose injection versus runtime retrieval/cache, and test rotation/failure.

Keep secret values out of source, image layers, logs, screenshots, and AI context.