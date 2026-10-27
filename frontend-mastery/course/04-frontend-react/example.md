# A small example

```jsx
function Counter() {
  const [count, setCount] = React.useState(0)
  function addThree() {
    setCount(c => c + 1)
    setCount(c => c + 1)
    setCount(c => c + 1)
  }
  return <button onClick={addThree}>{count}</button>
}
```

Compare three calls to setCount(count + 1). They all read the same render snapshot. A render can be started, repeated, or discarded; side effects during render make that dangerous.
