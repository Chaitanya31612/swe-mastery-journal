## Follow a concrete example

```ts
const visible = computed(() => tickets.value.filter(matchesFilter))
// Instead of passing selectedId to every row and asking each to compare:
// <TicketRow :ticket="ticket" :active="ticket.id === selectedId" />
// Only rows whose active value changes need that prop change.
```
For a heavy optional editor: const Editor = defineAsyncComponent(() => import('./Editor.vue')). Measure initial transfer/parse time and the first editor-open wait separately.