## Follow a concrete example

```ts
const route = useRoute()
const ticketId = computed(() => String(route.params.id))
watch(ticketId, loadTicket, { immediate: true }) // loadTicket guards stale work

const workspace = useWorkspaceStore()
const { selectedWorkspaceId } = storeToRefs(workspace)
// Route update: router.replace({ query: { ...route.query, q: text } })
```

These fragments assume Vue Router and Pinia are installed and imported. Parse numeric pages into bounded positive integers rather than blindly using Number(query.page).
