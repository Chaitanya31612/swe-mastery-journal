# Start with a small job for AI

A model can interpret a sentence or draft an explanation.

Your application still owns the facts, permissions, and actions.

## A small example

The user asks: “Show held parcels at the east depot.”

The model suggests a filter. Code checks that filter and runs an allowed query.

```text
User’s sentence
      ↓
Model suggests a filter
      ↓
Code checks fields and the current user’s access
      ↓
Database returns the matching records and exact count
```

The model does not need to write SQL or change a parcel.

## What the model knows

It works with the context you give it. It does not automatically know your live database or the current user’s permissions.

A fluent answer can still be wrong.

Use code for exact rules and counts. Use the model where varied language makes it helpful.

## Plan for failure now

If the model is unavailable, the ordinary filters should still work.

A useful AI feature should have a useful no-model path.

## Remember

**Model suggests → code checks → application decides.**
