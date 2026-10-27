class TicketEvent
  def self.completed(ticket)
    {'event_id' => SecureRandom.uuid, 'event_type' => 'TicketCompleted',
     'schema_version' => 1, 'occurred_at' => Time.current.iso8601(6),
     'aggregate_id' => ticket.id.to_s, 'aggregate_version' => ticket.event_version,
     'data' => {'ticket_id' => ticket.id}}
  end

  def self.validate!(event)
    raise ArgumentError, 'Unsupported schema/type' unless event['schema_version'] == 1 && event['event_type'] == 'TicketCompleted'
    raise ArgumentError, 'Missing identity' unless event['event_id'].is_a?(String) && !event['event_id'].empty?
    raise ArgumentError, 'Invalid ticket' unless event.dig('data', 'ticket_id').is_a?(Integer) && event['aggregate_id'] == event['data']['ticket_id'].to_s
    raise ArgumentError, 'Invalid version' unless event['aggregate_version'].is_a?(Integer) && event['aggregate_version'].positive?
    event
  end
end
