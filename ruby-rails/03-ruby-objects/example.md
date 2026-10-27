# A small example

```ruby
module Audit
  def label
    "audit(" + super + ")"
  end
end
class Task
  def label; "task"; end
end
Task.prepend(Audit)
p Task.new.label      # "audit(task)"
p Task.ancestors      # inspect the lookup path
p Task.new.method(:label).owner # Audit
```

Try include instead of prepend in a disposable Ruby file. Predict the owner before running it. The language book predates prepend; use the Ruby 2.7 docs for that addition.
