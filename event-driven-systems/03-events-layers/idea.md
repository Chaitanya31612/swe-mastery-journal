## Understand the idea

The client library handles protocol requests, metadata, batching, retries, and serialization integration. A bootstrap address helps discover the cluster. The client then communicates with relevant broker endpoints; bootstrap is not a permanent universal proxy.

Brokers host partition leaders/replicas and serve produce/fetch requests. Records are stored in log segments with indexes; the operating system page cache and sequential I/O are part of the performance picture. This is a useful layer model, not a need to memorize every disk-file suffix.

Controllers manage cluster metadata/leadership under the selected Kafka mode. The course lab uses Kafka 4.1 KRaft, not a ZooKeeper tutorial. Replica placement and acknowledgement policy decide which failures an accepted record should survive. A one-broker local lab cannot demonstrate multi-broker availability.
