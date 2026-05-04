# 05 - Vue Reactivity and Compiler Internals: Thought Questions

Companion to `docs/05-vue-reactivity-and-compiler-internals.md`. Four questions, all practical.

---

## Q1: Reactivity vanishes after destructuring

> What this tests: how `reactive` Proxies interact with destructuring and the role of `toRefs`.

A teammate's component:

```js
import { reactive } from 'vue';

export default {
  setup() {
    const state = reactive({ count: 0, name: 'A' });
    const { count, name } = state;

    setInterval(() => {
      state.count += 1;
    }, 1000);

    return { count, name };
  },
};
```

The template `{{ count }}` never updates. Explain why, then give the cleanest two-line fix.

---

## Q2: Computed vs watch decision

> What this tests: knowing when to reach for `computed` vs `watch` and recognizing watch misuse.

You're reviewing a PR with this composable:

```js
function useFullName(first, last) {
  const fullName = ref('');

  watch([first, last], () => {
    fullName.value = `${first.value} ${last.value}`;
  }, { immediate: true });

  return { fullName };
}
```

What's wrong with this design, and what's the senior-level rewrite? Beyond just "it should be `computed`", explain why the rewrite is strictly better in three concrete ways.

---

## Q3: When to reach for shallowRef

> What this tests: the trade-off of deep tracking vs mutation control on large data.

You have a data table component receiving 20,000 rows from an API. The rows render fine, but typing in the table's "filter" input causes noticeable lag. CPU profiling shows time spent in Vue's reactivity, not in your filter logic.

Walk through whether `shallowRef` would help, what the trade-off is, and what the actual mutation pattern would look like in your filter handler.

---

## Q4: Why this template is faster than it looks

> What this tests: understanding compiler optimizations (static hoisting, patch flags, block tree).

A junior dev says "this template re-renders the whole thing every time `message` changes; we should split it into smaller components for performance":

```html
<template>
  <article class="card">
    <header class="card-header">
      <h1>Welcome</h1>
      <p class="subtitle">Stay a while</p>
    </header>
    <section class="card-body">
      <p>{{ message }}</p>
    </section>
    <footer class="card-footer">
      <small>v1.0</small>
    </footer>
  </article>
</template>
```

Is the junior dev right? Explain what Vue's compiler actually does with this template, and what guidance you'd give them about when "split for perf" is real vs imagined.
