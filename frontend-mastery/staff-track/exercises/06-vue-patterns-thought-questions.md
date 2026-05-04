# 06 - Vue Composition Patterns and Tricks: Thought Questions

Companion to `docs/06-vue-composition-patterns-and-tricks.md`. Four questions, all practical.

---

## Q1: Composable that doesn't clean up

> What this tests: lifecycle ownership inside composables and the role of `onScopeDispose`.

A teammate's composable for tracking online status:

```js
// composables/useOnline.js
import { ref } from 'vue';

export function useOnline() {
  const isOnline = ref(navigator.onLine);

  window.addEventListener('online', () => isOnline.value = true);
  window.addEventListener('offline', () => isOnline.value = false);

  return { isOnline };
}
```

What's broken about this design? Walk through what would happen across a session of mounting and unmounting many components that use it. Then write the corrected version.

---

## Q2: Picking the right watch flush timing

> What this tests: knowing when DOM-after-render vs DOM-before-render matters.

You have an autocomplete component. When the user picks a suggestion, you want to:

1. Update the input to show the picked value.
2. Move focus to the next input in the form.

A teammate writes:

```js
watch(selectedValue, (newValue) => {
  inputValue.value = newValue;
  nextInput.value?.focus();
});
```

The focus sometimes lands on the wrong element. What's wrong, what's the fix, and what's the difference between `watch`, `watchPostEffect`, and `watchSyncEffect` for this case?

---

## Q3: Pinia or composable?

> What this tests: judgment about state placement and lifetime.

For each of these pieces of state, would you reach for a Pinia store or a composable? Justify each in one sentence.

1. The currently logged-in user's profile.
2. The validation state of a single form on a settings page.
3. The current theme (light/dark).
4. The contents of a shopping cart.
5. Whether the sidebar is collapsed.
6. Search filters on a product list page.

---

## Q4: shallowRef trade-off in practice

> What this tests: knowing when shallow reactivity is the right call and what the call site has to change.

You're optimizing a Kanban board with ~500 cards across columns. Drag-and-drop is the main interaction. Profiling shows a lot of time in reactivity overhead.

Your teammate proposes:

```js
const cards = shallowRef(initialCards);

function moveCard(cardId, fromColumn, toColumn) {
  const card = cards.value.find(c => c.id === cardId);
  card.column = toColumn;  // mutate in place
}
```

The drag works once, then breaks. Why? Two ways to fix it; pick one and explain the trade-off.
