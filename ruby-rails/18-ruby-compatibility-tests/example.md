## Follow a concrete example

```ruby
def delegate(*args, **kwargs, &block)
  target(*args, **kwargs, &block)
end
# Test positional args, explicit keywords including false,
# a final positional hash, and a passed block.
```

The Kafka training app in this course uses Ruby 3.3/Rails 7.2 separately. Its service/outbox ideas can be adapted, but its gem versions and migration syntax must not be pasted unchanged into Rails 4.2.
