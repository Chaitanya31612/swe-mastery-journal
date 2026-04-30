# Frontend Mastery Journal

> Goal: build senior frontend judgment, not framework trivia.
> Use this as a mental model guide, UI/UX coach, debugging manual, and revision map.

---

## How To Use This Folder

Read the docs in order once. After that, jump by situation:

- "I want the big picture of SPA internals" -> `docs/00-spa-mental-model-and-browser-internals.md`
- "JavaScript feels magical under load" -> `docs/01-javascript-runtime-for-frontend.md`
- "Reactivity and rendering are fuzzy" -> `docs/02-reactivity-rendering-and-state.md`
- "React, Next, and Vue feel similar but different" -> `docs/03-react-next-vue-differentiation.md`
- "I need senior frontend architecture judgment" -> `docs/04-frontend-architecture-data-and-performance.md`
- "I want to become much better at UI/UX" -> `docs/05-ui-ux-craft-and-product-thinking.md`
- "I want review checklists and debugging instincts" -> `docs/06-debugging-testing-and-review.md`
- "I want reps" -> `exercises/01-thought-exercises.md`
- "I want checked answers" -> `exercises/01-thought-exercises-answers.md`

---

## Folder Structure

```text
frontend-mastery/
├── README.md
├── docs/
│   ├── 00-spa-mental-model-and-browser-internals.md
│   ├── 01-javascript-runtime-for-frontend.md
│   ├── 02-reactivity-rendering-and-state.md
│   ├── 03-react-next-vue-differentiation.md
│   ├── 04-frontend-architecture-data-and-performance.md
│   ├── 05-ui-ux-craft-and-product-thinking.md
│   └── 06-debugging-testing-and-review.md
└── exercises/
    ├── 01-thought-exercises.md
    └── 01-thought-exercises-answers.md
```

---

## The Senior Frontend Mental Model

Frontend development is not "put data on screen".

It is the discipline of keeping this loop correct, fast, accessible, and emotionally calm:

```text
user intent
  -> input event
  -> JavaScript handler
  -> state transition
  -> render calculation
  -> DOM mutation
  -> browser layout and paint
  -> perceived feedback
  -> next user intent
```

Most frontend bugs come from losing track of one layer:

```text
browser runtime
  event loop, network, parser, layout, paint, compositor

JavaScript model
  values, identity, closures, async tasks, modules, memory

reactivity model
  how state changes are observed and turned into UI updates

rendering model
  when work runs, what is recomputed, what touches the DOM

data model
  server state, client state, URL state, form state, derived state

interaction model
  feedback, affordance, error recovery, latency hiding, accessibility
```

Senior intuition: a SPA is a distributed system with a tiny screen. The client, server, network, cache, router, browser, and human all have state.

---

## What This Track Deliberately Avoids

This is not:

- a React API encyclopedia
- a Next.js config catalog
- a Vue directive reference
- a CSS property dictionary
- a beginner HTML/CSS/JS tutorial

You can search exact APIs when needed.

This track teaches the foundation that makes search results obvious.

---

## Mastery Map

### 1. Browser First

If you know how the browser parses, schedules, lays out, paints, composites, and dispatches events, frontend performance stops feeling random.

### 2. JavaScript Runtime

If you know stack, heap, closures, tasks, microtasks, promises, modules, and object identity, framework behavior becomes easier to predict.

### 3. Reactivity

If you know how frameworks detect change, you know when UI updates are cheap, expensive, stale, batched, or accidentally skipped.

### 4. Rendering Trade-Offs

If you know client rendering, server rendering, hydration, streaming, static rendering, and partial interactivity, you can choose the right delivery model.

### 5. State Ownership

If each piece of state has one owner, UI code becomes smaller. If ownership is vague, everything becomes synchronization code.

### 6. UI/UX Fundamentals

If layout, hierarchy, copy, feedback, affordance, and recovery are strong, the product feels smarter than it is.

---

## Framework Differentiation In One Screen

```text
React
  Mental model: render is a pure description of UI for a given state.
  Strength: explicit data flow, ecosystem, composition, cross-platform ideas.
  Watch: unnecessary re-renders, effect misuse, state placed too high.

Vue
  Mental model: reactive values are tracked and targeted updates happen from dependencies.
  Strength: approachable ergonomics, fine-grained reactivity, single-file component flow.
  Watch: implicit dependencies, proxy identity surprises, overusing watchers.

Next.js
  Mental model: React plus routing, server/client boundaries, rendering modes, and caching.
  Strength: production app structure, server rendering, streaming, data placement.
  Watch: cache confusion, accidental client boundaries, hydration mismatches.
```

Interesting fact: React and Vue both make UI declarative, but they pay for that abstraction differently. React usually asks "which components should re-render?" Vue usually asks "which reactive dependencies changed?"

---

## Study Plan

### Pass 1: Build The Runtime Model

1. Read `00-spa-mental-model-and-browser-internals.md`.
2. Read `01-javascript-runtime-for-frontend.md`.
3. Explain why a click handler, a promise callback, and a paint do not all happen at the same time.

### Pass 2: Build The Reactivity Model

1. Read `02-reactivity-rendering-and-state.md`.
2. Draw how state moves from event to screen.
3. For any component you touch, classify each state variable by ownership.

### Pass 3: Compare Frameworks

1. Read `03-react-next-vue-differentiation.md`.
2. Translate one simple UI between React and Vue mentally.
3. Decide what belongs on the server versus client in a Next-style app.

### Pass 4: Practice Senior Judgment

1. Read `04-frontend-architecture-data-and-performance.md`.
2. Read `05-ui-ux-craft-and-product-thinking.md`.
3. Read `06-debugging-testing-and-review.md`.
4. Do the exercises without answers.

---

## Senior Rules Of Thumb

- Treat state as a liability. Every state variable needs an owner, lifetime, and invalidation story.
- Prefer derived values over duplicated state.
- Effects are for synchronizing with the outside world, not for organizing ordinary calculations.
- Fast UI is not only low milliseconds. It is immediate feedback, stable layout, clear progress, and graceful recovery.
- Most design polish is alignment, spacing, contrast, copy, and state quality. Fancy visuals come later.
- Make impossible states impossible. If you cannot, make them visible in tests and UI states.
- The URL is product state. If a user expects to share, refresh, back, or deep link, the URL should know.
- Performance work starts with measurement and ends with simpler work, less work, or later work.
- Accessibility is not a checklist after design. It is how the interface exposes meaning.
- A senior frontend engineer protects the user from network, browser, product, and team complexity.

---

## References Worth Keeping Nearby

- MDN Web Docs: https://developer.mozilla.org/
- Web.dev performance guides: https://web.dev/
- React docs: https://react.dev/
- Next.js docs: https://nextjs.org/docs
- Vue docs: https://vuejs.org/guide/introduction.html
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
