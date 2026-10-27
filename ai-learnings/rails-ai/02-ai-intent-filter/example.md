## Walk through an example

```ruby
proposal = provider.propose_filter(text: text)
filter = Ai::Filter.parse!(proposal)
relation = Shipment.visible_to(actor)
relation = filter.apply(relation) # only known fields and values
```

The offline fixture provider is deliberately a stub. It exercises the contract; it is not a substitute for evaluating a real model on varied user language.
