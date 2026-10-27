## Understand the idea

Before review, compare against the intended base and inspect the actual outgoing patch. Explain the trigger, resulting behavior, test evidence, and known limitation.

A long commit list is not a substitute for that explanation.

Fetch updates your remote-tracking knowledge. Integration is a separate decision.

A rejected push means the remote state changed; inspect before deciding how to integrate. force-with-lease is a check against an expected tip, not permission to surprise collaborators.

For a release, name the exact commit/artifact, schema compatibility assumptions, and rollback/data-recovery plan. Keep hotfix backports traceable.

A Git tag names a version but does not prove the deployed container matches it; connect it to an image digest or build record.