## Trace the execution

Receive E → validate → insert inbox + update report → commit DB → commit Kafka. Crash after DB commit before Kafka commit: receive E again → unique inbox says local effect exists → do not repeat it → commit progress.

Include consumer identity in deduplication scope when different projections independently need the same event. Their completion responsibilities are separate.
