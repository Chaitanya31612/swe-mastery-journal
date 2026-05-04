# 04 - Hooks and Concurrent React: Answers

Companion to `04-react-hooks-and-concurrent-thought-questions.md`.

---

## Q1: setState batching with stale state

`count` becomes `1`, not `3`.

Why: each `setCount(count + 1)` reads the same `count` from the current render's closure. All three calls compute `0 + 1 = 1`. The setState queue has three entries, all with value `1`. React applies them in order: state goes 0 -> 1 -> 1 -> 1. Final value is `1`.

Fix: use the functional form.

```jsx
function tripleIncrement() {
  setCount((c) => c + 1);
  setCount((c) => c + 1);
  setCount((c) => c + 1);
}
```

Why this works: each functional update receives the **previous queued result**, not the value from closure. The queue is now `[(c) => c+1, (c) => c+1, (c) => c+1]`. React threads them: `0 -> 1 -> 2 -> 3`. Final value is `3`.

Senior framing: any time a setState computes a new value from the current state, default to the functional form. The non-functional form is safe only when the new value doesn't depend on the previous one (e.g., `setCount(0)` to reset).

Anchored in `docs/04-react-hooks-and-concurrent.md` -> "How useState actually works".

---

## Q2: The infinite render loop

`options` is a fresh object literal on every render. The dep array `[productId, options]` always sees a new `options` reference, so the effect runs every render. The effect calls `setData`, which causes a re-render, which creates a new `options`, and so on.

Three fixes ranked by quality:

**Best: move the constant inside the effect.**

```jsx
useEffect(() => {
  const options = { include: ['reviews', 'related'] };
  fetchProduct(productId, options).then(setData);
}, [productId]);
```

Now `options` doesn't need to be a dep at all. It's a local constant, recreated each effect run, but only when `productId` actually changes.

**Acceptable: hoist outside the component if it's truly constant.**

```jsx
const PRODUCT_OPTIONS = { include: ['reviews', 'related'] };

function ProductPage({ productId }) {
  useEffect(() => {
    fetchProduct(productId, PRODUCT_OPTIONS).then(setData);
  }, [productId]);
}
```

**Acceptable but worse: useMemo.**

```jsx
const options = useMemo(() => ({ include: ['reviews', 'related'] }), []);
```

Works, but it's a workaround for the wrong placement. If the value is truly static, it doesn't belong recreated each render at all.

The wrong answer: "remove `options` from the deps array". That silences the lint rule but creates a stale-closure bug if `options` ever becomes dynamic.

Anchored in `docs/04-react-hooks-and-concurrent.md` -> "How useEffect actually works".

---

## Q3: When to reach for `startTransition`

The three options solve different problems:

**Debounce (200ms):** delays the work until the user pauses typing. The filter doesn't run on every keystroke. Pro: fewer total computations. Con: results lag behind the input by 200ms even when the system could keep up.

**`startTransition`:** the filter runs on every keystroke, but is marked as interruptible. The input stays responsive because typing is on the urgent lane and the filter is on a transition lane. Pro: results stream in immediately when the system can; UI never feels sluggish. Con: still doing the work, just yielding to higher priority.

**Web Worker:** moves the computation off the main thread entirely. Pro: zero impact on UI responsiveness, regardless of work size. Con: serialization cost to send/receive data, complexity of managing a worker.

Decision matrix:

- **Filter is fast (under ~50ms) but happens often:** debounce is overkill. `startTransition` (or no optimization) is fine.
- **Filter is moderate (50ms-200ms) and happens often:** `startTransition` is the sweet spot. The filter still runs, but never blocks input.
- **Filter is slow (over 200ms) and the user types fast:** debounce. Even `startTransition` will queue up unfinished filter work. Not running the work at all is better than running it and discarding it.
- **Filter is heavy (parsing, regex, large datasets) and you want both responsiveness and accuracy:** Worker. The serialization is one-time per keystroke; the win is no main-thread blocking ever.

Senior framing: `startTransition` doesn't reduce work, it reschedules it. For "this work is pointless if a newer keystroke is coming", debounce. For "this work is fine to do but shouldn't block input", `startTransition`. For "this work shouldn't even touch the main thread", Worker. They compose: you can debounce + `startTransition` + Worker for a complex case.

Anchored in `docs/04-react-hooks-and-concurrent.md` -> "Now: concurrent rendering" and "useDeferredValue: the read-side version".
