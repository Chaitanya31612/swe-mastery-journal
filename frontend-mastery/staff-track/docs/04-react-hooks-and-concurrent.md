# 04 - Hooks and Concurrent React

> Why this file matters to you as a senior dev: hooks feel magical until you see the linked list. Concurrent rendering feels arbitrary until you see lanes. After this doc, both are mechanical, and the rules of hooks stop sounding like superstition.

---

## The hooks data structure

Every function component fiber stores its hooks as a **linked list** on its `memoizedState` field. The order of nodes in that list is the order you called hooks during render.

```text
fiber.memoizedState
        |
        v
   [ hook 0 ]  ->  [ hook 1 ]  ->  [ hook 2 ]  ->  null
   useState(0)     useState('')    useEffect(...)
```

When your component renders the next time, React walks this list in order, expecting the hook at position N to match the call you make at position N. The hook itself doesn't know its name; it just knows its slot.

That's the whole reason behind the rules of hooks:

- "Don't call hooks conditionally" means "don't change the slot ordering between renders".
- "Don't call hooks inside loops" means the same thing, with extra steps.

If you call hooks conditionally, slot 1 might be `useState` on render A and `useEffect` on render B. React reads slot 1 and gets the wrong thing entirely.

> 💡 Insight - the rules of hooks are not stylistic. They're a consequence of the data structure. Once you see the linked list, you can't violate them by accident.

---

## How useState actually works

A simplified `useState`:

```js
function useState(initial) {
  const fiber = currentFiber;
  const hook = fiber.memoizedState[currentHookIndex] ?? createHook(initial);

  const setState = (next) => {
    hook.queue.push(next);
    scheduleUpdate(fiber);
  };

  hook.value = applyQueue(hook.value, hook.queue);
  hook.queue = [];

  currentHookIndex++;
  return [hook.value, setState];
}
```

A few things become obvious:

1. The hook lives on the fiber. It survives between renders because the fiber survives.
2. `setState` doesn't write the new value directly. It pushes onto a queue and schedules a re-render.
3. The new value is computed during the next render by applying the queue.

This is why **you can call `setState` multiple times in one event** and React batches them:

```js
function increment() {
  setCount(count + 1);  // queue: [count + 1]
  setCount(count + 1);  // queue: [count + 1, count + 1]   <- both based on stale `count`
}
```

Both reads of `count` see the same closure-captured value. The queue ends up with two identical operations. The functional form fixes it:

```js
function increment() {
  setCount((c) => c + 1);  // queue: [(c) => c + 1]
  setCount((c) => c + 1);  // queue: [(c) => c + 1, (c) => c + 1]
}
```

When React applies the queue, it threads each function over the previous result. Now you actually go up by 2.

> 🔍 Under the Hood - `useReducer` is the truthful version of `useState`. `useState` is implemented as `useReducer` with a hardcoded reducer that either takes the value or calls the function.

---

## How useEffect actually works

`useEffect` registers an effect node in the hook list with the callback and the dep array. React doesn't run the callback during render. It schedules it to run after commit.

```text
   render phase:
     useEffect(cb, [a, b])  -> store { cb, deps: [a, b] } on the hook

   commit phase:
     for each effect hook:
       if deps changed (or first commit):
         run last cleanup (if any)
         run cb, capture its return as new cleanup
```

The dep array is the entire mechanism. If the deps are referentially equal to last time, React skips running the effect.

```js
useEffect(() => {
  subscribe(userId);
  return () => unsubscribe(userId);
}, [userId]);
```

Render 1: `userId === 'a'`. Run effect. Cleanup is captured: `() => unsubscribe('a')`.

Render 2: `userId === 'b'`. Deps changed. Run cleanup from render 1 (`unsubscribe('a')`). Run new effect (`subscribe('b')`). Capture new cleanup.

Render 3: `userId === 'b'`. Deps same. Skip.

Unmount: run last captured cleanup.

> ⚠️ Trap - putting a non-primitive (object, array, function) in the dep array means the effect runs every render unless you stabilize it with `useMemo`/`useCallback`. The lint rule pushes you to add it; the actual fix is often "don't put it in deps, recompute it inside the effect".

---

## useMemo, useCallback, useRef in two lines each

`useMemo(fn, deps)` runs `fn` and caches the result. Returns the cache while deps are unchanged. Useful for stabilizing the identity of expensive computations or derived data structures.

`useCallback(fn, deps)` is `useMemo(() => fn, deps)`. Returns the same function reference while deps are unchanged. Useful when downstream `React.memo` or `useEffect` depends on the function's identity.

`useRef(initial)` returns a stable object `{ current: initial }`. Mutating `.current` does **not** trigger a re-render. Useful for holding values you want to read without re-rendering, and for DOM refs (because React assigns the DOM node to `.current` when the ref is attached).

```js
const inputRef = useRef(null);
useEffect(() => {
  inputRef.current.focus();
}, []);
```

> 💡 Insight - `useRef` is the escape hatch from React's pure render contract. If a value should be mutable but shouldn't trigger renders (timers, latest-value boxes, imperative handles), `useRef` is the right tool, not `useState`.

---

## useContext: cheap reads, not cheap subscriptions

`useContext(MyContext)` reads the nearest provider's value. When the value changes, every consumer of that context re-renders.

