# 01 - JavaScript Runtime For Frontend

You already know JavaScript syntax. This doc is about the runtime model that explains frontend bugs: identity, closures, async scheduling, modules, memory, and TypeScript boundaries.

---

## The Core Idea

JavaScript in the browser is mostly:

```text
single call stack
heap of objects
event loop
task queues
microtask queue
browser APIs around it
```

It feels concurrent because the browser can do I/O, timers, rendering, and user input around your code.

But your JavaScript callback runs like this:

```text
start callback
  -> run to completion
  -> no other JS interrupts it
  -> microtasks run
  -> browser may render
```

Senior intuition: most frontend race conditions are not true thread races. They are ordering, ownership, cancellation, and stale closure problems.

---

## Values, References, And Identity

Primitive values compare by value:

```js
1 === 1; // true
'a' === 'a'; // true
```

Objects compare by identity:

```js
{} === {}; // false

const user = { id: 1 };
const sameUser = user;

user === sameUser; // true
```

Frameworks care deeply about identity.

React example:

```js
const visibleItems = items.filter((item) => item.visible);
```

Every render creates a new array. That is fine unless a child or memoized calculation depends on stable identity.

Vue example:

```js
const selectedUser = reactive({ id: 1 });
```

Vue wraps objects in proxies. The reactive proxy and raw object are not always identity-equivalent in the way you casually expect.

Senior rule: identity is a signal. Create new identity when meaning changed. Preserve identity when meaning did not.

---

## Mutation Versus Replacement

Mutation changes an existing object:

```js
user.name = 'Asha';
```

Replacement creates a new object:

```js
user = { ...user, name: 'Asha' };
```

React prefers replacement because state comparison and render scheduling depend on new references:

```js
setUser((previousUser) => ({
  ...previousUser,
  name: 'Asha',
}));
```

This is wrong in React state:

```js
user.name = 'Asha';
setUser(user);
```

The reference did not change, so React may treat it as no meaningful update.

Vue can track property mutation through proxies:

```js
const user = reactive({ name: 'Mira' });

user.name = 'Asha';
```

That is idiomatic Vue.

Senior intuition: React says "tell me state changed by giving me a new value." Vue says "I watched which reactive property was read, and I can trigger the dependents when it mutates."

---

## Closures

A closure is a function carrying access to variables from the scope where it was created.

```js
function createCounter() {
  let count = 0;

  return function increment() {
    count += 1;
    return count;
  };
}

const increment = createCounter();

increment(); // 1
increment(); // 2
```

In frontend code, closures are powerful and dangerous because UI changes over time.

Classic stale closure:

```js
function SearchBox() {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const timerId = setTimeout(() => {
      console.log(query);
    }, 1000);

    return () => clearTimeout(timerId);
  }, []);
}
```

The effect captures the initial `query` because the dependency array says the effect does not depend on anything.

Better:

```js
useEffect(() => {
  const timerId = setTimeout(() => {
    console.log(query);
  }, 1000);

  return () => clearTimeout(timerId);
}, [query]);
```

Senior intuition: every callback is a photograph of the variables at creation time.

---

## Tasks And Microtasks

Example:

```js
button.addEventListener('click', () => {
  console.log('click start');

  Promise.resolve().then(() => {
    console.log('microtask');
  });

  setTimeout(() => {
    console.log('timer');
  }, 0);

  console.log('click end');
});
```

Output after click:

```text
click start
click end
microtask
timer
```

Why it matters:

- promise callbacks run before timers
- a long microtask chain can delay rendering
- `await` splits a function into continuation work
- UI updates may batch inside the same event turn

Example:

```js
async function save() {
  setStatus('saving');

  await api.save();

  setStatus('saved');
}
```

This is not one continuous synchronous function. Everything after `await` resumes later.

Senior intuition: `await` improves reading order, not temporal simplicity.

---

## Race Conditions Without Threads

Search example:

```js
async function runSearch(query) {
  const results = await searchApi(query);

  setResults(results);
}
```

Bug:

```text
user types "r"
request A starts
user types "re"
request B starts
request B finishes first
UI shows "re"
request A finishes later
UI wrongly shows "r"
```

Better with request identity:

```js
let latestRequestId = 0;

async function runSearch(query) {
  latestRequestId += 1;
  const requestId = latestRequestId;

  const results = await searchApi(query);

  if (requestId !== latestRequestId) {
    return;
  }

  setResults(results);
}
```

