# 05 - Vue Reactivity and Compiler Internals

> Why this file matters to you as a senior dev: Vue is your daily driver. The reactivity system is the single most impactful thing to actually understand, because every weird bug, every "why didn't this update", and every performance question routes through it. Once you can sketch `track`/`trigger` on a whiteboard, Vue stops surprising you.

---

## The two-line summary of Vue reactivity

When you read a reactive property during a tracked function, Vue records "this function depends on this property". When you write that property, Vue re-runs every function that depends on it.

That's it. Everything in Vue 3 reactivity (refs, computed, watch, render effects) is built on those two operations: **track** on read, **trigger** on write.

```text
   read state.count    ->  track(state, 'count', activeEffect)
   write state.count   ->  trigger(state, 'count')  -> re-run dependent effects
```

If you can hold that picture, the rest is implementation detail.

---

## reactive(), implemented in 30 lines

A working sketch of `reactive`:

```js
let activeEffect = null;
const targetMap = new WeakMap();  // target -> Map<key, Set<effect>>

function track(target, key) {
  if (!activeEffect) return;
  let depsMap = targetMap.get(target);
  if (!depsMap) targetMap.set(target, (depsMap = new Map()));
  let dep = depsMap.get(key);
  if (!dep) depsMap.set(key, (dep = new Set()));
  dep.add(activeEffect);
}

function trigger(target, key) {
  const dep = targetMap.get(target)?.get(key);
  if (dep) dep.forEach((effect) => effect());
}

function reactive(target) {
  return new Proxy(target, {
    get(obj, key, receiver) {
      track(obj, key);
      const value = Reflect.get(obj, key, receiver);
      return typeof value === 'object' && value !== null ? reactive(value) : value;
    },
    set(obj, key, value, receiver) {
      const ok = Reflect.set(obj, key, value, receiver);
      trigger(obj, key);
      return ok;
    },
  });
}

function effect(fn) {
  activeEffect = fn;
  fn();
  activeEffect = null;
}
```

The `targetMap` is the dependency graph. The `Proxy` is what intercepts reads and writes so we can track and trigger. The `effect` wrapper is what makes "the currently running function" available to `track`.

That's the engine. Vue's real implementation is more polished (deep tracking, scheduler, dirty-checking for computed, effect scopes) but every concept lives in this 30-line sketch.

> 💡 Insight - Vue's reactivity has nothing to do with components. It's a standalone library (`@vue/reactivity`). You can use it in plain JS. Components are just one consumer that wraps their render function in an `effect`.

---

## Why Vue 3 changed from Vue 2's defineProperty

Vue 2 used `Object.defineProperty` to install getter/setter pairs on every property of every reactive object, recursively, **at object creation time**. Three consequences you've probably hit:

1. Adding new properties later didn't trigger reactivity. You needed `Vue.set(obj, key, value)`.
2. Array index assignments (`arr[0] = ...`) and length changes didn't trigger reactivity. You needed mutating methods (`.push`, `.splice`) which Vue 2 patched.
3. The whole tree was walked eagerly, even properties never read. Big objects = big upfront cost.

Vue 3 uses `Proxy`. A proxy intercepts **all** property access, including new keys and array operations. It's lazy: child objects are only wrapped reactive when you actually access them (the `get` handler does the recursion).

```js
// Vue 2 hurts:
const state = Vue.observable({ a: 1 });
state.b = 2;            // not reactive

// Vue 3 just works:
const state = reactive({ a: 1 });
state.b = 2;            // reactive
```

> 🔍 Under the Hood - `Proxy` is a built-in JS feature, not a Vue invention. Vue 3 piggybacks on the language; Vue 2 had to fight it. This is also why Vue 3 dropped IE11 support: no Proxy in IE.

---

## ref vs reactive: the distinction that actually matters

Two ways to make state reactive:

```js
const count = ref(0);
const state = reactive({ count: 0 });
```

They feel interchangeable for trivial cases. They aren't.

`reactive` only works on objects. It returns a Proxy. You access properties directly: `state.count`.

`ref` wraps any value (including primitives) in an object: `{ value }`. It's reactive on the `.value` property. Inside templates, the `.value` is auto-unwrapped. Inside JS, you write `count.value`.

The reason both exist: primitives can't be Proxy targets (no properties to intercept), so refs are the only way to make a primitive reactive. Once you have refs, the team chose to make them work for objects too, for ergonomics.

The trade-off in practice:

```js
// reactive: clean access, easy to lose reactivity by destructuring.
const state = reactive({ count: 0, name: 'A' });
const { count } = state;     // count is just a number now, not reactive!

// ref: extra .value, but reactivity survives reassignment.
const count = ref(0);
let copy = count;            // copy is the same ref; reactivity preserved.
```

> ⚠️ Trap - destructuring a `reactive` object pulls primitive values out. They become plain values, disconnected from reactivity. `toRefs(state)` solves this by returning an object whose properties are individual refs pointing back at the reactive source.

```js
const { count, name } = toRefs(state);   // count and name are now refs, still tied to state
```

The senior heuristic: **use refs by default**, especially for things you might destructure or pass around. Use `reactive` for grouped state that always stays grouped (form models, big objects).

---

## computed: cached, lazy, dirty-checked

`computed` is an effect with two extra rules: it caches its result, and it only re-runs when read after a dependency changed.

```js
const fullName = computed(() => `${first.value} ${last.value}`);
```

Sketch:

```text
   read fullName.value
       |
       v
   if dirty:  re-run getter, store result, mark clean
   else:      return cached result

   any dependency changes  ->  mark dirty (do not re-run yet)
```

Two implications:

