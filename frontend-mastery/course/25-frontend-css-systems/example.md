## Follow a concrete example

```css
:root { --space-2: .5rem; --focus: #006c88; }
.ticket-action { padding: .65rem 1rem; border: 1px solid currentColor; }
.ticket-action:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
.ticket-action[aria-busy="true"] { cursor: progress; }
@media (prefers-reduced-motion: reduce) {
  .progress-pulse { animation: none; }
}
```
Keep destructive color separate from ordinary selection. Give errors text and a field association, not only a red border.