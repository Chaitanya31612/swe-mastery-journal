# A small example

```jsx
// app/tasks/page.jsx — Server Component concept.
import CompleteButton from './CompleteButton'
export default async function Page() {
  const tasks = await readAllowedTasks() // server-only boundary
  return tasks.map(task => <div key={task.id}>
    {task.title}<CompleteButton id={task.id} />
  </div>)
}
// CompleteButton.jsx begins with 'use client'; it owns interaction.
// Its server mutation must authenticate, authorize, validate,
// update data, then apply the chosen revalidation strategy.
```

This is a boundary sketch, not a complete runnable app. readAllowedTasks and the mutation must be implemented with the selected version’s APIs and access rules.
