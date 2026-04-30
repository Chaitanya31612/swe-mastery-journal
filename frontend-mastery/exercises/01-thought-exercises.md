# 01 - Frontend Mastery Thought Exercises

Use these like senior review reps. Do not jump to answers first.

Answers are in `01-thought-exercises-answers.md`.

---

## Exercise 1: Classify The State

For each item, classify it as server state, client state, URL state, form state, derived state, or external state.

1. Current page number in a searchable table.
2. Text typed into a comment box before submit.
3. User profile returned from `/api/me`.
4. Whether a dropdown menu is open.
5. Filtered list calculated from `items` and `query`.
6. Browser online/offline status.
7. Selected project id in a shareable dashboard URL.
8. Whether a destructive confirmation dialog is visible.

Questions:

- Which of these should survive refresh?
- Which of these should be globally stored?
- Which of these should never be stored because it can be derived?

---

## Exercise 2: React Render Mystery

You have this React shape:

```jsx
function Dashboard() {
  const [hoveredRowId, setHoveredRowId] = useState(null);

  return (
    <>
      <Header />
      <HugeChart />
      <Table
        hoveredRowId={hoveredRowId}
        onHoverRow={setHoveredRowId}
      />
    </>
  );
}
```

Every row hover makes the chart rerender.

Questions:

- Why can that happen?
- What is the simplest architectural fix?
- When would memoization be the right fix instead?

---

## Exercise 3: Vue Reactivity Surprise

You see this Vue code:

```js
const state = reactive({
  search: '',
  page: 1,
});

const { search } = state;
```

The UI stops updating when `state.search` changes.

Questions:

- What likely happened?
- What should you use instead?
- Why does this differ from a plain object destructuring mental model?

---

## Exercise 4: Next Boundary Decision

A product page contains:

1. Product title.
2. Product description.
3. Price fetched from database.
4. Image gallery with client-side carousel controls.
5. Add-to-cart button.
6. Reviews list.
7. Review sort dropdown.

Questions:

- Which parts can naturally be server-rendered?
- Which parts require client interactivity?
- Where would you place the client boundary?
- What mistake would accidentally ship too much JavaScript?

---

## Exercise 5: Hydration Mismatch

A server-rendered component outputs:

```jsx
function Greeting() {
  return <p>{new Date().toLocaleTimeString()}</p>;
}
```

Questions:

- Why can hydration mismatch?
- What are two better designs?
- Which design would you choose for a dashboard clock?

---

## Exercise 6: Search Race

User types quickly into a search box.

```text
"r" request starts
"re" request starts
"rea" request starts
"rea" finishes first
"r" finishes last
```

The UI shows results for `"r"`.

Questions:

- What kind of bug is this?
- How can you fix it with request identity?
- How can you fix it with cancellation?
- Which fix do you prefer if the API supports aborting?

---

## Exercise 7: Loading State Choice

A user opens an analytics page. The page has:

- stable navigation/sidebar
- summary cards
- a large chart
- a detailed table

The chart is slow. The table is slower.

Questions:

- Should the whole page become one spinner?
- What should stay visible?
- Where would you use skeletons?
- What should happen if the table fails but cards succeed?

---

## Exercise 8: Optimistic Delete

A user deletes an item from a list. The action is reversible for 10 seconds.

Questions:

- Would you use a confirmation dialog or undo snackbar?
- What should happen immediately after click?
- What should happen if the server delete fails?
- What state needs to be preserved for rollback?

---

## Exercise 9: Effect Or Derived Value

React code:

```jsx
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const [fullName, setFullName] = useState('');

useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);
```

Questions:

- What is wrong with this shape?
- What should replace it?
- When would storing `fullName` be acceptable?

---

## Exercise 10: Design The Empty State

A filtered projects table shows no results for `status=archived`.

Questions:

- Write bad empty-state copy.
- Write better empty-state copy.
- What action should be offered?
- How does this differ from first-use empty state?

---

## Exercise 11: Performance Diagnosis

A page has poor INP. API calls are fast. Bundle size is acceptable. Clicking a filter freezes the UI for 500ms.

Questions:

- Which layer is likely responsible?
- What evidence would you collect?
- Name three likely fixes.
- What would be a bad premature fix?

---

## Exercise 12: Routing Judgment

A modal opens to edit a project.

Questions:

- When should the modal state be in the URL?
- When should it stay local?
- What should happen on refresh if the URL contains the modal state?
- What should happen to focus when the modal closes?

---

## Exercise 13: Framework Choice

You are building an internal authenticated operations dashboard:

- heavy tables
- frequent filters
- no SEO need
- API already exists
- team knows React but not Next cache semantics

Questions:

- Would you default to plain React, Vue, or Next?
- What would make Next worth it anyway?
- What would be the main risk of choosing Next by default?

---

## Exercise 14: Accessibility Review

A design uses a clickable card:

```html
<div class="card" onclick="openProject()">
  <h2>Project Atlas</h2>
  <p>Updated today</p>
</div>
```

Questions:

- What is wrong?
- If it navigates, what element should it be?
- If it performs an action, what element should it be?
- What states must be visible?

---

## Exercise 15: Senior PR Review

A PR adds a global `uiStore` with:

```text
isUserMenuOpen
hoveredTableRowId
currentSearchDraft
selectedProjectId
theme
```

Questions:

- Which values do not belong globally?
- Which value might belong globally?
- Which value might belong in the URL?
- What review comment would you leave?
