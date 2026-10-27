publisher = KafkaPublisher.new
worker = OutboxDispatcher.new(publisher)
begin
  loop { sleep 0.2 unless worker.tick }
ensure
  publisher.close
end