- **Computed is cheap to read**, even thousands of times, as long as nothing changed.
- **Computed is lazy**. If nothing reads it, it doesn't run. If you change a dependency but nobody reads the computed, no work happens.

This is why "use computed for derived data" is the right default. You almost never need to manually cache.

```js
// Don't do this:
const fullName = ref('');
watch([first, last], () => {
  fullName.value = `${first.value} ${last.value}`;
});

// Do this:
const fullName = computed(() => `${first.value} ${last.value}`);
```

The watch version creates an extra reactive node (the ref), an extra effect, and runs eagerly even if nobody reads it. Computed avoids all three.

> 💡 Insight - if a computed depends on async data, it should depend on a ref that holds that data, not the in-flight promise. Reactivity tracks values, not promises. Mixing them is how you get "my computed is always undefined".

---

## The scheduler: why DOM updates aren't synchronous

When a reactive write happens, Vue doesn't immediately re-run effects. It queues them and flushes on the next microtask.

```js
state.count = 1;
state.count = 2;
state.count = 3;
console.log(button.textContent);   // still old value
```

The render effect was triggered three times but it's deduped in the queue. By the time the queue flushes (next microtask), only one render runs, with the final value.

```js
await nextTick();
console.log(button.textContent);   // now updated
```

`nextTick` is the API to wait for the next flush. It's literally `Promise.resolve()` plumbed through Vue's queue.

> 🔍 Under the Hood - Vue's queue has a flush phase ordering: pre (before render), sync (immediately, opt-in), post (after render). This is what `flush: 'post'` on watchers controls. We get into this in the patterns doc.

---

## The compiler: why Vue 3 templates are fast

Vue templates aren't interpreted at runtime. They're compiled to render functions at build time. The compiler does serious optimization that you should know about, because it changes how you should write templates.

### Static hoisting

Anything in a template that doesn't reference reactive state is **hoisted out of the render function**, allocated once, and reused on every render.

```html
<template>
  <div class="card">
    <h1>Static title</h1>
    <p>{{ message }}</p>
  </div>
</template>
```

Compiles to something like:

```js
// Hoisted once, never re-created:
const _hoisted_1 = createVNode('h1', null, 'Static title');

function render() {
  return createVNode('div', { class: 'card' }, [
    _hoisted_1,
    createVNode('p', null, message.value),  // only this part re-runs
  ]);
}
```

The static `<h1>` is allocated at module load, not per render.

### Patch flags

The compiler annotates each dynamic node with what specifically can change: text, class, style, props, full keyed children, etc.

```js
createVNode('p', { class: dynamicClass }, message.value, PatchFlag.CLASS | PatchFlag.TEXT)
```

At update time, Vue's runtime checks the flag and only diffs the marked attributes. If the flag is just `TEXT`, Vue updates the text content and skips everything else.

Compare to React, which has to diff all props and children to know what changed: Vue's compiler hands the runtime a cheat sheet, so the diff is a fraction of the work.

### Block tree

Vue groups nodes into "blocks" anchored at structural directives (`v-if`, `v-for`). Within a block, only nodes with patch flags need diffing; static nodes are skipped entirely. The block tree is flat (an array of dynamic descendants), so Vue iterates a small array instead of walking a deep tree.

```text
   Template tree                 Block tree (what Vue actually walks)

   div                            [ p (TEXT), span (CLASS) ]
   ├── h1 (static)
   ├── p {{ msg }}
   ├── footer (static)
   │   └── span :class
```

> 💡 Insight - this is why Vue's update path is often faster than React's for non-trivial templates. React diffs every node by structure. Vue diffs only the nodes the compiler flagged, in a flat list.

---

## What this means for how you write templates

Three real-world consequences:

1. **Static markup is free.** Don't worry about extracting "static parts" into separate components for perf. The compiler already does it.
2. **Computed and template expressions are fine.** Each expression becomes a dynamic patch slot; the rest of the template stays static.
3. **`v-if` vs `v-show` is a real choice.** `v-if` creates and destroys block boundaries; `v-show` keeps the DOM but toggles `display`. For frequently-toggled UI, `v-show` is cheaper. For rarely-shown heavy subtrees, `v-if` saves render and memory.

> ⚠️ Trap - `v-for` on an element that also has `v-if` is a known foot-gun. The order of evaluation isn't what you'd guess, and both directives are doing structural work. Wrap `v-for` in a `<template v-if>` parent if you need both.

---

## How components hook into reactivity

When a component renders for the first time, Vue wraps its render function in an effect. That effect:

1. Calls the render function, which reads reactive state, which calls `track`.
2. The effect is now subscribed to every reactive dependency the render touched.
3. If any of those dependencies trigger, the effect re-runs (after the scheduler dedupes).
4. The next render produces a new VDOM tree, which is patched against the previous one using the patch flags.

```text
   setup() runs once  ->  defines reactive state
   render effect runs  ->  reads state, tracks deps, produces VDOM
   state changes  ->  trigger  ->  scheduler queues render effect
   next microtask  ->  render runs again  ->  new VDOM  ->  patch
```

This is why **what you read in your template defines what triggers re-renders**. If your template doesn't read a piece of reactive state, that state changing doesn't re-render the component.

---

## What to carry forward

- Vue reactivity is two operations: `track` on read, `trigger` on write. Everything else is built on top.
- Vue 3's Proxy-based system fixes Vue 2's defineProperty limitations (new keys, array operations, eager walks).
- `ref` works on any value (including primitives) and survives destructuring; `reactive` is for grouped objects but loses reactivity if you destructure.
- `computed` is cached and lazy; prefer it over `watch` for derived values.
- The compiler's static hoisting, patch flags, and block tree are why Vue updates are surgical. You don't need to hand-optimize templates; the compiler already did.
