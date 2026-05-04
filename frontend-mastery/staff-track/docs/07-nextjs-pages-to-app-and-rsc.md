# 07 - Next.js: From Pages Router to App Router and RSC

> Why this file matters to you as a senior dev: you know Pages Router. App Router is not a different framework, it's the same ideas with a different boundary. This doc is the bridge: every concept lands as an evolution of something you already understand. Once you see the mapping, RSC stops feeling alien.

---

## The honest framing of the change

Pages Router was: "files in `pages/` become routes. Each page is a React component. Some pages get a `getServerSideProps` or `getStaticProps` that runs on the server and feeds props in."

App Router is: "files in `app/` become routes. Each route is a tree of components, some run on the server, some run on the client, and the data fetching is colocated with the component that needs it."

The architectural shift is **moving from page-level data fetching to component-level data fetching**, made possible by React Server Components (RSC).

```text
   Pages Router                                 App Router

   pages/products/[id].js                       app/products/[id]/page.tsx
     getServerSideProps -> fetches data           page.tsx fetches data directly (server component)
     export default function Page(props)         layout.tsx wraps it
     all client JS                                only client what's marked 'use client'
```

> 💡 Insight - RSC is not "SSR but better". SSR renders React on the server and ships HTML plus the JS to re-hydrate. RSC renders React on the server and ships **a description of the rendered tree** plus the JS only for components that need interactivity. Different output, different mental model.

---

## What a Server Component actually is

A Server Component is a React component that runs **only on the server**. It can:

