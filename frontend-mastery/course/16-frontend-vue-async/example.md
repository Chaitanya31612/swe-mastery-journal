## Follow a concrete example

```ts
watch(query, async (text, _old, onCleanup) => {
  let active = true
  const controller = new AbortController()
  onCleanup(() => { active = false; controller.abort() })
  loading.value = true; error.value = ''
  try {
    const r = await fetch('/api/tickets?q=' + encodeURIComponent(text),
      { signal: controller.signal })
    if (!r.ok) throw new Error('Search failed')
    const body = await r.json()
    if (active) rows.value = body // validate body at the real boundary
  } catch (e) {
    if (active && !controller.signal.aborted) error.value = 'Could not search'
  } finally {
    if (active) loading.value = false
  }
})
```
