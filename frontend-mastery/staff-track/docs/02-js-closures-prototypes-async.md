# 02 - Closures, Prototypes, and Async Internals

> Why this file matters to you as a senior dev: closures explain "why is my state stale", prototypes explain "why does my class behave that way", and Promise internals explain every async bug you've ever shipped. These three together cover most language-level confusion in modern frameworks.

---

## Closures are about lexical environments, not about "trapping variables"

Every function in JavaScript carries a hidden reference: the **lexical environment** at the place it was defined. Not where it was called. Where it was *defined*.

That environment is a chain of variable bindings. When you read a variable inside the function, the engine walks the chain outward until it finds the binding.

```text
  outer environment
  +-------------------+
  | a = 1             |
  | inner = function  |
  +-------------------+
            |
            v
  inner's environment
  +-------------------+
  | b = 2             |
  +-------------------+
```

Inside `inner`, looking up `b` succeeds in the inner env. Looking up `a` walks one step outward. That walk is the closure.

```js
function counter() {
  let count = 0;
  return function increment() {
    count += 1;
    return count;
  };
}

const next = counter();
next();  // 1
next();  // 2
```

`count` is not a "trapped variable". It's a binding that lives in `counter`'s environment, and `increment` keeps that environment alive because it holds a reference to it. `counter` returned long ago. The binding survives because the inner function survives.

---

## The stale closure bug, demystified

This is the React bug everyone hits at least once.

```jsx
function SearchBox() {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const id = setTimeout(() => {
      console.log(query);
    }, 1000);
    return () => clearTimeout(id);
  }, []);
}
```

The effect runs once on mount. At that moment, `query` is `''`. The arrow function inside `setTimeout` closes over **that specific binding from that specific render**. When you type later, React renders a new `SearchBox` with a fresh `query` binding, but the old timer is still pointing at the old environment.

The fix is not "make the closure smarter". It's "tell the effect that it depends on `query`":

```jsx
useEffect(() => {
  const id = setTimeout(() => console.log(query), 1000);
  return () => clearTimeout(id);
}, [query]);
```

> 💡 Insight - every render in React creates a new set of bindings. The lint rule for exhaustive deps is not stylistic. It exists because the engine has no way to "look at the latest version" of a variable; closures only see the binding from when they were created.

---

## Prototypes: one chain, no magic

A JavaScript object is a bag of properties plus a hidden link called `[[Prototype]]`. When you read a property and the object doesn't have it, the engine follows that link and looks on the prototype. If still not found, follow again. Until the chain ends at `null`.

```text
  myDog ----[[Prototype]]----> Dog.prototype ----[[Prototype]]----> Animal.prototype ----[[Prototype]]----> Object.prototype ----> null
  { name: "Rex" }              { bark() {} }                        { eat() {} }                             { hasOwnProperty() {} }
```

Calling `myDog.bark()`:

1. Does `myDog` have a `bark` property? No.
2. Does `Dog.prototype` have one? Yes. Call it with `this = myDog`.

That `this = myDog` is the part everyone forgets: when you call a method through an object, `this` becomes the receiver, not the object that defined the method.

```js
const dog = {
  name: 'Rex',
  bark() {
    return `${this.name} barks`;
  },
};

const fn = dog.bark;
fn();          // "undefined barks", `this` is no longer `dog`
dog.bark();    // "Rex barks", `this` is `dog`
```

> ⚠️ Trap - passing methods as callbacks (`element.addEventListener('click', this.handleClick)`) detaches them from their `this`. Use `.bind(this)` or arrow functions or class fields to keep `this` glued.

---

## class is sugar over the prototype chain

If you've used `class`, you've used prototypes. You just got a syntax that hides the wiring.

```js
class Animal {
  eat() {}
}

class Dog extends Animal {
  bark() {}
}
```

is roughly:

```js
function Animal() {}
Animal.prototype.eat = function () {};

function Dog() {}
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.bark = function () {};
```

`Dog.prototype` is an object whose `[[Prototype]]` is `Animal.prototype`. Instances of `Dog` link to `Dog.prototype`, which links to `Animal.prototype`. One chain, two prototype objects, plenty of confusion if you stare at it cold.

> 🔍 Under the Hood - `instanceof` walks the prototype chain looking for `Constructor.prototype`. That's why `dog instanceof Animal` is true: `Animal.prototype` is somewhere in the chain.

---

## this in four binding modes

People memorize `this` rules. The shortcut is to know there are exactly four cases, in priority order.

1. **`new` binding**: `new Foo()` creates a fresh object and binds `this` to it.
2. **Explicit binding**: `fn.call(obj)`, `fn.apply(obj, args)`, `fn.bind(obj)`. Forces `this`.
3. **Implicit binding**: `obj.fn()`. `this` becomes `obj`.
4. **Default binding**: `fn()`. `this` is `undefined` in strict mode, `globalThis` otherwise.

Arrow functions are the exception: they don't bind their own `this`. They lexically capture it from the enclosing scope. That's why you use arrows for callbacks where you want `this` to refer to the outer object.

```js
class Counter {
  constructor() {
    this.count = 0;
    document.querySelector('button').addEventListener('click', () => {
      this.count += 1;  // `this` is the Counter, captured lexically
    });
  }
}
```

If you used a normal function there, `this` would be the button element.

---

## Promises are state machines

