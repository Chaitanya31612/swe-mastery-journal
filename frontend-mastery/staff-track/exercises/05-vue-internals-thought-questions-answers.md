# 05 - Vue Reactivity and Compiler Internals: Answers

Companion to `05-vue-internals-thought-questions.md`.

---

## Q1: Reactivity vanishes after destructuring

The bug: `const { count, name } = state` reads `state.count` and `state.name` at that moment, getting the primitive values. Those primitives are returned to the template as plain `0` and `'A'`. Vue's reactivity tracks property access on the proxy; once you've extracted the value, there's no proxy involvement.

The interval mutates `state.count`, which triggers any effect that read `state.count` through the proxy. But the template never reads through the proxy; it reads the local primitive bindings. So the trigger has nothing to update.

Cleanest fix: `toRefs`.

```js
const state = reactive({ count: 0, name: 'A' });
const { count, name } = toRefs(state);
```

`toRefs` returns an object where each property is a ref pointing back at the corresponding property of the reactive source. Destructuring now gives you ref bindings, which Vue auto-unwraps in the template.

Anchored in `docs/05-vue-reactivity-and-compiler-internals.md` -> "ref vs reactive: the distinction that actually matters".

---

## Q2: Computed vs watch decision

The rewrite:

```js
function useFullName(first, last) {
  const fullName = computed(() => `${first.value} ${last.value}`);
  return { fullName };
}
```

Three concrete reasons it's strictly better:

1. **Lazy.** The watch version eagerly recomputes whenever `first` or `last` changes, even if no template ever reads `fullName`. The computed version only runs the getter when something actually reads `fullName.value`. If the consumer is conditionally rendered, you save the work.

2. **Cached.** A computed memoizes its last result. Reading `fullName.value` 50 times in a render reuses the last cached string. The watch version stores the string in a ref but doesn't memoize the computation; if you replaced the watch with manual reads in the template, you'd recompute every time. (For this simple expression that doesn't matter; for complex derivations it does.)

3. **Smaller surface area.** The watch version creates a ref + a watcher (two reactive primitives). The computed version is one primitive. Fewer moving parts, less to misuse.

The wrong answer often given: "but `watch` lets you do `immediate: true`, so it's the same". That confuses "fires on mount" with "lazy". `immediate` only changes the first-fire timing; it doesn't make watch lazy.

Anchored in `docs/05-vue-reactivity-and-compiler-internals.md` -> "computed: cached, lazy, dirty-checked" and `docs/06-vue-composition-patterns-and-tricks.md` -> "Computed vs watch: the deciding question".

---

## Q3: When to reach for shallowRef

Yes, `shallowRef` would help here, because Vue's deep reactive walk is the bottleneck.

What's happening: when you do `ref(largeArrayOf20000Rows)`, Vue's `ref` doesn't walk the array eagerly, but the array is unwrapped to a deep `reactive` proxy on access. Every row, every cell, every nested property is wrapped in a Proxy. When the filter input changes, anything that touches the array triggers tracking work proportional to the depth of access.

`shallowRef` makes only the `.value` reassignment reactive. The contents are not deep-tracked. To trigger an update, you replace the array (or the relevant subtree) instead of mutating in place.

The mutation pattern in the filter handler:

```js
const rows = shallowRef(initialRows);

function applyFilter(query) {
  // Replace the value to trigger reactivity.
  rows.value = initialRows.filter(r => r.name.includes(query));
}
```

The trade-off: deep tracking lets you do `rows.value[0].name = 'X'` and see updates. With shallow, you have to replace.

For a filter use case this is ideal because filtering naturally produces a new array. For an "edit one cell" feature, shallow forces you to do `rows.value = [...rows.value.slice(0, i), { ...rows.value[i], cellChange }, ...rows.value.slice(i+1)]`, which is verbose. Choose based on the dominant mutation pattern.

`markRaw` is also worth considering for things like third-party row instances or Map/Set values that should never participate in reactivity at all.

Anchored in `docs/06-vue-composition-patterns-and-tricks.md` -> "shallowRef and shallowReactive: opt out of deep tracking".

---

## Q4: Why this template is faster than it looks

The junior dev is wrong, and splitting into components would actually make it slower (more component boundaries, more setup calls, more proxy creations).

What the compiler does:

- Everything in `<header>` and `<footer>` is purely static (no reactive references). The compiler **hoists** these vnodes out of the render function. They're created once at module load and reused on every render.
- The only dynamic part is the `<p>{{ message }}</p>`. The compiler tags this with a patch flag (TEXT only).
- The block tree records that this `<article>` block has exactly one dynamic descendant. When the message changes, Vue's runtime walks a flat list of dynamic nodes (length 1), updates the text, and skips everything else.

Visually:

```text
   First render: build the whole tree, hoist statics.
   Subsequent renders when message changes:
       look at block's dynamic-children list -> [p]
       check patch flag -> TEXT
       update p.textContent  <- one DOM operation
       done
```

You cannot beat that by splitting into components. Splitting adds component instances, setup overhead, and an additional layer of vnode reconciliation. Vue's compiler already turned this into the optimal update.

Guidance for the junior:

> "Split for perf" is real when you have:
>
> - A genuinely large component (hundreds of dynamic nodes).
> - A part of the tree with very different update frequency from the rest (e.g., a chart that re-renders every second alongside a static sidebar).
> - A component you want to memoize via `v-memo` because the inputs are stable.
>
> Otherwise, "smaller is faster" is folk wisdom that ignores what the compiler already does.

Anchored in `docs/05-vue-reactivity-and-compiler-internals.md` -> "The compiler: why Vue 3 templates are fast".
