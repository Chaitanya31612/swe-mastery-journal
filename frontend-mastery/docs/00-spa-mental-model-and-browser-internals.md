# 00 - SPA Mental Model And Browser Internals

This doc is the foundation. React, Next, and Vue sit on top of the browser. If the browser model is weak, framework behavior feels magical. If the browser model is strong, most frontend decisions become mechanical.

---

## The Core Idea

A Single Page Application is not a page that never reloads.

It is an application that takes responsibility for work the browser used to do by default:

```text
traditional page
  browser requests URL
  server returns HTML
  browser displays a full document
  navigation asks the server for a new document

SPA
  browser loads an app shell
  JavaScript owns routing, state, rendering, and interaction
  navigation often changes UI without replacing the full document
```

That shift gives you smoother interactions, richer state, and less full-page interruption.

It also gives you more ways to break loading, routing, accessibility, caching, performance, and back-button behavior.

Senior intuition: a SPA borrows power from the browser, but also borrows responsibility.

---

## The Frontend Loop

Every interactive screen repeatedly does this:

```text
input
  user clicks, types, scrolls, drags, focuses, navigates

event
  browser dispatches an event to JavaScript

state transition
  code decides what changed

render calculation
  framework computes the next UI description

commit
  framework mutates the DOM

browser rendering
  style -> layout -> paint -> composite

feedback
  user sees, hears, or feels the result
```

When a UI feels bad, ask which link in this loop failed.

Examples:

- Click feels dead -> missing immediate feedback or blocked main thread.
- Page jumps -> layout changed after paint without reserved space.
- Spinner flashes -> loading state is technically correct but emotionally noisy.
- Back button breaks -> router state and URL state disagree.
- Form loses input -> component identity changed and local state was destroyed.

---

## Browser Loading Pipeline

When the browser receives a document, it builds several internal structures:

```text
HTML bytes
  -> tokens
  -> DOM tree

CSS bytes
  -> CSSOM tree

DOM + CSSOM
  -> render tree
  -> layout boxes
  -> paint commands
  -> compositor layers
  -> pixels
```

JavaScript can interrupt this pipeline because scripts may read or mutate the document.

Example:

```html
<div id="app"></div>
<script>
  document.getElementById('app').textContent = 'Loaded';
</script>
```

The browser cannot pretend the script has no effect. It must run it at the right time.

Senior intuition: HTML and CSS are streaming-friendly. JavaScript is often a checkpoint.

---

## Critical Rendering Path

The browser wants to show useful pixels quickly.

The critical path is the minimum work needed before first meaningful display:

```text
HTML needed for structure
CSS needed for visible styling
font choices that affect text display
JavaScript that blocks rendering or hydration
images needed above the fold
```

Bad version:

```text
HTML arrives
  -> giant CSS blocks render
  -> giant JS downloads
  -> JS parses
  -> JS executes
  -> app fetches data
  -> app renders
  -> user finally sees useful UI
```

Better version:

```text
HTML arrives with useful shell or content
  -> critical CSS is small
  -> non-critical JS is delayed or split
  -> layout space is reserved
  -> user sees stable progress
  -> interactivity arrives progressively
```

Interesting fact: a page can have fast network timing and still feel slow if the first visible thing is blank, unstable, or unresponsive.

---

## The Main Thread

Most frontend JavaScript runs on the main thread.

The main thread also handles many browser tasks:

```text
parse HTML
run JavaScript
calculate styles
layout
paint setup
dispatch events
run timers
run promise callbacks
```

If your JavaScript runs too long, the browser cannot respond.

Example:

```js
button.addEventListener('click', () => {
  const startedAt = performance.now();

  while (performance.now() - startedAt < 300) {
    // Simulate expensive work.
  }

  button.textContent = 'Done';
});
```

The user clicked immediately, but the visual response waits until the task ends.

Senior intuition: a blocked main thread is not "slow JavaScript" only. It is delayed input, delayed paint, delayed feedback, and lost trust.

---

## Event Loop In Frontend Terms

The event loop coordinates work:

```text
take one task
  -> run JavaScript until the stack is empty
  -> run queued microtasks
  -> browser may render
  -> take next task
```

Common task sources:

```text
tasks
  click event, timer callback, network event, script execution

microtasks
  promise callbacks, queueMicrotask, mutation observer callbacks

render opportunity
  style, layout, paint, composite
```

Example:

```js
console.log('A');

setTimeout(() => {
  console.log('B');
}, 0);

Promise.resolve().then(() => {
  console.log('C');
});

console.log('D');
```

Output:

```text
A
D
C
B
```

Why:

```text
current script task runs first
promise microtask runs before next task
timer task runs later
```

Senior intuition: promises do not make code parallel. They schedule continuations.

---

## Layout, Paint, Composite

Browser rendering is not one operation.

```text
style
  Which CSS rules apply?

layout
  What size and position is every box?

paint
  What pixels need to be drawn for borders, text, shadows, backgrounds?

composite
  How are layers combined on screen?
```

Some changes are more expensive than others:

