# 06 - Vue Composition Patterns and Tricks: Answers

Companion to `06-vue-patterns-thought-questions.md`.

---

## Q1: Composable that doesn't clean up

What's broken: every call to `useOnline()` adds two new event listeners to `window`. The composable never removes them. Across a session where many components mount and unmount, listener count grows unboundedly. The handlers retain their refs, and the refs retain their reactive subscribers.

Symptoms over time:

- Memory grows on each navigation.
- Each `online`/`offline` event triggers more and more handlers.
- Devtools shows the listeners stacking up.

The fix uses `onScopeDispose` so the cleanup ties to the calling component's effect scope:

```js
import { ref, onScopeDispose } from 'vue';

export function useOnline() {
  const isOnline = ref(navigator.onLine);

  const onOnline = () => isOnline.value = true;
  const onOffline = () => isOnline.value = false;

  window.addEventListener('online', onOnline);
  window.addEventListener('offline', onOffline);

  onScopeDispose(() => {
    window.removeEventListener('online', onOnline);
    window.removeEventListener('offline', onOffline);
  });

  return { isOnline };
}
```

Two things to notice:

- I assigned the handlers to named variables so I have references to remove. Without that, you can't remove inline arrow functions.
- `onScopeDispose` works in components (fires on unmount) and in custom effect scopes (fires on `scope.stop()`). It's strictly more general than `onUnmounted`.

The wrong answer: "use a single global listener and have all callers share state". That works (and might even be more efficient) but it's a different design. The minimum fix is to make the existing design clean up after itself.

Anchored in `docs/06-vue-composition-patterns-and-tricks.md` -> "Composable design checklist" and "Effect scopes: cleanup as a primitive".

---

## Q2: Picking the right watch flush timing

The bug: `watch` flushes **before** render by default. So when the watcher runs, the DOM still reflects the previous render. `nextInput.value?.focus()` either focuses the wrong element or focuses something that's about to be re-rendered.

Fix: use `watchPostEffect` (or `watch` with `{ flush: 'post' }`):

```js
watch(selectedValue, (newValue) => {
  inputValue.value = newValue;
  nextInput.value?.focus();
}, { flush: 'post' });
```

After flush 'post', Vue has already updated the DOM, so `nextInput` refers to the correct element.

The differences:

- `watch` (`flush: 'pre'`, default): fires before the next render. Good for "I want to react to a change and have my reaction reflected in the upcoming render." Bad for DOM measurement or focusing.
- `watchPostEffect` (`flush: 'post'`): fires after the next render. Use when you need DOM updates to be applied first.
- `watchSyncEffect` (`flush: 'sync'`): fires immediately on the reactive change, no batching. Defeats Vue's batching, so multiple writes in one tick fire the effect multiple times. Reserve for cases where you genuinely need synchronous reaction (e.g., a derived ref that absolutely must be in sync before any other code runs).

The wrong answer: "use `nextTick` inside the watcher". This works but is a workaround:

```js
watch(selectedValue, async (newValue) => {
  inputValue.value = newValue;
  await nextTick();
  nextInput.value?.focus();
});
```

`flush: 'post'` does the same thing more directly. `nextTick` is what you reach for when you don't own the watcher (e.g., reacting to a prop change in a parent).

Anchored in `docs/06-vue-composition-patterns-and-tricks.md` -> "The watch family: pick the right one".

---

## Q3: Pinia or composable?

1. **Logged-in user's profile.** Pinia. App-wide, single source of truth, persists across route changes, used by many unrelated components.

2. **Validation state of one form.** Composable. Local to the form, each form should have its own instance, never shared across pages.

3. **Current theme.** Pinia. App-wide, persists, often syncs with localStorage. Could be a composable singleton, but Pinia gives you devtools for free.

4. **Shopping cart contents.** Pinia. Multiple unrelated parts read it (header badge, cart page, checkout). Survives page navigation. Mutations are app-level.

5. **Whether sidebar is collapsed.** Composable singleton or a small Pinia store. It's app-wide UI state. Use Pinia if you want devtools or persistence; composable if it's a five-line concern that only one layout component cares about.

6. **Search filters on a product list page.** Composable, ideally tied to URL state. Filters are page-local; they should be shareable via URL, not held in a global store. Putting them in Pinia creates the trap of "leftover filter state" when the user comes back to the page.

The pattern: app-wide, multi-consumer, persists -> Pinia. Local, single-feature, ephemeral -> composable. URL-shareable -> URL state, not either.

Anchored in `docs/06-vue-composition-patterns-and-tricks.md` -> "When Pinia beats composables, and vice versa".

---

## Q4: shallowRef trade-off in practice

The bug: `shallowRef` makes only the `.value` reassignment reactive. Mutating a property of an item inside the array (`card.column = toColumn`) doesn't trigger anything because the array contents are not deep-tracked.

The drag works once because Vue's render had already produced DOM tied to the initial array. After the mutation, no trigger fires, no re-render, the new column doesn't update.

Two fixes:

**Fix 1: Replace the array (or the row) to trigger reactivity.**

```js
function moveCard(cardId, fromColumn, toColumn) {
  cards.value = cards.value.map(c =>
    c.id === cardId ? { ...c, column: toColumn } : c
  );
}
```

Trade-off: cleanest for shallowRef. Allocates a new array on every move. For 500 cards, that's a 500-element map; cheap. For 500,000, you'd think harder.

**Fix 2: Manually trigger after mutation.**

```js
import { triggerRef } from 'vue';

function moveCard(cardId, fromColumn, toColumn) {
  const card = cards.value.find(c => c.id === cardId);
  card.column = toColumn;
  triggerRef(cards);
}
```

Trade-off: avoids reallocating, but it's imperative and easy to forget. Every code path that mutates needs to call `triggerRef`.

I'd pick Fix 1 by default. It's harder to misuse, and the cost (one allocation per drag) is negligible at this scale. Reach for `triggerRef` only when allocation is profiled to be the bottleneck.

The wrong answer: "switch back to `ref` and accept the perf cost". Sometimes that's right; in this case the user said reactivity overhead was the bottleneck, so going back to deep tracking would undo the optimization.

Anchored in `docs/06-vue-composition-patterns-and-tricks.md` -> "shallowRef and shallowReactive: opt out of deep tracking".
