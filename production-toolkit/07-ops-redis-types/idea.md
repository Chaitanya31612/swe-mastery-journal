## Understand the idea

Redis is a networked data-structure service, not just a faster hash in your Ruby process. Each operation has a data type, cost, key scope, and failure behavior.

Keep network round trips and memory in mind.

Strings fit values/counters. Hashes fit fields under one key.

Sets answer membership/uniqueness. Sorted sets rank members by score.

Lists model ordered pushes/pops. Streams provide a retained entry structure with consumer-group features.

Pub/Sub is a different live-delivery contract and should not be mistaken for a durable queue.

Name keys with scope and purpose. Decide expiry deliberately.

Use SCAN-style iteration for operational browsing rather than blocking a large server with a casual KEYS *. An atomic command is not the same thing as an atomic multi-command business workflow.