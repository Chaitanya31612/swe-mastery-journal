## Follow a concrete example

```text
src/api/tickets.ts         HTTP + parsing + error contract
src/composables/useSearch.ts  current request + cleanup
src/stores/workspace.ts    shared workspace identity, if needed
src/components/TicketForm.vue  owned draft + accessible errors
src/views/TicketsView.vue  URL context + composition
src/router/index.ts       routes + navigation UX
```
Write a five-line contract for each file before implementation. Test the observable behavior, not this exact directory spelling.