## Follow a concrete example

```html
<button type="button" aria-expanded="false" aria-controls="filters">
  Filters
</button>
<section id="filters" aria-label="Ticket filters" hidden>...</section>
<p role="status" aria-live="polite">15 tickets loaded</p>
```
The application must update expanded and hidden state together. ARIA describes behavior; it does not implement keyboard handling for a custom widget automatically.