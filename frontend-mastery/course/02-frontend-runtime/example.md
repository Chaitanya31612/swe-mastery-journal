# A small example

```js
console.log('A')
setTimeout(() => console.log('B'), 0)
Promise.resolve().then(() => console.log('C'))
console.log('D')
// A, D, C, B

let latest = 0
async function search(query) {
  const request = ++latest
  const response = await fetch('/api/search?q=' + encodeURIComponent(query))
  if (!response.ok) throw new Error('Search failed')
  const rows = await response.json()
  if (request === latest) showRows(rows)
}
// The surrounding UI must also handle loading/errors per request.
```
