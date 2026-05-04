# 02 - Closures, Prototypes, Async: Thought Questions

Companion to `docs/02-js-closures-prototypes-async.md`. Three questions, all practical.

---

## Q1: The stale closure in disguise

> What this tests: lexical environments and how rendering creates fresh bindings.

You're reviewing a search component:

```jsx
function SearchPanel() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  async function handleSearch() {
    const data = await fetchResults(query);
    setResults(data);
  }

  useEffect(() => {
    const id = setInterval(handleSearch, 5000);
    return () => clearInterval(id);
  }, []);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

The user reports: "I type a query, but the auto-refresh keeps fetching the empty string." Why? Pick the cleanest fix.

---

## Q2: The race that wasn't a race

> What this tests: async/await ordering, in-flight requests, and the distinction between concurrency and parallelism in single-threaded code.

A teammate's PR includes this handler for a "save and refresh" button:

```js
async function handleSaveAndRefresh() {
  await saveDraft();
  await refreshList();
  await refreshSidebar();
}
```

You suggested making the refreshes parallel:

```js
async function handleSaveAndRefresh() {
  await saveDraft();
  await Promise.all([refreshList(), refreshSidebar()]);
}
```

The teammate pushed back: "That's wrong, JavaScript is single-threaded, `Promise.all` doesn't actually parallelize anything." How do you respond, with a concrete reason?

---

## Q3: this binding in a class

> What this tests: how `this` binding works at the call site, and the practical fix.

```js
class TaskList {
  constructor() {
    this.tasks = [];
  }

  add(task) {
    this.tasks.push(task);
    document.querySelector('button').addEventListener('click', this.clear);
  }

  clear() {
    this.tasks = [];
  }
}
```

When the button is clicked, the click handler errors with `Cannot set properties of undefined`. What's wrong, and what are two ways to fix it (and which would you recommend in code review)?
