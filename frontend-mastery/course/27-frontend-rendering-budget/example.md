## Follow a concrete example

```js
// Avoid repeatedly interleaving style writes with layout reads.
const widths = cards.map(card => card.getBoundingClientRect().width)
cards.forEach((card, i) => { card.style.setProperty('--measured-width', `${widths[i]}px`) })
```
This is only useful when measurement is actually needed.

CSS layout can often express the goal without JavaScript measurement at all. requestAnimationFrame schedules before a frame; it does not make expensive work free.