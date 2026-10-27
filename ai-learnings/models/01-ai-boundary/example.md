## Walk through an example

```ruby
proposal = intent_model.propose(text: "Late parcels at the east depot")
filter = AllowedFilter.parse!(proposal)
rows = Shipment.visible_to(actor).where(filter.to_conditions)
count = rows.count # exact count comes from the database
```

This is a design fragment, not a standalone Rails application. The full training app comes later. Notice that actor is supplied by authenticated application code, not a model argument.
