## Walk through an example

```ruby
facts = Ai::FactBuilder.call(actor: actor, shipment_id: id)
# {source_version: '...', facts: [{id: 'F1', field: 'hold_reason', value: 'address_missing'}]}
explanation = provider.explain(facts: facts)
```
The fixture rule is small and inspectable. Its coverage is limited.

A useful production rule registry grows through reviewed code/tests, not automatically promoted model guesses.