# 01 - JS Engine and Runtime: Thought Questions

Companion to `docs/01-js-engine-and-runtime.md`. Three questions, all practical. Try them cold; answers in the paired `-answers.md` file.

---

## Q1: Predict the order

> What this tests: event loop turn-taking between sync code, microtasks, and timers.

```js
console.log('1');

setTimeout(() => console.log('2'), 0);

Promise.resolve().then(() => {
  console.log('3');
  Promise.resolve().then(() => console.log('4'));
});

queueMicrotask(() => console.log('5'));

console.log('6');
```

What's the output, and why exactly?

---

## Q2: Why is this loop fast in dev and slow in production?

> What this tests: V8 hidden classes and inline caches, and the gap between dev assumptions and production hot paths.

You wrote a function that processes user records. In your dev test data (10 records, all the same shape), it's fast. On production (10,000 records, occasionally a record has an extra field for legacy reasons), it's notably slower than you'd expect from just the size difference.

```js
function processRecords(records) {
  let total = 0;
  for (let i = 0; i < records.length; i++) {
    total += records[i].score;
  }
  return total;
}
```

The records are all `{ id, name, score }` except some legacy ones that are `{ id, name, score, legacyFlag }`. Why is performance worse than 1000x slower, and what's the cheapest fix?

---

## Q3: Spot the leak

> What this tests: closure-driven memory leaks and retention via event listeners.

A teammate's PR adds analytics tracking on a settings panel:

```js
function initPanel(panelEl) {
  const heavyConfig = JSON.parse(largeConfigBlob);

  panelEl.querySelector('button').addEventListener('click', () => {
    analytics.track('settings_save', heavyConfig);
  });
}

// called whenever the panel is mounted
panelMounts.forEach(initPanel);
```

The panel is mounted and unmounted dozens of times per session as the user navigates. Memory keeps growing. What's wrong, and what's your review comment?