A Promise is one of three states: **pending**, **fulfilled**, or **rejected**. Once it transitions out of pending, it never changes. The `.then` callbacks attached to it are scheduled as microtasks when the state settles.

```text
       new Promise()
            |
            v
       [ pending ]
        /       \
   resolve()   reject()
      v             v
[ fulfilled ]   [ rejected ]
   |                |
   .then handlers   .catch handlers (queued as microtasks)
```

That's the whole machine. Everything else (chaining, `Promise.all`, `async`/`await`) is built on those three states and the microtask queue.

```js
const p = new Promise((resolve) => {
  console.log('A');
  resolve('value');
  console.log('B');
});

p.then((value) => console.log('C:', value));

console.log('D');
```

Output:

```text
A
B
D
C: value
```

The executor (`A`/`B`) runs synchronously. `resolve` settles the promise. The `.then` continuation is queued as a microtask. `D` runs (still synchronous). Then the stack drains and `C:` runs.

> 💡 Insight - calling `resolve` does not immediately call `.then` handlers. It only marks the promise as settled and schedules the handlers. This is what makes promise behavior consistent regardless of whether they settle sync or async.

---

## async/await is sugar, but it changes one thing

`async function` always returns a Promise. `await` pauses the function (in the sugar sense) until the awaited promise settles, then resumes the rest as a microtask.

```js
async function flow() {
  const a = await stepOne();
  const b = await stepTwo(a);
  return b;
}
```

is mentally:

```js
function flow() {
  return stepOne().then((a) => {
    return stepTwo(a).then((b) => b);
  });
}
```

Two practical consequences:

**Errors throw, not reject**. Inside an `async` function, you `throw err` or use `try`/`catch`. From the outside, that throw becomes a rejection. This is the one place where the sugar buys real syntactic clarity.

**Sequential awaits serialize**. Two `await`s in a row do work one after the other. If the work is independent, that's wasted latency.

```js
const user = await fetchUser();
const posts = await fetchPosts();
```

If those are independent, you're paying twice. Use `Promise.all`:

```js
const [user, posts] = await Promise.all([fetchUser(), fetchPosts()]);
```

> ⚠️ Trap - every sequential `await` should earn its sequence. If you're awaiting B but B doesn't actually need A's value, you've turned a 200ms parallel fetch into a 400ms serial chain.

---

## Cancellation: AbortController is the right pattern

Promises don't have built-in cancellation. The standard pattern is `AbortController`:

```js
const controller = new AbortController();

fetch('/api/search', { signal: controller.signal })
  .then((res) => res.json())
  .then(setResults)
  .catch((err) => {
    if (err.name === 'AbortError') return;
    showError(err);
  });

// Somewhere else:
controller.abort();
```

The `signal` is what you pass to anything that accepts cancellation. `fetch`, modern Web APIs, and increasingly third-party libraries all support it.

For your own async code, you check the signal yourself:

```js
async function pollUntilReady(signal) {
  while (!signal.aborted) {
    const res = await checkStatus({ signal });
    if (res.ready) return res;
    await sleep(1000);
  }
  throw new DOMException('Aborted', 'AbortError');
}
```

> 💡 Insight - every async operation in a UI should have a "what if the user moved on" answer. Either cancel it (`AbortController`) or check relevance when it resolves (request id pattern). If neither, you're inviting race conditions.

---

## Generators in 60 seconds

A generator is a function that can pause and resume. You probably won't write them often, but you should be able to read them, because async iterators and certain library internals lean on them.

```js
function* range(start, end) {
  for (let i = start; i < end; i++) {
    yield i;
  }
}

for (const n of range(0, 3)) {
  console.log(n);  // 0, 1, 2
}
```

Each `yield` returns a value and pauses. The next call to `.next()` resumes where it left off. `for...of` calls `.next()` for you.

Async generators add `await`:

```js
async function* fetchPages(url) {
  let next = url;
  while (next) {
    const page = await fetch(next).then((r) => r.json());
    yield page.items;
    next = page.nextUrl;
  }
}

for await (const items of fetchPages('/api/list')) {
  render(items);
}
```

This is how you stream paginated data lazily without building a giant array.

> 🔍 Under the Hood - `async function*` returns an async iterator. `for await ... of` calls `.next()` and awaits the resulting promise on each turn. Frameworks like Next.js use these patterns under the hood for streaming SSR.

---

## A senior debug pattern for async ordering

When async behavior is wrong, write the order in pseudo-time:

```text
T=0   click handler runs, calls fetchOne(), starts loading=true
T=1   click happens again, calls fetchOne() again
T=200 second fetch resolves first, sets loading=false, sets data="second"
T=300 first fetch resolves, sets loading=false, sets data="first"  <- bug
```

Now the bug isn't "promises are weird". It's "I have no relevance check". The fix writes itself: track an in-flight id, or `AbortController` the previous request, or guard with a stale check.

---

## What to carry forward

- A closure is a reference to a lexical environment. Every render or every loop iteration creates new environments; closures point at the one they were born in.
- Prototypes are one chain of objects. `class` is sugar over that chain. `this` is bound by call site, except for arrow functions which capture it lexically.
- Promises are a tiny state machine: pending, fulfilled, rejected. `.then` callbacks run as microtasks once the promise settles.
- `async`/`await` is sugar over `.then`. Sequential awaits serialize work; use `Promise.all` for independent operations.
- Every async UI flow needs a cancellation or relevance story. `AbortController` is the standard primitive.