```text
change width
  may trigger layout, paint, composite

change color
  may trigger paint, composite

change transform
  often only composite

change opacity
  often only composite
```

This is why animations usually prefer:

```css
.panel {
  transform: translateY(0);
  opacity: 1;
}
```

over:

```css
.panel {
  top: 0;
  height: 300px;
}
```

Do not memorize property lists. Memorize the question:

```text
Did I change geometry, pixels, or only layer composition?
```

---

## Forced Layout

The browser batches layout work when possible.

You can accidentally force it to stop and calculate layout immediately:

```js
box.style.width = '300px';

const width = box.offsetWidth;

box.style.height = `${width / 2}px`;
```

Reading `offsetWidth` after writing layout-affecting styles forces the browser to answer "what is the layout now?"

Bad loop:

```js
items.forEach((item) => {
  item.style.width = '300px';
  const height = item.offsetHeight;
  item.style.marginTop = `${height / 4}px`;
});
```

Better shape:

```js
const itemHeights = items.map((item) => item.offsetHeight);

items.forEach((item, index) => {
  item.style.width = '300px';
  item.style.marginTop = `${itemHeights[index] / 4}px`;
});
```

Senior intuition: separate reads from writes when touching layout directly.

---

## SPA Routing

Classic navigation:

```text
click link
  -> browser requests new HTML document
  -> previous JavaScript context disappears
```

SPA navigation:

```text
click link
  -> router intercepts navigation
  -> history API updates URL
  -> app chooses route component
  -> app fetches data if needed
  -> app renders new screen
```

The URL still matters.

A good SPA preserves browser expectations:

- refresh should keep the same screen when possible
- back and forward should behave predictably
- links should be real links when navigation is intended
- important view state should be shareable when users expect sharing
- route changes should announce meaningful context for assistive tech

Bad smell:

```text
The screen changes, but the URL does not.
```

Sometimes that is fine for a tab inside a card. It is usually wrong for product-level navigation.

---

## Rendering Modes

Modern frontend is not only SPA versus server pages.

Useful mental model:

```text
CSR - client-side rendering
  Browser gets a shell. JavaScript builds most UI.

SSR - server-side rendering
  Server returns HTML for the current request. JavaScript may hydrate it.

SSG - static generation
  HTML is created ahead of time.

ISR or revalidation
  Static output updates on a schedule or trigger.

Streaming
  Server sends UI in chunks as data becomes ready.

Partial hydration or islands
  Only some regions become interactive.
```

Trade-off map:

```text
Need fast first content?
  Prefer server or static HTML.

Need rich authenticated app behavior?
  Client rendering may be fine after login.

Need SEO or share previews?
  Server or static output helps.

Need highly personalized data?
  Think carefully about caching and server/client boundaries.

Need instant local interaction?
  Keep that interaction close to the client.
```

Senior intuition: rendering is data placement plus interaction placement.

---

## Hydration

Hydration means:

```text
server sends HTML
browser displays it
JavaScript loads
framework attaches event handlers and internal state to existing DOM
```

Hydration can fail or feel bad when:

- server HTML does not match client render
- client needs data the server did not have
- too much JavaScript must load before interaction
- the page looks ready but ignores clicks
- browser extensions or time-dependent values alter markup

Example mismatch:

```js
function Clock() {
  return <p>{new Date().toLocaleTimeString()}</p>;
}
```

The server time and client time may differ.

Better shape:

```js
function Clock() {
  const [time, setTime] = useState(null);

  useEffect(() => {
    setTime(new Date().toLocaleTimeString());
  }, []);

  return <p>{time || 'Loading time...'}</p>;
}
```

This makes the unstable value explicitly client-owned.

Senior intuition: hydration is not free. It is the cost of turning already-visible HTML into a living app.

---

## What Makes A SPA Feel Fast

Not just:

```text
low API latency
small bundle
high Lighthouse score
```

Also:

```text
immediate acknowledgement
stable layout
clear loading shape
optimistic feedback where safe
short main-thread tasks
predictable navigation
cached repeated work
useful empty states
recoverable errors
```

Example:

```text
User clicks Save.

Bad:
  Button does nothing for 800ms, then changes.

Better:
  Button immediately shows "Saving..."
  duplicate clicks are prevented
  form remains stable
  success appears near the action
  failure gives recovery
```

Fast is a feeling created by technical and interaction design choices together.

---

## Senior Debugging Questions

When a frontend issue is vague, ask:

- Is this a loading problem, interaction problem, rendering problem, data problem, or perception problem?
- Is the main thread blocked?
- Did the browser paint before the expensive work?
- Is layout shifting because space was not reserved?
- Is state duplicated between URL, cache, component, and form?
- Is the user waiting without knowing the system heard them?
- Is this broken only before hydration, after hydration, or after navigation?
- Did we optimize the wrong phase of the experience?

---

## The One-Sentence Model

A SPA is an event-driven state machine running inside the browser rendering pipeline.

If you know the state machine and the pipeline, you can reason about almost anything.
