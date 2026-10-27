## Walk through an example

```ruby
case call.name
when 'list_shipments'
  args = AllowedFilter.parse!(JSON.parse(call.arguments))
  result = tools.list_shipments(actor: actor, filter: args)
else
  raise UnsupportedTool
end
# Return the serialized result paired with call.call_id, using the provider's format.
```
A case/registry allowlist is intentional. Never convert a tool name directly to constantize, send, SQL, a shell command, or an arbitrary URL.