- `await` directly in the component body (it's an async function).
- Read databases, env vars, secrets, file system.
- Import server-only code (Node modules, ORM clients).

It cannot:

- Use `useState`, `useEffect`, or any other browser-specific hook.
- Attach event handlers.
- Use browser APIs (`window`, `localStorage`).

```jsx
// app/products/[id]/page.tsx
export default async function ProductPage({ params }) {
  const product = await db.product.findUnique({ where: { id: params.id } });
  return (
    <article>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <Price amount={product.price} />
      <AddToCartButton productId={product.id} />
    </article>
  );
}
```

`ProductPage` is a Server Component. It runs on the server, fetches the product, returns JSX. None of this code ships to the browser.

`AddToCartButton` is interactive. It needs to be a Client Component:

```jsx
// app/products/[id]/AddToCartButton.tsx
'use client';

import { useState } from 'react';

export function AddToCartButton({ productId }) {
  const [adding, setAdding] = useState(false);
  return (
    <button onClick={() => addToCart(productId, setAdding)} disabled={adding}>
      {adding ? 'Adding...' : 'Add to cart'}
    </button>
  );
}
```

The `'use client'` directive at the top is the boundary. Everything imported from this file (and the file's own code) runs in the browser.

---

## The Pages-to-App mapping you already know

If you mentally translate, App Router is a few APIs you've already used, just relocated:

| Pages Router                              | App Router equivalent                                        |
|-------------------------------------------|--------------------------------------------------------------|
| `pages/products/[id].js`                  | `app/products/[id]/page.tsx`                                 |
| `getServerSideProps`                      | `await fetch()` directly in the server component             |
| `getStaticProps`                          | Same as above; caching makes it static                       |
| `getStaticPaths` + `getStaticProps`       | `generateStaticParams` + server component                    |
| `_app.js`                                 | `app/layout.tsx` (root layout)                               |
| `_document.js`                            | `app/layout.tsx` provides the `<html>` and `<body>`           |
| `pages/api/*`                             | `app/api/*/route.ts` (route handlers)                        |
| `next/router` (`useRouter`)               | `next/navigation` (`useRouter`, `usePathname`, `useSearchParams`) |
| Per-page data fetching                    | Per-component data fetching (RSC)                            |

The shift to learn is not the file naming. It's that data fetching moved from "one block at the top of the page" to "wherever the component that needs the data lives".

> 💡 Insight - every server component can `await`. That means a deep component buried in the tree can fetch its own data without prop-drilling from the page. This was impossible in Pages Router, and it's the single biggest ergonomic win.

---

## Server/Client boundary, drawn as a tree

The rule: **a Client Component cannot import a Server Component**, but a Server Component can import a Client Component.

```text
   <Page>                       (server)
     <Layout>                   (server)
       <Header>                 (server)
         <CartIndicator />      (client)
       </Header>
       <Main>                   (server)
         <ProductList />        (server, async, fetches data)
         <ReviewSection>        (server)
           <ReviewSortDropdown /> (client)
           <ReviewList />       (server)
         </ReviewSection>
       </Main>
     </Layout>
   </Page>
```

Server components compose with each other freely. When you cross into a Client Component, that's the **boundary**. Everything inside that boundary, plus everything that boundary imports, is shipped to the browser.

The senior heuristic: **push the `'use client'` boundary as deep as possible**. Don't put it at a layout or a page. Put it on the smallest leaf that actually needs interactivity.

```jsx
// Bad: top of the page is client.
'use client';
export default function Page() {
  // ...renders product, cart, reviews, AddToCart, etc.
  // Now everything ships to the browser.
}

// Good: server page, client only where needed.
export default async function Page() {
  const product = await fetchProduct();
  return (
    <>
      <ProductHero product={product} />     {/* server */}
      <AddToCartButton id={product.id} />   {/* client */}
      <Reviews productId={product.id} />    {/* server */}
    </>
  );
}
```

> ⚠️ Trap - accidentally adding `'use client'` to a layout is the most common bundle-bloat bug. Half the app becomes client-rendered for the sake of one button. Always check what you're marking.

---

## Passing data across the boundary

Props from server to client must be **serializable**. Plain objects, arrays, primitives, dates: fine. Functions, class instances, Maps with non-serializable values: not fine.

```jsx
// Server component
<AddToCartButton onAdd={() => track('add')} />     // ERROR: function not serializable

// Server component
<AddToCartButton productId={product.id} />          // OK: string
```

If you need to pass behavior, the pattern is **Server Actions** (functions tagged `'use server'`):

```jsx
// app/products/[id]/actions.ts
'use server';

export async function addToCart(productId) {
  // runs on the server, but can be invoked from a client component
}

// app/products/[id]/AddToCartButton.tsx
'use client';
import { addToCart } from './actions';

export function AddToCartButton({ productId }) {
  return <button onClick={() => addToCart(productId)}>Add</button>;
}
```

`addToCart` runs on the server. The client component imports a reference; calling it is an RPC across the boundary.

> 🔍 Under the Hood - Server Actions are POST requests under the covers. The framework hides that, but the implication is real: they cost a network round-trip and they're not for high-frequency calls. Use them for mutations, not for reads (use server components for reads).

---

## Streaming SSR with Suspense

Pages Router rendered the entire page on the server, then sent the HTML. If one slow query held up the page, the whole page was slow.

App Router streams. Server components render in parallel. When they hit a slow `await`, the framework wraps that subtree in a Suspense boundary (you can also do it explicitly), sends what's ready, and continues streaming the rest.

```jsx
export default async function Page() {
  return (
    <>
      <ProductHero product={await fetchProduct()} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews />
      </Suspense>
    </>
  );
}
```

The hero renders first and goes out as HTML. The reviews part streams later. The user sees the hero immediately; the reviews fill in as the data arrives.

```text
   T=0    request arrives
   T=50   hero ready -> stream <ProductHero/> HTML
   T=50   <Suspense> placeholder streamed (skeleton)
   T=300  reviews data ready -> stream replacement HTML
   T=300  client patches the skeleton with real reviews
```

> 💡 Insight - streaming changes "time to first byte" into "time to first useful byte". The number that matters is when the user sees something they can read or click, not when the whole page is rendered.

---

## Hydration: same word, different mechanics in App Router

In Pages Router, hydration meant: server rendered HTML for the page; client downloads JS; React attaches handlers and state to the existing DOM.

In App Router, hydration is **selective**. Only the Client Component subtrees hydrate. Server Component subtrees never hydrate; they're pure HTML.

```text
   server-rendered tree (HTML)
   ├── ProductHero  (server only, no JS shipped)
   ├── AddToCart    (client, hydrates)
   ├── Reviews      (server only)
   └── ReviewSort   (client, hydrates)
```

Two consequences:

- **Less JS shipped.** Server-only subtrees cost zero client bytes.
- **Hydration boundaries match `'use client'` boundaries.** If you have one big `'use client'` at the page level, the whole page hydrates.

> 💡 Insight - hydration also progresses with streaming. As more HTML arrives, more `'use client'` islands become hydrate-able. The user can interact with hydrated parts before the rest has even rendered.

---

## Where to do data fetching

Three places, with different uses:

**Server components (default).** For loads that should happen at request time, with full server access.

```jsx
const product = await fetchProduct(id);
```

**Route Handlers (`app/api/*/route.ts`).** For endpoints called by client code or external systems. Use these like Pages Router's `pages/api`.

```ts
export async function POST(req) {
  const data = await req.json();
  return Response.json(await db.create(data));
}
```

**Server Actions.** For mutations triggered from forms or client components. Server-side function, callable from the client.

The senior heuristic: **read with server components, write with server actions, build APIs with route handlers**. If you find yourself making a `fetch('/api/...')` call from a client component to get data the server already has, you're using the wrong tool.

---

## When to keep using Pages Router

App Router is the future for new projects. For existing projects, the migration is non-trivial. The honest framing:

- If your app is a thin frontend over an existing API, Pages Router is still fine.
- If you don't need streaming, server actions, or per-component data fetching, the upgrade buys you less.
- Mixing the two routers in one app works (`pages/` and `app/` can coexist), so migrations can be incremental.

> ⚠️ Trap - migrating because "App Router is the new way" without a real benefit is a great way to introduce caching bugs and bundle regressions. The boundary discipline App Router requires is real engineering work.

---

## What to carry forward

- App Router moves data fetching from the page level to the component level. Server components can `await` directly, no `getServerSideProps` block.
- The `'use client'` directive marks the server/client boundary. Push it as deep as possible; the smaller the client surface, the less JS ships.
- Server components cannot use hooks or attach handlers. Client components cannot import server components (only the other way). Props across the boundary must be serializable.
- Streaming SSR with Suspense lets ready content render first while slower subtrees fill in. This is the biggest user-facing win over Pages Router.
- Read with server components, mutate with server actions, expose APIs with route handlers. Don't `fetch('/api')` from a client component for data the server already has.
