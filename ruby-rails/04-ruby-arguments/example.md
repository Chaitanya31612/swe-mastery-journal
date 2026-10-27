# A small example

```ruby
def create_task(title, urgent: false)
  [title, urgent]
end
def forward(*args, **kwargs, &block)
  create_task(*args, **kwargs, &block)
end
p forward("ship", urgent: true) # ["ship", true]

label = "old"
reader = -> { label }
label = "new"
p reader.call                  # "new"

double = ->(n) { n * 2 }
p double.call(3)                # 6
```
