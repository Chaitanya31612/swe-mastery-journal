## Follow a concrete example

```ruby
require 'aws-sdk-sqs'
sqs = Aws::SQS::Client.new(region: ENV.fetch('AWS_REGION'))
messages = sqs.receive_message(queue_url: ENV.fetch('QUEUE_URL'),
  wait_time_seconds: 20, max_number_of_messages: 10).messages
messages.each do |message|
  process_idempotently(message.body) # commit durable effect first
  sqs.delete_message(queue_url: ENV.fetch('QUEUE_URL'),
    receipt_handle: message.receipt_handle)
end
```

The loop is a teaching boundary. Add graceful shutdown, bounded concurrency, validation, visibility extension, error policy, and telemetry for a real worker.
