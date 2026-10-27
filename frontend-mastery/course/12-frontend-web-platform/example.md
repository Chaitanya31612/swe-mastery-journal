## Follow a concrete example

```js
const response = await fetch('/api/tickets', {
  headers: { Accept: 'application/json' }
})
if (!response.ok) throw new Error(`Load failed (${response.status})`)
const data = await response.json()
```
In DevTools, record status, initiator, cache indication, request ID, and Cache-Control. Compare a normal reload and a deliberate cache-disabled debugging run.

Disabling cache is a diagnostic, not a production fix.