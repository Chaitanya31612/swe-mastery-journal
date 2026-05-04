# 09 - UI/UX Craft and Perceived Performance

> Why this file matters to you as a senior dev: the difference between a UI that feels "fine" and one that feels like Linear or Stripe is rarely a single technique. It's a stack of small decisions about feedback, motion, latency masking, and respect for the user's attention. Once you can name those decisions, you can make them deliberately.

---

## The framing: UX is the management of expectations

Users don't actually have a stopwatch. They have a sense of "this app respects me" or "this app is slow". Those judgments are formed in the first 200 milliseconds and sustained by every interaction afterward.

The frame shift: you're not optimizing milliseconds. You're managing the user's mental model of "what is happening". Fast responses build trust. Quiet responses break it. Inconsistent responses create anxiety.

> 💡 Insight - Stripe's checkout doesn't feel fast because the network is fast. It feels fast because every click acknowledges immediately, every state change is named, every error tells you what to do next. The actual transaction is the same speed as a worse-designed competitor's.

---

## Linear, Vercel, Stripe, Apple: four schools, one philosophy

Each company has a distinctive UI vibe. The shared philosophy is "the system never makes the user wait without knowing why".

**Linear**: optimistic UI is the default. Click anything; the UI commits instantly. The mutation happens in the background. If it fails, recover gracefully. Keyboard navigation is first-class. Animation is short and informative.

**Vercel**: every state is named. Loading is never a generic spinner; it's "Building your deployment", "Routing to a region", "Provisioning". The system narrates itself.

**Stripe**: input fields are unforgiving about correctness but forgiving about UX. Error messages are placed near the field, copy is human, you never lose entered data. Forms feel like they trust you.

**Apple**: motion has meaning. Things that come from offscreen come from where they should. Things that disappear go where they're going. Spatial consistency is a UX feature.

You can copy the patterns. The deeper move is copying the **discipline**: every interaction has been considered, no state is unhandled, no copy is generic.

---

## Perceived performance: the four levers

There are exactly four levers for making UI feel faster without actually being faster. Master these and you'll outperform "actually faster" UIs that don't use them.

### Lever 1: Acknowledge immediately

The user clicked. Show them the system heard them. **Within the same event loop turn**, ideally before the next paint.

```jsx
// Bad: button does nothing for 300ms.
async function handleSave() {
  await api.save();
  toast('Saved');
}

// Better: state changes synchronously.
async function handleSave() {
  setStatus('saving');
  try {
    await api.save();
    setStatus('saved');
  } catch (err) {
    setStatus('error');
  }
}
```

Even 100ms without acknowledgement registers as "did it click?" The button changing label, going disabled, showing a spinner: any of these proves the click was heard.

> 💡 Insight - the perceived latency of a click is the time until something on screen changes, not the time until the operation completes. These are different numbers. Always optimize the first.

### Lever 2: Optimistic UI

For low-risk reversible actions, commit the change locally before the server confirms. If the server disagrees, roll back and apologize.

```jsx
function toggleStar(id) {
  setItems((items) => items.map(i => i.id === id ? { ...i, starred: !i.starred } : i));
  api.toggleStar(id).catch(() => {
    setItems((items) => items.map(i => i.id === id ? { ...i, starred: !i.starred } : i));
    toast('Could not save. Reverted.');
  });
}
```

The user clicks the star, it fills instantly, life moves on. If the network fails, they see a toast and the star reverts.

When **not** to use optimistic UI:

- Payment flows. Never lie about money.
- Permission changes. The user must know if they failed.
- Destructive actions without undo. If it can't be reversed, get confirmation.

> ⚠️ Trap - optimistic UI without rollback is just a lie. You must handle the failure path explicitly, and you must show the user when reality diverged from their expectation.

### Lever 3: Skeleton screens, but only when they help

Skeletons preserve layout while content loads. They're great when the layout is predictable and the wait is non-trivial (over ~300ms).

They hurt when:

