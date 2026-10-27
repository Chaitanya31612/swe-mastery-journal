class ReportingConsumer
  def run
    consumer = Rdkafka::Config.new(
      'bootstrap.servers' => ENV.fetch('KAFKA_BROKERS'),
      'group.id' => 'reporting-v1', 'client.id' => 'learning-reporting',
      'auto.offset.reset' => 'earliest', 'enable.auto.commit' => false,
      'enable.auto.offset.store' => false
    ).consumer
    consumer.subscribe('ticket-events')
    consumer.each do |message|
      event = JSON.parse(message.payload)
      outcome = ApplicationRecord.uncached { ApplyReportingEvent.call(event) } # commits inbox + effect first
      Rails.logger.info("consumed event_id=#{event.fetch('event_id')} partition=#{message.partition} offset=#{message.offset} outcome=#{outcome}")
      consumer.store_offset(message) # stores message.offset + 1
      consumer.commit(nil, false)    # synchronous, after DB commit
    end
  ensure
    consumer&.close
  end
end
