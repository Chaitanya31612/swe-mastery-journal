require 'test_helper'
class AwsAdaptersTest < ActiveSupport::TestCase
  def sqs
    Aws::SQS::Client.new(stub_responses: true, region: 'us-east-1')
  end

  test 'S3 signature restricts key and expiry' do
    s3 = Aws::S3::Client.new(stub_responses: true, region: 'us-east-1')
    url = AttachmentUpload.new(s3: s3, bucket: 'synthetic-training-bucket').call(ticket_id: 4, attachment_id: 9)
    assert_includes url, '/training/tickets/4/9'
    assert_includes url, 'X-Amz-Expires=300'
  end

  test 'SQS acknowledges only after handler succeeds' do
    client = sqs
    client.stub_responses(:receive_message, messages: [{message_id: 'm1', receipt_handle: 'h1', body: '{"event_id":"e1"}'}])
    applied = []
    QueueWorker.new(sqs: client, queue_url: 'https://sqs.us-east-1.amazonaws.com/123456789012/training', handler: ->(e) { applied << e.fetch('event_id') }).tick
    assert_equal ['e1'], applied
    assert_equal [:receive_message, :delete_message], client.api_requests.map { |r| r[:operation_name] }
  end

  test 'SQS failure leaves receipt unacknowledged' do
    client = sqs
    client.stub_responses(:receive_message, messages: [{receipt_handle: 'h1', body: '{}'}])
    worker = QueueWorker.new(sqs: client, queue_url: 'https://sqs.us-east-1.amazonaws.com/123456789012/training', handler: ->(_) { raise 'db failed' })
    assert_raises(RuntimeError) { worker.tick }
    assert_equal [:receive_message], client.api_requests.map { |r| r[:operation_name] }
  end
end
