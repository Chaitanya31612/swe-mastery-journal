## Understand the idea

An event envelope makes meaning explicit. Include event_id, event_type, schema_version, aggregate identity/version, occurred_at, and minimal payload.

Distinguish when the business fact happened from when a consumer processed it.

Do not publish an entire Rails model by habit. It couples consumers to private columns and may expose data they do not need.

Use the smallest fact that supports the subscriber’s job. A schema registry can help manage format compatibility; it does not decide business meaning or permission policy for you.

For evolution, add optional fields with clear defaults where compatible. Renaming/removing a required field can break old consumers.

Producers and consumers may run different versions during deployment. Test representative old/new messages, not only the newest example.