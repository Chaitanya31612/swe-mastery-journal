## Break it and reason about the repair

A group may be subscribed to the wrong topic or have a different ID. earliest does not rewind existing commits. Resetting offsets can repeat external effects.

**Remember:** Outbox → record → group → inbox → projection.


### A real local-lab failure: stale empty outbox reads

The first long-running rails runner cached an empty SELECT. New HTTP requests inserted outbox rows, but the dispatcher kept seeing its cached empty result. The live smoke timed out. The repair runs each poll inside ApplicationRecord.uncached. This is separate from Redis caching and Kafka lag. Trace the database query before blaming the broker. The final lab smoke checks actual delivery after a new row is inserted.
