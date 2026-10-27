class KafkaPublisher
  def initialize
    @producer = Rdkafka::Config.new(
      'bootstrap.servers' => ENV.fetch('KAFKA_BROKERS'),
      'client.id' => 'learning-outbox', 'enable.idempotence' => true,
      'acks' => 'all', 'message.timeout.ms' => 10000
    ).producer
  end

  def publish(event, key:)
    report = @producer.produce(topic: 'ticket-events', key: key, payload: JSON.generate(event)).wait(max_wait_timeout: 15)
    Rails.logger.info("published event_id=#{event.fetch('event_id')} partition=#{report.partition} offset=#{report.offset}")
    report
  end

  def close
    @producer.close
  end
end
