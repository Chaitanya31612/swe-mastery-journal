## Trace the execution

Trace DNS → connection/TLS → request headers → server response → HTTP cache → app adapter → UI state. When the page is stale, identify which layer supplied the stale copy.

A 304 response is used with a cached representation. A 200 with old data can come from a backend cache.

A CORS error may hide a response from JavaScript while the server still received the request. Do not assume a browser error means no side effect happened.