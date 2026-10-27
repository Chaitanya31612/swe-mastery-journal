## Follow a concrete example

```text
POST /tickets
Idempotency-Key: client-generated-command-id
Body: {title, workspaceId}

DB transaction:
  claim unique (actor_scope, command_key)
  compare request fingerprint if already claimed
  create ticket and store response identity
  commit
```
For GET /tickets?after=...&limit=..., cap limit on the server and use a deterministic ordered key. Tokens are data, not authorization.