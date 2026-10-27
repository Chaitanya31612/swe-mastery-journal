## Follow a concrete example

```sh
# Inside the lab Kafka container:
/opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka:9092   --describe --group ticket-reporting-v1
/opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092   --describe --topic ticket-events
```
Use the exact lab group/topic names. Read commands before using them in any other cluster.

Offset reset is a deliberate mutation, not a first diagnostic.