# 04 - Frontend Architecture, Data, And Performance

Senior frontend architecture is mostly conscious placement:

```text
Where does this state live?
Where does this data load?
Where does this computation run?
Where does this interaction happen?
Where is the user waiting?
```

---

## The Core Idea

A frontend app is a graph of ownership.

```text
URL owns navigation state
server owns persisted data
cache owns fetched snapshots
forms own drafts
components own local interaction
design system owns visual primitives
router owns route transitions
browser owns focus, history, storage, layout, network
```

When ownership is clear, code stays boring.

When ownership is unclear, you write glue:

```text
sync effect
prop drilling
global store patches
localStorage rescue logic
manual invalidation
loading flag coordination
```

Senior intuition: most messy frontend code is not "bad React" or "bad Vue". It is unclear ownership.

---

## State Placement Ladder

Put state as low as possible, but no lower.

```text
can it be calculated from existing values?
  -> derived value, no state

does only one component need it?
  -> local component state

do siblings need to coordinate?
  -> lift to nearest shared parent

does it represent navigation or shareable filters?
  -> URL state

is it persisted backend data?
  -> server-state cache or framework loader

is it app-wide client preference?
  -> global client store or browser storage
```

Example:

```text
search input draft
  local form state

submitted search query
  URL state

search results
  server-state cache keyed by URL query

selected row hover
  local component state

selected row for detail panel
  URL state if deep-linkable, local state if purely temporary
```

Senior rule: state placement should follow user expectation, not developer convenience.

---

## Data Loading Shapes

### Fetch-On-Render

```text
render component
  -> effect starts fetch
  -> loading
  -> data arrives
  -> render again
```

Simple, but can create waterfalls:

```text
Parent loads
  then Child loads
    then Grandchild loads
```

### Fetch-Then-Render

```text
route knows data requirements
  -> fetch starts before screen renders
  -> render with data or planned loading state
```

Often better for route-level pages.

### Render-As-You-Fetch

```text
start fetching early
  -> render shell immediately
  -> reveal data sections as ready
```

Best when combined with good suspense/loading boundaries or streaming.

Senior intuition: data should start loading at the earliest owner that knows it is needed.

---

## Avoiding Waterfalls

Bad:

```text
load user
  -> after user loads, load projects
    -> after projects load, load tasks
```

If requests are independent, start together:

```js
const [user, projects, tasks] = await Promise.all([
  fetchUser(),
  fetchProjects(),
  fetchTasks(),
]);
```

If one depends on another, make that dependency explicit:

```js
const user = await fetchUser();

const [projects, notifications] = await Promise.all([
  fetchProjects(user.organizationId),
  fetchNotifications(user.id),
]);
```

Senior rule: every sequential `await` in loading code should earn its sequence.

---

## Cache Thinking

A cache is not a magic faster box. It is a consistency trade.

Ask:

```text
What is the cache key?
Who can mutate this data?
When is it stale?
How is it invalidated?
Can stale data be shown?
What happens offline or after reconnect?
```

Example cache key:

```text
['projects', organizationId, { status: 'active' }]
```

Bad key:

```text
['projects']
```

Why bad:

```text
active, archived, and different organizations can collide
```

Senior intuition: cache bugs often look like UI bugs because the UI faithfully renders the wrong cached truth.

---

## Optimistic Updates

Optimistic update:

```text
user acts
  -> UI updates immediately
  -> request runs
  -> success confirms or failure rolls back
```

Good fit:

- like button
- checkbox toggle
- reorder list
- local rename
- low-risk save with reversible failure

Risky fit:

- payment
- permission change
- destructive delete without undo
- inventory-sensitive action

Example shape:

```js
const previousItems = items;

setItems((currentItems) => {
  return currentItems.filter((item) => item.id !== deletedItemId);
});

try {
  await deleteItem(deletedItemId);
} catch (error) {
  setItems(previousItems);
  showToast('Delete failed. Item restored.');
}
```

Senior rule: optimistic UI needs a rollback or reconciliation story.

---

## Forms Are State Machines

A form is not a pile of inputs.

```text
idle
  -> dirty
  -> validating
  -> submitting
  -> submitted
  -> failed
```

Each field may also have:

```text
empty
touched
dirty
valid
invalid
pending async validation
disabled
```

Bad UX:

```text
show every validation error before the user interacts
```

Better:

```text
validate on input for format hints
show errors after blur or submit intent
keep submit failure near the submit action and field failures near fields
preserve user input on failure
```

Senior intuition: forms are where product trust is won or lost.

---

