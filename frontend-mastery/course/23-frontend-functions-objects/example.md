## Follow a concrete example

```js
function counter() {
  let value = 0
  return () => ++value
}
const a = counter(), b = counter()
a() // 1
a() // 2
b() // 1: separate closure

const formatter = { prefix: 'Ticket', label(id) { return `${this.prefix} ${id}` } }
const detached = formatter.label
const safe = formatter.label.bind(formatter)
safe(4) // 'Ticket 4'
// detached(4) throws when this is undefined in strict mode.
```
A timer callback reading a mutable selectedId will see its later value. Pass the intended ID as a local argument if the operation should belong to the original selection.