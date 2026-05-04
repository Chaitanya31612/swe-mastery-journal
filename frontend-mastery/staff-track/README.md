# Frontend Staff Track

> Why this track exists: the original [frontend-mastery/](../) docs are a senior reference. This track is the mental-model upgrade that sits behind it. You read this when you want to think like the engineer maintaining the framework, not just using it.

---

## How to read this track

Read the docs in order on the first pass. Each one assumes the previous one has landed.

After that, jump by question:

- "I keep getting closure or async ordering wrong" -> `docs/01-js-engine-and-runtime.md` and `docs/02-js-closures-prototypes-async.md`
- "I want to actually understand React's render model" -> `docs/03-react-fiber-and-reconciliation.md`
- "I want to know what hooks really are" -> `docs/04-react-hooks-and-concurrent.md`
- "Vue is my daily driver and I want to feel the engine" -> `docs/05-vue-reactivity-and-compiler-internals.md`
- "I want Vue tricks I can use this week" -> `docs/06-vue-composition-patterns-and-tricks.md`
- "I know Pages Router, App Router still feels alien" -> `docs/07-nextjs-pages-to-app-and-rsc.md`
- "Next.js caching scares me" -> `docs/08-nextjs-routing-and-caching.md`
- "I want to ship UIs that feel like Linear" -> `docs/09-uiux-craft-and-perceived-performance.md`
- "I want reps" -> `exercises/`

---

## Folder layout

```text
staff-track/
├── README.md
├── docs/
│   ├── 01-js-engine-and-runtime.md
│   ├── 02-js-closures-prototypes-async.md
│   ├── 03-react-fiber-and-reconciliation.md
│   ├── 04-react-hooks-and-concurrent.md
│   ├── 05-vue-reactivity-and-compiler-internals.md
│   ├── 06-vue-composition-patterns-and-tricks.md
│   ├── 07-nextjs-pages-to-app-and-rsc.md
│   ├── 08-nextjs-routing-and-caching.md
│   └── 09-uiux-craft-and-perceived-performance.md
└── exercises/
    ├── 01-js-engine-thought-questions.md
    ├── 01-js-engine-thought-questions-answers.md
    ├── ...
    └── 09-uiux-thought-questions-answers.md
```

Every doc has a paired exercise file with 3-4 practical questions, and a separate answers file. Attempt cold, then check.

---

## Callout legend

The callouts are not decoration. Each one signals a specific kind of attention.

> 💡 Insight - counterintuitive or staff-level nuance. The kind of thing that flips your mental model when you finally see it.

> ⚠️ Trap - common mistake or misconception. If you nod and skip, you will hit it later.

> 🔍 Under the Hood - spec or engine internals. Read these when you want to know why, not just what.

> Plain blockquote without an icon is an interesting fact. Skim or savor, your call.

---

## Voice and conventions

- Pair-programming tone. One idea per paragraph.
- Code examples for every non-trivial concept, language tag on the fence.
- ASCII diagrams for flows (render pipeline, diffing, event loop).
- Every doc closes with `## What to carry forward`, 3-5 bullets you should be able to recite.
- When something is genuinely "go read the docs", I say so and move on. Depth lives where it actually compounds.

---

## What this track is not

- An API encyclopedia. Search for specific APIs.
- A beginner walkthrough of JSX, components, or what `setState` is.
- An exhaustive feature list for any framework.
- A guarantee that every detail is current with the very latest minor release. The mental models age slower than the APIs.

---

## Suggested study cadence

You can binge it, but the material rewards spacing. One doc per session is a sane default. The exercises are the part that actually moves the needle. Skipping them is the difference between "I read about Fiber" and "I can debug a Fiber bug in someone else's app".