## Routing Architecture

Routes are product boundaries.

Good route design:

```text
/projects
/projects?status=active
/projects/acme
/projects/acme/settings
```

Weak route design:

```text
/app
```

with everything hidden in client state.

Use URL state for:

- selected resource
- filters users share
- search query after submit
- pagination
- tab when it changes page meaning
- modal when deep linking matters

Keep local state for:

- hover
- open menu
- unsaved input draft
- temporary animation
- non-shareable disclosure state

Senior rule: if support, QA, or another user needs to reproduce the screen, the URL should carry enough state.

---

## Component Architecture

A useful split:

```text
page or route component
  coordinates data and major layout

feature component
  owns product behavior for a focused feature

UI component
  reusable visual primitive

headless component
  behavior without styling

utility
  pure calculation or adapter
```

Bad component:

```text
UserSettingsPage
  fetches data
  validates forms
  owns modals
  formats dates
  defines table columns
  handles permissions
  contains 900 lines of JSX
```

Better shape:

```text
UserSettingsPage
  -> loads route data and layout

UserProfileForm
  -> owns profile draft and validation

UserAccessPanel
  -> owns permission UI

DangerZone
  -> owns destructive flows

formatUserDate
  -> pure formatting utility
```

Senior intuition: split by reason to change, not by arbitrary file size.

---

## Design System Boundaries

Design system components should own:

- visual consistency
- accessibility semantics
- keyboard behavior for primitives
- tokens and variants
- predictable composition APIs

Feature code should own:

- business rules
- data fetching
- product copy
- permission checks
- flow-specific state

Bad:

```text
Button component knows "cancel subscription" rules
```

Better:

```text
CancelSubscriptionDialog owns flow
Button owns button semantics and style
```

Senior rule: reusable components should be product-aware only when the product concept itself is reusable.

---

## Performance Budget

Performance is a budget across phases:

```text
network
  bytes, request count, priority, caching

JavaScript
  parse, compile, execute, long tasks

rendering
  style, layout, paint, composite

data
  waterfalls, cache misses, backend latency

perception
  feedback, skeleton, progressive reveal, layout stability
```

Common fix map:

```text
large bundle
  code split, remove dependency, server-render static UI

slow interaction
  reduce rerender scope, move heavy work, defer non-urgent updates

slow route
  preload, parallelize data, stream, cache, reduce waterfalls

layout shift
  reserve space, define image dimensions, stabilize fonts

slow list
  paginate, virtualize, memoize row work, reduce DOM nodes
```

Senior rule: do not optimize what you have not located.

---

## Core Web Vitals As Product Signals

Use these as signals, not religion.

```text
LCP - Largest Contentful Paint
  How soon does the main content appear?

INP - Interaction to Next Paint
  How responsive are interactions?

CLS - Cumulative Layout Shift
  Does the page move unexpectedly?
```

Translate to product language:

```text
LCP bad
  user waits to understand page

INP bad
  user feels ignored

CLS bad
  user loses spatial trust
```

Interesting fact: users perceive unstable UI as slower even when raw loading time is unchanged.

---

## Expensive Dependencies

Every dependency costs:

- bytes
- parse time
- security surface
- update burden
- API lock-in
- mental model

Ask before adding:

```text
Is this solving a hard problem or avoiding a small function?
Is it tree-shakeable?
Does it work with SSR?
Does it respect accessibility?
Does it support our design system?
What happens if it is abandoned?
```

Senior pushback: a dependency can be correct even for small code if the domain is tricky, like date/time, accessibility primitives, i18n, or rich text. Avoiding dependencies blindly is also amateur.

---

## Workers

Web workers move CPU work off the main thread.

Good fit:

- parsing large files
- search indexing
- image processing
- expensive diffing
- data transforms that do not need DOM

Not fit:

- direct DOM work
- tiny calculations
- code that needs synchronous UI state access

Mental model:

```text
main thread
  owns UI and DOM

worker
  owns isolated computation

postMessage
  copies or transfers data between them
```

Senior intuition: workers improve responsiveness, not raw simplicity.

---

## Architecture Smell List

- same state exists in URL, store, and component
- every component imports the global store
- effects copy data between local states
- loading flags are manually coordinated across siblings
- route changes reset surprising state
- components know too much about API response shape
- design system components contain feature business logic
- modals cannot be linked or recovered when product expects it
- tests require mocking half the app to verify one interaction
- performance fixes are added before measuring the bottleneck

---

## The One-Sentence Model

Frontend architecture is the art of placing state, data, work, and feedback at the layer that owns them.
