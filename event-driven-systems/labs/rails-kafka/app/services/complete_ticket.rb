class CompleteTicket
  def self.call(id)
    Ticket.transaction do
      ticket = Ticket.lock.find(id)
      # Retried completion command is a no-op in this one-way lab workflow.
      unless ticket.status == 'completed'
        ticket.update!(status: 'completed', event_version: ticket.event_version + 1)
        event = TicketEvent.completed(ticket)
        OutboxEvent.create!(event_id: event.fetch('event_id'),
                            aggregate_key: ticket.id.to_s, envelope: event)
      end
      ticket
    end
  end
end
