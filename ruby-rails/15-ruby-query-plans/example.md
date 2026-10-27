## Follow a concrete example

```ruby
# Bounded interactive list.
rows = workspace.tickets.where(status: 'open').order(:id).limit(50).pluck(:id, :title)
# Deliberate batch processing in the legacy Rails style.
workspace.tickets.where(status: 'closed').find_each(batch_size: 500) do |ticket|
  rebuild_projection(ticket)
end
```

Do not assume a custom order survives legacy find_each. If the business requires an order, design and test an explicit cursor strategy.
