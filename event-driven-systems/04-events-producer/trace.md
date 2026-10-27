## Trace the execution

Saved event E → client buffer → batch send → broker acknowledgement → mark outbox published. Crash after acknowledgement but before the DB mark means E may be published again.

The producer’s protocol identity does not make the DB mark and Kafka append one transaction. The consumer inbox is still needed for this gap.