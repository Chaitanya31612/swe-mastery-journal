## Walk through an example

```ruby
class ReadShipmentFacts
  def call(actor:, shipment_id:)
    shipment = Shipment.visible_to(actor).find(shipment_id)
    {id: shipment.id, status: shipment.status, hold_reason: shipment.verified_hold_reason}
  end
end
```

No tenant_id or admin flag is accepted from the model. The returned fields are a deliberate allowlist.
