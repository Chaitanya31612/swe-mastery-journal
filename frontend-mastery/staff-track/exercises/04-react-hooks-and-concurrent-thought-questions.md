# 04 - Hooks and Concurrent React: Thought Questions

Companion to `docs/04-react-hooks-and-concurrent.md`. Three questions, all practical.

---

## Q1: setState batching with stale state

> What this tests: how the setState queue applies updates and why functional setters matter.

A counter component:

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  function tripleIncrement() {
    setCount(count + 1);
    setCount(count + 1);
    setCount(count + 1);
  }

  return <button onClick={tripleIncrement}>{count}</button>;
}
```

Click the button. What's the new value of `count`? What's the fix to make it actually triple-increment, and why does the fix work?

---

## Q2: The infinite render loop

> What this tests: the `useEffect` dep contract and how non-primitive deps invalidate every render.

A teammate's PR fetches data:

```jsx
function ProductPage({ productId }) {
  const [data, setData] = useState(null);

  const options = { include: ['reviews', 'related'] };

  useEffect(() => {
    fetchProduct(productId, options).then(setData);
  }, [productId, options]);

  return <Product data={data} />;
}
```

The page makes infinite API requests. Why? Pick the cleanest fix.

---

## Q3: When to reach for `startTransition`

> What this tests: distinguishing urgent and non-urgent updates and when concurrent features actually buy you something.

You have a search input. Typing into it filters a list of 5,000 items. Without optimization, typing fast feels janky.

A teammate suggests three options:

1. Debounce the filter by 200ms.
2. Use `startTransition` around the filter update.
3. Move the filter computation to a Web Worker.

When would you pick each? Specifically, when does `startTransition` win over debouncing, and when does debouncing win over `startTransition`?
