## Follow a concrete example

```ts
type Ticket = { id: string; title: string }
type LoadState =
  | { kind: 'loading' }
  | { kind: 'ready'; rows: Ticket[] }
  | { kind: 'failed'; message: string }

function heading(state: LoadState) {
  if (state.kind === 'ready') return `${state.rows.length} tickets`
  return state.kind === 'failed' ? state.message : 'Loading tickets'
}
```

Write a parser that accepts unknown and rejects missing/non-string IDs before creating a Ticket. Do not use response.json() as Ticket[] as your validation step.
