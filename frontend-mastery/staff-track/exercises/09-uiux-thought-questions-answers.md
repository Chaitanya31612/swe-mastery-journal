# 09 - UI/UX Craft and Perceived Performance: Answers

Companion to `09-uiux-thought-questions.md`.

---

## Q1: Optimistic, debounced, or pessimistic?

1. **Favorite star.** Optimistic. Reversible, low-stakes. The star fills instantly; on failure, it un-fills with a quiet toast.

2. **$200 payment.** Pessimistic. Money requires explicit confirmation. Show a loading state ("Processing..."), block resubmits, and only show success when the server confirms. Never lie about money.

3. **Rename a file.** Optimistic. The rename appears immediately; on failure, revert with a toast. Duplicate names or permission errors should rollback gracefully.

4. **Auto-save a draft.** Debounced (settle for ~500ms-1s after typing stops), then save in the background with a subtle "Saving..." -> "Saved" indicator. No need for optimistic since the user already sees their typed text; what they need is confidence the system has it.

5. **Delete an account.** Pessimistic, with explicit confirmation, often with a typed-name guard ("Type your email to confirm"). This is the rare case where adding friction is the right design.

6. **Drag-and-drop reorder.** Optimistic. The user dropped the item into the new position; the UI commits instantly. Server save happens after; on failure, animate the item back and toast.

7. **Autocomplete search.** Throttled (or debounced at ~150ms) plus request cancellation. Each keystroke shouldn't trigger a fetch; we wait for a brief settle, and we cancel in-flight requests when a new keystroke comes in.

The pattern: **reversibility and stakes determine the strategy**. Reversible + low-stakes -> optimistic. Irreversible or high-stakes -> pessimistic. Frequent high-volume input -> throttle/debounce.

Anchored in `docs/09-uiux-craft-and-perceived-performance.md` -> "Perceived performance: the four levers".

---

## Q2: Reviewing an "all states" gap

Four states the component fails to handle:

1. **Loading.** While `useActivities()` is fetching, `activities` is likely `undefined`. The `.map` on undefined throws. Even if the hook returns `[]` initially, the panel shows the heading and empty content for an unknown duration. Should show a skeleton (a few placeholder rows) so the layout is stable and the user knows content is coming.

2. **Error.** If the fetch fails, the user sees "Recent activity" with nothing under it. Indistinguishable from "no activity". Should show an error message with a retry button: "Couldn't load activity. Retry?" The user has agency.

3. **Empty (no activity yet).** A new user with no activity sees a header and zero rows. Looks broken or like a loading state stalled. Should show an empty state with helpful copy: "No activity yet. Your team's recent updates will appear here."

4. **Stale data (refetch in progress while showing previous data).** When the panel refetches in the background (e.g., user comes back to the tab), the user sees stale data with no indication it's being refreshed. Should show a subtle indicator (small spinner in the corner, or a "Refreshing..." chip) so the user knows the data may shortly update.

Bonus: **partial failure.** If activities are paginated and one page fails to load, what happens? Real apps need to handle "loaded the first 50, failed to load page 2".

The senior framing: every component you build should have a state matrix. Walking the matrix during code review catches more real bugs than reading the happy-path code.

Anchored in `docs/09-uiux-craft-and-perceived-performance.md` -> "Empty, loading, error: the three states everyone forgets".

---

## Q3: The "looks fast" rewrite

What's wrong from a perceived-performance perspective:

- **No acknowledgement.** Click happens, button stays identical for the entire request. Even 200ms feels like "did it click?"
- **No protection from double-click.** Click twice fast, two requests fire.
- **`alert()` on failure.** Modal interruption, can't be styled, breaks flow, disrespects the user.
- **Flow is purely sequential.** No use of optimistic transition, no prefetch of step data.

Rewrite (one of several reasonable versions):

```jsx
function SaveAndContinue() {
  const [step, setStep] = useState(currentStep);
  const [status, setStatus] = useState('idle');  // idle | saving | error

  async function handleClick() {
    if (status === 'saving') return;  // protect from double-click
    setStatus('saving');

    try {
      const result = await api.saveStep(step);
      if (!result.ok) throw new Error(result.error ?? 'Save failed');
      setStep(step + 1);
      setStatus('idle');
    } catch (err) {
      setStatus('error');
    }
  }

  return (
    <div>
      <button
        onClick={handleClick}
        disabled={status === 'saving'}
        aria-busy={status === 'saving'}
      >
        {status === 'saving' ? 'Saving...' : 'Save and continue'}
      </button>
      {status === 'error' && (
        <p role="alert" className="error">
          We couldn't save. Check your connection and try again.
        </p>
      )}
    </div>
  );
}
```

Three improvements (at minimum):

1. **Synchronous acknowledgement.** Button label changes to "Saving..." in the same event turn as the click. The user knows the system heard them.
2. **Double-submit protection.** Disabled while saving, plus a guard at the top of `handleClick`. No way to fire two requests.
3. **Inline error with recovery.** Instead of `alert`, the error is a labeled message right under the button. Stays in flow, can be styled, can include action ("retry").

Bonus improvements you could add:

- **Optimistic step transition** if the save is low-risk: increment `step` immediately, roll back if save fails.
- **Prefetch step+1 data** as soon as the click fires, so the next screen has data ready by the time the save returns.
- **Keyboard shortcut** (Cmd+Enter) to save without mousing to the button.

The senior framing: every async UI flow benefits from this checklist. Acknowledgement, protection from re-fire, inline error recovery. Once it becomes habit, every button you ship feels intentional.

Anchored in `docs/09-uiux-craft-and-perceived-performance.md` -> "Perceived performance: the four levers" and "A senior review checklist for any UI change".
