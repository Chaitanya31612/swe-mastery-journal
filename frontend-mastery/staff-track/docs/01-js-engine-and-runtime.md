# 01 - The JavaScript Engine and Runtime

> Why this file matters to you as a senior dev: every framework you use sits on a JS engine and a host runtime. When perf gets weird, hydration mismatches, or async ordering bites, the bug almost always lives at this layer. You want to be able to point at the layer, not guess.

---

## The two things people conflate

The first thing to untangle: "JavaScript engine" and "JavaScript runtime" are different.

The **engine** parses and executes JS. V8 in Chrome and Node, JavaScriptCore in Safari, SpiderMonkey in Firefox. The engine knows about syntax, values, the call stack, the heap, and garbage collection. It does not know about `setTimeout`, `fetch`, or the DOM.

The **runtime** is the engine plus everything around it: the event loop, the task queues, the host APIs (DOM in browsers, `fs` in Node), and the threading model that makes the engine actually do useful work.

> 💡 Insight - when you say "JavaScript is single-threaded", you mean the engine's call stack is single-threaded. The runtime around it is wildly multi-threaded. The browser parses HTML, paints pixels, runs network I/O, and decodes images on other threads. They just don't share the JS heap.

---

## V8 in one diagram

```text
        source code
            |
            v
       [ Parser ]  --produces-->  AST
            |
            v
       [ Ignition ]  -->  bytecode + interpreter
            |
            | (hot code paths flagged)
            v
       [ TurboFan ]  -->  optimized machine code
            |
            | (deopt if assumptions break)
            v
       back to bytecode
```

V8 starts with the interpreter (Ignition) so your code runs fast. As functions get called repeatedly with consistent shapes, TurboFan compiles them down to optimized machine code. If the assumptions break later (a function was always called with `number`, suddenly gets a `string`), V8 deoptimizes back to bytecode.

This is why "tight loops over consistent shapes are fast" is real engineering advice and not folklore.

```js
function sumPoints(points) {
  let total = 0;
  for (let i = 0; i < points.length; i++) {
    total += points[i].x + points[i].y;
  }
  return total;
}
```

If every `point` has the same shape (same property order, same types), TurboFan loves this loop. If you sometimes pass `{ x, y }` and sometimes `{ y, x }` or `{ x, y, z }`, V8 keeps churning through different hidden classes and the optimized version doesn't stick.

> ⚠️ Trap - building objects by adding properties in different orders across your code base creates different hidden classes for what looks like "the same shape". For frequently-allocated objects in hot paths, set all properties in the constructor in the same order, every time.

---

## Hidden classes and inline caches

V8 doesn't store objects as hash maps the way the JS spec implies. It builds a **hidden class** (also called a "shape" or "map") that records property names and offsets. Two objects with the same hidden class can be accessed by the same machine-code path.

```js
function makePoint(x, y) {
  const point = {};
  point.x = x;     // hidden class C1
  point.y = y;     // hidden class C2 (transitions from C1)
  return point;
}

function makeWeird(x, y) {
  const point = {};
  point.y = y;     // hidden class C1' (different from C1!)
  point.x = x;     // hidden class C2' (not the same as C2)
  return point;
}
```

Two functions, "same" object, two completely different hidden class chains. The optimizer can't share machine code between them.

**Inline caches** are the next step: when V8 compiles `point.x`, it remembers "for hidden class C2, `x` is at offset 0". Next call with the same shape skips the lookup. Across many shapes, the cache gets polluted ("megamorphic") and access slows down.

> 🔍 Under the Hood - this is why frameworks like Vue, when shipping reactive proxies, are careful about how they wrap objects. Wrapping a reactive object inside another reactive object would cascade hidden-class transitions and tank performance for tight reactive paths.

---

## The call stack and the heap

Two memory regions you should be able to picture:

```text
  Stack                         Heap
+---------+                +-----------------+
| frame 3 |                | { x: 1, y: 2 }  |
+---------+                | "hello"         |
| frame 2 |                | function () {}  |
+---------+                | [1, 2, 3]       |
| frame 1 |                +-----------------+
+---------+
```

Stack holds **frames**: one per function call. Each frame has its local variables and a return address. When the function returns, the frame is popped. This is why deep recursion blows up: you exceed the stack's fixed budget.

Heap holds **objects**: anything that isn't a primitive lives here. Variables on the stack often hold a reference (a pointer) into the heap.

```js
function makeUser() {
  const name = 'Asha';
  const user = { name };  // user lives on the stack as a reference
  return user;            // the object itself stays in the heap
}

const u = makeUser();     // u still points at that heap object
```

`makeUser`'s frame is gone, but the object survives because something still references it. That's the basis of garbage collection.

---

## Garbage collection in two sentences

V8 uses a **generational GC**: most objects die young, so it splits the heap into a "young generation" (cheap to scan, scanned often) and an "old generation" (expensive to scan, scanned rarely). When you allocate, you get a slot in the young space. If you survive a couple of GC cycles, you get promoted to the old space.

The senior takeaway is not "do GC manually". It's **understand what keeps objects alive longer than you think**: closures, arrays you forgot to clear, event listeners you never removed, detached DOM nodes a component still holds a ref to.

```js
function attachLogger(button) {
  const buffer = new Array(1_000_000).fill('log');
  button.addEventListener('click', () => {
    console.log(buffer.length);
  });
}
```

