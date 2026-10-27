# A small example

```js
// A tiny browser experiment, not a framework router replacement.
const button = document.querySelector('#open-tasks')
button?.addEventListener('click', () => {
  history.pushState({}, '', '/tasks')
  document.querySelector('main').textContent = 'Task list'
})
window.addEventListener('popstate', () => {
  console.log('Back/forward URL:', location.pathname)
})
```
Predict which events need a fresh document request. Use the Network panel with synthetic pages. pushState changes the URL; it does not fetch or render a route for you.