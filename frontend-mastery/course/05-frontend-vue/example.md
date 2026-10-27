# A small example

```js
// Vue 3 teaching example.
import { reactive, computed, toRefs } from 'vue'
const state = reactive({ count: 0 })
const { count: plainCount } = state   // primitive snapshot
const { count } = toRefs(state)      // linked ref
const doubled = computed(() => state.count * 2)
state.count++
console.log(plainCount, count.value, doubled.value) // 0, 1, 2
```
Vue 2 comparison: adding a missing key to an observed object needs Vue.set(obj, key, value) or a deliberate object replacement. Test with the version the screen actually uses.