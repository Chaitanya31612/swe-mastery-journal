# 4. Producers: acknowledgements, idempotence, and duplicate business events

**Beginner · about 2 hours with practice**

Distinguish client retry deduplication from repeated application publication.

## Use it

Reliable publication of saved Rails events.

**Benefit:** Clear publication evidence and stable retry identity.

**Cost or limit:** The DB/Kafka publication gap still permits repeats.

## Work in this order

1. [Understand](idea.md).
2. [Example](example.md).
3. [Execution trace](trace.md).
4. [Failure](failure.md).
5. [Repair practice](practice/repair.md).
6. [Changed-condition practice](practice/transfer.md).

Take the quiz in Software Learnings. Reference answers live in answers/ and unlock in the app after submission.

## Reference

- [Kafka producer config](https://kafka.apache.org/41/configuration/producer-configs/)
- [Ruby rdkafka client](https://github.com/karafka/rdkafka-ruby)
