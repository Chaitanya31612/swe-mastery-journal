# 07 - Next.js Pages to App and RSC: Answers

Companion to `07-nextjs-rsc-thought-questions.md`.

---

## Q1: Where does 'use client' actually belong?

What's wrong: putting `'use client'` at the page level forces everything (title, description, price, reviews list) to be a Client Component. None of those need interactivity; they're all just data display. You'd ship megabytes of JS to render text that could be plain HTML.

The correct boundary structure:

```text
   page.tsx                                     server (async, fetches data)
   ├── ProductHero (title, desc, price)         server
   ├── ImageGallery                             server
   │   └── ImageGalleryControls (click zoom)    client  <- 'use client'
   ├── AddToCartButton                          client  <- 'use client'
   └── ReviewsSection                           server
       ├── ReviewSortDropdown (client picks order) client  <- 'use client'
       └── ReviewList (renders data)            server
```

The principle: **`'use client'` lives on the smallest leaf that needs interactivity**. The image data, review data, price, etc., never become Client Components. Their HTML is rendered on the server and shipped as static markup.

For the gallery specifically: the gallery layout, image URLs, and alt text are server-rendered. Only the click-to-zoom controls (the part that needs `onClick` and state) are client. You'd build it as a Server Component that imports a Client Component:

```jsx
// ImageGallery.tsx (server component)
import { ImageGalleryControls } from './ImageGalleryControls';

export function ImageGallery({ images }) {
  return (
    <div className="gallery">
      {images.map(img => <img key={img.id} src={img.url} alt={img.alt} />)}
      <ImageGalleryControls totalImages={images.length} />
    </div>
  );
}
```

The bundle impact: with this structure, only the JS for `ImageGalleryControls`, `AddToCartButton`, and `ReviewSortDropdown` ships to the browser. The rest is HTML.

The wrong answer often given: "but if I need state in any descendant, the parent has to be a Client Component, right?" No. The parent can be a Server Component that **renders** Client Components as children. The Client Component boundary is exactly the imported file marked `'use client'` and its descendants, not the whole tree above it.

Anchored in `docs/07-nextjs-pages-to-app-and-rsc.md` -> "Server/Client boundary, drawn as a tree".

---

## Q2: Server Action or Route Handler?

1. **"Add product to cart" button.** Server Action. It's a mutation triggered from a Client Component, and the action needs server-side authorization, DB write, and revalidation. Server Action is the canonical fit.

2. **Stripe webhook endpoint.** Route Handler. External systems POST to it; it must be a real URL with full HTTP control. Server Actions aren't designed for external callers.

3. **Load user profile on `/settings`.** Server component fetch. The page is rendered on the server; just `await` the profile in the server component. No need for an API.

4. **"Submit feedback" form.** Server Action. Form submission with mutation, ideally with `useActionState` for the form's submitting/error state.

5. **Search-as-you-type.** Route Handler (or a server component with searchParams if the result is part of a page). A keystroke-driven endpoint with no mutation, called frequently from the client; Server Actions add latency overhead. Route Handler is the right tool.

6. **Cron-triggered endpoint.** Route Handler. External callers (the cron service) need a stable URL with auth.

The pattern: **mutations from your own UI -> Server Actions. External callers -> Route Handlers. Reads in server-rendered pages -> server component fetches.**

The wrong answer: "always use Route Handlers because they're more flexible". You're paying flexibility tax for cases where Server Actions are simpler and faster.

Anchored in `docs/07-nextjs-pages-to-app-and-rsc.md` -> "Where to do data fetching".

---

## Q3: The hydration mismatch

What's happening: the server renders the component at one moment (using server's local time), and the client re-renders during hydration at another moment (using browser's local time). If those two moments fall on different sides of noon (or use different time zones), the rendered greeting differs.

The flicker the user sees: they get the server's HTML first ("Good morning"), then React hydrates and re-renders with the client's value ("Good afternoon"), so the text changes.

It only sometimes shows up because:

- It depends on the request hitting the server right before noon (server time) and the browser rendering right after.
- It depends on time zone differences between server and user.
- During `next dev`, server and client are usually the same machine, so the bug rarely shows locally.

Cleanest fix: render a stable server output, then update on the client after mount.

```jsx
'use client';

import { useState, useEffect } from 'react';

export function GreetingCard({ name }) {
  const [greeting, setGreeting] = useState('Hello');

  useEffect(() => {
    setGreeting(new Date().getHours() < 12 ? 'Good morning' : 'Good afternoon');
  }, []);

  return <div><h1>{greeting}, {name}</h1></div>;
}
```

The first render (server and initial client) shows "Hello". After mount, the effect runs and updates to the time-dependent greeting. No mismatch because the server and client agree on the initial value.

Better still, if the greeting can be deterministic from server-known data (e.g., user's stored timezone), compute it on the server and pass it down:

```jsx
// page.tsx (server)
const greeting = computeGreetingForUser(user);
return <GreetingCard name={user.name} greeting={greeting} />;
```

That avoids the flicker entirely.

The wrong answer: "use `suppressHydrationWarning`". That hides the warning but doesn't fix the flicker. The user still sees the swap. `suppressHydrationWarning` is for cases where you genuinely don't care about the mismatch (e.g., a timestamp that's expected to be slightly different).

Anchored in `docs/07-nextjs-pages-to-app-and-rsc.md` -> "Hydration: same word, different mechanics in App Router".
