# 08 - Next.js Routing and Caching

> Why this file matters to you as a senior dev: the App Router file structure is mostly common sense. The caching is where Next.js earns its reputation for being "magical" or "confusing", depending on the day. This doc tames the caching by treating it as one system with four cooperating layers, with a decision framework for when to opt in or out.

---

## Routing: a tree of segments

Each folder under `app/` is a route segment. Files inside the folder give the segment its behavior:

```text
app/
├── layout.tsx          <- root layout, wraps everything
├── page.tsx            <- /
├── loading.tsx         <- shown via Suspense while page renders
├── error.tsx           <- error boundary for this segment
├── not-found.tsx       <- 404 boundary
├── products/
│   ├── layout.tsx      <- wraps every /products/* page
│   ├── page.tsx        <- /products
│   └── [id]/
│       ├── page.tsx    <- /products/123
│       └── reviews/
│           └── page.tsx <- /products/123/reviews
```

Layouts compose. The root layout wraps the products layout, which wraps the page. State in a layout (a `'use client'` layout, or server-rendered shell) persists across child route changes; only the changing segment re-renders.

> 💡 Insight - this is why "preserve scroll on a sidebar while the main panel changes" is trivial in App Router. The sidebar is in a parent layout, so it doesn't unmount when the child page changes. Pages Router required gymnastics for this.

### Special files, in one breath

- `page.tsx`: the route's UI.
- `layout.tsx`: persistent UI wrapping child segments.
- `loading.tsx`: instant fallback while the segment loads (built on Suspense).
- `error.tsx`: error boundary scoped to this segment and below.
- `not-found.tsx`: 404 boundary.
- `template.tsx`: like layout but **does** unmount on navigation (use rarely).
- `route.ts`: API endpoint for this URL (POST/GET/etc.).

### Dynamic and parallel routes (briefly)

`[id]` is a dynamic segment, available as `params.id`. `[...slug]` is a catch-all. `[[...slug]]` is an optional catch-all.

`@modal` and `@feed` folders are parallel routes: multiple "slots" rendered into the same layout simultaneously. Useful for things like a feed plus a sidebar that update independently.

`(group)` (parens) is a route group: organizational, doesn't appear in the URL. Useful for sharing layouts across unrelated routes.

That's enough routing to be productive. The docs cover the edge cases; the mental model is "folders are segments, special files give them behavior, layouts compose".

---

## The caching system: four layers, one mental model

Next.js has four caches. They cooperate, but they're independent. The trick is knowing which layer is responsible for what.

```text
   Request ----> Router Cache (client, in memory)
                    |
                    v
                Full Route Cache (server, persisted)
                    |
                    v
                Data Cache (server, persisted)
                    |
                    v
                Request Memoization (server, per-request)
                    |
                    v
                Origin (DB, API)
```

Each layer has different scope, different lifetime, different invalidation. Knowing which layer's behavior you're seeing is the entire game.

### Layer 1: Request Memoization

Scope: a single server-rendered request.

If two server components in the same render both call `fetch('/api/x')`, the second call uses the in-memory result from the first. No double-fetching even if components don't know about each other.

```jsx
// Both call fetchUser(); only one network request fires.
async function Sidebar() {
  const user = await fetchUser();
  return <Avatar user={user} />;
}

async function Header() {
  const user = await fetchUser();
  return <Greeting user={user} />;
}
```

Lifetime: the duration of one render. Cleared after the response is sent.

Invalidation: automatic, doesn't apply across requests.

> 💡 Insight - request memoization is why React docs say "fetch in the component that needs it, don't lift it". The "duplicate fetch" concern doesn't apply at this layer.

### Layer 2: Data Cache

Scope: server-side, across requests, persisted across deployments by default.

This is the long-lived cache that turns "dynamic data fetching" into "static-feeling pages". `fetch` calls in server components are cached by URL + options unless you opt out.

```jsx
// Cached forever (until you invalidate).
const data = await fetch('/api/products');

// Revalidate every 60 seconds.
const data = await fetch('/api/products', { next: { revalidate: 60 } });

// Never cache (always hit the origin).
const data = await fetch('/api/products', { cache: 'no-store' });
```

Invalidation:

- Time-based: `next: { revalidate: N }`.
- Tag-based: `next: { tags: ['products'] }` plus `revalidateTag('products')` after a mutation.
- Path-based: `revalidatePath('/products')`.

> ⚠️ Trap - if you `fetch` in a server component and don't pass options, you're caching forever by default. Make this an explicit choice, not an accident.

### Layer 3: Full Route Cache

Scope: server-side, the rendered RSC payload of a route.

When a route is statically rendered (no dynamic data, no `cookies()`/`headers()`/`searchParams` reads, default cache settings), Next.js caches the rendered RSC output. Subsequent requests serve the pre-rendered payload.

This is what makes `next build` produce static pages without you setting up `getStaticProps`.

