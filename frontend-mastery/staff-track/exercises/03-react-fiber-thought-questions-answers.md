# 03 - React Fiber and Reconciliation: Answers

Companion to `03-react-fiber-thought-questions.md`.

---

## Q1: The vanishing form input

The bug: switching between `EditableRow` and `ReadonlyRow` changes the **component type** for that row. React's diff sees `EditableRow` -> `ReadonlyRow` -> `EditableRow` and tears down each previous instance every time. The internal state of `EditableRow` (the input value) is destroyed when it's replaced by `ReadonlyRow`, even though the key stayed the same.

Keys identify the slot, but the component **type** also has to match for state to survive. Mismatched types = rebuilt subtree = lost state.

Two clean fixes:

**Fix 1: One component, conditional rendering inside.**

```jsx
function TodoRow({ item, onUpdate }) {
  return item.editing
    ? <EditableContent item={item} onSave={onUpdate} />
    : <ReadonlyContent item={item} />;
}

// In TodoList:
items.map((item) => <TodoRow key={item.id} item={item} onUpdate={onUpdate} />);
```

`TodoRow` is the same component every render. Its child changes type, but the input lives inside `EditableContent`, which is freshly mounted on each edit toggle. This still loses state on toggle, but the toggle is the user's intentional act, so it's expected behavior.

**Fix 2: Always render `EditableRow`, hide based on `editing`.**

```jsx
function TodoRow({ item, onUpdate }) {
  return <EditableRow item={item} editing={item.editing} onSave={onUpdate} />;
}
```

Now `EditableRow` is always mounted. State persists across edit toggles. Whether this is desirable depends on UX; some apps want the draft preserved across edit toggles, others want it cleared.

The wrong answer: "use `key={item.id + (item.editing ? '-edit' : '-read')}`". That works, but it's also forcing remount on every toggle for the same reason as Fix 1, just less obviously.

Anchored in `docs/03-react-fiber-and-reconciliation.md` -> "Component identity is what preserves state".

---

## Q2: Why does memoization not help here

`React.memo` only short-circuits if all props are referentially equal to last render. The parent passes:

- `config = { sort: 'date', filters }` -> a new object every render.
- `onChange = (val) => setFilter(val)` -> a new function every render.

Both fail referential equality. Memo does nothing. The child renders every time.

The fix is to stabilize the identities, but the **better** fix is to ask why these are being recreated:

- `config` should be `useMemo(() => ({ sort: 'date', filters }), [filters])`.
- `onChange` should be `useCallback((val) => setFilter(val), [setFilter])`.

Or, even better, restructure: pass `filters` directly instead of wrapping it in `config`, and let `setFilter` itself be the prop (it's stable from `useState`).

```jsx
function Dashboard({ filters }) {
  return <ExpensiveTable filters={filters} onChange={setFilter} />;
}
```

Now memo works because `filters` and `setFilter` are stable when they're stable.

The wrong answer: "wrap the parent in memo too". That doesn't help; the parent's render isn't the problem, the child's prop identity is.

Anchored in `docs/03-react-fiber-and-reconciliation.md` -> "Why React is sometimes slow, in one mental model".

---

## Q3: When swapping the key fixes the bug

One-line fix:

```jsx
<UserForm key={userId} userId={userId} />
```

Changing the `key` is React's idiomatic "treat this as a different component instance". When `userId` changes, the key changes, the previous `UserForm` unmounts (state destroyed), and a new one mounts (fresh state).

This is the supported way to **opt into a state reset** without restructuring the component itself. You're using the key as a public API for "discriminate this instance from the previous one".

The wrong answer: "add a `useEffect` that resets state when `userId` changes". This works but is fragile: every state field has to be in the reset effect, and every new state field added later has to be added to the reset, or the bug returns. Key-based reset is mechanical.

Anchored in `docs/03-react-fiber-and-reconciliation.md` -> "Component identity is what preserves state".
