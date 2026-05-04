# 06 - Vue Composition Patterns and Tricks

> Why this file matters to you as a senior dev: the previous doc was the engine. This one is the steering wheel. These are the patterns and levers you can pull at work this week to make Vue code feel cleaner, faster, and easier to maintain. Each section is something I'd recommend pushing in code review.

---

## Composables: think "reusable reactive logic", not "mixins reborn"

A composable is a function that returns reactive state and the operations to mutate it. The shape that scales is **return refs and methods, never the raw reactive object**.

```js
// composables/useCounter.js
import { ref, computed } from 'vue';

export function useCounter(initial = 0) {
  const count = ref(initial);
  const isZero = computed(() => count.value === 0);

  function increment() { count.value += 1; }
  function reset() { count.value = initial; }

  return { count, isZero, increment, reset };
}
```

In a component:

```js
const { count, increment } = useCounter(10);
```

This destructures cleanly because `count` is a ref. The reactivity survives the destructure.

> 💡 Insight - composables are just functions. Their power is not in any framework magic; it's that reactive primitives (`ref`, `reactive`, `computed`, `watch`) work outside of components. You're sharing reactive logic the same way you share a utility function.

### Composable design checklist

When I review a composable, I check three things:

1. **Does it return refs (or computeds)?** If it returns a `reactive(...)`, destructuring breaks reactivity at the call site. Bad ergonomics.
2. **Does it own its lifecycle cleanup?** If the composable creates a timer, listener, or watcher, it must clean up itself. The escape hatch is `onScopeDispose`, which fires when the surrounding effect scope is destroyed (component unmount, in most cases).
3. **Is the input shape flexible?** Accepting refs as inputs (or `MaybeRef<T>` if you're typing it) makes the composable usable in more contexts.

```js
// Listener composable that cleans up after itself.
import { onScopeDispose } from 'vue';

export function useEventListener(target, event, handler) {
  target.addEventListener(event, handler);
  onScopeDispose(() => target.removeEventListener(event, handler));
}
```

> ⚠️ Trap - composables called outside `setup()` (or before await in async setup) lose access to the component's effect scope. Lifecycle hooks like `onMounted` silently no-op. This is the #1 reason "my composable doesn't run its cleanup".

---

## The watch family: pick the right one

Vue gives you four ways to react to changes. They differ in what they track and when they flush.

| API                   | Tracks                              | Flush timing       | Initial run? |
|-----------------------|-------------------------------------|--------------------|--------------|
| `watch(src, cb)`      | Explicit source(s)                  | Pre-render (default) | No           |
| `watchEffect(cb)`     | Anything reactive read inside       | Pre-render         | Yes          |
| `watchPostEffect(cb)` | Anything reactive read inside       | Post-render        | Yes          |
| `watchSyncEffect(cb)` | Anything reactive read inside       | Sync (immediate)   | Yes          |

The senior framing:

- Use `watch` when you know exactly what you're watching. It's explicit and does not run on mount unless you pass `{ immediate: true }`.
- Use `watchEffect` when the dependencies are obvious from the body and you'd duplicate them in the source list. It auto-tracks.
- Use `watchPostEffect` when you need the DOM to be updated before your callback runs (measure layout, focus an input that just appeared).
- Use `watchSyncEffect` rarely. It defeats batching. Reserve for cases where you genuinely need synchronous reaction.

```js
// Need the DOM updated first.
watchPostEffect(() => {
  if (input.value && shouldFocus.value) {
    input.value.focus();
  }
});
```

> ⚠️ Trap - `watch(refValue, cb)` watches a ref. `watch(() => obj.value, cb)` watches via getter. If you watch `obj.value` directly without the getter, you're passing a stale snapshot, and changes won't fire. When in doubt, use the getter form.

---

## Computed vs watch: the deciding question

Both can react to changes. The deciding question:

> Am I producing a value, or am I causing a side effect?

Producing a value: `computed`. Side effect: `watch` (or `watchEffect`).

```js
// Producing a value: computed.
const total = computed(() => items.value.reduce((s, i) => s + i.price, 0));

// Causing a side effect (analytics): watch.
watch(total, (newTotal) => {
  trackEvent('cart_total_changed', { total: newTotal });
});
```

If you find yourself writing a `watch` whose only job is `someRef.value = derivedExpression`, replace it with `computed`. The watch version is strictly worse: eager, less cache, more code.

---

## Ref unwrapping: the rules people forget

Auto-unwrapping is convenient until it isn't. The rules:

```js
const count = ref(0);

// In templates: auto-unwrapped.
{{ count }}             // works, prints 0

// In setup() return value, accessed in template: auto-unwrapped.
return { count };       // template can use {{ count }}

// In JS: NEVER auto-unwrapped. Always .value.
console.log(count);      // logs the ref object
console.log(count.value); // logs 0
```

Two places that catch people:

**Refs inside reactive objects are unwrapped.**

```js
const count = ref(0);
const state = reactive({ count });
console.log(state.count);   // 0, not the ref object
```

**Refs inside arrays or Maps are NOT unwrapped.**

```js
const items = reactive([ref(0), ref(1)]);
console.log(items[0]);      // the ref object, not 0
console.log(items[0].value); // 0
```

The rule of thumb: only the direct properties of a `reactive` object unwrap refs. Anything one layer deeper (array elements, nested Maps) does not.

> 💡 Insight - when this trips you up, the diagnostic is "where is the auto-unwrap supposed to fire?" If your value is sitting inside a Map, an Array, or a non-reactive object, there's nobody to do the unwrap. Use `.value` explicitly.

---

## shallowRef and shallowReactive: opt out of deep tracking

Vue's deep tracking is great until you hand it a 50,000-row table or a non-reactive third-party instance (a Map, a chart library object, a Proxy from another system).

`shallowRef` makes the `.value` reactive but doesn't recurse into it. `shallowReactive` makes the top-level keys reactive but doesn't recurse.

```js
// Deep reactive: every cell of every row tracked. Pricey.
const tableData = ref(largeDataset);

// Shallow: only the assignment of tableData.value is reactive.
const tableData = shallowRef(largeDataset);

// Mutate via reassignment, not in-place:
tableData.value = [...tableData.value, newRow];
```

The trade-off is mutability ergonomics. Deep tracking lets you `tableData.value[0].name = 'X'` and the UI updates. Shallow forces you to replace the array (or specific row) to trigger reactivity.

For large datasets where you control mutations through a single seam (a setter function, a Pinia action), shallow is a huge win.

```js
// Even more aggressive: never proxy this object.
const chartInstance = markRaw(createChart(canvas));
```

`markRaw` permanently flags an object as non-reactive. Useful for class instances, third-party objects, and anything you really don't want Vue to wrap.

> ⚠️ Trap - `markRaw` is permanent. Once marked, the object cannot become reactive again, even if you put it in a `reactive()`. Use it for things that genuinely don't belong in the reactive system.

---

## v-memo and v-once: skip work the framework can't skip alone

The compiler optimizes static parts automatically. But sometimes you have **dynamic-but-stable** parts: a list row whose content depends on props, but those props haven't changed.

`v-memo` is "skip patching this subtree if these dependencies are unchanged".

```html
<div v-for="item in items" :key="item.id" v-memo="[item.id, item.selected]">
  <!-- big subtree -->
</div>
```

If `item.id` and `item.selected` are the same as last render, Vue skips the entire diff for that row, even if the parent re-rendered.

`v-once` is "render this subtree once, then never update it".

```html
<header v-once>
  <h1>{{ user.name }}</h1>
</header>
```

After the first render, this block is frozen. Use only when you're certain the data won't change.

> 💡 Insight - for long lists with stable rows, `v-memo` can be a 10x perf win. The cost is one array allocation per row per render and the dep comparison. Only worth it for non-trivial subtrees.

---

## provide/inject as scoped DI

Props go top-down, one parent at a time. When you need to push a value through many layers, prop drilling is annoying. `provide`/`inject` lets a component publish a value to its descendants.

```js
// Parent
provide('theme', themeRef);

// Deep child
const theme = inject('theme');
```

Two pieces of senior advice:

**Use Symbols for keys, not strings.** Strings collide. Symbols don't.

```js
// keys.js
export const ThemeKey = Symbol('theme');

// Parent
provide(ThemeKey, themeRef);

// Child
const theme = inject(ThemeKey);
```

**Provide refs, not raw values.** If you provide a primitive, it's a snapshot; the child won't see updates. Provide a ref or a reactive object.

```js
provide(ThemeKey, ref('dark'));   // good, reactive
provide(ThemeKey, 'dark');        // bad, frozen value
```

For "should I use provide/inject or Pinia?", the heuristic: provide/inject for things scoped to a component subtree (a form's validation context, a panel's theme override). Pinia for app-wide state.

---

## Effect scopes: cleanup as a primitive

Vue's `effectScope` is the lower-level primitive behind component lifecycle cleanup. Useful when you're managing reactive state outside of components (e.g., a singleton service, a long-lived store).

```js
import { effectScope } from 'vue';

const scope = effectScope();

scope.run(() => {
  // any watch, watchEffect, computed created here is owned by the scope
  watchEffect(() => sync(state));
});

// later:
scope.stop();   // stops every effect inside the scope
```

Pinia uses this internally. So do plenty of advanced composables. If you ever need "create a bunch of reactive things and dispose them together", effect scopes are the answer.

---

## When Pinia beats composables, and vice versa

Both can hold state. Both are reactive. The deciding factors:

**Use a composable when:**
- The state is local to a feature, page, or component subtree.
- Each consumer should get its own instance (a `useForm()` per form).
- The logic doesn't need devtools, time travel, or cross-feature subscriptions.

**Use Pinia when:**
- The state is genuinely app-wide (auth, current user, theme).
- Multiple unrelated parts of the app read and write it.
- You want a single source of truth that survives re-mounts.
- You want devtools integration and store-level testing helpers.

The mistake I see: people start with Pinia because it's "the state library" and end up with stores for things that are local UI concerns. The result is that `$reset` becomes a chore, every store is global, and the file count explodes.

> 💡 Insight - a composable that returns the same instance on every call (a singleton) is functionally a Pinia store without the devtools. If you want app-wide singleton state, use Pinia. The devtools alone usually pay for it.

---

## A small bag of tricks worth adopting

**`toRefs` for splitting a reactive object cleanly:**

```js
const state = reactive({ count: 0, name: 'A' });
return { ...toRefs(state), increment };  // template can use count and name as refs
```

**`unref` when you don't know if you got a ref or a value:**

```js
function describe(x) {
  return `Value: ${unref(x)}`;
}
```

**`computed` with a setter for two-way derived state:**

```js
const fullName = computed({
  get: () => `${first.value} ${last.value}`,
  set: (val) => {
    [first.value, last.value] = val.split(' ');
  },
});
```

Useful when you bind a form input to a derived value and want edits to flow back.

**Async setup with `<script setup>` and Suspense:**

```vue
<script setup>
const data = await fetchData();
</script>
```

Wraps in a Suspense boundary in the parent. Top-level await in setup is a real feature, not a hack.

---

## What to carry forward

- Composables are reusable reactive logic. Return refs, own your cleanup with `onScopeDispose`, design for flexible inputs.
- Pick from the watch family by what you're tracking and when you need to flush. `computed` for derived values, `watch` for side effects.
- Auto-unwrapping is local to direct properties of `reactive` objects and template scope. Everywhere else, reach for `.value`.
- `shallowRef`, `shallowReactive`, and `markRaw` are escape hatches for big or non-reactive data. `v-memo` and `v-once` are escape hatches for repeated render work.
- Provide/inject for scoped DI; Pinia for app-wide state. Composables should be the first tool, stores the second.
