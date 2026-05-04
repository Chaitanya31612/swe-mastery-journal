# 07 - Next.js Pages to App and RSC: Thought Questions

Companion to `docs/07-nextjs-pages-to-app-and-rsc.md`. Three questions, all practical.

---

## Q1: Where does 'use client' actually belong?

> What this tests: server/client boundary discipline and bundle-bloat awareness.

A teammate wants to migrate a product page from Pages Router. The page has:

- A title and description (just data display).
- A price (data display, formatted).
- An image gallery with click-to-zoom.
- An "Add to cart" button.
- A reviews list (just data display).
- A review-sort dropdown (changes the order via client interaction).

They proposed putting `'use client'` at the top of `app/products/[id]/page.tsx` because "we need event handlers in the gallery and the dropdown anyway".

Walk through what's wrong with this approach and sketch the correct boundary structure (which components are server, which are client, and where the directives live).

---

## Q2: Server Action or Route Handler?

> What this tests: knowing the right tool for mutations, reads, and external integrations.

For each of these, decide: server action, route handler, or server component fetch?

1. The "Add product to cart" button on a product page.
2. A webhook endpoint that receives Stripe events.
3. Loading the user's profile data when they visit `/settings`.
4. A "Submit feedback" form on the marketing page.
5. A search-as-you-type feature where every keystroke fetches results.
6. A scheduled cron job that needs an HTTP endpoint to trigger it.

---

## Q3: The hydration mismatch

> What this tests: understanding what hydration actually verifies and why differing server/client output causes warnings.

A teammate's component:

```jsx
'use client';

import { useState, useEffect } from 'react';

export function GreetingCard({ name }) {
  const greeting = new Date().getHours() < 12 ? 'Good morning' : 'Good afternoon';

  return (
    <div>
      <h1>{greeting}, {name}</h1>
    </div>
  );
}
```

In production, users sometimes see a hydration mismatch warning. They report that "the greeting flickers between morning and afternoon on first load."

Explain exactly what's happening, why the bug only sometimes shows up, and what's the cleanest fix that doesn't make the page slower.
