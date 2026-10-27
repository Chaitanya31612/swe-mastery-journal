## Understand the idea

fetch resolves for an HTTP 404 or 500. Check response.ok before treating the body as success. A network failure is different from a server returning a deliberate error response.

The browser HTTP cache, a service worker, your query cache, and the server cache are separate copies. Cache-Control describes HTTP caching policy. An ETag can let the server say “not changed.” A fresh fetch call does not prove the server recomputed the data.

Cookies are sent according to origin/site, credentials mode, SameSite, and cookie attributes. CORS is a browser response-access rule, not authorization. A preflight request checks whether the browser may send a certain cross-origin request. Inspect both request and response headers before changing settings.
