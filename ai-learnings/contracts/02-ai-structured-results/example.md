## Walk through an example

```ruby
allowed = %w[status depot_name]
raise InvalidIntent unless proposal.is_a?(Hash)
raise InvalidIntent unless (proposal.keys - allowed).empty?
raise InvalidIntent unless %w[open held released].include?(proposal.fetch('status'))
# Next: resolve depot_name through the actor's authorized records.
```
The complete lab uses a more explicit schema and rejection paths. Do not use a cast, JSON.parse, or a citation ID check as a complete correctness validator.