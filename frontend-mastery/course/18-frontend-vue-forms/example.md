## Follow a concrete example

```ts
const draft = reactive({ title: '', priority: 'normal' })
const saving = ref(false)
const errors = ref<Record<string, string>>({})
async function save() {
  if (saving.value) return
  errors.value = draft.title.trim() ? {} : { title: 'Enter a title' }
  if (Object.keys(errors.value).length) return
  saving.value = true
  try { await submitDraft({ ...draft }) }
  catch { errors.value = { form: 'Could not save. Your edits are kept.' } }
  finally { saving.value = false }
}
```

submitDraft must check HTTP status and map field/conflict errors; this fragment shows ownership, not a complete request adapter.
