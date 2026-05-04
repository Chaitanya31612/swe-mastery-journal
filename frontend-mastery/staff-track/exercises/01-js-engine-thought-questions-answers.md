# 01 - JS Engine and Runtime: Answers

Companion to `01-js-engine-thought-questions.md`. Cross-references back to `docs/01-js-engine-and-runtime.md`.

---

## Q1: Predict the order

Output:

```text
1
6
3
5
4
2
```

Walking through it:

- `1` runs synchronously.
- `setTimeout(..., 0)` schedules a **task**, which won't run until microtasks drain.
- The first `Promise.resolve().then(...)` queues a microtask that will log `3` and queue another microtask.
- `queueMicrotask(...)` queues another microtask that will log `5`.
- `6` runs synchronously.

Now the call stack is empty. The microtask queue runs to completion before any task runs:

- First microtask: log `3`, queue another microtask for `4`.
- Second microtask (the one queued by `queueMicrotask`): log `5`.
- Third microtask (the one queued during `3`'s callback): log `4`.

Microtask queue is empty. Now we pick up tasks. The timer fires: `2`.

The wrong answer most people give: putting `4` before `5`. The trap is that microtasks queued during microtask execution run in the **same drain cycle**, but they go to the back of the queue. `5` was queued earlier, so it runs first.

Anchored in `docs/01-js-engine-and-runtime.md` -> "The event loop, properly".

---

## Q2: Why is this loop fast in dev and slow in production?

Two records with different shapes (`{ id, name, score }` vs `{ id, name, score, legacyFlag }`) means two different hidden classes in V8. The property access `records[i].score` was inline-cached for the first shape, then becomes **polymorphic** (multiple shapes) once the legacy records are seen, and eventually **megamorphic** if more shapes accumulate.

In dev with 10 same-shape records, the inline cache is monomorphic and machine-code fast. In production with mixed shapes, V8 falls back to a slower, more general lookup path.

The wrong answer is "10000 records is just slow". A loop over 10000 monomorphic-shape records is comically fast on modern hardware. The slowdown isn't proportional to the size; it's a constant factor on every property access.

The cheapest fix: normalize the records to one shape at the boundary (when you load them), even if you have to add `legacyFlag: undefined` to non-legacy records. Or strip `legacyFlag` from the legacy ones on load. Either way, every record going into the hot loop has the same shape.

Anchored in `docs/01-js-engine-and-runtime.md` -> "Hidden classes and inline caches".

---

## Q3: Spot the leak

Two problems compound:

1. **The listener is never removed.** Every call to `initPanel` adds a new click listener to that button (and if the same button is re-mounted, listeners stack). Even if the listener is on a fresh DOM node every time, the closure over `heavyConfig` keeps that data alive.

2. **`heavyConfig` is captured by the listener closure.** Every time `initPanel` runs, a new `heavyConfig` object is parsed and held alive by the listener. Across many mounts, you accumulate copies in memory.

Review comment, in roughly the words I'd use:

> This leaks. Two issues:
>
> 1. Move `heavyConfig` outside `initPanel` (or load it once at module init), so we don't allocate a fresh copy per mount.
> 2. Return a cleanup function from `initPanel` that removes the listener, and have the caller invoke it on unmount. Without that, even one-shot mounts retain the closure as long as the button stays in any retained DOM tree.
>
> Bonus: if `heavyConfig` is genuinely only needed by the analytics call, pass just the fields analytics needs, not the whole blob.

Anchored in `docs/01-js-engine-and-runtime.md` -> "Garbage collection in two sentences" and the listener-cleanup discussion.
