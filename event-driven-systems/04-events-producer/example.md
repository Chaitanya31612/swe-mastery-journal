## Follow a concrete example

```ruby
producer = Rdkafka::Config.new(
  'bootstrap.servers' => ENV.fetch('KAFKA_BROKERS'),
  'enable.idempotence' => true,
  'acks' => 'all'
).producer
handle = producer.produce(topic: 'ticket-events',
  key: ticket_key, payload: JSON.generate(event_envelope))
handle.wait # publication result; not consumer completion
```
The tested lab supplies lifecycle/error handling. On a one-replica topic, acks=all still means only that configured replica set, not three-broker durability.