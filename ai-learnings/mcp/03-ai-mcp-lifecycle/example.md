## Walk through an example

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

This is one request in an initialized connection. A later tools/call request has its own request ID and arguments. The provider's model tool-call identifier belongs to another layer.
