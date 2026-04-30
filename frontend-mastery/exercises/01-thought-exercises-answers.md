# 01 - Frontend Mastery Thought Exercises Answers

Use these after attempting `01-thought-exercises.md`.

---

## Exercise 1: Classify The State

1. Current page number in a searchable table -> URL state if shareable or refreshable, local state if temporary widget state.
2. Text typed into a comment box before submit -> form state.
3. User profile returned from `/api/me` -> server state.
4. Whether a dropdown menu is open -> local client state.
5. Filtered list calculated from `items` and `query` -> derived state.
6. Browser online/offline status -> external state.
7. Selected project id in a shareable dashboard URL -> URL state.
8. Whether a destructive confirmation dialog is visible -> local client state, URL state only if deep linking/recovery is expected.

Should survive refresh:

- URL state.
- Server state after refetch or cache restore.
- Some preferences in storage, like theme.

Should be global:

- Rarely any of these except app-wide preference like theme.
- User profile may live in an auth/session cache, not a random UI store.

Should never be stored:

- Filtered list if it is purely calculated from `items` and `query`.

---

## Exercise 2: React Render Mystery

It happens because `hoveredRowId` belongs to `Dashboard`. Updating it rerenders `Dashboard`, so children can render too.

Simplest fix:

```text
Move hover state into Table or row-level components if only the table needs it.
```

Memoization is right when:

- the state genuinely belongs in the parent
- the chart is expensive
- chart props are stable
- you have measured or observed real cost

Do not memoize first if the real problem is state placed too high.

---

## Exercise 3: Vue Reactivity Surprise

Destructuring pulled `search` out of the reactive proxy in a way that can lose reactivity.

Use:

```js
const search = toRef(state, 'search');
```

or:

```js
const { search } = toRefs(state);
```

Why it differs:

```text
Vue tracks access through the proxy/ref.
Plain destructuring copies the current property value instead of preserving the reactive access path.
```

---

## Exercise 4: Next Boundary Decision

Server-render naturally:

- product title
- description
- price
- initial reviews list
- static gallery markup if possible

Client interactivity:

- carousel controls
- add-to-cart button
- review sort dropdown if it updates without navigation or requires browser interaction

Good boundary:

```text
Product page stays server-rendered.
Client components wrap only ImageCarouselControls, AddToCartButton, and interactive ReviewSort.
```

Mistake:

```text
Adding 'use client' at the top of the entire product page or layout because one child needs click state.
```

That ships too much JavaScript.

---

## Exercise 5: Hydration Mismatch

The server time and client time can differ, so the server HTML does not match the first client render.

Better designs:

```text
1. Render a stable placeholder on server, then set time after client mount.
2. Pass a server-generated timestamp as data and render that exact value on both server and first client render.
```

For a dashboard clock:

```text
Use a client-owned clock component that renders a stable placeholder or server timestamp first, then starts ticking after mount.
```

---

## Exercise 6: Search Race

This is an async ordering bug. Older work finishes after newer work and overwrites it.

Request identity:

```js
let latestRequestId = 0;

async function search(query) {
  latestRequestId += 1;
  const requestId = latestRequestId;

  const results = await searchApi(query);

  if (requestId !== latestRequestId) {
    return;
  }

  setResults(results);
}
```

Cancellation:

```js
let currentController;

async function search(query) {
  currentController?.abort();

  const controller = new AbortController();
  currentController = controller;

  const results = await searchApi(query, {
    signal: controller.signal,
  });

  setResults(results);
}
```

Prefer cancellation when supported because it avoids wasted network/server/client work. Still handle abort errors intentionally.

---

## Exercise 7: Loading State Choice

Do not replace the whole page with one spinner.

Keep visible:

- navigation/sidebar
- page title
- filter controls if usable
- any already-known cached data
- layout shell

Use skeletons:

- summary cards if their shape is known
- chart region if the chart area is predictable
- table rows if table shape is predictable

If table fails but cards succeed:

```text
Show cards.
Show chart if ready.
Show a localized table error with retry.
Do not collapse the whole page into failure.
```

