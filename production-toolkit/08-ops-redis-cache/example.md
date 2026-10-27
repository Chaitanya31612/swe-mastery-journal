## Follow a concrete example

```ruby
key = "workspace:#{workspace_id}:ticket:#{ticket_id}:v#{version}"
# Rails.cache.fetch(key, expires_in: 60) { load_allowed_summary }
```
The loader and key must use trusted scope. A versioned key helps only if the reader knows the current version through a reliable path.

Do not make version lookup cost or authorization disappear from the diagram.