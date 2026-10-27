# A small example

```ruby
first = ["open"]
second = first
second << "done"
p first                    # ["open", "done"]
second = ["closed"]
p first                    # still ["open", "done"]

settings = { enabled: false }
p settings[:enabled] || true # true: the false value was lost
p settings.fetch(:enabled, true) # false

buckets = Hash.new { |h, key| h[key] = [] }
buckets[:today] << "task-1"
p buckets[:tomorrow]        # []: a different array
```