- The layout is unstable (skeleton shows a wrong shape, then content rearranges).
- The wait is too short (skeleton flashes for 50ms and looks like a glitch).
- The content is below the fold (waste of design effort; the user can't see it anyway).

```jsx
// Wrong: spinner in the middle of an empty page.
{loading ? <Spinner /> : <Dashboard data={data} />}

// Better: skeleton that mirrors the final layout.
{loading ? <DashboardSkeleton /> : <Dashboard data={data} />}
```

The senior version of this rule: **show the user what's coming, then fill it in**. Never show "blank, then suddenly content". The visual jump is what feels jarring, not the wait.

### Lever 4: Prefetch what's likely next

If the user is hovering on a link, they might click. Start fetching the next page before they decide.

```jsx
// Next.js Link prefetches automatically.
<Link href="/products" prefetch>Products</Link>

// Custom: prefetch on hover.
<button
  onMouseEnter={() => queryClient.prefetchQuery(...)}
  onClick={() => navigate(...)}
>
  Open
</button>
```

Apple, Linear, and Vercel all do this aggressively. Hover-to-prefetch turns "click and wait" into "click and it's already there".

Cost: bandwidth, server load, possibly wasted requests. For high-value navigation paths, the cost is worth it. For every link in a list of 1000 items, it's not.

---

## Affordances: tell the user what they can do

An affordance is a visual cue that says "this is interactive". Buttons look pressable. Links look clickable. Drag handles look draggable.

The mistake is to make everything look the same in pursuit of "clean design". Cleanliness is not the goal. **Predictability** is the goal.

Three concrete rules:

1. **Buttons should look like buttons.** Different from text, different from links, different from drag handles. If your "minimal" design makes them indistinguishable, your design is failing.
2. **Hover states should reveal interactivity.** Cursor change, color change, slight elevation. The user moves their cursor over your UI as a question; the hover state is your answer.
3. **Disabled states should explain why.** A grey button with no tooltip is a dead end. A grey button with "Complete profile to enable" is a path forward.

> 💡 Insight - every "clean" design from Linear, Stripe, or Apple still has unmistakable affordances. The cleanliness is in the surrounding noise, not in hiding what's interactive.

---

## Empty, loading, error: the three states everyone forgets

Most components implicitly assume "data is here". They handle the success case beautifully and crash on the others.

A senior component handles four states:

```text
                  no request yet -> empty state
                  request in flight -> loading state
                  request failed -> error state with recovery
                  request succeeded with no data -> empty state with action
                  request succeeded with data -> normal render
```

For each component you build, walk through this list. If any state is "I didn't think about that", that's a bug waiting.

```jsx
function Inbox({ messagesQuery }) {
  if (messagesQuery.isLoading) return <InboxSkeleton />;
  if (messagesQuery.isError) return <ErrorState onRetry={messagesQuery.refetch} />;
  if (messagesQuery.data.length === 0) return <EmptyInbox />;
  return <MessageList messages={messagesQuery.data} />;
}
```

The empty state is where most products fail to charm. A blank screen with "No messages" is forgettable. An illustration plus copy plus a "Compose" button turns an empty inbox into an onboarding moment.

---

## Motion: when it earns its place

Motion is a tool, not decoration. Three legitimate uses:

1. **Spatial continuity.** When something moves, animating it makes the user understand "this is the same thing, just somewhere else". Disappear-and-reappear is jarring; slide-from-here-to-there is intuitive.
2. **State change confirmation.** A checkmark animating in says "yes, that worked", more clearly than a static check would.
3. **Anticipation.** Hover on a card, the card lifts. The user knows it's clickable before they read it.

Bad uses:

- Decoration without information. Floating particles in the background. Rotating logos. Don't.
- Long durations. Anything over 300ms feels slow. Anything under 100ms feels instant. The sweet spot is 150-250ms for most UI motion.
- Fighting the user. If the user wants to see the next state, motion that delays it is friction.

```css
.card {
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}
```

Subtle. Fast. Reinforces that the card is interactive. Doesn't get in the way.

> ⚠️ Trap - `prefers-reduced-motion`. Some users have vestibular disorders or just don't want animation. Honor it.

```css
@media (prefers-reduced-motion: reduce) {
  .card { transition: none; }
}
```

---

## Accessibility as a design constraint

Accessibility is often treated as "stuff you add later for screen readers". That's the wrong frame. The right frame: **accessibility is the discipline of building UI that works without your assumptions**.

Your assumptions you didn't notice:

- The user is using a mouse. They might not be.
- The user can see all your colors. They might not.
- The user is using a fast device with stable internet. They might not.
- The user is reading English at fluent speed. They might not.

A11y baked into design produces UI that's better for everyone:

- Keyboard navigation works -> power users can use shortcuts.
- Color contrast is high -> the UI is readable in sunlight.
- Forms have clear labels and error messages -> everyone fills them out faster.
- Pages have proper heading hierarchy -> SEO improves.
- Interactive elements have generous tap targets -> mobile users are happier.

The senior baseline:

- Use semantic HTML. `<button>` for buttons. `<a>` for navigation. `<form>` for forms. Don't reinvent these as `<div>` with click handlers.
- Make focus states visible. The dotted ring or custom outline is not optional.
- Label every input. `<label for>` or `aria-label`, not placeholder-only.
- Test with the keyboard alone. Tab through the whole flow. If you can't reach something, neither can a keyboard user.
- Run an automated audit (axe, Lighthouse) but don't trust it alone. It catches the structural stuff, not the semantic stuff.

> 💡 Insight - keyboard-first navigation is not just for people with disabilities. Every power user (developers, designers, anyone in a flow state) keyboards more than they mouse. Apps that respect keyboard navigation feel professional in a way mouse-only apps never will.

---

## Microcopy: the writing is part of the UI

Generic copy ("Submit", "An error occurred") wastes the cheapest improvement available. Specific copy ("Save changes", "We couldn't reach the server, retrying in 5s") makes the UI feel intelligent.

Three rules I'd push in code review:

1. **Buttons should describe what they do, not what they are.** "Save changes" beats "Submit". "Delete project" beats "OK".
2. **Errors should suggest the fix.** "Email is required" is bad. "Enter your work email so we can send the invite" is good.
3. **Loading states should name the operation.** "Loading" is okay. "Compiling your function" is better. "Building, this takes about 30 seconds" is best.

> Interesting fact: Stripe's documentation has a dedicated content style guide. The microcopy in their UI is treated with the same rigor as their API design. It's the kind of investment that compounds.

---

## A senior review checklist for any UI change

Before merging, walk through this:

1. **Acknowledgement.** Does every action change something visible within 100ms?
2. **Loading.** Is there a skeleton or named loading state for waits over ~300ms?
3. **Empty.** Is there a designed empty state with a clear next action?
4. **Error.** Is there a recovery path? Does the error explain what happened in human language?
5. **Affordance.** Can a new user tell what's interactive at a glance?
6. **Keyboard.** Can you complete the flow without a mouse?
7. **Motion.** Is every animation under 300ms and respectful of reduced-motion?
8. **Copy.** Is every button labeled with the action, every error with the fix?

This list is the difference between "shipped" and "shipped well".

---

## What to carry forward

- Perceived performance is about acknowledgement and expectation management. The four levers are: acknowledge immediately, commit optimistically, skeleton predictable layouts, prefetch likely paths.
- Linear/Vercel/Stripe/Apple share a discipline more than a technique: no state is unhandled, no copy is generic, no interaction is silent.
- Every component has four states (loading, empty, error, success). If any are "I'll handle that later", you have a bug.
- Motion has three legitimate uses: spatial continuity, state confirmation, anticipation. Anything else is decoration.
- Accessibility is design discipline that improves UX for everyone. Semantic HTML, visible focus, labeled inputs, keyboard-first navigation.
