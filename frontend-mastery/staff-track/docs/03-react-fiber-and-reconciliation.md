# 03 - React, Fiber, and Reconciliation

> Why this file matters to you as a senior dev: you don't write React day-to-day, but when you do touch it (or review it, or migrate from it), the difference between guessing and knowing comes down to one mental model: render is a tree-diffing algorithm, and Fiber is the data structure that makes it pausable. Get those two right and most React advice clicks into place.

---

## What "reconciliation" actually means

When you call `setState`, React doesn't immediately touch the DOM. It builds a new tree of what the UI *should* look like, compares it against the old tree, and figures out the smallest set of DOM operations that gets you from old to new.

That comparison is **reconciliation**. The output of reconciliation is a list of side effects ("update this text node", "insert this element", "remove this listener"). The DOM is only touched when React applies those effects.

```text
  state changes
       |
       v
  build new element tree (render phase)
       |
       v
  diff against current tree
       |
       v
  produce list of effects
       |
       v
  apply effects to the DOM (commit phase)
```

Two phases. Render is pure and can be thrown away. Commit is the only phase that mutates the DOM.

> 💡 Insight - render being pure is not a stylistic preference. It's the contract that lets React abandon a render mid-flight if a more important update comes in. Write side effects in render and concurrent mode breaks for you.

---

## Why Fiber replaced the old reconciler

Pre-2017, React's reconciler was recursive. It walked the tree top-down, calling each component's render function on the call stack. That meant once a render started, it had to finish synchronously. A heavy tree could block the main thread for hundreds of milliseconds.

Fiber is a rewrite that turns reconciliation into a **work loop over a linked list of nodes** (called fibers). Instead of recursing, React picks a fiber, does some work on it, and then chooses whether to continue or yield.

```text
          Stack reconciler                     Fiber reconciler

   render(A)                                fiber A -> work -> next
     render(B)                                fiber B -> work -> next
       render(C)                              fiber C -> work -> yield?
       render(D)                              fiber D -> work -> next
     render(E)                                ...

   Synchronous, can't yield               Iterative, can pause
```

The win is not raw speed. It's **interruptibility**. React can do part of the work, check whether something more urgent came in (a click, a higher-priority lane), and either continue or restart.

---

## What a Fiber actually is

A fiber is a JavaScript object representing one unit of work for one component instance. Roughly:

```js
{
  type: 'function or string or class',
  stateNode: 'the DOM node or instance',

  return: parentFiber,         // up the tree
  child: firstChildFiber,      // down
  sibling: nextSiblingFiber,   // across

  pendingProps: {},            // the new props
  memoizedProps: {},           // props from last commit
  memoizedState: hooksList,    // for function components, the linked list of hooks
  alternate: workInProgressOrCurrent,

  effectTag: 'Placement | Update | Deletion | ...',
  // ...lots more
}
```

That `return`/`child`/`sibling` shape is the linked list React walks. It's not a literal flat list, it's a tree, but the pointers let React traverse it without recursion.

The `alternate` pointer is the one that unlocks **double buffering**. Every committed fiber has a counterpart being built (the work-in-progress, often called WIP). When commit happens, React swaps which one is current.

```text
          current tree                  workInProgress tree

   App  <-----alternate----->   App'
    |                            |
   Page <-----alternate----->   Page'
    |                            |
   List <-----alternate----->   List'
```

Render mutates the WIP tree. Current tree is untouched until commit. If render gets thrown away mid-flight, the current tree is still valid and the user sees no flicker.

> 🔍 Under the Hood - `useState`'s "previous state" is read from `current`'s memoizedState. The "next state" gets written into `workInProgress`'s memoizedState. That's why you can dispatch multiple updates in one event and React processes them as a queue against a fresh starting state.

---

## Render phase: walking the tree

React's work loop, simplified:

```js
function workLoop() {
  while (workInProgress !== null && shouldContinue()) {
    workInProgress = performUnitOfWork(workInProgress);
  }
}

function performUnitOfWork(fiber) {
  // Call the component, produce children, attach them.
  const next = beginWork(fiber);
  if (next !== null) return next;

  // No more children, walk back up via siblings or return.
  return completeWork(fiber);
}
```

For each fiber, `beginWork` calls the component (for function components, this is invoking your function and running its hooks). The output is the new children. React attaches them as new fibers in the WIP tree.

`completeWork` is where React records what changed: did the props differ? Did children get added or removed? It builds the **effect list**, which is the queue of mutations to apply later.

`shouldContinue` is the interruption point. In concurrent mode, React checks if there's a higher-priority update or if the browser needs the main thread. If yes, the work loop stops and resumes later.

> ⚠️ Trap - "render phase" is not the moment your DOM updates. It's the moment your component function runs. Logging, mutating state, or throwing an effect into render runs at the wrong time and breaks concurrent rendering.

---

## Commit phase: the only phase that touches the DOM

After the WIP tree is fully built and React has its effect list, it commits. Commit is **synchronous and uninterruptible**. Three sub-phases:

```text
1. before mutation: snapshot DOM state if needed (getSnapshotBeforeUpdate, etc.)
2. mutation:        apply DOM changes (insert, update, delete)
3. layout:          run layout effects (useLayoutEffect, refs)

   browser paints

4. passive effects: run useEffect (after paint)
```

