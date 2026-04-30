# 02 - Reactivity, Rendering, And State

This is the heart of modern frontend. Frameworks differ in syntax, but they all answer the same question:

```text
When data changes, how does the right UI update happen with the least wrongness and acceptable cost?
```

---

## The Core Idea

UI frameworks turn state into UI.

```text
state
  -> render calculation
  -> UI description
  -> DOM update
  -> browser paint
```

The framework has to know:

- what changed
- what depends on what changed
- when to run render work
- how much DOM to mutate
- when effects should run
- what to clean up

Reactivity is the system that connects "data changed" to "UI should update".

---

## Two Big Reactivity Families

### Render-Tree Reactivity

React mostly works like this:

```text
state update
  -> schedule component render
  -> component function runs again
  -> child render work may happen
  -> compare previous and next UI descriptions
  -> commit DOM changes
```

You explicitly call setters:

```js
setCount((count) => count + 1);
```

The component reruns. React asks what the UI should look like now.

### Dependency-Tracking Reactivity

Vue mostly works like this:

```text
component renders
  -> reactive reads are tracked
  -> reactive write happens
  -> only dependent effects are scheduled
  -> DOM update is patched
```

You mutate reactive values:

```js
count.value += 1;
```

Vue knows which render effect read `count.value`, so it can update targeted dependents.

Senior intuition: React rerenders by component ownership. Vue rerenders by tracked dependencies.

---

## A Tiny Reactivity System

This is not production code. It is the intuition.

```js
let activeEffect = null;

function createSignal(initialValue) {
  let value = initialValue;
  const subscribers = new Set();

  return {
    get() {
      if (activeEffect) {
        subscribers.add(activeEffect);
      }

      return value;
    },

    set(nextValue) {
      value = nextValue;

      subscribers.forEach((subscriber) => {
        subscriber();
      });
    },
  };
}

function effect(callback) {
  activeEffect = callback;
  callback();
  activeEffect = null;
}

const count = createSignal(0);

effect(() => {
  console.log(`Count is ${count.get()}`);
});

count.set(1);
```

Output:

```text
Count is 0
Count is 1
```

The trick:

```text
while rendering, remember what state was read
when that state changes, rerun the dependent work
```

Vue, Svelte, Solid, MobX, and signals-style systems differ in implementation, but this mental model travels far.

---

## A Tiny Virtual DOM Model

Virtual DOM is a UI description in JavaScript objects.

```js
const previousTree = {
  type: 'button',
  props: { disabled: false },
  children: ['Save'],
};

const nextTree = {
  type: 'button',
  props: { disabled: true },
  children: ['Saving...'],
};
```

Diff:

```text
same type: button
changed prop: disabled false -> true
changed text: Save -> Saving...
```

Patch DOM:

```js
button.disabled = true;
button.textContent = 'Saving...';
```

Senior intuition: virtual DOM is not magic speed. It is a portable way to describe UI and calculate mutations. Its cost is JavaScript work. Its value is predictability, composition, and cross-platform render targets.

---

## React Render And Commit

React has two broad phases:

```text
render phase
  calculate next UI
  can be interrupted in concurrent rendering
  should be pure

commit phase
  apply DOM changes
  run layout effects
  browser may paint
  run passive effects
```

Component function:

```js
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      {count}
    </button>
  );
}
```

On click:

```text
event handler runs
  -> setCount schedules update
  -> React renders Counter again
  -> React compares old and new element output
  -> React commits text update
```

Important consequence: render must not cause side effects.

Bad:

```js
function UserProfile({ user }) {
  localStorage.setItem('lastUserId', user.id);

  return <h1>{user.name}</h1>;
}
```

Better:

```js
function UserProfile({ user }) {
  useEffect(() => {
    localStorage.setItem('lastUserId', user.id);
  }, [user.id]);

  return <h1>{user.name}</h1>;
}
```

Senior intuition: render describes. Commit changes. Effects synchronize.

---

## React Effects Are Synchronization

Effects are often misused as lifecycle callbacks.

Better mental model:

```text
useEffect synchronizes React state with an external system.
```

External systems include:

- DOM APIs outside React
- network subscriptions
- timers
- browser storage
- analytics
- imperative widgets

Not effects:

```js
useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);
```

Better:

```js
const fullName = `${firstName} ${lastName}`;
```

Effect with cleanup:

```js
useEffect(() => {
  function handleResize() {
    setWidth(window.innerWidth);
  }

  window.addEventListener('resize', handleResize);

  return () => {
    window.removeEventListener('resize', handleResize);
  };
}, []);
```

Senior rule: if an effect only rearranges your own state, question it hard.

---

## React Lifecycle Without Class Terms

Functional React lifecycle is not "mounted, updated, unmounted" only.

More useful:

```text
component is rendered
  function runs and returns UI description

component is committed
  DOM is updated

layout effects run
  before browser paint, useful for measuring layout

browser paints
  user sees result

passive effects run
  after paint, useful for subscriptions and network sync

component may render again
  because props, state, context, or parent render changed

component unmounts
  cleanup functions run
```

Use `useLayoutEffect` rarely:

```js
useLayoutEffect(() => {
  const height = ref.current.getBoundingClientRect().height;
  setMeasuredHeight(height);
}, []);
```

Why rare:

```text
It blocks paint.
```

Senior intuition: the question is not "which lifecycle method?" It is "must this happen before paint, after paint, or outside React entirely?"

---

## Vue Reactivity Internals

Vue 3 uses proxies for reactive objects.

Conceptually:

