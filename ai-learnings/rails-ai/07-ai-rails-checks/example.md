## Walk through an example

```ruby
provider = FixtureProvider.new(fault: :unknown_citation)
result = ExplanationService.new(provider: provider).call(actor: actor, shipment_id: shipment.id)
assert_equal 'fallback', result.fetch(:state)
assert_equal shipment.verified_hold_reason, result.fetch(:verified_reason)
```
A fixture deliberately returning a bad answer tests the validator. It does not prove that the live model rarely returns bad answers.