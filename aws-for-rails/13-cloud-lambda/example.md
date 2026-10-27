## Follow a concrete example

```ruby
# Handler shape illustration for a selected Ruby event runtime.
def handler(event:, context:)
  event.fetch('Records').each do |record|
    handle_record_idempotently(record)
  end
  { processed: event.fetch('Records').length }
end
```

The event schema and partial-batch response must match the selected trigger. Do not copy this return value as if it acknowledges every source type correctly.