The route opts out of full route caching automatically when:
- It uses dynamic functions (`cookies()`, `headers()`, `searchParams`).
- It uses uncached `fetch` (`cache: 'no-store'`).
- You explicitly mark it dynamic (`export const dynamic = 'force-dynamic'`).

```jsx
// This page becomes dynamic (no full route cache) because it reads cookies.
export default async function Page() {
  const session = cookies().get('session');
  // ...
}
```

> 🔍 Under the Hood - "static" in App Router doesn't mean "no JS". It means the RSC payload is pre-rendered. Client components inside still get JS shipped and hydrate normally.

### Layer 4: Router Cache

Scope: client-side, the user's browser, in-memory.

When the user navigates between routes, the router caches the RSC payloads of recently visited segments. Hitting back, switching tabs, or visiting a previously-loaded route reuses the cached output.

This is what makes navigation feel instant in a Next.js app even when the underlying data is dynamic.

Invalidation:

- Default TTL is short (around 30 seconds for dynamic routes, longer for static).
- A server action with `revalidatePath` or `revalidateTag` invalidates relevant entries.
- A hard refresh blows it away.
- `router.refresh()` from `useRouter()` forces re-fetch of the current route.

> ⚠️ Trap - the router cache is why "I made a mutation and the list still shows the old data" happens. Invalidate the right tag or path after mutations, or call `router.refresh()` from a client component.

---

## Putting it together: a mutation flow

A user adds a product. What needs to happen?

```text
   Server Action: addProduct()
        |
        |  insert into DB
        |  revalidateTag('products')
        v
   Data Cache:  drops cached fetches with tag 'products'
        |
        v
   Full Route Cache:  drops routes that use those fetches
        |
        v
   Router Cache (client):  framework re-fetches affected segments
        |
        v
   UI updates with the new product
```

You don't manually invalidate every layer. `revalidateTag` cascades. The trick is **tagging your fetches consistently** so invalidation has something to grab.

```jsx
// Read with a tag.
const products = await fetch('/api/products', { next: { tags: ['products'] } });

// Mutate, then invalidate.
'use server';
export async function addProduct(data) {
  await db.product.create({ data });
  revalidateTag('products');
}
```

> 💡 Insight - caching tags are domain concepts, not URL concepts. Tag by what the data *is* (`products`, `user-profile`), not where it lives. That way mutations to that domain invalidate everywhere it's read.

---

## A decision framework: static, dynamic, or revalidated?

For each route, ask:

1. **Does the user need fresh data on every visit?** If yes, dynamic (`cache: 'no-store'` or `force-dynamic`). The route renders per-request.

2. **Is the data fresh enough if it's a few minutes old?** If yes, revalidated. Use `next: { revalidate: 60 }` or similar. The route is statically rendered but the cache refreshes periodically.

3. **Does the data only change on explicit events (deploys, mutations)?** If yes, static plus tag-based revalidation. Tag the fetches; mutations call `revalidateTag`.

4. **Is the route per-user authenticated?** It has to be dynamic. Reading cookies/headers automatically makes it so.

```text
   Static                 Revalidated            Dynamic
   |                      |                      |
   marketing pages        product catalog        user dashboard
   docs                   blog index             checkout
   pricing                feature flags          settings
```

The wrong default is "everything dynamic". You'll pay for it in latency and infrastructure cost. The right default is "static unless I have a reason", with revalidation as the middle ground.

> ⚠️ Trap - `force-dynamic` on a route disables every server cache for that route. It's a sledgehammer. Reach for it only when you've ruled out per-fetch `cache: 'no-store'` or `revalidate: 0`.

---

## When the caching gets in your way

Three signals you're fighting the cache:

1. **"My mutation worked but the list shows old data."** Either you didn't invalidate, or you invalidated the wrong thing. Check your tags.
2. **"Two users see each other's data."** Almost always: you cached a per-user fetch globally. Either don't cache it (`cache: 'no-store'`) or include the user id in the cache key via the URL.
3. **"My local dev shows changes; production doesn't."** Your local has no Full Route Cache; production does. Check whether the route is static and needs invalidation.

The senior debugging move: **assume nothing about caching, verify each layer**. Use the network tab and the response headers (`x-nextjs-cache`, `x-vercel-cache`) to see what hit.

---

## What to carry forward

- App Router routing is folders as segments, layouts that compose, and special files (`page`, `layout`, `loading`, `error`) that give segments behavior.
- Four caches, in order: Request Memoization (per-render), Data Cache (cross-request), Full Route Cache (rendered RSC), Router Cache (client). Each has different scope and lifetime.
- Default `fetch` in server components caches forever. Always make caching an explicit choice (`revalidate`, `tags`, or `no-store`).
- Tag fetches by domain. Mutations call `revalidateTag` to invalidate everywhere that domain is read.
- The wrong default is "everything dynamic". Static plus revalidation is usually the right baseline, with dynamic for genuinely per-request routes.
