## Follow a concrete example

```ruby
Ticket.transaction do
  ticket.lock!
  unless ticket.completed?
    ticket.update!(status: 'completed', version: ticket.version + 1)
    OutboxEvent.create!(event_id: SecureRandom.uuid,
      aggregate_id: ticket.id.to_s,
      envelope: build_completed_event(ticket))
  end
end
```

The runnable lab defines every model/migration/service and keeps this transaction local. No network call is made while holding the ticket lock.