That last part is the gotcha. Context is not a fine-grained subscription. If you put a big object in context and any field changes, every consumer re-renders.

```jsx
// This re-renders all consumers when ANY field changes.
<UserContext.Provider value={{ profile, settings, theme }}>

// Splitting context lets consumers subscribe to only what they need.
<ProfileContext.Provider value={profile}>
  <SettingsContext.Provider value={settings}>
    <ThemeContext.Provider value={theme}>
```

For app-wide state where you need fine-grained subscriptions, reach for a state library (Zustand, Redux Toolkit, Jotai). Context is for "this component subtree needs to read X" cases, not for app-wide mutable state.

---

## Now: concurrent rendering

The big idea: React can have **multiple renders in flight** at different priorities. The default (urgent) renders block until done. Lower-priority renders can be paused, resumed, or thrown away.

This is implemented via **lanes**. Every update gets tagged with a lane. The scheduler picks the highest-priority lane that has pending work and processes it.

```text
   lanes (highest priority -> lowest)

   SyncLane         <- click handlers, input
   InputContinuousLane
   DefaultLane      <- regular setState
   TransitionLane   <- startTransition
   IdleLane
```

A click that calls `setState` goes into a sync-ish lane. React renders that update without yielding. A `startTransition` update goes into a transition lane. React can pause it if a more urgent update arrives.

```jsx
function FilterableList({ items }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(items);

  function handleChange(e) {
    setQuery(e.target.value);                     // urgent: input must feel responsive
    startTransition(() => {
      setResults(filterExpensive(items, e.target.value));  // non-urgent
    });
  }
}
```

Without transitions, every keystroke does the expensive filter and the input lags. With transitions, the keystroke updates instantly; the filter happens at lower priority and can be interrupted by the next keystroke.

> 💡 Insight - transitions are not "make it async". They're "tag this update as interruptible". The work still happens on the main thread; the scheduler just gets to defer it.

---

## useDeferredValue: the read-side version

Sometimes you don't own the `setState` call but you want to defer rendering work that depends on a value.

```jsx
function Results({ query }) {
  const deferredQuery = useDeferredValue(query);
  const list = useMemo(() => filterExpensive(deferredQuery), [deferredQuery]);
  return <List items={list} />;
}
```

`useDeferredValue` returns the previous value initially, then schedules a low-priority update with the new value. The first render shows stale data without blocking the input; the deferred re-render computes the expensive list.

`startTransition` is "I'm causing this state change, mark it as deferrable". `useDeferredValue` is "I'm reading a value, give me a deferred version of it". They're two sides of the same lane mechanism.

---

## Suspense as data coordination

A `<Suspense>` boundary is a React component that catches when a child component **suspends** (throws a Promise instead of rendering). When that happens, React shows the fallback and waits for the promise to resolve before retrying.

```jsx
<Suspense fallback={<Skeleton />}>
  <UserProfile userId={id} />
</Suspense>
```

If `UserProfile` calls a Suspense-aware data hook (like `use(promise)` or a router-integrated loader) and the data isn't ready yet, it throws the promise. React catches it at the boundary, renders the fallback, and re-tries when the promise resolves.

The senior framing: **Suspense is not a loading library, it's a coordination boundary**. It lets multiple parts of a tree wait for their data in parallel and only show "ready" UI when they're collectively ready.

```jsx
<Suspense fallback={<PageSkeleton />}>
  <Sidebar />            // suspends on user data
  <Main>
    <Suspense fallback={<MainSkeleton />}>
      <Posts />          // suspends on posts data
    </Suspense>
  </Main>
</Suspense>
```

Outer boundary waits for Sidebar (and the inner boundary's fallback). Inner boundary waits for Posts. Sidebar can render before Posts is ready; you see the inner skeleton while Posts loads.

> ⚠️ Trap - Suspense only coordinates components that are *suspense-integrated* (`use()`, frameworks like Next.js's data fetching, libraries like React Query in Suspense mode). Plain `useEffect` fetches do not trigger Suspense.

---

## What concurrent rendering actually changes for you

Three practical things:

1. **Input stays responsive while expensive renders are in flight.** Use `startTransition` or `useDeferredValue` to mark the expensive work.
2. **Suspense becomes useful for data, not just code splitting.** With suspense-integrated data fetching, you get coordinated loading states and streaming.
3. **Effects can run twice in development (Strict Mode)**, which is React's way of forcing you to write effects that can be paused, replayed, and resumed safely.

The pattern that breaks under concurrent: anything in render that has side effects. Network calls, mutating refs, console-logging-as-debugging. They might run more than once, run partially, or run for a render that gets thrown away.

---

## What to carry forward

- Hooks are a linked list keyed by call order. The rules of hooks are a consequence of the data structure, not a style choice.
- `useState` is a queue against the previous state. The functional form is the only safe form when you're updating from a value that might already be stale.
- `useEffect` is "after commit, if deps changed, run cleanup then run callback". Stabilize non-primitive deps or move them inside the effect.
- Concurrent React is built on lanes. Transitions and `useDeferredValue` mark work as interruptible. The scheduler picks the highest-priority lane.
- Suspense coordinates data readiness across a subtree. It needs suspense-aware data sources to do anything.