Better with cancellation when the API supports it:

```js
const controller = new AbortController();

fetch('/search?q=reactivity', {
  signal: controller.signal,
});

controller.abort();
```

Senior rule: every async UI flow needs an answer for "what if this finishes after it is no longer relevant?"

---

## Debounce, Throttle, And Idle Work

Debounce waits for quiet:

```js
function debounce(callback, delayMs) {
  let timerId;

  return (...args) => {
    clearTimeout(timerId);

    timerId = setTimeout(() => {
      callback(...args);
    }, delayMs);
  };
}
```

Use debounce for:

- search after typing pauses
- autosave after edits settle
- resize work after resizing stops

Throttle limits frequency:

```js
function throttle(callback, delayMs) {
  let isWaiting = false;

  return (...args) => {
    if (isWaiting) {
      return;
    }

    callback(...args);
    isWaiting = true;

    setTimeout(() => {
      isWaiting = false;
    }, delayMs);
  };
}
```

Use throttle for:

- scroll position sampling
- pointer movement
- frequent telemetry that does not need every event

Senior intuition: debounce protects work from noise. Throttle protects frame budget from frequency.

---

## Modules And Bundle Shape

ES modules are statically analyzable:

```js
import { formatPrice } from './money.js';
```

That helps bundlers build dependency graphs.

Dynamic imports split code:

```js
const ChartPanel = lazy(() => import('./ChartPanel'));
```

Useful when:

- route is not visited by everyone
- component is heavy
- dependency is rare or admin-only
- below-the-fold interaction can wait

Bad split:

```text
Split every tiny component.
```

That creates too many requests, overhead, and loading states.

Good split:

```text
Split by route, heavy feature, permission boundary, or interaction boundary.
```

Senior intuition: bundles are product architecture made visible to the network.

---

## Memory Leaks In Frontend

Memory leaks usually come from retained references.

Common sources:

- event listeners not removed
- timers not cleared
- subscriptions not unsubscribed
- cached data with no eviction
- detached DOM nodes still referenced
- long-lived closures capturing large objects

Example:

```js
function mountPanel() {
  const panel = document.querySelector('.panel');

  window.addEventListener('resize', () => {
    panel.textContent = window.innerWidth;
  });
}
```

If the panel is removed, the resize callback still holds it.

Better:

```js
function mountPanel() {
  const panel = document.querySelector('.panel');

  function handleResize() {
    panel.textContent = window.innerWidth;
  }

  window.addEventListener('resize', handleResize);

  return function unmountPanel() {
    window.removeEventListener('resize', handleResize);
  };
}
```

Framework equivalent: clean up effects, watchers, subscriptions, observers, and timers.

---

## TypeScript Reality

TypeScript protects compile-time assumptions.

It does not prove runtime truth.

```ts
type User = {
  id: string;
  name: string;
};

const user = (await response.json()) as User;
```

This is a claim, not validation.

Better at external boundaries:

```ts
function parseUser(value: unknown): User {
  if (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  ) {
    const possibleUser = value as Record<string, unknown>;

    if (
      typeof possibleUser.id === 'string' &&
      typeof possibleUser.name === 'string'
    ) {
      return {
        id: possibleUser.id,
        name: possibleUser.name,
      };
    }
  }

  throw new Error('Invalid user payload');
}
```

Senior rule: TypeScript is strongest inside your codebase. Validate at boundaries: API, storage, URL, feature flags, postMessage, and third-party scripts.

---

## JavaScript Choices That Affect Frameworks

### Object Identity

```js
const options = { sort: 'name' };
```

If created inside a render function, this is new every render.

### Function Identity

```js
const handleClick = () => save(user.id);
```

This is also new every render unless stabilized.

### Derived State

Bad:

```js
const [fullName, setFullName] = useState('');
```

When `firstName` and `lastName` already exist, this creates synchronization work.

Better:

```js
const fullName = `${firstName} ${lastName}`;
```

### Async Lifetime

Every async operation may outlive:

- the component
- the route
- the user intent
- the auth session
- the data version it was based on

That is why cancellation and relevance checks matter.

---

## The One-Sentence Model

Frontend JavaScript is event-driven code where identity, closure timing, async ordering, and main-thread budget decide whether frameworks behave predictably.
