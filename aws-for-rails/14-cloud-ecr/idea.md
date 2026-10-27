## Understand the idea

A container registry stores images. A tag is a name that can move unless policy prevents it. A digest identifies image content. Deploying latest makes it difficult to know what actually ran during an incident.

ECR integrates registry access with AWS identity. Build/push identity and workload pull identity can have different permissions. A successful push does not prove the image runs, and a vulnerability scan does not prove the application is safe or compatible.

Setup: create a deliberate training repository, configure tag policy/retention, authenticate the build identity, build from an identified source revision, push a revision tag, record the digest, and test pull/run under the workload’s identity. Keep rollback artifacts long enough for the release plan.