That `buffer` lives forever, even after `attachLogger` returns, because the click handler closes over it. If you never remove the listener, you never free the buffer.

> ⚠️ Trap - DevTools "memory" tab shows you the leak after you have it. The cheaper habit is to assume any subscription, listener, observer, or timer is a leak unless you can name where it gets cleaned up.

---

## The event loop, properly

Here is the model worth memorizing.

```text
+--------------------------------------+
|             Call stack               |
+--------------------------------------+
              ^
              | (run to completion)
              |
+--------------------------------------+
|         Microtask queue              |  <- Promise callbacks, queueMicrotask
+--------------------------------------+
              ^
              | (drain fully between tasks)
              |
+--------------------------------------+
|           Task queue                 |  <- timers, I/O, click events, etc.
+--------------------------------------+
              ^
              | (one task per loop turn)
              |
        [ event loop ]  -- yields to browser rendering opportunities
```

Each tick:

1. Pull one **task** off the task queue. Push its callback onto the stack.
2. Run it to completion. The stack must be empty before we move on.
3. Drain the **entire microtask queue**. Every promise continuation queued during step 2, plus any queued during step 3 itself.
4. The browser may do a render pass.
5. Repeat.

```js
console.log('A');

setTimeout(() => console.log('B'), 0);

Promise.resolve().then(() => {
  console.log('C');
  Promise.resolve().then(() => console.log('D'));
});

console.log('E');
```

Output:

```text
A
E
C
D
B
```

`A` and `E` are synchronous. The promise microtasks (`C`, then `D` queued from inside `C`) drain fully before the timer task `B` runs.

> 💡 Insight - a long microtask chain can starve rendering. If you keep queueing promise continuations from inside promise continuations, the browser cannot get a paint in. This is why `await` in a tight loop can feel slow and freeze the UI even when individual awaits look fine.

---

## await is just sugar over microtasks

This is the part that fixes most async confusion.

```js
async function save() {
  setStatus('saving');
  await api.save();
  setStatus('saved');
}
```

Mentally rewrite that as:

```js
function save() {
  setStatus('saving');
  return api.save().then(() => {
    setStatus('saved');
  });
}
```

Everything after an `await` is a microtask continuation. The function does not pause. It returns a promise immediately, and the rest is scheduled.

This is why:

```js
button.addEventListener('click', async () => {
  setLoading(true);
  await fetchData();
  setLoading(false);
});
```

The first `setLoading(true)` runs synchronously inside the click handler. The `setLoading(false)` runs as a microtask after `fetchData` resolves. If another click happens between, you have two in-flight requests racing each other, and the one that resolves last wins. The handler being `async` did not buy you any concurrency safety.

> ⚠️ Trap - `async` functions return immediately. If your event handler is async and you don't track the in-flight request, you're inventing race conditions for free.

---

## Tasks vs microtasks for frameworks

React, Vue, and most async-aware libraries lean hard on the microtask queue.

- React schedules state updates and tries to flush them as microtasks within the same event so multiple `setState` calls coalesce into one render.
- Vue's reactive system schedules re-renders into the microtask queue (`nextTick` is built on this).

That's why:

```js
count.value += 1;
console.log(button.textContent);  // still old value
await nextTick();
console.log(button.textContent);  // updated
```

Vue scheduled the update, but it hasn't flushed yet. Your sync `console.log` ran before the microtask drained.

> 🔍 Under the Hood - `Promise.resolve().then(...)` is the cheapest "do this after the current sync code" primitive. `setTimeout(..., 0)` is *much* slower because it enters the task queue, which means rendering opportunities first.

---

## Memory model and what "shared" means

Workers and the main thread don't share JS heap memory. They communicate via `postMessage`, which copies (or transfers) data. The exception is `SharedArrayBuffer` plus `Atomics`, which gives you actual shared memory but requires cross-origin isolation headers.

This matters because the easy answer to "JS is single-threaded" is "use workers". And it works, but you need to think about serialization cost.

```js
const worker = new Worker('parse.js');

worker.postMessage(hugeBlob);  // hugeBlob is structured-cloned
```

A 50 MB object getting cloned to send to a worker can be slower than just doing the work on the main thread. Transferable objects (`ArrayBuffer`, `MessagePort`, etc.) can be moved instead of copied, which is the senior workaround.

> Interesting fact: Chrome's V8 and Node.js share the same engine, which is why Node feature parity with browser JS is so tight. The runtime around it is completely different (no DOM, but `fs`, `net`, `process`, etc.), but the language and engine are the same binary lineage.

---

## A tiny mental checklist for engine-related debugging

When something feels off at the engine layer, ask in this order:

1. Is this code running on the call stack right now, or has it been queued? If queued, microtask or task?
2. Is this object's shape consistent across the hot path?
3. Is something keeping a reference alive past the lifetime I expected?
4. Am I assuming `await` pauses the world? It doesn't.

Most "weird async" or "weird perf" bugs collapse to one of these.

---

## What to carry forward

- The engine runs JS. The runtime gives it timers, I/O, the DOM, the event loop. They are different layers; debug at the right one.
- V8 optimizes for consistent object shapes and consistent call sites. Inconsistency forces deoptimization.
- The event loop runs one task, fully drains microtasks, then maybe paints. Long microtask chains starve rendering.
- `await` is not a pause. Code after it is a microtask continuation. Race conditions are easy to invent if you forget that.
- Objects survive as long as something references them. Closures, listeners, timers, and detached DOM are the usual suspects when memory grows.
