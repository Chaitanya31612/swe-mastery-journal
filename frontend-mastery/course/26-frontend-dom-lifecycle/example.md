## Follow a concrete example

```ts
import { onMounted, onUnmounted } from 'vue'
const onResize = () => { /* measure only what this component owns */ }
onMounted(() => window.addEventListener('resize', onResize))
onUnmounted(() => window.removeEventListener('resize', onResize))
```

Use the same function identity when removing the listener. removeEventListener('resize',()=>work()) does not remove a different arrow registered earlier. Disconnect observers and close subscriptions through their own APIs.