`useLayoutEffect` runs synchronously between mutation and paint. That's why it can read measurements and write back to state without flicker, but it also blocks the browser from painting until you're done. Use sparingly.

`useEffect` runs after paint, asynchronously. It does not block the user from seeing the updated UI.

```text
                 commit phase                              after paint
   |---------------------------------|
   | mutate DOM | run layout effects |   <- browser paints   | run passive effects |
   |---------------------------------|                       |---------------------|
                                   user sees update here
```

> 💡 Insight - if you `setState` inside `useLayoutEffect`, React performs an extra synchronous render before painting. That's how you get "measure then resize" without flicker, and also how you accidentally double your render work for every commit.

---

## Diffing is heuristic, not optimal

The "compare two trees" problem is O(n^3) in the general case. React cheats: it makes two assumptions that turn it into O(n).

**Assumption 1: different types produce different trees.** If a `<div>` becomes a `<span>`, React doesn't try to match them. It tears down the old tree and builds the new one from scratch. Children's state is destroyed.

**Assumption 2: keys identify which children are which.** When you render a list, React needs to match old children to new children. By default it matches by index. If you pass a `key`, it matches by key.

```jsx
// Without keys: React matches by index.
// Inserting at the start triggers a cascade of "this index now has different content".
[<Row a/>, <Row b/>] -> [<Row c/>, <Row a/>, <Row b/>]
//  index 0    index 1     index 0    index 1    index 2
//  (a -> c, content changed)  (b -> a, content changed)  (insert b)

// With stable keys: React matches by id.
[<Row key="a"/>, <Row key="b"/>] -> [<Row key="c"/>, <Row key="a"/>, <Row key="b"/>]
//  React sees: "c is new, a and b are the same nodes, just reordered"
```

> ⚠️ Trap - using array index as a key is fine when the list never reorders. The moment it does, child component state and DOM identity stick to the wrong rows. This is the classic "form field carries the wrong value after delete" bug.

---

## Component identity is what preserves state

Hooks, refs, and any state inside a component live on the fiber. The fiber is identified by its position in the tree plus its type plus its key.

If any of those change between renders, React treats it as a different component. State resets, refs detach, effects re-run from scratch.

```jsx
// Conditionally swap components: state lost
{isAdmin ? <AdminPanel /> : <UserPanel />}

// Same component, conditional behavior: state preserved
<Panel mode={isAdmin ? 'admin' : 'user'} />
```

Both render different UI. The first one resets state every time `isAdmin` flips. The second keeps state.

> 💡 Insight - "I want to reset child state when a prop changes" is a real use case, and the idiomatic way to do it is to put that prop in the `key`. Changing the key is the supported way to force React to treat it as a new component.

---

## Why React is sometimes slow, in one mental model

Whenever React is "slow", trace it to one of:

1. **Too many fibers being walked.** Big lists rendered without virtualization.
2. **Component functions doing too much work.** Heavy computation in render, called every render.
3. **Identity churn.** New objects/functions every render cause memoized children to invalidate, forcing them to re-render too.
4. **Commit work too large.** A single render produces hundreds of DOM mutations because keys are wrong or component types changed.
5. **useLayoutEffect chains.** Synchronous post-mutation work that delays paint.

`React.memo`, `useMemo`, and `useCallback` are surgical tools for cases 2 and 3. They are not "make React faster" buttons; they're "stabilize this identity so something downstream doesn't invalidate".

```jsx
// Without memo, options is a new object every render of Parent.
// Child's useEffect([options]) runs every render. Bad.
function Parent() {
  return <Child options={{ sort: 'name' }} />;
}

// Stabilize identity.
function Parent() {
  const options = useMemo(() => ({ sort: 'name' }), []);
  return <Child options={options} />;
}
```

> 🔍 Under the Hood - `React.memo` wraps a component so that its `beginWork` short-circuits if all props are referentially equal to last time. The diff still happens at the parent; you're just preventing the child's render function from running.

---

## When state placement is the real fix

Performance fixes via memoization are a last resort. The real fix is usually **moving state down**.

```jsx
// Hover state at the page level: every hover re-renders the chart.
function Page() {
  const [hoveredId, setHoveredId] = useState(null);
  return (
    <>
      <ExpensiveChart />
      <Table onHover={setHoveredId} hoveredId={hoveredId} />
    </>
  );
}

// Hover state inside the table: chart untouched.
function Page() {
  return (
    <>
      <ExpensiveChart />
      <Table />
    </>
  );
}
```

If the chart doesn't need to know about hover, hover doesn't belong at the page level. The whole memoization conversation evaporates.

> Interesting fact: most "we need React.memo everywhere" arguments dissolve when you audit state placement first. State at the right level is the cheapest perf optimization there is.

---

## What to carry forward

- React reconciliation is a tree diff. Render is pure and can be discarded; commit is the only phase that mutates the DOM.
- Fiber is a linked-list-of-objects representation that makes the work loop pausable. Concurrent rendering exists because Fiber can yield.
- Double buffering (`current` and `workInProgress`) is why React can throw away a render mid-flight without flicker.
- Diffing relies on two assumptions: type identity and key identity. Violate them and state migrates to the wrong children.
- The cheapest perf fix is moving state down. Memoization is for when that's not possible, not as a default.