```js
const state = reactive({ count: 0 });
```

becomes:

```text
read state.count
  -> track active effect as dependent on count

write state.count
  -> trigger effects dependent on count
```

Tiny proxy example:

```js
function reactive(target) {
  return new Proxy(target, {
    get(object, key) {
      track(object, key);
      return object[key];
    },

    set(object, key, value) {
      object[key] = value;
      trigger(object, key);
      return true;
    },
  });
}
```

Vue templates are compiled into render functions. During render, reactive reads are tracked.

```vue
<template>
  <button>{{ count }}</button>
</template>
```

Conceptually:

```js
function render() {
  return h('button', count.value);
}
```

When `count.value` changes, Vue knows this render effect depends on it.

Senior intuition: Vue feels more automatic because dependencies are collected by reads.

---

## Vue Lifecycle And Watchers

Composition API lifecycle:

```js
onMounted(() => {
  startSubscription();
});

onUnmounted(() => {
  stopSubscription();
});
```

Use `computed` for derived values:

```js
const fullName = computed(() => {
  return `${firstName.value} ${lastName.value}`;
});
```

Use `watch` for side effects caused by reactive changes:

```js
watch(searchQuery, async (query, previousQuery, onCleanup) => {
  const controller = new AbortController();

  onCleanup(() => {
    controller.abort();
  });

  results.value = await searchApi(query, {
    signal: controller.signal,
  });
});
```

Bad smell:

```text
watching state only to copy it into other state
```

Prefer computed or a clearer owner.

Senior rule: computed is for values. watch is for effects.

---

## Batching

Frameworks batch updates to avoid waste.

Without batching:

```text
set firstName
render
set lastName
render
set age
render
```

With batching:

```text
set firstName
set lastName
set age
render once
```

React batches many updates in the same event turn. Vue queues DOM updates and flushes them asynchronously.

Vue example:

```js
count.value += 1;

console.log(button.textContent); // may still show old DOM text

await nextTick();

console.log(button.textContent); // DOM is updated
```

Senior intuition: state changes before DOM changes. If you need updated DOM, you need the framework's post-update timing primitive.

---

## Component Identity

Frameworks preserve state by matching component identity.

React list example:

```js
items.map((item) => (
  <TodoRow key={item.id} item={item} />
));
```

Bad:

```js
items.map((item, index) => (
  <TodoRow key={index} item={item} />
));
```

If order changes, state can stick to the wrong row.

Vue equivalent:

```vue
<TodoRow
  v-for="item in items"
  :key="item.id"
  :item="item"
/>
```

Senior intuition: keys are not for suppressing warnings. Keys define identity across time.

---

## State Ownership

Most frontend complexity is state ownership complexity.

Classify every piece of state:

```text
server state
  data owned by backend, cached by frontend

client state
  UI state owned by frontend

URL state
  state users can navigate, share, refresh, or bookmark

form state
  temporary user input before commit

derived state
  computed from other state

external state
  browser, storage, media query, auth provider, websocket, worker
```

Bad:

```text
selectedProjectId in URL
selectedProjectId in global store
selectedProjectId in component state
selectedProjectId in localStorage
```

This is four sources of truth.

Better:

```text
URL owns selectedProjectId
query/cache owns project data
component derives selectedProject from selectedProjectId + cached projects
```

Senior rule: if two places can disagree, they eventually will.

---

## Server State Is Different

Server state has properties local UI state does not:

- remote ownership
- async fetching
- caching
- staleness
- invalidation
- retries
- deduplication
- optimistic updates
- background refresh

Bad manual shape:

```js
const [data, setData] = useState(null);
const [error, setError] = useState(null);
const [isLoading, setIsLoading] = useState(false);
```

This is fine once. It becomes painful across an app.

Senior choice:

```text
Use a server-state tool or framework data layer when the app needs caching,
deduplication, invalidation, pagination, optimistic updates, or route-level loading.
```

Examples:

- React Query or SWR in React apps
- framework loaders in router-driven apps
- Next server data fetching when data belongs near the server boundary
- Vue Query or Pinia plus explicit fetch policy in Vue apps

The exact tool matters less than the ownership model.

---

## Derived State

Derived state is state you can calculate from other state.

Bad:

```js
const [items, setItems] = useState([]);
const [visibleItems, setVisibleItems] = useState([]);
```

Better:

```js
const visibleItems = items.filter((item) => {
  return item.visible;
});
```

Memoize only when needed:

```js
const visibleItems = useMemo(() => {
  return items.filter((item) => item.visible);
}, [items]);
```

Vue:

```js
const visibleItems = computed(() => {
  return items.value.filter((item) => item.visible);
});
```

Senior intuition: duplicated derived state converts calculation into synchronization.

---

## Rendering Performance

Rendering gets slow when:

- too many components rerender
- expensive calculations run during render
- large lists render all rows
- object/function identities change unnecessarily
- context/global state invalidates broad trees
- DOM layout work is forced repeatedly
- data fetching waterfalls delay render

Common fixes:

```text
move state down
  reduce rerender scope

split components by responsibility
  isolate change frequency

memoize expensive calculations
  avoid repeating CPU work

virtualize large lists
  render visible rows only

normalize server data
  avoid expensive nested updates

use framework data loading well
  avoid waterfalls
```

Senior rule: do not memoize randomly. First identify whether the cost is render frequency, render cost, DOM cost, network wait, or perception.

---

## The One-Sentence Model

Reactivity is dependency management over time; rendering is the scheduled work of turning changed state into changed pixels.
