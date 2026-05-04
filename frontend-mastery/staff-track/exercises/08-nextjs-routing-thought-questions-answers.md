# 08 - Next.js Routing and Caching: Answers

Companion to `08-nextjs-routing-thought-questions.md`.

---

## Q1: Mutation didn't refresh the list

The cache layer responsible: most likely the **Data Cache** (cross-request, persists). The `fetch('/api/projects')` in the server component caches by default. The action wrote to the DB but didn't invalidate the cached fetch, so the next request still got the cached pre-mutation list.

The Full Route Cache may also be involved if the route is statically rendered. In that case, even the rendered output is cached.

Corrected action:

```ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createProject(formData) {
  await db.project.create({ data: { name: formData.get('name') } });
  revalidatePath('/projects');
  redirect('/projects');
}
```

`revalidatePath('/projects')` invalidates both the Data Cache entries used by that route and the Full Route Cache for that route.

The cleaner long-term version uses **tags** so multiple routes that read the same data can be invalidated together:

```ts
// In the server component:
const projects = await fetch('/api/projects', {
  next: { tags: ['projects'] }
}).then(r => r.json());

// In the action:
import { revalidateTag } from 'next/cache';

export async function createProject(formData) {
  await db.project.create({ data: { name: formData.get('name') } });
  revalidateTag('projects');
  redirect('/projects');
}
```

Now any route that reads `tags: ['projects']` gets invalidated, regardless of where it lives. This is the senior pattern: tag by domain, invalidate by tag.

The wrong answer: "use `cache: 'no-store'` on the fetch". That works (the list always re-fetches) but throws away every benefit of caching. You'd pay full latency on every visit, even visits where nothing changed. Tag-based invalidation gives you the cache benefit and the freshness.

Anchored in `docs/08-nextjs-routing-and-caching.md` -> "Putting it together: a mutation flow".

---

## Q2: Static, revalidated, or dynamic?

1. **Marketing homepage with featured products updating a few times a day.** Revalidated, every hour or two. Static is fine; dynamic is overkill. Tag the featured-products fetch and `revalidateTag` from the admin tool when curators publish a change for instant updates.

2. **Blog post detail page with comments.** Two-layer answer. The post itself: static, revalidated occasionally. The comments: dynamic, or fetched in a separate component with `cache: 'no-store'`. Or use a client-component comment widget that fetches its own data, leaving the post itself fully static.

3. **User's `/dashboard`.** Dynamic. Reads cookies/session; the route opts into dynamic automatically. Caching wouldn't be safe even if you wanted it.

4. **Pricing page.** Static. The price doesn't change per visit. If pricing updates, deploy or `revalidatePath` from a CMS hook.

5. **"Latest deals" page, freshness within 1 minute.** Revalidated, `revalidate: 60`. The 60-second staleness is acceptable; static rendering means most users hit the cached version.

6. **Product detail with prices changing a few times daily.** Static (the catalog content) plus `revalidate: 300` or tag-based invalidation. The product description, images, and metadata are static; the price update is the trigger. If prices change in your admin tool, that tool calls `revalidateTag('product:N')` after the change.

The pattern: default to static, opt into revalidation for "fresh enough" data, opt into dynamic only when truly per-request. Mix strategies within one page if different parts have different freshness needs.

Anchored in `docs/08-nextjs-routing-and-caching.md` -> "A decision framework: static, dynamic, or revalidated?".

---

## Q3: Two users seeing each other's data

What's wrong: the `fetch('/api/messages?session=' + sessionId)` is cached in the Data Cache by URL. If two users have similar session IDs (or, in the real bug, you weren't actually putting the session ID in the URL and it was identical for everyone), Next.js might serve a cached response. Even if the URL is different per user, you're caching personalized data, which is a cardinal sin.

Two fixes:

**Fix 1: opt out of caching for personalized fetches.**

```ts
const messages = await fetch(`/api/messages`, {
  cache: 'no-store',
  headers: { authorization: `Bearer ${sessionToken}` }
}).then(r => r.json());
```

Each user's request hits the origin. No cross-user contamination. Cost: full latency on every visit.

**Fix 2: don't fetch over HTTP at all; query the DB directly.**

```ts
const messages = await db.message.findMany({
  where: { userId: session.userId }
});
```

Server components can talk to the database directly. Skipping the HTTP layer skips the cache entirely. Cost: a different architectural choice, but often simpler and faster in App Router apps.

The senior framing: **never cache anything that depends on user identity unless the cache key includes the user**. The default fetch caching is great for shared data; it's a footgun for personalized data.

The wrong answer: "make the API endpoint return `Cache-Control: no-store`". That doesn't help because Next.js's Data Cache is independent of HTTP cache headers; the framework caches by default unless you tell it not to.

Anchored in `docs/08-nextjs-routing-and-caching.md` -> "When the caching gets in your way".
