# 02 - Closures, Prototypes, Async: Answers

Companion to `02-js-language-thought-questions.md`.

---

## Q1: The stale closure in disguise

The bug: `useEffect` runs with `[]` deps, so it captures `handleSearch` from the first render. That `handleSearch` closes over the initial `query` (empty string). Every interval call uses that frozen closure.

Most-common wrong fix: add `query` to the effect's deps array. That works (the interval gets recreated on every keystroke), but it's wasteful: you're tearing down and recreating the timer constantly, and you might fire a fetch immediately after each keystroke.

Cleanest fix: keep the timer stable, but read the latest `query` via a ref:

```jsx
const queryRef = useRef(query);
useEffect(() => { queryRef.current = query; }, [query]);

useEffect(() => {
  const id = setInterval(() => {
    fetchResults(queryRef.current).then(setResults);
  }, 5000);
  return () => clearInterval(id);
}, []);
```

Refs don't get captured by closure timing because you read `.current` lazily, at the moment the interval fires.

Alternative: use a library/utility that gives you a stable callback that always sees the latest value (`useEvent`-style). The mental model is the same: separate "I want a stable identity" from "I want the latest value".

Anchored in `docs/02-js-closures-prototypes-async.md` -> "The stale closure bug, demystified".

---

## Q2: The race that wasn't a race

The teammate is wrong. JavaScript being single-threaded refers to the call stack, but **I/O does not run on the call stack**. `fetch`, network requests, timers, and most async work are handed off to the runtime (browser or Node), which has plenty of threads.

`Promise.all([refreshList(), refreshSidebar()])` starts both fetches at the moment of evaluation. They run concurrently in the network layer. The single thread coordinates them, but it doesn't *do* the I/O. The total wait time is `max(refreshList, refreshSidebar)` instead of `refreshList + refreshSidebar`.

Concrete numeric example to show the pushback:

> If `refreshList` takes 200ms and `refreshSidebar` takes 250ms, the sequential version waits 450ms. The parallel version waits 250ms. The single thread isn't doing more work; it's not blocked waiting for I/O that's already in flight.

Anchored in `docs/02-js-closures-prototypes-async.md` -> "async/await is sugar, but it changes one thing".

---

## Q3: this binding in a class

`this.clear` is a method reference. When you pass it to `addEventListener`, the function is detached from `this`. When the click fires, `this` is the button (or `undefined` in strict mode), so `this.tasks = []` errors.

Two fixes:

**Fix 1: bind in the constructor.**

```js
class TaskList {
  constructor() {
    this.tasks = [];
    this.clear = this.clear.bind(this);
  }
  clear() { this.tasks = []; }
}
```

**Fix 2: class field with arrow function.**

```js
class TaskList {
  tasks = [];
  clear = () => {
    this.tasks = [];
  };
}
```

Recommendation: **Fix 2** for new code. It's terser, doesn't repeat the method name, and the arrow form makes the lexical-`this` capture explicit. Fix 1 is fine for older codebases or class hierarchies where you need the method on the prototype.

The wrong answer: "use `addEventListener('click', () => this.clear())`". This works but creates a fresh arrow on every call to `add`, which means you can never `removeEventListener` the listener you added. For one-time setup it's fine; for anything you might want to remove, it's a future bug.

Anchored in `docs/02-js-closures-prototypes-async.md` -> "this in four binding modes".
