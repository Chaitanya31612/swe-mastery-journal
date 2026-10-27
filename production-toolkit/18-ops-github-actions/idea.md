## Understand the idea

A workflow is triggered by an event and runs jobs/steps on runners. CI should produce relevant evidence for a change: type checks, tests, build, and selected integration checks.

CD promotes a known artifact into an environment under deliberate permissions.

Build once from a known revision and record the image digest. Do not rebuild independently for staging and production and call them the same tested artifact.

Cache dependencies for speed, but do not let a cache replace a lockfile or validation.

Choose narrow workflow permissions and supported temporary cloud identity where appropriate. Untrusted PR code must not receive powerful deployment secrets.

Pin third-party actions according to the team’s supply-chain policy and review their access.