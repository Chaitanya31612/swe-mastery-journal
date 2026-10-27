require 'aws-sdk-sqs'
class QueueWorker
  def initialize(sqs:, queue_url:, handler:)
    @sqs, @queue_url, @handler = sqs, queue_url, handler
  end

  def tick
    response = @sqs.receive_message(queue_url: @queue_url, max_number_of_messages: 1,
                                    wait_time_seconds: 1, visibility_timeout: 30)
    response.messages.each do |message|
      @handler.call(JSON.parse(message.body)) # durable, idempotent handler
      @sqs.delete_message(queue_url: @queue_url, receipt_handle: message.receipt_handle)
    end
  end
end
