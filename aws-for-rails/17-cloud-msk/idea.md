## Understand the idea

MSK provides managed Kafka options. It reduces parts of broker infrastructure work, but does not choose event keys, schemas, consumer groups, offset policy, or business idempotence for you. Provisioned/serverless options have different configuration and capacity contracts.

A client needs reachable advertised broker endpoints, the selected authentication/TLS mechanism, authorization, and compatible client support. “The bootstrap server responds” is not enough if metadata returns endpoints the client cannot reach.

Setup: choose the MSK offering/version, private connectivity and access mechanism, topic/partition policy, client credentials/role support, monitoring, and retention. Run the local Kafka lab first. Then test a synthetic event and replay in the chosen training AWS environment.
