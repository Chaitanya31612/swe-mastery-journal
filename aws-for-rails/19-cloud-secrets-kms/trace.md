## Trace the execution

Workload role → permitted secret retrieval/key use → validated runtime config → client connection → rotation → refresh/reconnect. Test denied access and stale credentials without revealing values.

For incident response, distinguish revoking application access, rotating a credential, and changing encryption-key policy. They do not all revoke an already issued download URL or terminate every connection instantly.