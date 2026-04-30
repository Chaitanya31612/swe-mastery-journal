# 03 - React, Next, And Vue Differentiation

This doc is not a feature list. It is the senior comparison: what each tool is optimizing for, what mental model it asks from you, and what trade-offs become visible under pressure.

---

## The Core Distinction

React, Vue, and Next are not three equal categories.

```text
React
  UI library for describing interfaces with components.

Vue
  Progressive framework for building interfaces with component-level reactivity.

Next.js
  Application framework built around React, routing, rendering modes, server/client boundaries, and deployment concerns.
```

So the real comparison is:

```text
React vs Vue
  component and reactivity model

React app vs Next app
  client app architecture vs full-stack rendering architecture

Vue app vs Next app
  client-first progressive framework vs React-based server-aware application framework
```

Senior intuition: comparing React to Next is like comparing an engine to a car platform.

---

## The Same Counter In Three Mental Models

### React

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount((value) => value + 1)}>
      {count}
    </button>
  );
}
```

Mental model:

```text
set state
  -> component rerenders
  -> React calculates next UI
  -> React commits changed DOM
```

### Vue

```vue
<script setup>
import { ref } from 'vue';

const count = ref(0);
</script>

<template>
  <button @click="count += 1">
    {{ count }}
  </button>
</template>
```

Mental model:

```text
mutate reactive value
  -> Vue triggers effects that read it
  -> Vue patches changed DOM
```

### Next

```jsx
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount((value) => value + 1)}>
      {count}
    </button>
  );
}
```

Mental model:

```text
this component must run in the browser because it has state and click handling
```

Next adds a placement decision:

```text
Does this code belong on the server, client, or both?
```

---

## React's Under-The-Hood Workflow

React is centered around render purity and scheduling.

```text
event or update source
  -> update is queued
  -> React schedules work
  -> component functions run
  -> React builds next element tree
  -> reconciliation compares previous and next trees
  -> commit mutates host environment
  -> effects run at the appropriate time
```

React's power:

- components are plain functions of props and state
- data flow is explicit
- composition scales well
- scheduling model can prioritize urgent and non-urgent work
- render targets can be DOM, native, terminal, canvas-like custom renderers

React's cost:

- rerender scope can be broad
- identity matters a lot
- effect misuse creates loops and stale state
- local ergonomics depend heavily on conventions and libraries
- architecture is not included by default

React senior choices:

```text
Where should state live?
What render work happens when it changes?
Is this effect really synchronization?
Is this object/function identity meaningful?
Should this update be urgent or transition-like?
Is this server state being treated as client state?
```

---

## Vue's Under-The-Hood Workflow

Vue is centered around dependency tracking and compiler-assisted ergonomics.

```text
component setup runs
  -> reactive state is created
  -> template compiles to render function
  -> render effect reads reactive values
  -> Vue records dependencies
  -> reactive mutation triggers dependent effects
  -> scheduler batches updates
  -> virtual DOM patch updates DOM
```

Vue's power:

- reactive dependencies are tracked automatically
- templates make UI structure readable
- computed values and watchers map cleanly to common needs
- single-file components keep template, logic, and style close
- local productivity is high

Vue's cost:

- proxies can make identity and destructuring surprising
- automatic tracking can hide dependency edges
- watchers are easy to overuse
- large apps still need strict state and module boundaries
- template magic can obscure generated render behavior

Vue senior choices:

```text
Should this be ref, reactive, computed, or plain value?
Should this be computed or watch?
Am I destructuring away reactivity?
Is mutation local and clear, or should state ownership move?
Is this dependency implicit enough to surprise maintainers?
```

---

## Next's Under-The-Hood Workflow

Next is React plus application infrastructure.

The main added model is boundaries:

```text
server
  can access databases, private environment variables, server caches
  cannot use browser-only APIs or event handlers

client
  can handle clicks, local state, effects, browser APIs
  ships JavaScript to the browser

network boundary
  server output must be serialized to client-compatible data
```

In App Router style architecture, the default mindset is:

```text
render as much as possible on the server
move only interactive leaves to the client
```

Workflow:

```text
request route
  -> server resolves route segments
  -> server components fetch/render where allowed
  -> output streams to browser
  -> client components hydrate
  -> user interactions run in browser
