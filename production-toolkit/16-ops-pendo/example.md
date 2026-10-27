## Follow a concrete example

```js
// Only after the relevant confirmed outcome and SDK readiness.
pendo.track('TicketAssignmentCompleted', {
  method: 'bulk', outcome: 'partial_success', schemaVersion: 1
})
```
Do not include private ticket text. Handle SDK loading/failure so analytics does not break the main task.

A frontend event can be missed and is not the authoritative assignment record.