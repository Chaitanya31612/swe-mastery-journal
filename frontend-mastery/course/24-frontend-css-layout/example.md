## Follow a concrete example

```css
* { box-sizing: border-box; }
.workspace {
  display: grid;
  grid-template-columns: minmax(180px, 240px) minmax(0, 1fr);
  gap: 1.5rem;
}
.results { min-width: 0; }
.toolbar { display: flex; flex-wrap: wrap; gap: .75rem; }
pre { overflow-x: auto; max-width: 100%; }
@media (max-width: 48rem) {
  .workspace { grid-template-columns: 1fr; }
}
```

The code block scrolls inside its panel. It should not make the entire page wider than the viewport. Test a long unbroken identifier, browser zoom, and translated text.
