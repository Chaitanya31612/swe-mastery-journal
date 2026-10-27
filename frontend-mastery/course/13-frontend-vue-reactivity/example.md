## Follow a concrete example

```ts
import { ref, computed, nextTick } from 'vue'
const query = ref('')
const tickets = ref([{ title: 'Refund request' }])
const visible = computed(() => tickets.value.filter(t =>
  t.title.toLowerCase().includes(query.value.toLowerCase())))

async function openPanel() {
  panelOpen.value = true // panelOpen is a ref owned by this component
  await nextTick()
  panelElement.value?.focus() // template ref, after its v-if DOM update
}
```
