## Follow a concrete example

```ruby
# Portable Ruby / Rails 4.2-style service seam.
Result = Struct.new(:ok, :value, :error)
class AssignTicket
  def call(actor:, ticket:, assignee:)
    return Result.new(false, nil, :not_allowed) unless allowed?(actor, ticket)
    Ticket.transaction do
      ticket.update!(assignee_id: assignee.id)
      Result.new(true, ticket.id, nil)
    end
  end
  # allowed? must implement the actual policy; not client-supplied trust.
end
```
