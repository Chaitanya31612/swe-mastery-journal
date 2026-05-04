# 09 - UI/UX Craft and Perceived Performance: Thought Questions

Companion to `docs/09-uiux-craft-and-perceived-performance.md`. Three questions, all practical.

---

## Q1: Optimistic, debounced, or pessimistic?

> What this tests: matching feedback strategy to action consequence.

For each interaction, decide: optimistic UI (instant commit, rollback on failure), pessimistic UI (show loading, wait for server), or debounced/throttled (wait for user to settle). Justify each.

1. Toggling a "favorite" star on a tweet.
2. Submitting a payment for $200.
3. Renaming a file in a file manager.
4. Auto-saving a draft document while the user types.
5. Deleting an account permanently.
6. Reordering items in a sortable list via drag-and-drop.
7. Searching for users in a "share with" autocomplete.

---

## Q2: Reviewing an "all states" gap

> What this tests: thinking about empty/loading/error states as first-class design.

A teammate's PR adds a "Recent activity" panel:

```jsx
function ActivityPanel() {
  const { data: activities } = useActivities();
  return (
    <div className="panel">
      <h2>Recent activity</h2>
      {activities.map(a => <ActivityItem key={a.id} item={a} />)}
    </div>
  );
}
```

You review it. List four specific states this component fails to handle, and for each, describe what the UI should do. (No code needed; the design intent is the point.)

---

## Q3: The "looks fast" rewrite

> What this tests: applying perceived-performance levers in a realistic flow.

A teammate's "Save and continue" button on a multi-step form:

```jsx
function SaveAndContinue() {
  const [step, setStep] = useState(currentStep);

  async function handleClick() {
    const result = await api.saveStep(step);
    if (result.ok) {
      setStep(step + 1);
    } else {
      alert('Save failed');
    }
  }

  return <button onClick={handleClick}>Save and continue</button>;
}
```

Users complain that the form "feels slow" even when the API is fast. Walk through what's wrong from a perceived-performance perspective and rewrite the handler with at least three improvements.
