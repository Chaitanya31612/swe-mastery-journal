## Walk through an example

```ruby
class ReadShipmentFactsTool < MCP::Tool
  description 'Read permitted shipment facts for this actor'
  input_schema(properties: {shipment_id: {type: 'integer'}},
               required: ['shipment_id'], additionalProperties: false)
  def self.call(shipment_id:, server_context:)
    actor = server_context.fetch(:actor)
    facts = Ai::FactBuilder.call(actor: actor, shipment_id: shipment_id)
    MCP::Tool::Response.new([{type: 'text', text: JSON.generate(facts)}])
  end
end
```

The complete lab supplies the service, context binding, routes, fixtures and checks. This fragment alone is not an authenticated server.
