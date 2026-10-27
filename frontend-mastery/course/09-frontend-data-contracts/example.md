## Follow a concrete example

```js
const api = { retries: 0, muted: false, note: null }
const retries = api.retries ?? 3 // preserves 0
const muted = api.muted ?? true // preserves false

const saved = { title: 'Export fails', tags: ['billing'] }
const draft = { ...saved, tags: [...saved.tags] }
draft.tags.push('urgent') // does not change saved.tags
```
For a PATCH request, omit note to leave it alone; send note:null only if the server contract means “clear.” Do not invent that meaning on the client alone.