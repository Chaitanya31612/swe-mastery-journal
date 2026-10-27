# A small example

```js
// Pure decision: safe to test without a browser.
export function visibleTasks(tasks, filter) {
  return tasks.filter(task => filter !== 'open' || !task.done)
}
// Component scenario:
// 1. Type an edit. 2. Simulate failed save.
// 3. Assert draft is still present and retry is available.
// Race scenario:
// 1. Start query A. 2. Start query B.
// 3. Resolve B then A. Assert only B remains visible.
```
Use deferred promises/fake requests to control completion order. A timeout-based guess makes the test flaky.