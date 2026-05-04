# 03 - React Fiber and Reconciliation: Thought Questions

Companion to `docs/03-react-fiber-and-reconciliation.md`. Three questions, all practical.

---

## Q1: The vanishing form input

> What this tests: component identity, keys, and how state is preserved across renders.

A teammate built a "todo with edit mode" feature:

```jsx
function TodoList({ items, onUpdate }) {
  return items.map((item) => {
    if (item.editing) {
      return <EditableRow key={item.id} item={item} onSave={onUpdate} />;
    }
    return <ReadonlyRow key={item.id} item={item} />;
  });
}
```

The bug: when the user clicks "edit" on a row, types into the input, then clicks "edit" on a different row, the **first** row's input goes back to the original value. The second row's edit mode opens with empty input even if `item.text` was set. Why? What's the cleanest fix?

---

## Q2: Why does memoization not help here

> What this tests: identity churn, prop stability, and where memoization actually pays off.

A junior teammate tries to fix slow renders by memoizing:

```jsx
function Dashboard({ filters }) {
  const config = { sort: 'date', filters };  // new object every render
  const onChange = (val) => setFilter(val);  // new function every render

  return <ExpensiveTable config={config} onChange={onChange} />;
}

const ExpensiveTable = React.memo(function ExpensiveTable({ config, onChange }) {
  // ...
});
```

`ExpensiveTable` is wrapped in `React.memo` but still re-renders on every parent render. Explain what's happening and what to actually fix.

---

## Q3: When swapping the key fixes the bug

> What this tests: using key as a state-reset mechanism rather than just a list-identity tool.

A modal opens to edit a user. The form is reused: when you close it and open it for a different user, the form fields show the previous user's edits.

```jsx
function EditUserModal({ userId, isOpen, onClose }) {
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <UserForm userId={userId} />
    </Modal>
  );
}
```

`UserForm` has internal state for the form fields. What's the one-line fix to make the form reset when `userId` changes, without restructuring `UserForm` itself?
