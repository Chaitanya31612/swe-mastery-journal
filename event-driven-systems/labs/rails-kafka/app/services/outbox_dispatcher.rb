# One serial dispatcher. Parallel publishing needs an additional ordering policy.
class OutboxDispatcher
  def initialize(publisher)
    @publisher = publisher
  end

  def tick
    ApplicationRecord.uncached do
    event = OutboxEvent.where(published_at: nil).order(:id).first
    return false unless event
    @publisher.publish(event.envelope, key: event.aggregate_key) # wait for ACK
    # Crash here: publish repeats with the SAME event_id after restart.
    event.update!(published_at: Time.current)
    true
    end
  end
end