---

## Exercise 8: Optimistic Delete

Use undo snackbar if the action is reversible for 10 seconds.

Immediately:

- remove item from visible list
- show undo snackbar
- prevent duplicate delete action for that item

If server delete fails:

- restore the item
- show clear failure copy
- keep user context

Preserve:

- deleted item data
- original index or ordering context
- any selection/focus context needed for restoration

---

## Exercise 9: Effect Or Derived Value

Wrong shape:

```text
fullName is duplicated derived state.
The effect creates an extra render and synchronization risk.
```

Replace with:

```jsx
const fullName = `${firstName} ${lastName}`;
```

Storing `fullName` is acceptable when:

- user can edit it independently
- it comes from a persisted backend field
- the value is expensive and memoized rather than stored as separate state
- it intentionally freezes a snapshot in time

---

## Exercise 10: Design The Empty State

Bad:

```text
No data.
```

Better:

```text
No archived projects
No projects match the archived filter.
```

Action:

```text
Clear filter
```

Difference from first-use:

```text
Filtered empty means data may exist outside the current filter.
First-use empty means the user has not created anything yet, so teach and invite creation.
```

---

## Exercise 11: Performance Diagnosis

Likely layer:

```text
main-thread JavaScript, render cost, or layout work after filter click
```

Evidence:

- Performance profile around the click
- React/Vue DevTools render information
- long task timing
- component render counts
- layout/paint cost in DevTools

Likely fixes:

- move filter state lower or reduce invalidated tree
- memoize expensive filtered calculations
- virtualize large list/table
- defer non-urgent render work
- move CPU-heavy transform to worker
- avoid layout reads/writes in loops

Bad premature fix:

```text
Adding CDN, changing backend, or lazy-loading random components when the freeze is local CPU/render work.
```

---

## Exercise 12: Routing Judgment

Put modal state in URL when:

- user should share it
- refresh should preserve it
- browser back should close it
- support/QA need direct reproduction
- modal represents a resource view

Keep local when:

- it is a temporary menu-like interaction
- it contains unsaved draft not meant to deep link
- sharing it would be confusing

On refresh with URL modal state:

```text
Load the underlying page and open the modal if the resource exists.
Show recoverable error if it does not.
```

On close:

```text
Return focus to the control that opened the modal, or a logical fallback if that control no longer exists.
```

---

## Exercise 13: Framework Choice

Default:

```text
Plain React SPA is a strong default here because SEO is irrelevant, API exists, team knows React, and heavy client interactivity dominates.
```

Next becomes worth it if:

- route-level server rendering matters
- you need server-side auth/data colocation
- deployment platform strongly favors it
- streaming or server components reduce real client cost
- the team can own the cache and boundary model

Main risk:

```text
Choosing Next for status reasons, then fighting cache behavior, server/client boundaries, and extra complexity without product benefit.
```

Vue could also be good if the team is strong in Vue and values its reactivity ergonomics.

---

## Exercise 14: Accessibility Review

Wrong:

- `div` has no native button/link semantics
- keyboard users may not reach or activate it
- role/name/state are unclear
- focus state is likely missing

If it navigates:

```html
<a href="/projects/atlas" class="card">
  <h2>Project Atlas</h2>
  <p>Updated today</p>
</a>
```

If it performs an action:

```html
<button type="button" class="card">
  <span class="card-title">Project Atlas</span>
  <span>Updated today</span>
</button>
```

Visible states:

- hover
- focus
- active/pressed if relevant
- disabled if relevant

---

## Exercise 15: Senior PR Review

Does not belong globally:

- `isUserMenuOpen`
- `hoveredTableRowId`
- `currentSearchDraft`

Might belong globally:

- `theme`

Might belong in URL:

- `selectedProjectId`, if it defines the current view or should be shareable/refreshable

Review comment:

```text
This store mixes app-wide preference, navigation state, and temporary interaction state. Keep menu open and hover local, keep search draft in the form, put selected project in the URL if it defines the view, and keep only true app-wide preference like theme in global UI state.
```
