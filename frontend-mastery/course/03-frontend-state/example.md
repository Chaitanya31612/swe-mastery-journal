# A small example

```js
const tasks = [
  { id: 1, done: false }, { id: 2, done: true }
]
const filter = 'open'
const visible = tasks.filter(task => filter !== 'open' || !task.done)
// Store tasks + filter. Derive visible.
```

Sketch state for a task screen: URL query, fetched task rows, selected task ID, edit draft, save status. Decide what survives refresh, navigation, and a failed save.