```

Next's power:

- routing and layouts are built into architecture
- server rendering is first-class
- streaming can reduce waiting on slow data
- server components reduce client JavaScript for non-interactive UI
- data placement becomes explicit

Next's cost:

- caching layers can be confusing
- server/client boundaries require discipline
- hydration and serialization constraints surface often
- debugging spans server, browser, build, and deployment
- accidental client components can bloat bundles

Next senior choices:

```text
Can this component stay server-only?
Where is the data fetched and cached?
Is this personalized, static, dynamic, or revalidated?
Does this value cross the server/client boundary safely?
Is this loading state route-level, component-level, or optimistic?
```

---

## React Versus Vue: Change Detection

React:

```text
You tell React state changed.
React reruns components.
React compares output.
```

Vue:

```text
Vue tracks what reactive values were read.
You mutate reactive values.
Vue reruns dependent effects.
```

Example implication:

```js
// React
setUser({ ...user, name: 'Nia' });
```

```js
// Vue
user.name = 'Nia';
```

React optimizes through:

- component boundaries
- memoization
- keys
- scheduler
- avoiding unnecessary state lifting

Vue optimizes through:

- dependency tracking
- computed caching
- compiler hints
- stable template structure
- targeted update scheduling

Senior intuition: React is explicit and broad by default. Vue is implicit and targeted by default.

---

## React Versus Vue: Lifecycle Feel

React:

```text
render function runs often
effects synchronize after commit
cleanup happens before next effect or unmount
```

Vue:

```text
setup creates component state once
template/render effect tracks dependencies
lifecycle hooks describe mounted/unmounted timing
watchers react to dependency changes
```

React asks:

```text
What should UI be for this state?
```

Vue asks:

```text
Which reactive dependencies should update which effects?
```

Neither is superior in the abstract.

React makes dependency and data flow explicit. Vue reduces ceremony by tracking more for you.

---

## React App Versus Next App

A plain React app often starts client-first:

```text
load JS
render app shell
fetch data
render content
handle routes in browser
```

A Next app can start server-first:

```text
request URL
server renders route
stream HTML or RSC payload
hydrate interactive parts
continue client navigation
```

Choose client-first React when:

- app is mostly authenticated dashboard
- SEO is irrelevant
- deployment simplicity matters
- rich client state dominates
- backend already provides APIs cleanly

Choose Next-style architecture when:

- first content matters
- route-level data loading matters
- SEO/share previews matter
- server and UI are tightly related
- you want layouts, routing, rendering modes, and data placement conventions

Pushback: do not choose Next just because it is "more advanced". If every screen is behind auth, data is highly dynamic, SEO is irrelevant, and your team does not understand the cache model, plain React can be simpler.

---

## Server Components In Plain English

A server component is UI code that renders on the server and does not ship as interactive JavaScript.

Good fit:

```jsx
async function ProductDetails({ productId }) {
  const product = await getProduct(productId);

  return (
    <section>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </section>
  );
}
```

Bad fit:

```jsx
function ProductDetails() {
  const [isOpen, setIsOpen] = useState(false);

  return <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>;
}
```

That needs the client.

Mental model:

```text
server components fetch and prepare UI
client components interact and manage browser state
```

Trade-off:

```text
less client JavaScript
  but stronger boundary rules
```

Senior intuition: Server Components are not "React but faster". They are a different placement model for component work.

---

## Common Wrong Choices

### Lifting State Too High

Bad:

```text
App owns modal hover state
```

Impact:

```text
tiny interaction invalidates huge subtree
```

Better:

```text
keep state at the lowest owner that needs to coordinate it
```

### Making Everything Global

Bad:

```text
global store owns form field text
```

Impact:

```text
temporary local edits become app-wide synchronization
```

Better:

```text
form owns draft state
server/cache owns saved state
```

### Using Effects As Data Flow

Bad:

```text
prop changes -> effect copies prop to state -> second effect reacts to copied state
```

Better:

```text
derive directly or create a clear reducer/state machine
```

### Client Component By Accident

Bad in Next:

```text
top layout becomes client because one tiny child needs click state
```

Impact:

```text
too much JavaScript ships
```

Better:

```text
keep layout server-side and isolate interactive leaf
```

---

## Decision Map

```text
Need mostly interactive authenticated dashboard?
  React or Vue SPA can be excellent.

Need content pages, SEO, server data, streaming, and route conventions?
  Next is a strong fit.

Team values explicit JavaScript and ecosystem flexibility?
  React is a strong fit.

Team values integrated ergonomics and reactive templates?
  Vue is a strong fit.

Need strict server/client placement and reduced client JS?
  Next with server-first discipline.

Need simple deployable widget or internal tool?
  Do not over-framework it.
```

---

## Senior Comparison Table

```text
Concern                 React                         Vue                           Next
------------------------------------------------------------------------------------------------
Category                UI library                    Progressive framework          React app framework
Change model            scheduled rerender            dependency tracking            React plus server/client placement
Default state style     immutable replacement          reactive mutation              depends on boundary
Architecture included   minimal                        moderate                       high
Routing                 external                      official router common          built in
Server rendering        possible via frameworks        possible via frameworks        first-class
Main risk               effect and rerender misuse     hidden reactive coupling        cache and boundary confusion
Best skill              state ownership                reactivity discipline           data placement
```

---

## The One-Sentence Model

React teaches explicit render thinking, Vue teaches dependency-tracked reactivity, and Next teaches server/client placement as an architectural decision.
