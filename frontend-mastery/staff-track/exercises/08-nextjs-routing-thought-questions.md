# 08 - Next.js Routing and Caching: Thought Questions

Companion to `docs/08-nextjs-routing-and-caching.md`. Three questions, all practical.

---

## Q1: Mutation didn't refresh the list

> What this tests: knowing which cache layer to invalidate and how tags propagate.

You ship a feature: a "Create project" form on `/projects` that uses a Server Action. The action creates the project and redirects back to `/projects`. The new project doesn't appear in the list until the user does a hard refresh.

The relevant code:

```jsx
// app/projects/page.tsx (server component)
const projects = await fetch('/api/projects').then(r => r.json());

// app/projects/actions.ts
'use server';
export async function createProject(formData) {
  await db.project.create({ data: { name: formData.get('name') } });
  redirect('/projects');
}
```

Walk through which cache layer is responsible for the stale list, then write the corrected `createProject` function.

---

## Q2: Static, revalidated, or dynamic?

> What this tests: applying the decision framework for cache strategy.

For each of these routes, decide: static, revalidated (and at what interval), or fully dynamic. Justify in one sentence each.

1. The marketing homepage with a "Featured products" section that updates a few times a day.
2. A blog post detail page with comments visible at the bottom.
3. The user's `/dashboard` showing their personalized data.
4. A pricing page.
5. A "Latest deals" page that needs to reflect changes within the next minute.
6. A product detail page where the price changes a few times per day, but the catalog rarely changes.

---

## Q3: Two users seeing each other's data

> What this tests: cache key scoping and the trap of caching personalized data globally.

A teammate's page:

```jsx
// app/inbox/page.tsx
import { cookies } from 'next/headers';

export default async function InboxPage() {
  const sessionId = cookies().get('session')?.value;
  const messages = await fetch(`/api/messages?session=${sessionId}`).then(r => r.json());
  return <MessageList messages={messages} />;
}
```

In production, users occasionally report seeing other users' messages. What's wrong, and what are two ways to fix it?
