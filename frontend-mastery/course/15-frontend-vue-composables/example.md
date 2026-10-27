## Follow a concrete example

```ts
import { ref, onUnmounted } from 'vue'
export function useSelection() {
  const selectedId = ref<string | null>(null) // per call
  const select = (id: string) => { selectedId.value = id }
  const clear = () => { selectedId.value = null }
  return { selectedId, select, clear }
}

export function useWindowResize(update: () => void) {
  window.addEventListener('resize', update)
  onUnmounted(() => window.removeEventListener('resize', update))
}
// Browser-only example: guard window access in SSR code.
```
